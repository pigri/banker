# -*- coding: utf-8 -*-

import json
import requests


class Lunchmoney(object):
    def __init__(self, **kwargs):
        token = kwargs['token']
        self.url = 'https://dev.lunchmoney.app/v1/transactions'
        self.headers = {
            'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}

    def jsonTemplate(self, data):
        data = json.dumps(data)
        response = '''{"transactions":%s, "debit_as_negative":true, "check_for_recurring": true, "apply_rules": true }''' % (
            data)
        return str(response)

    def getAllTransactions(self, payload):
        req = requests.get(self.url,
                           headers=self.headers, params=payload)
        return req.content

    def insertTransactions(self, data):
        json_tempalte = self.jsonTemplate(data)
        req = requests.post(self.url,
                            data=json_tempalte, headers=self.headers)
        return req.text
