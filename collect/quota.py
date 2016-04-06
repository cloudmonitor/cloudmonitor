# _*_ coding:utf-8 _*_


from settings import *
from floatingip import get_floating_ips
from securitygroup import get_security_groups


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



