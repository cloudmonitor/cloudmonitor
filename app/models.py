# _*_ coding:utf-8 _*_

# from . import login_manager
from flask.ext.login import UserMixin

# USER = []


class User(UserMixin):

    def __init__(self, attrdict):
        self._parse_json(attrdict)

    def _parse_json(self, attrdict):
        self.id = attrdict['access']['user']['id']
        self.username = attrdict['access']['user']['username']
        self.token_id = attrdict['access']['token']['id']
        if 'tenant' in attrdict['access']['token']:
            self.tenant_id = attrdict['access']['token']['tenant']['id']
            self.tenant_name = attrdict['access']['token']['tenant']['name']
        else:
            self.tenant_id = ''
            self.tenant_name = ''

    def to_json(self):
        json_user = {
            'id': self.id,
            'username': self.username,
            'token_id': self.token_id,
            'tenant_id': self.tenant_id,
            'tenant_name': self.tenant_name
        }
        return json_user

    def set_tenant(self):
        pass

    # def get_id(self):
    #     if len(USER) != 0:
    #         return USER[0].id
    #     return None


# @login_manager.user_loader
# def load_user(user_id):
#     return USER[0]
