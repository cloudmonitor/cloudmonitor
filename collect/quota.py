# _*_ coding:utf-8 _*_

from flask import request
from settings import *
from floatingip import get_floating_ips
from securitygroup import get_security_groups
from identify import get_admin_token
from util import auth_is_available


def get_tenant_limits(token_id, tenant_id):
    """获取租户的资源配额限制"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id)
    r = requests.get(url+'/limits', headers=headers)
    limits = r.json()
    limits["limits"]["absolute"]["totalFloatingIpsUsed"] = _get_tenant_floatingips_used(token_id, tenant_id)
    limits["limits"]["absolute"]["totalSecurityGroupsUsed"] = _get_tenant_securitygroups_used(token_id)
    return limits


def _get_tenant_floatingips_used(token_id, tenant_id):
    """获取当前租户创建了多少floatingip"""
    floatingips = get_floating_ips(token_id)
    return len(floatingips["floatingips"])


def _get_tenant_securitygroups_used(token_id):
    """获取当前租户创建了多少安全组"""
    securitygroups = get_security_groups(token_id)
    return len(securitygroups["security_groups"])


def _get_compute_quota(tenant_id):
    """根据租户id获取计算方面的配额"""
    compute_quota = {}
    admin_token_id = get_admin_token()['access']['token']['id']
    headers = {"Content-type": "application/json", "X-Auth-Token": admin_token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT01+'/os-quota-sets/'+tenant_id + '/detail'
    r = requests.get(url, headers=headers)
    compute_quota_list = r.json()
    compute_quota['metadata_items'] = compute_quota_list['quota_set']['metadata_items']['limit']
    compute_quota['cores'] = compute_quota_list['quota_set']['cores']['limit']
    compute_quota['instances'] = compute_quota_list['quota_set']['instances']['limit']
    compute_quota['injected_files'] = compute_quota_list['quota_set']['injected_files']['limit']
    compute_quota['injected_file_content_bytes'] = compute_quota_list['quota_set']['injected_file_content_bytes']['limit']
    compute_quota['ram'] = compute_quota_list['quota_set']['ram']['limit']
    return compute_quota


def _get_network_quota(tenant_id):
    """根据获取所有网络方面的配额"""
    admin_token_id = get_admin_token()['access']['token']['id']
    headers = {"Content-type": "application/json", "X-Auth-Token": admin_token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT+'/quotas'
    r = requests.get(url, headers=headers)
    network_info_list =  r.json()
    for i in range(len(network_info_list['quotas'])):
        if tenant_id == network_info_list['quotas'][i]['tenant_id']:
            network_info = network_info_list['quotas'][i]
            break
    return network_info


@auth_is_available
def get_tenant_quota(tenant_id):
    """获取跟租户相关的配额信息"""
    compute_info = _get_compute_quota(tenant_id)
    network_info = _get_network_quota(tenant_id)
    tenant_quota = dict(network_info, **compute_info)
    return json.dumps(tenant_quota)


def get_tenant_quota_bak(token,tenant_id):
    """获取跟租户相关的配额信息"""
    if auth_is_available(token):
        compute_info = _get_compute_quota(tenant_id)
        network_info = _get_network_quota(tenant_id)
        tenant_quota = dict(network_info, **compute_info)
        return tenant_quota
    else:
        return json.loads('{"error":"not available"}')