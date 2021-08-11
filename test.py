

from datatransform import dataTransform
from config import Config
from helper import *
from assets import Assets
from csv_load import Csv
import unittest


class MyTestCase(unittest.TestCase):

    def test_Config(self):
        csv_read_type = Config(template_type='kh').template()[
            'parsing_settings']['csv_read_type']
        self.assertEqual(csv_read_type, 'dict_reader')

    def test_Assets(self):
        asset_id = Assets(bank_name='n26').getAssetID()[
            'eur']
        self.assertEqual(asset_id, 5878)

    def test_dateParsingFormat(self):
        config = Config(template_type='all').template()
        bank_dates = {
            'kh': '2020.01.01',
            'revolut': '1. Jan 2020',
            'otp_debit': '20200101',
            'otp_credit': '20200101',
            'n26': '2020-01-01'
        }
        for bank in config:
            date_format = config[bank]['parsing_settings']['date_format']
            date_converting = str(dateConverter(
                date_format, bank_dates[bank]))
            self.assertEqual(date_converting, '2020-01-01')

    def test_DataTransform_kh(self):
        test_data_result = {}
        bank = 'kh'
        file_path = 'test/data/kh.csv'
        config = Config(template_type=bank).template()
        csv_read_type = config['parsing_settings']['csv_read_type']
        csv_column_config = config['csv_column_config']
        delimiter = config['parsing_settings']['delimiter']
        date_format = config['parsing_settings']['date_format']
        raw_data = Csv(csv_read_type=csv_read_type, file_path=file_path,
                       delimiter=delimiter).reader()
        data = dataTransform().transform(bank_name=bank, raw_data=raw_data,
                                         csv_column_config=csv_column_config, date_format=date_format)
        for row in data:
            test_data_result.update({'date': '2020-04-30'})
            test_data_result.update({'payee': 'TEST PAYEE'})
            test_data_result.update(
                {'amount': row['transaction']['amount']})
            test_data_result.update(
                {'currency': row['transaction']['currency']})
            test_data_result.update({'notes': 'TEST NOTES'})
            self.assertDictEqual(row['transaction'], test_data_result)

    def test_DataTransform_revolut(self):
        test_data_result = {}
        bank = 'revolut'
        file_path = 'test/data/revolut.csv'
        config = Config(template_type=bank).template()
        csv_read_type = config['parsing_settings']['csv_read_type']
        csv_column_config = config['csv_column_config']
        delimiter = config['parsing_settings']['delimiter']
        date_format = config['parsing_settings']['date_format']
        raw_data = Csv(csv_read_type=csv_read_type, file_path=file_path,
                       delimiter=delimiter).reader()
        data = dataTransform().transform(bank_name=bank, raw_data=raw_data,
                                         csv_column_config=csv_column_config, date_format=date_format)
        for row in data:
            test_data_result.update({'date': '2020-04-30'})
            test_data_result.update({'payee': 'TEST PAYEE'})
            if row['transaction']['payee'] == 'TEST INCOME':
                test_data_result.update({'payee': 'TEST INCOME'})
                if float(row['transaction']['amount']) >= 0:
                    pass
                else:
                    raise(ValueError)
            else:
                if float(row['transaction']['amount']) < 0:
                    pass
                else:
                    print(row['transaction']['amount'])
                    raise(ValueError)
            test_data_result.update(
                {'amount': row['transaction']['amount']})
            test_data_result.update(
                {'currency': row['transaction']['currency']})
            test_data_result.update({'notes': 'TEST NOTES'})
            self.assertDictEqual(row['transaction'], test_data_result)

    def test_DataTransform_n26(self):
        test_data_result = {}
        bank = 'n26'
        file_path = 'test/data/n26.csv'
        config = Config(template_type=bank).template()
        csv_read_type = config['parsing_settings']['csv_read_type']
        csv_column_config = config['csv_column_config']
        delimiter = config['parsing_settings']['delimiter']
        date_format = config['parsing_settings']['date_format']
        raw_data = Csv(csv_read_type=csv_read_type, file_path=file_path,
                       delimiter=delimiter).reader()
        data = dataTransform().transform(bank_name=bank, raw_data=raw_data,
                                         csv_column_config=csv_column_config,
                                         date_format=date_format)
        for row in data:
            test_data_result.update({'date': '2020-04-30'})
            test_data_result.update({'payee': 'TEST PAYEE'})
            test_data_result.update(
                {'amount': row['transaction']['amount']})
            test_data_result.update(
                {'currency': row['transaction']['currency']})
            test_data_result.update({'notes': 'TEST NOTES'})
            self.assertDictEqual(row['transaction'], test_data_result)

    def test_DataTransform_otp_debit(self):
        test_data_result = {}
        bank = 'otp_debit'
        file_path = 'test/data/otp_debit.csv'
        config = Config(template_type=bank).template()
        csv_read_type = config['parsing_settings']['csv_read_type']
        csv_column_config = config['csv_column_config']
        delimiter = config['parsing_settings']['delimiter']
        date_format = config['parsing_settings']['date_format']
        raw_data = Csv(csv_read_type=csv_read_type, file_path=file_path,
                       delimiter=delimiter).reader()
        data = dataTransform().transform(bank_name=bank, raw_data=raw_data,
                                         csv_column_config=csv_column_config,
                                         date_format=date_format)
        for row in data:
            test_data_result.update({'date': '2020-04-30'})
            test_data_result.update({'payee': 'TEST PAYEE'})
            if row['transaction']['payee'] == 'TEST PAYEE NOTES':
                test_data_result.update({'payee': 'TEST PAYEE NOTES'})
            test_data_result.update(
                {'amount': row['transaction']['amount']})
            test_data_result.update(
                {'currency': row['transaction']['currency']})
            test_data_result.update({'notes': 'TEST NOTES'})
            if row['transaction']['payee'] == 'TEST PAYEE NOTES':
                test_data_result.update({'notes': 'TEST PAYEE NOTES'})
            self.assertDictEqual(row['transaction'], test_data_result)

    def test_DataTransform_otp_credit(self):
        test_data_result = {}
        bank = 'otp_credit'
        file_path = 'test/data/otp_credit.csv'
        config = Config(template_type=bank).template()
        csv_read_type = config['parsing_settings']['csv_read_type']
        csv_column_config = config['csv_column_config']
        delimiter = config['parsing_settings']['delimiter']
        date_format = config['parsing_settings']['date_format']
        raw_data = Csv(csv_read_type=csv_read_type, file_path=file_path,
                       delimiter=delimiter).reader()
        data = dataTransform().transform(bank_name=bank, raw_data=raw_data,
                                         csv_column_config=csv_column_config,
                                         date_format=date_format)
        for row in data:
            test_data_result.update({'date': '2020-04-30'})
            test_data_result.update({'payee': 'TEST PAYEE'})
            if row['transaction']['payee'] == 'TEST PAYEE NOTES':
                test_data_result.update({'payee': 'TEST PAYEE NOTES'})
            test_data_result.update(
                {'amount': row['transaction']['amount']})
            test_data_result.update(
                {'currency': row['transaction']['currency']})
            test_data_result.update({'notes': 'TEST NOTES'})
            if row['transaction']['payee'] == 'TEST PAYEE NOTES':
                test_data_result.update({'notes': 'TEST PAYEE NOTES'})
            self.assertDictEqual(row['transaction'], test_data_result)


if __name__ == '__main__':
    unittest.main()
