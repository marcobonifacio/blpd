import blpd

def test_connection():
    """ Test the Bloomberg connection. """
    conn = blpd.BLP()
    conn.close()


def test_connection_verbose():
    """ Test the Bloomberg connection. """
    conn = blpd.BLP(verbose=True)
    conn.close()


def test_bdp_string_verbose():
    """ Test BDP function. """
    conn = blpd.BLP(verbose=True)
    df = conn.bdp('UCG IM Equity', 'NAME')
    print(df)
    conn.close()


def test_bdp_string_overrides_verbose():
    """ Test BDP function. """
    conn = blpd.BLP(verbose=True)
    df = conn.bdp('UCG IM Equity', 'NAME', overrides={'REL_INDEX': 'ITSMBANC'})
    print(df)
    conn.close()


def test_bdp_list_verbose():
    """ Test BDP function. """
    conn = blpd.BLP(verbose=True)
    df = conn.bdp(['UCG IM Equity', 'ISP IM Equity'], ['NAME', 'COUNTRY_FULL_NAME'])
    print(df)
    conn.close()


def test_bdp_list_trasnpose_verbose():
    """ Test BDP function. """
    conn = blpd.BLP(verbose=True)
    df = conn.bdp(['UCG IM Equity', 'ISP IM Equity'], ['NAME', 'COUNTRY_FULL_NAME'], transpose=True)
    print(df)
    conn.close()


def main():
    """ Run the tests. """
    test_connection_verbose()
    test_bdp_string_verbose()
    test_bdp_string_overrides_verbose()
    test_bdp_list_verbose()
    test_bdp_list_trasnpose_verbose()


if __name__ == '__main__':
    main()
