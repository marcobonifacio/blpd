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
CATEGORY = blp.Name('category')
MESSAGE = blp.Name('message')
SUBCATEGORY = blp.Name('subcategory')


def _formatSecurity(security: str, prefix: str) -> str:
    """ Format a security in a valid Bloomberg syntax. """
    prefixes = ['ticker', 'cusip', 'wpk', 'isin', 'buid', 'sedol1', 'sedol2',
                'sicovam', 'common', 'bsid', 'svm', 'cins', 'cats', 'bbgid']
    if prefix.lower() == 'ticker':
        return(security)
    else:
        if prefix.lower() in prefixes:
            return(f'/{prefix.lower()}/{security}')
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


    def _addSecurities(self) -> None:
        """ Add a list of securities to a request. """
        if isinstance(self.securities, str):
            self.securities = [self.securities]
        elif isinstance(self.securities, list):
            pass
        else:
            print('Securities must be a string or a list') # Raise error
        for sec in _formatSecsList(self.securities, self.prefix):
            self.request.append('securities', sec)


    def _addFields(self) -> None:
        """ Add a list of fields to a request. """
        if isinstance(self.fields, str):
            self.fields = [self.fields]
        elif isinstance(self.fields, list):
            pass
        else:
            print('Fields must be a string or a list') # Raise error
        for fld in self.fields:
            self.request.append('fields', fld)


    def _addDays(self) -> None:
        """ Add fill days options to a historical request. """
        options = {'A': 'ALL_CALENDAR_DAYS',
                   'T': 'ACTIVE_DAYS_ONLY',
                   'W': 'NON_TRADING_WEEKDAYS'}
        try:
            self.request.set('nonTradingDayFillOption', options[self.days])
        except KeyError:
            print('Options are A / T / W')


    def _addFill(self) -> None:
        """ Add fill method options to a historical request. """
        options = {'N': 'NIL_VALUE',
                   'P': 'PREVIOUS_VALUE'}
        try:
            self.request.set('nonTradingDayFillMethod', options[self.fill])
        except KeyError:
            print('Options are N / P')


    def _addPeriod(self) -> None:
        """ Add periodicity options to a historical request. """
        optionsAdj = {'A': 'ACTUAL',
                      'C': 'CALENDAR',
                      'F': 'FISCAL'}
        optionsSel = {'D': 'DAILY',
                      'M': 'MONTHLY',
                      'Q': 'QUARTERLY',
                      'S': 'SEMI_ANNUALLY',
                      'W': 'WEEKLY',
                      'Y': 'YEARLY'}
        try:
            self.request.set('periodicityAdjustment', optionsAdj[self.per[0]])
            self.request.set('periodicitySelection', optionsAdj[self.per[1]])
        except KeyError:
            print('Options are A / C / F and D / M / Q / S / W / Y')


    def _addQuoteType(self) -> None:
            """ Add quote type options to a historical request. """
            options = {'P': 'PRICING_OPTION_PRICE',
                       'Y': 'PRICING_OPTION_YIELD'}
            try:
                self.request.set('pricingOption', options[self.qtTyp])
            except KeyError:
                print('Options are P / Y')


    def _addQuote(self) -> None:
            """ Add quote options to a historical request. """
            options = {'C': 'OVERRIDE_OPTION_CLOSE',
                       'G': 'OVERRIDE_OPTION_GPA'}
            try:
                self.request.set('overrideOption', options[self.quote])
            except KeyError:
                print('Options are C / G')


    def _addMandatoryOptions(self) -> None:
        """ Add mandatory options to a historical request. """
        self.request.set('returnRelativeDate', self.dtFmt)
        self._addDays()
        self._addFill()
        self._addPeriod()
        self._addQuoteType()
        self._addQuote()
        self.request.set('adjustmentFollowDPDF', self.useDPDF)


    def _addFacultativeOptions(self) -> None:
        """ Add facultative options to a historical request. """
        self.request.set('calendarCodeOverride', self.cdr)
        self.request.set('currency', self.fx)
        self.request.set('maxDataPoints', self.points)
        self.request.set('adjustmentAbnormal', self.cshAdjAbnormal)
        self.request.set('adjustmentSplit', self.capChg)
        self.request.set('adjustmentNormal', self.cshAdjNormal)


    def _addOverrides(self) -> None:
        """ Manage request arguments. """
        if self.overrides is None:
            pass
        elif isinstance(self.overrides, dict):
            overrides = self.request.getElement(OVERRIDES)
            oslist = []
            for key, value in self.overrides.items():
                oslist.append(overrides.appendElement())
                oslist[-1].setElement(FIELD_ID, key)
                oslist[-1].setElement('value', value)
        else:
            print('Overrides must be a dict') # Raise error


    def bdp(self, securities: Union['str', 'list'],
    fields: Union['str', 'list'], prefix: Union['str', 'list']='ticker',
    overrides: dict=None) -> pd.DataFrame:
        """ Send a reference request to Bloomberg (mimicking Excel function
        BDP). """
        self.request = self.refDataService.createRequest('ReferenceDataRequest')
        self.securities = securities
        self.fields = fields
        self.prefix = prefix
        self.overrides = overrides
        self._addSecurities()
        self._addFields()
        self._addOverrides()
        if self.verbose is True:
            print(f'Sending request: {self.request}')
        cid = self.session.sendRequest(self.request)
        if self.verbose is True:
            print(f'Correlation ID is: {cid}')
        data = pd.DataFrame()
        exceptions = pd.DataFrame()
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
                        if secData.hasElement(SECURITY_ERROR):
                            secError = secData.getElement(SECURITY_ERROR)
                            exceptions.loc[name, 'Field'] = None
                            exceptions.loc[name, 'Category'] = \
                            secError.getElementAsString(CATEGORY)
                            exceptions.loc[name, 'Subcategory'] = \
                            secError.getElementAsString(SUBCATEGORY)
                            exceptions.loc[name, 'Message'] = \
                            secError.getElementAsString(MESSAGE)
                        fieldsException = secData.getElement(FIELD_EXCEPTIONS)
                        for fieldEx in fieldsException.values():
                            if fieldEx.hasElement(FIELD_ID):
                                fieldId = fieldEx.getElementAsString(FIELD_ID)
                                errorInfo = fieldEx.getElement(ERROR_INFO)
                                exceptions.loc[name, 'Field'] = fieldId
                                exceptions.loc[name, 'Category'] = \
                                errorInfo.getElementAsString(CATEGORY)
                                exceptions.loc[name, 'Subcategory'] = \
                                errorInfo.getElementAsString(SUBCATEGORY)
                                exceptions.loc[name, 'Message'] = \
                                errorInfo.getElementAsString(MESSAGE)
            if ev.eventType() == blp.Event.RESPONSE:
                break
        return(data, exceptions)


    def bdh(self, securities: Union['str', 'list'],
    field: Union['str', 'list'], startDate: str, endDate: str,
    prefix: Union['str', 'list']='ticker', cdr: str=None, fx: str=None,
    dtFmt: bool=False, days: str='W', fill: str='P', per: str='CD',
    points: int=None, qtTyp: str='Y', quote: str='C', useDPDF: bool=True,
    cshAdjAbnormal: bool=None, capChg: bool=None, cshAdjNormal: bool=None,
    overrides: dict=None) -> pd.DataFrame:
        """ Send a historical request to Bloomberg (mimicking Excel function
        BDH). """
        self.request = self.refDataService.createRequest('HistoricalDataRequest')
        self.securities = securities
        self.fields = fields
        self.startDate = startDate
        self.endDate = endDate
        self.prefix = prefix
        self.cdr = cdr
        self.fx = fx
        self.dtFmt = dtFmt
        self.days = days
        self.fill = fill
        self.per = per
        self.points = points
        self.qtTyp = qtTyp
        self.quote = quote
        self.useDPDF = useDPDF
        self.cshAdjAbnormal = cshAdjAbnormal
        self.capChg = capChg
        self.cshAdjNormal = cshAdjNormal
        self.overrides = overrides
        self._addSecurities()
        self._addFields()
        self.request.set('startDate', self.startDate)
        self.request.set('endDate', self.endDate)
        self._addMandatoryOptions()
        self._addFacultativeOptions()
        self._addOverrides()
