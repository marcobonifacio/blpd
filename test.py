from blpd import blp

def test_connection():
    """ Test the Bloomberg connection. """
    conn = blp.BLP()
    conn.close()


def test_connection_verbose():
    """ Test the Bloomberg connection, verbose mode. """
    conn = blp.BLP(verbose=True)
    conn.close()


def test_bdp_string_verbose():
    """ Test BDP function, verbose mode. """
    conn = blp.BLP(verbose=True)
    df, ex = conn.bdp('UCG IM Equity', 'NAME')
    print(df)
    print(ex)
    conn.close()


def test_bdp_string_isin_verbose():
    """ Test BDP function with isin instead of ticker. """
    conn = blp.BLP(verbose=True)
    df, ex = conn.bdp('IT0005239360', 'NAME', 'isin')
    print(df)
    print(ex)
    conn.close()


def test_bdp_string_overrides_verbose():
    """ Test BDP function with overrides. """
    conn = blp.BLP(verbose=True)
    df1, ex1 = conn.bdp('UCG IM Equity', 'BETA_ADJ_OVERRIDABLE')
    df2, ex2 = conn.bdp('UCG IM Equity', 'BETA_ADJ_OVERRIDABLE',
    overrides={'BETA_OVERRIDE_REL_INDEX': 'ITSMBANC'})
    print(df1)
    print(df2)
    conn.close()


def test_bdp_string_bad_sec_verbose():
    """ Test BDP function with bad security ticker. """
    conn = blp.BLP(verbose=True)
    df, ex = conn.bdp('UCT IM Equity', 'NAME', errors=True)
    print(df)
    print(ex)
    conn.close()


def test_bdp_list_verbose():
    """ Test BDP function with a list of tickers. """
    conn = blp.BLP(verbose=True)
    df, ex = conn.bdp(['UCG IM Equity', 'ISP IM Equity'],
    ['NAME', 'COUNTRY_FULL_NAME'])
    print(df)
    print(ex)
    conn.close()


def test_bdp_list_swap_verbose():
    """ Test BDP function with a list of tickers. """
    conn = blp.BLP(verbose=True)
    df, ex = conn.bdp(['UCG IM Equity', 'ISP IM Equity'],
    ['NAME', 'COUNTRY_FULL_NAME'], swap=True)
    print(df)
    print(ex)
    conn.close()


def test_bdp_list_missing_data_verbose():
    """ Test BDP function with a list of tickers. """
    conn = blp.BLP(verbose=True)
    df, ex = conn.bdp(['UCG IM Equity', 'EI643289@BGN Corp'], ['NAME', 'CPN'])
    print(df)
    print(ex)
    conn.close()


def test_bdp_list_bad_sec_verbose():
    """ Test BDP function with a good and a bad security ticker. """
    conn = blp.BLP(verbose=True)
    df, ex = conn.bdp(['UCG IM Equity', 'UCT IM Equity'],
    ['NAME', 'COUNTRY_FULL_NAME'])
    print(df)
    print(ex)
    conn.close()


def test_bdp_list_bad_fld_verbose():
    """ Test BDP function with a good and a bad field name. """
    conn = blp.BLP(verbose=True)
    df, ex = conn.bdp(['UCG IM Equity', 'ISP IM Equity'], ['NAME', 'NAMT'])
    print(df)
    print(ex)
    conn.close()


def test_bdh_string_verbose():
    """ Test BDH function, verbose mode. """
    conn = blp.BLP(verbose=True)
    df, ex = conn.bdh('UCG IM Equity', 'PX_LAST', '20180410')
    print(df)
    print(ex)
    conn.close()


def test_bdh_string_cdr_verbose():
    """ Test BDH function, verbose mode. """
    conn = blp.BLP(verbose=True)
    df, ex = conn.bdh('UCG IM Equity', 'PX_LAST', '20180410', cdr='IT')
    print(df)
    print(ex)
    conn.close()


def test_bdh_string_bad_cdr_verbose():
    """ Test BDH function, verbose mode. """
    conn = blp.BLP(verbose=True)
    df, ex = conn.bdh('UCG IM Equity', 'PX_LAST', '20180410', cdr='IW')
    print(df)
    print(ex)
    conn.close()


def test_bdh_string_fx_verbose():
    """ Test BDH function, verbose mode. """
    conn = blp.BLP(verbose=True)
    df, ex = conn.bdh('UCG IM Equity', 'PX_LAST', '20180410', fx='USD')
    print(df)
    print(ex)
    conn.close()


def test_bdh_string_bad_fx_verbose():
    """ Test BDH function, verbose mode. """
    conn = blp.BLP(verbose=True)
    df, ex = conn.bdh('UCG IM Equity', 'PX_LAST', '20180410', fx='USP')
    print(df)
    print(ex)
    conn.close() # Raise Exception


def test_bdh_list_verbose():
    """ Test BDH function, verbose mode. """
    conn = blp.BLP(verbose=True)
    df, ex = conn.bdh(['UCG IM Equity', 'ISP IM Equity'],
    ['PX_LAST', 'CUR_MKT_CAP'], '20180410')
    print(df)
    print(ex)
    conn.close()


def test_bdh_list_swap_verbose():
    """ Test BDH function, verbose mode. """
    conn = blp.BLP(verbose=True)
    df, ex = conn.bdh(['UCG IM Equity', 'ISP IM Equity'],
    ['PX_LAST', 'CUR_MKT_CAP'], '20180410', swap=True)
    print(df)
    print(ex)
    conn.close()


def test_bdh_list_bad_sec_verbose():
    """ Test BDH function, verbose mode. """
    conn = blp.BLP(verbose=True)
    df, ex = conn.bdh(['UCG IM Equity', 'UCT IM Equity'],
    ['PX_LAST', 'CUR_MKT_CAP'], '20180410')
    print(df)
    print(ex)
    conn.close()


def test_bdh_list_bad_fld_verbose():
    """ Test BDH function, verbose mode. """
    conn = blp.BLP(verbose=True)
    df, ex = conn.bdh(['UCG IM Equity', 'ISP IM Equity'],
    ['PX_LAST', 'PX_LAPT'], '20180410')
    print(df)
    print(ex)
    conn.close()


def main():
    """ Run the tests. """
    test_bdp_string_bad_sec_verbose()


if __name__ == '__main__':
    main()
