import blpapi as blp
import datetime as dt
import pandas as pd


SECURITY_DATA = blp.Name('securityData')
SECURITY = blp.Name('security')
FIELD_DATA = blp.Name('fieldData')
FIELD_EXCEPTIONS = blp.Name('fieldExceptions')
FIELD_ID = blp.Name('fieldId')
SECURITY_ERROR = blp.Name('securityError')
ERROR_INFO = blp.Name('errorInfo')


def formatSecurity(security: str, prefix: str) -> str:
    """ Format a security in a valid Bloomberg syntax. """
    prefixes = ['ticker', 'cusip', 'wpk', 'isin', 'buid', 'sedol1', 'sedol2',
                'sicovam', 'common', 'bsid', 'svm', 'cins', 'cats', 'bbgid']
    if prefix == 'ticker':
        return(security)
    else:
        if prefix is in prefixes:
            return(f'\{prefix}\{security}')
        else:
            print('Topic prefix is not correct')
            return()


def formatSecsList(securities: list, prefix) -> list:
    """ Format a list of securities in a valid Bloomberg syntax. """
    output = []
    if type(prefix) == 'str':
        for s in securities:
            output.append(formatSecurity(s, prefix))
    elif type(prefix) == 'list':
        if len(prefix) == len(securities):
            for s, p in zip(securities, prefix):
                output.append(formatSecurity(s, p))
        else:
            print('Securities and prefixes length do not match')
    else:
        print('Prefix type is not correct')


class BLP():
    """ Implementation of the Request/Response Paradigm to mimick Excel API. """

    def __init__(self, host='localhost', port=8194, verbose=False, start=True):
        """ Initialize a BLP session. """
        self.active = False
        self.host = host
        self.port = port
        self.verbose = verbose
        if start is True:
            self.open()


    def open(self):
        """ Start a BLP session. """
        if self.active is False:
            sessionOptions = blp.SessionOptions()
            sessionOptions.setServerHost(self.host)
            sessionOptions.setServerPort(self.port)
            if self.verbose is True:
                print(f'Connecting to {self.host}:{self.port}.')
            self.session = blp.Session(sessionOptions)
            if self.session.start() is False:
                print('Failed to start session.')
                return()
            if self.verbose is True:
                print('Starting session...')
            if session.openService('//blp/refdata') is False:
                print('Failed to open refdata service.')
                return()
            if self.verbose is True:
                print('Opening refdata service...')
            self.refDataService = self.session.getService('//blp/refdata')
            self.active = True


    def close(self):
        """ End a BLP session. """
        if self.active is True:
            self.session.stop()
            if self.verbose is True:
                print('Closing the session...')
            self.active = False
