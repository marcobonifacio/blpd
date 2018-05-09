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
        data = self.conn.bdp('UCG IM Equity', 'NAME')
        data_ = pd.DataFrame(columns=['NAME'], index=['UCG IM Equity'],
        data=['UNICREDIT SPA'])
        pd.util.testing.assert_frame_equal(data, data_)


    def test_bdp_one_sec_isin_one_field(self):
        data = self.conn.bdp('IT0005239360', 'NAME', 'isin')
        data_ = pd.DataFrame(columns=['NAME'],
        index=['/isin/IT0005239360'], data=['UNICREDIT SPA'])
        pd.util.testing.assert_frame_equal(data, data_)


    def test_bdp_one_sec_one_field_override(self):
        data = self.conn.bdp('UCG IM Equity', 'REL_INDEX',
        overrides={'REL_INDEX': 'ITSMBANC'})
        data_ = pd.DataFrame(columns=['REL_INDEX'],
        index=['UCG IM Equity'], data=['ITSMBANC'])
        pd.util.testing.assert_frame_equal(data, data_)


    def test_bdp_one_bad_sec_one_field(self):
        data, err = self.conn.bdp('UCT IM Equity', 'NAME', errors=True)
        data_ = pd.DataFrame()
        # err_ = pd.DataFrame(columns=['Field', 'Category','Subcategory',
        # 'Message'], index=['UCT IM Equity'], data=[[np.NaN, 'BAD_SEC',
        # 'INVALID_SECURITY', 'Unknown/Invalid Security  [nid:xxx] ']])
        pd.util.testing.assert_frame_equal(data, data_)
        assert isinstance(err, pd.DataFrame) # Variable message in err dataframe


    def test_bdp_one_sec_one_bad_field(self):
        data, err = self.conn.bdp('UCG IM Equity', 'NAMT', errors=True)
        data_ = pd.DataFrame()
        err_ = pd.DataFrame(columns=['Field', 'Category', 'Subcategory',
        'Message'], index=['UCG IM Equity'], data=[['NAMT', 'BAD_FLD',
        'INVALID_FIELD', 'Field not valid']])
        pd.util.testing.assert_frame_equal(data, data_)
        pd.util.testing.assert_frame_equal(err, err_)


if __name__ == '__main__':
    unittest.main()
