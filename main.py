# -*- coding: utf-8 -*-


import json
import calendar
import click

from lunchmoney import Lunchmoney
from helper import genUuid
from database import Transaction
from csv_load import Csv
from config import Config
from datatransform import dataTransform


@click.group(chain=True)
def cli():
    pass


@cli.command('data-import')
@click.option('--bank-type',
              type=click.Choice(['kh', 'revolut',
                                 'n26', 'otp_debit',
                                 'otp_credit'], case_sensitive=True))
@click.option('--file-path', help='CSV file path', type=click.Path(exists=True))
def data_import(bank_type, file_path):
    bank = str(bank_type)
    config = Config(template_type=bank).template()
    csv_read_type = config['parsing_settings']['csv_read_type']
    csv_column_config = config['csv_column_config']
    delimiter = config['parsing_settings']['delimiter']
    date_format = config['parsing_settings']['date_format']
    file_path = str(file_path)
    raw_data = Csv(csv_read_type=csv_read_type, file_path=file_path,
                   delimiter=delimiter).reader()
    data = dataTransform().transform(bank_name=bank, raw_data=raw_data,
                                     csv_column_config=csv_column_config, date_format=date_format)
    for row in data:
        random_id = genUuid()
        print(Transaction.create(
            id=random_id, data=row['transaction'], asset_id=row['asset_id']))


@cli.command('lunchmoney-id')
@click.option('--token', help='Lunchmoney api token')
@click.option('--year', help='Example format: 2020')
@click.option('--month', help='Exampel format: 05')
def lunchmoney_id_import(token, year, month):
    start_of_day = ("%s-%s-01" % (year, month))
    last_day_month = calendar.monthrange(int(year), int(month))[1]
    end_of_day = ("%s-%s-%s" % (year, month, last_day_month))
    query_result = json.loads(Lunchmoney(token=str(token)).getAllTransactions(
        {'start_date': start_of_day, 'end_date': end_of_day}))
    for row in query_result['transactions']:
        (Transaction.update(lunchmoney_id=row['id']).where(
            Transaction.id == row['external_id'])).execute()


@cli.command('data-export')
@click.option('--token', help='Lunchmoney api token')
def data_export(token):
    query_result = Transaction.select(Transaction.id, Transaction.data, Transaction.asset_id).where(
        Transaction.lunchmoney_id.is_null(True))
    result = []
    for row in query_result:
        data = dict(row.data)
        data.update({'asset_id': row.asset_id})
        data.update({'external_id': row.id})
        result.append(data)
    response = Lunchmoney(token=str(token)).insertTransactions(result)
    print(response)


if __name__ == '__main__':
    cli()
