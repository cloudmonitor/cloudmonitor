# _*_ coding:utf-8 _*_

from settings import *


def get_floating_ips(token_id, tenant_id):
    """ 列出floating ip"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id) + '/os-floating-ips'
    r = requests.get(url, headers=headers)
    return r.json()


def get_floating_ips_pool(token_id, tenant_id):
    """获取分配外网IP的网络"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id) + '/os-floating-ip-pools'
    r = requests.get(url, headers=headers)
    return r.json()


def allocate_floating_ips(token_id, tenant_id, data):
    """分配一个floating ip"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id) + '/os-floating-ips'
    r = requests.post(url, data=data, headers=headers)
    return r.json()


def release_floating_ips(token_id, tenant_id, floating_ip_ids):
    """分配一个floating ip"""
    release_status = {}
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    for i in range(len(floating_ip_ids["floating_ip_ids"])):
        url = NOVA_ENDPOINT.format(tenant_id=tenant_id) + '/os-floating-ips/' + floating_ip_ids["floating_ip_ids"][i]
        r = requests.delete(url, headers=headers)
        release_status[floating_ip_ids["floating_ip_ids"][i]] = r.status_code
    return release_status
