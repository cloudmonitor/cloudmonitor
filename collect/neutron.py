# _*_ coding:utf-8 _*_

from settings import *


def get_tenant_networks(token_id):
    """获取租户的flavor"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT
    r = requests.get(url+'/networks', headers=headers)
    return r.json()


def get_tenant_subnets(token_id):
    """获取租户的flavor"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT
    r = requests.get(url+'/subnets', headers=headers)
    return r.json()


def get_tenant_routers(token_id):
    """获取租户的flavor"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT
    r = requests.get(url+'/routers', headers=headers)
    return r.json()


def get_tenant_ports(token_id):
    """ 获取所有的端口的信息"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + "/ports"
    r = requests.get(url=url, headers=headers)
    return r.json()




