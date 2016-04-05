# _*_ coding:utf-8 _*_

from settings import *


def get_tenant_instances(token_id, tenant_id):
    """获取某一租户下的所有vm"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id)
    r = requests.get(url+'/servers/detail', headers=headers)
    return r.json()


def get_tenant_instance(token_id, tenant_id, instance_id):
    """获取某一租户下的某一vm"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id)
    r = requests.get(url+'/servers/'+instance_id, headers=headers)
    return r.json()


# def get_tenant_limits(token_id, tenant_id):
#     """获取租户的资源配额限制"""
#     headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
#     url = NOVA_ENDPOINT.format(tenant_id=tenant_id)
#     r = requests.get(url+'/limits', headers=headers)
#     return r.json()


def get_tenant_flavors(token_id, tenant_id):
    """获取租户的flavor"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id)
    r = requests.get(url+'/flavors/detail', headers=headers)
    return r.json()