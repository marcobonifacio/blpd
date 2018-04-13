import blpd

def test_connection():
    """ Test the Bloomberg connection. """
    conn = blpd.BLP()
    conn.close()


def test_connection_verbose():
    """ Test the Bloomberg connection, verbose mode. """
    conn = blpd.BLP(verbose=True)
    conn.close()


def test_bdp_string_verbose():
    """ Test BDP function, verbose mode. """
    conn = blpd.BLP(verbose=True)
    df, ex = conn.bdp('UCG IM Equity', 'NAME')
    print(df)
    print(ex)
    conn.close()


def test_bdp_string_isin_verbose():
    """ Test BDP function with isin instead of ticker. """
    conn = blpd.BLP(verbose=True)
    df, ex = conn.bdp('IT0005239360', 'NAME', 'isin')
    print(df)
    print(ex)
    conn.close()


def test_bdp_string_overrides_verbose():
    """ Test BDP function with overrides. """
    conn = blpd.BLP(verbose=True)
    df1, ex1 = conn.bdp('UCG IM Equity', 'BETA_ADJ_OVERRIDABLE')
    df2, ex2 = conn.bdp('UCG IM Equity', 'BETA_ADJ_OVERRIDABLE',
    overrides={'BETA_OVERRIDE_REL_INDEX': 'ITSMBANC'})
    print(df1)
    print(df2)
    conn.close()


def test_bdp_string_bad_sec_verbose():
    """ Test BDP function with bad security ticker. """
    conn = blpd.BLP(verbose=True)
    df, ex = conn.bdp('UCT IM Equity', 'NAME')
    print(df)
    print(ex)
    conn.close()


def test_bdp_list_verbose():
    """ Test BDP function with a list of tickers. """
    conn = blpd.BLP(verbose=True)
    df, ex = conn.bdp(['UCG IM Equity', 'ISP IM Equity'],
    ['NAME', 'COUNTRY_FULL_NAME'])
    print(df)
    print(ex)
    conn.close()


def test_bdp_list_missing_data_verbose():
    """ Test BDP function with a list of tickers. """
    conn = blpd.BLP(verbose=True)
    df, ex = conn.bdp(['UCG IM Equity', 'EI643289@BGN Corp'], ['NAME', 'CPN'])
    print(df)
    print(ex)
    conn.close()


def test_bdp_list_bad_sec_verbose():
    """ Test BDP function with a good and a bad security ticker. """
    conn = blpd.BLP(verbose=True)
    df, ex = conn.bdp(['UCG IM Equity', 'UCT IM Equity'],
    ['NAME', 'COUNTRY_FULL_NAME'])
    print(df)
    print(ex)
    conn.close()


def test_bdp_list_bad_fld_verbose():
    """ Test BDP function with a good and a bad field name. """
    conn = blpd.BLP(verbose=True)
    df, ex = conn.bdp(['UCG IM Equity', 'ISP IM Equity'], ['NAME', 'NAMT'])
    print(df)
    print(ex)
    conn.close()


def main():
    """ Run the tests. """
    test_bdp_string_verbose()


if __name__ == '__main__':
    main()
