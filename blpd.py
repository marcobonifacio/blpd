"""
blpd

Module to make syncronous requests to Bloomberg, returning a Pandas dataframe.
Based on native Bloomberg API.

Functions:
    bdp: reference request, similar to Excel BDP.
    bdh: historical request, similar to Excel BDH.
"""

import blpapi as blp
import datetime as dt
from optparse import OptionParser
import pandas as pd

#------------------------------------------------------------------------------
# Constants
#------------------------------------------------------------------------------

SECURITY_DATA = blp.Name('securityData')
SECURITY = blp.Name('security')
FIELD_DATA = blp.Name('fieldData')
FIELD_EXCEPTIONS = blp.Name('fieldExceptions')
FIELD_ID = blp.Name('fieldId')
SECURITY_ERROR = blp.Name('securityError')
ERROR_INFO = blp.Name('errorInfo')

#------------------------------------------------------------------------------
# Functions
#------------------------------------------------------------------------------

def parseCmdLine():
    """ Parses command line. """
    parser = opt.OptionParser(description='Retrieve reference data.')
    parser.add_option('-a',
                      '--ip',
                      dest='host',
                      help='server name or IP (default: %default)',
                      metavar='ipAddress',
                      default='localhost')
    parser.add_option('-p',
                      dest='port',
                      type='int',
                      help='server port (default: %default)',
                      metavar='tcpPort',
                      default=8194)
    parser.add_option('-f') # Error fix on Jupyter Notebooks

    (options, args) = parser.parse_args()

    return(options)


def bdp(securities, fields, prefix=None, rows=False, verbose=False, **kwargs):
    """ Sends a reference request to Bloomberg.
    Parameters:
        securities: string or tuple / list of valid Bloomberg tickers.
        fields: string or tuple / list of valid Bloomberg fields.
        prefix: string or tuple / list of valid Bloomberg topic prefix
                (ticker, cusip, wpk, isin, buid, sedol1, sedol2, sicovam,
                common, bsid, svm, cins, cats, bbgid). If a string, used for
                all securities, if a tuple / list, must match the length of
                securities list (default: None).
        rows: boolean. If True, returns the fields in rows (default: False).
        verbose: boolean. If True prints out Bloomberg response messages (default: False).
        **kwargs: any valid parameter.
    Optional arguments:
        returnEids: boolean (True returns name and value for EID date).
        returnFormattedValue: boolean (True forces data as a string).
        useUTCTime: boolean (True returns values in UTC).
        forcedDelay: boolean (True forces delayed data from exchange).
        overrides: list of dicts (every dict has keys 'fieldId' and 'value').
    Returns a pandas.DataFrame object.
    """
