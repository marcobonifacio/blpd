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


class BLPWrapper():
    """ Python wrapper of Bloomberg API to mimick Excel API Request / Response






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


def formatSecs(securities, prefix=None):
    """ Format valid securities. """


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
    global options
    options = parseCmdLine()

    # Fill SessionOptions
    sessionOptions = blp.SessionOptions()
    sessionOptions.setServerHost(options.host)
    sessionOptions.setServerPort(options.port)

    if verbose:
        print(f'Connecting to {options.host}:{options.port}')

    # Create a Session
    session = blp.Session(sessionOptions)

    # Start a Session
    if not session.start():
        print('Failed to start session.')
        return

    if verbose:
        print('Starting session...')

    if not session.openService('//blp/refdata'):
        print ('Failed to open //blp/refdata')
        return

    if verbose:
        print('Opening //blp/refdata service')

    refDataService = session.getService('//blp/refdata')
    request = refDataService.createRequest('ReferenceDataRequest')

    # Append securities to request
    if type(securities) is str:
        request.append('securities', securities)
    elif type(securities) is list or type(securities) is tuple:
        for sec in securities:
            request.append('securities', sec)
    else:
        print('Securities type not supported.')
        return

    # Append fields to request
    if type(fields) is str:
        request.append('fields', fields)
    elif type(fields) is list or type(fields) is tuple:
        for fld in fields:
            request.append('fields', fld)
    else:
        print('Fields type not supported.')
        return

    # Add optional arguments to request
    for k in kwargs:
        if k == 'overrides':
            overrides = request.getElement('overrides')
            os = []
            for key, value in kwargs[k].items():
                os.append(overrides.appendElement())
                os[-1].setElement('fieldId', key)
                os[-1].setElement('value', value)
        else:
            request.set(k, kwargs[k])

    if verbose:
        print('Sending request: '.format(request))
    cid = session.sendRequest(request)

    try:
        df = pd.DataFrame()
        # Process received events
        while(True):
            # We provide timeout to give the chance to Ctrl+C handling:
            ev = session.nextEvent(500)
            for msg in ev:
                if cid in msg.correlationIds():
                    if not msg.hasElement(SECURITY_DATA):
                        print('Unexpected message:')
                        print(msg)
                        return

                    securityDataArray = msg.getElement(SECURITY_DATA)
                    for securityData in securityDataArray.values():
                        name = securityData.getElementAsString(SECURITY)
                        fieldData = securityData.getElement(FIELD_DATA)
                        for field in fieldData.elements():
 #                           if field.isValid():
                             df.loc[name, str(field.name())] = \
                             field.getValueAsString()
 #                           else:
 #                               df.loc[name, field.name()] = \
 #                               pd.np.NaN

                        fieldExceptionArray = \
                            securityData.getElement(FIELD_EXCEPTIONS)
                        for fieldException in fieldExceptionArray.values():
                            pass

#                    return(df)
            # Response completly received, so we could exit
            if ev.eventType() == blp.Event.RESPONSE:
                break
    finally:
        # Stop the session
        return(df)
        session.stop()
