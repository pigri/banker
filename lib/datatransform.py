# -*- coding: utf-8 -*-

import re
from helper import dateConverter
from assets import Assets


class dataTransform(object):
    def transform(self, **kwargs):
        class khBank(dataTransform):
            def data_transform(self, row):
                currency = row[csv_column_config['currency']].lower()
                notes = row[csv_column_config['notes']]
                amount = row[csv_column_config['amount']]
                payee = row[csv_column_config['payee'][1]]

                if payee == '':
                    payee = row[csv_column_config['payee'][0]]
                date = str(dateConverter(
                    date_format, row[csv_column_config['date']]))
                return {'date': date, 'payee': payee,
                        'amount': amount, 'currency': currency, 'notes': notes}

            def asset_id(self, row, asset_ids):
                return asset_ids[row[csv_column_config['asset_id']]]

        class revolutBank(dataTransform):
            def data_transform(self, row):
                currency = self.__currency(row)
                paid_out = row[csv_column_config['amount'][0] %
                               (currency.upper())]
                paid_in = row[csv_column_config['amount'][1] %
                              (currency.upper())]
                if paid_out == '':
                    amount = paid_in.replace(',', '')
                else:
                    expense = '-' + paid_out.strip()
                    amount = expense.replace(',', '')

                notes = row[csv_column_config['notes']]
                payee = row[csv_column_config['payee']]
                date = str(dateConverter(
                    date_format, row[csv_column_config['date']]))
                return {'date': date, 'payee': payee,
                        'amount': amount, 'currency': currency, 'notes': notes}

            def asset_id(self, row, asset_ids):
                currency = self.__currency(row)
                return asset_ids[currency]

            def __currency(self, row):
                fields = []
                for key in row.keys():
                    if re.match('^Paid Out(.*)', key) != None:
                        fields.append(key.split(' ')[2].replace(
                            ')', '').replace('(', '').lower())
                return fields[0]

        class otpBank(dataTransform):
            def data_transform(self, row):
                currency = csv_column_config['currency']
                if currency != 'huf':
                    currency = row[csv_column_config['currency']].lower()
                notes = row[csv_column_config['notes']]
                amount = row[csv_column_config['amount']]
                payee = row[csv_column_config['payee']]
                date = str(dateConverter(
                    date_format, row[csv_column_config['date']]))
                if payee == '':
                    payee = notes
                return {'date': date, 'payee': payee,
                        'amount': amount, 'currency': currency, 'notes': notes}

            def asset_id(self, row, asset_ids):
                return asset_ids[row[csv_column_config['asset_id']]]

        class n26Bank(dataTransform):
            def data_transform(self, row):
                currency = self.__currency(row)
                amount = row[csv_column_config['amount'] %
                             (currency.upper())]
                notes = row[csv_column_config['notes']]
                payee = row[csv_column_config['payee']]
                date = str(dateConverter(
                    date_format, row[csv_column_config['date']]))
                return {'date': date, 'payee': payee,
                        'amount': amount, 'currency': currency, 'notes': notes}

            def asset_id(self, row, asset_ids):
                currency = self.__currency(row)
                return asset_ids[currency]

            def __currency(self, row):
                fields = []
                for key in row.keys():
                    if re.match('^Amount\D{6}$', key) != None:
                        fields.append(key.split(' ')[1].replace(
                            ')', '').replace('(', '').lower())
                return fields[0]

        bank_name = str(kwargs['bank_name'])
        if re.match('otp_(.*)', bank_name):
            bank_name = 'otp'
        raw_data = kwargs['raw_data']
        csv_column_config = kwargs['csv_column_config']
        date_format = str(kwargs['date_format'])
        asset_ids = Assets(bank_name=bank_name).getAssetID()
        for i in dataTransform.__subclasses__():
            bank_class = bank_name + "Bank"
            if str(i).split('.')[4].replace("'>", '') == bank_class:
                function = bank_name + "Bank"
        data = []
        for row in raw_data:
            main = {}
            main['transaction'] = {}
            transaction = eval(function + "().data_transform(%s)" % (row))
            asset_id = eval(function + "().asset_id(%s,%s)" %
                            (row, asset_ids))
            main['transaction'].update(transaction)
            main.update({'asset_id': asset_id})
            data.append(main)
        return data
