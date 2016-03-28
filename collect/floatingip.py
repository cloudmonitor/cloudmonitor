# _*_ coding:utf-8 _*_

from settings import *


def get_floating_ips(token_id):
    """ 列出floating ip"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + '/floatingips'
    r = requests.get(url, headers=headers)
    return r.json()



