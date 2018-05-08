import unittest
import numpy as np
import pandas as pd
from blpd import blp


class TestBLP(unittest.TestCase):


    def setUp(self):
        self.conn = blp.BLP()


    def tearDown(self):
        self.conn.close()


    def test_bdp_one_sec_one_field(self):
        df, _ = self.conn.bdp('UCG IM Equity', 'NAME')
        df_expected = pd.DataFrame(columns=['NAME'], index=['UCG IM Equity'],
        data=['UNICREDIT SPA'])
        pd.util.testing.assert_frame_equal(df, df_expected)


    def test_bdp_one_sec_isin_one_field(self):
        df, _ = self.conn.bdp('IT0005239360', 'NAME', 'isin')
        df_expected = pd.DataFrame(columns=['NAME'],
        index=['/isin/IT0005239360'], data=['UNICREDIT SPA'])
        pd.util.testing.assert_frame_equal(df, df_expected)


    def test_bdp_one_sec_one_field_override(self):
        df, _ = self.conn.bdp('UCG IM Equity', 'REL_INDEX',
        overrides={'REL_INDEX': 'ITSMBANC'})
        df_expected = pd.DataFrame(columns=['REL_INDEX'],
        index=['UCG IM Equity'], data=['ITSMBANC'])
        pd.util.testing.assert_frame_equal(df, df_expected)


    def test_bdp_one_bad_sec_one_field(self):
        df, _ = self.conn.bdp('UCT IM Equity', 'NAME')
        df_expected = pd.DataFrame()
        err_expected = pd.DataFrame(columns=['Field', 'Category',
        'Subcategory', 'Message'], index=['UCT IM Equity'], data=[[np.NaN,
        'BAD_SEC', 'INVALID_SECURITY', 'Unknown/Invalid Security  [nid:172] ']])
        pd.util.testing.assert_frame_equal(df, df_expected)
        pd.util.testing.assert_frame_equal(_, err_expected)


    def test_bdp_one_sec_one_bad_field(self):
        df, _ = self.conn.bdp('UCG IM Equity', 'NAMT')
        df_expected = pd.DataFrame()
        err_expected = pd.DataFrame(columns=['Field', 'Category',
        'Subcategory', 'Message'], index=['UCG IM Equity'], data=[['NAMT',
        'BAD_FLD', 'INVALID_FIELD', 'Field not valid']])
        pd.util.testing.assert_frame_equal(df, df_expected)
        pd.util.testing.assert_frame_equal(_, err_expected)


if __name__ == '__main__':
    unittest.main()
