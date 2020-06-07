# -*- coding: utf-8 -*-

from yaml import load, Loader


class Config(object):
    def __init__(self, **kwargs):
        self.template_type = str(kwargs['template_type'])

    def template(self):
        stream = open('config/config.yml', 'r')
        template = load(stream, Loader=Loader)
        stream.close()
        if self.template_type == 'all':
            return template
        return template[self.template_type]
