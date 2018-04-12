import blpapi as blp
import datetime as dt
import pandas as pd
from typing import Union


SECURITY_DATA = blp.Name('securityData')
SECURITY = blp.Name('security')
FIELD_DATA = blp.Name('fieldData')
FIELD_EXCEPTIONS = blp.Name('fieldExceptions')
FIELD_ID = blp.Name('fieldId')
SECURITY_ERROR = blp.Name('securityError')
ERROR_INFO = blp.Name('errorInfo')
OVERRIDES = blp.Name('overrides')


def _formatSecurity(security: str, prefix: str) -> str:
    """ Format a security in a valid Bloomberg syntax. """
    prefixes = ['ticker', 'cusip', 'wpk', 'isin', 'buid', 'sedol1', 'sedol2',
                'sicovam', 'common', 'bsid', 'svm', 'cins', 'cats', 'bbgid']
    if prefix == 'ticker':
        return(security)
    else:
        if prefix in prefixes:
            return(f'\{prefix}\{security}')
        else:
            print('Topic prefix is not correct') # Raise error
            return()


def _formatSecsList(securities: list, prefix: Union[str, list]) -> list:
    """ Format a list of securities in a valid Bloomberg syntax. """
    output = []
    if isinstance(prefix, str):
        for s in securities:
            output.append(_formatSecurity(s, prefix))
    elif isinstance(prefix, list):
        if len(prefix) == len(securities):
            for s, p in zip(securities, prefix):
                output.append(_formatSecurity(s, p))
        else:
            print('Securities and prefixes length do not match') # Raise error
    else:
        print('Prefix type is not correct') # Raise error
    return(output)


class BLP():
    """ Implementation of the Request/Response Paradigm to mimick Excel API. """

    def __init__(self, host: str='localhost', port: int=8194,
    verbose: bool=False, start: bool=True) -> None:
        """ Initialize a BLP session. """
        self.active = False
        self.host = host
        self.port = port
        self.verbose = verbose
        if start is True:
            self.open()


    def open(self) -> None:
        """ Start a BLP session. """
        if self.active is False:
            sessionOptions = blp.SessionOptions()
            sessionOptions.setServerHost(self.host)
            sessionOptions.setServerPort(self.port)
            if self.verbose is True:
                print(f'Connecting to {self.host}:{self.port}.')
            self.session = blp.Session(sessionOptions)
            if self.session.start() is False:
                print('Failed to start session.') # Raise error
                return()
            if self.verbose is True:
                print('Starting session...')
            if self.session.openService('//blp/refdata') is False:
                print('Failed to open refdata service.') # Raise error
                return()
            if self.verbose is True:
                print('Opening refdata service...')
            self.refDataService = self.session.getService('//blp/refdata')
            self.active = True


    def close(self) -> None:
        """ End a BLP session. """
        if self.active is True:
            self.session.stop()
            if self.verbose is True:
                print('Closing the session...')
            self.active = False


    def _addSecurities(self) -> list:
        """ Add a list of securities to a request. """
        if isinstance(self.securities, str):
            self.securities = [self.securities]
        elif isinstance(self.securities, list):
            pass
        else:
            print('Securities must be a string or a list') # Raise error
        for sec in _formatSecsList(self.securities, self.prefix):
            self.request.append('securities', sec)


    def _addFields(self) -> list:
        """ Add a list of fields to a request. """
        if isinstance(self.fields, str):
            self.fields = [self.fields]
        elif isinstance(self.fields, list):
            pass
        else:
            print('Fields must be a string or a list') # Raise error
        for fld in self.fields:
            self.request.append('fields', fld)


    def _addArguments(self, kwargs) -> None:
        """ Manage request arguments. """
        for k in kwargs:
            if k == 'overrides':
                overrides = self.request.getElement(OVERRIDES)
                o = []
                for key, value in kwargs[k].items():
                    o.append(overrides.appendElement())
                    o[-1].setElement(FIELD_ID, key)
                    o[-1].setElement('value', value)
            else:
                self.request.set(k, kwargs[k]) # To be managed


    def bdp(self, securities: Union['str', 'list'],
    fields: Union['str', 'list'], prefix: Union['str', 'list']='ticker',
    transpose: bool=False, **kwargs) -> pd.DataFrame:
        """ Send a reference request to Bloomberg (mimicking Excel function
        BDP). """
        self.request = self.refDataService.createRequest('ReferenceDataRequest')
        self.securities = securities
        self.fields = fields
        self.prefix = prefix
        self._addSecurities()
        self._addFields()
        self._addArguments(kwargs)
        if self.verbose is True:
            print(f'Sending request: {self.request}')
        cid = self.session.sendRequest(self.request)
        if self.verbose is True:
            print(f'Correlation ID is: {cid}')
        data = pd.DataFrame()
        while(True):
            ev = self.session.nextEvent(500)
            for msg in ev:
                if cid in msg.correlationIds():
                    securitiesData = msg.getElement(SECURITY_DATA)
                    if self.verbose is True:
                        print(f'Securities data: {securitiesData}')
                    for secData in securitiesData.values():
                        name = secData.getElementAsString(SECURITY)
                        fieldsData = secData.getElement(FIELD_DATA)
                        for field in fieldsData.elements():
                            data.loc[name, str(field.name())] = \
                            field.getValueAsString()
            if ev.eventType() == blp.Event.RESPONSE:
                break
        if transpose is False:
            return(data)
        else:
            return(data.T)
