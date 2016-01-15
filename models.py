# _*_ coding:utf-8 _*_



class User(object):

    def __init__(self, attrdict):
        self._parse_json(attrdict)

    def _parse_json_touser(self, attrdict):
        self.id = attrdict['access']['user']['id']
        self.username = attrdict['access']['user']['username']
        self.token_id = attrdict['access']['user']['username']
        self.tenants = []

