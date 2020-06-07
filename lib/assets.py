# -*- coding: utf-8 -*-

from yaml import load, Loader
from os import environ


class Assets(object):
    def __init__(self, **kwargs):
        self.bank_name = str(kwargs['bank_name'])

    def getAssetID(self):
        config = 'config/assets.yml'
        if environ['ENV'] == 'test':
            config = 'config/assets_test.yml'
        stream = open(config, 'r')
        assets = load(stream, Loader=Loader)
        stream.close()
        if self.bank_name == 'all':
            return assets
        return assets[self.bank_name]
