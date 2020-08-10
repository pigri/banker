# -*- coding: utf-8 -*-

from datetime import datetime
import uuid



def dateConverter(input_date_format, date_string):
    date_format = str(input_date_format)
    formated_date = datetime.strptime(date_string, date_format).date()
    # REVOLUT DATE FIX
    formated_date = formated_date.replace(2020)
    return formated_date

def genUuid():
    return uuid.uuid4()
