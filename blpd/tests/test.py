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


    def test_bdp_two_secs_two_fields(self):
        data = self.conn.bdp(['UCG IM Equity', 'ISP IM Equity'], ['NAME',
        'COUNTRY_FULL_NAME'])
        data_ = pd.DataFrame(columns=['NAME', 'COUNTRY_FULL_NAME'],
        index=['UCG IM Equity', 'ISP IM Equity'], data=[['UNICREDIT SPA',
        'ITALY'], ['INTESA SANPAOLO', 'ITALY']])
        pd.util.testing.assert_frame_equal(data, data_)


    def test_bdp_two_secs_two_fields_swapped(self):
        data = self.conn.bdp(['UCG IM Equity', 'ISP IM Equity'], ['NAME',
        'COUNTRY_FULL_NAME'], swap=True)
        data_ = pd.DataFrame(columns=['UCG IM Equity', 'ISP IM Equity'],
        index=['NAME', 'COUNTRY_FULL_NAME'], data=[['UNICREDIT SPA',
        'INTESA SANPAOLO'], ['ITALY', 'ITALY']])
        pd.util.testing.assert_frame_equal(data, data_)


    def test_bdp_two_secs_two_fields_one_missing(self):
        data, err = self.conn.bdp(['UCG IM Equity', 'EI643289@BGN Corp'],
        ['NAME', 'CPN'], errors=True)
        data_ = pd.DataFrame(columns=['NAME', 'CPN'],
        index=['UCG IM Equity', 'EI643289@BGN Corp'], data=[['UNICREDIT SPA',
        np.NaN], ['UNICREDIT SPA', 6.125]])
        err_ = pd.DataFrame(columns=['Field', 'Category', 'Subcategory',
        'Message'], index=['UCG IM Equity'], data=[['CPN', 'BAD_FLD',
        'NOT_APPLICABLE_TO_REF_DATA', 'Field not applicable to security']])
        pd.util.testing.assert_frame_equal(data, data_)
        pd.util.testing.assert_frame_equal(err, err_)


    def test_bdh_one_sec_one_field(self):
        data = self.conn.bdh('UCG IM Equity', 'NET_REV', 'FY2016', 'FY2017',
        per='FY')
        data_ = pd.DataFrame(columns=pd.MultiIndex.from_tuples(
        [('UCG IM Equity', 'NET_REV')]), index=[pd.to_datetime('2016-12-31'),
        pd.to_datetime('2017-12-31')], data=[[19484.224], [20130.646]])
        pd.util.testing.assert_frame_equal(data, data_)


    def test_bdh_two_secs_two_fields(self):
        data = self.conn.bdh(['UCG IM Equity', 'ISP IM Equity'], ['NET_REV',
        'NET_INCOME'], 'FY2016', 'FY2017', per='FY')
        data_ = pd.DataFrame(columns=pd.MultiIndex.from_product(
        [['UCG IM Equity', 'ISP IM Equity'], ['NET_REV', 'NET_INCOME']]),
        index=[pd.to_datetime('2016-12-31'), pd.to_datetime('2017-12-31')],
        data=[[19484.22, -11790.09, 18168.00, 3111.00], [20130.65, 5473.07,
        24249.00, 7316.00]])
        pd.util.testing.assert_frame_equal(data, data_)


    def test_bdh_two_secs_two_fields_swapped(self):
        data = self.conn.bdh(['UCG IM Equity', 'ISP IM Equity'], ['NET_REV',
        'NET_INCOME'], 'FY2016', 'FY2017', per='FY', swap=True)
        data_ = pd.DataFrame(columns=pd.MultiIndex.from_product(
        [['UCG IM Equity', 'ISP IM Equity'], ['NET_REV', 'NET_INCOME']]),
        index=[pd.to_datetime('2016-12-31'), pd.to_datetime('2017-12-31')],
        data=[[19484.22, -11790.09, 18168.00, 3111.00], [20130.65, 5473.07,
        24249.00, 7316.00]]).swaplevel(axis=1)
        pd.util.testing.assert_frame_equal(data, data_)


if __name__ == '__main__':
    unittest.main()
