# -*- coding: utf-8 -*-

import csv


class Csv(object):
    def __init__(self, **kwargs):
        self.csv_read_type = str(kwargs['csv_read_type'])
        self.file_path = str(kwargs['file_path'])
        self.delimiter = str(kwargs['delimiter'])

    def reader(self):
        if self.csv_read_type == 'dict_reader':
            return self.__dictReader()
        elif self.csv_read_type == 'line_reader':
            return self.__lineReader()
        else:
            return {'error_message': 'Undifined reader type'}

    def __dictReader(self):
        data = []
        with open('%s' % (str(self.file_path)), 'r') as csvfile:
            file = csv.DictReader(
                csvfile, delimiter=str(self.delimiter))
            for row in file:
                data.append(row)
        return data

    def __lineReader(self):
        data = []
        with open('%s' % (str(self.file_path)), 'r') as csvfile:
            file = csv.reader(
                csvfile, delimiter=str(self.delimiter))
            for row in file:
                data.append(row)
        return data
