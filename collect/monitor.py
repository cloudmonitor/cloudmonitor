# _*_ coding:utf-8 _*_

import requests
import json
import types

# 常量

CREDENTIAL_PASSWORD = '{"auth": {"tenantName": "%s", "passwordCredentials": {"username": "%s", "password": "%s"}}}'
CREDENTIAL_TOKEN = '{"auth":{"tenantName":"%s","token":{"id":"%s"}}}'

CEILOMETER_METER_SAMPLE = 'http://192.168.0.170:8777/v2/meters/{meter_name}'

KEYSTONE_ENDPOINT = 'http://controller:5000/v2.0'
GLANCE_ENDPOINT = 'http://controller:9292/v2'
NOVA_ENDPOINT = 'http://controller:8774/v2/{tenant_id}'
NEUTRON_ENDPOINT = 'http://controller:9696/v2.0'
CEILOMETER_ENDPOINT = 'http://controller:8777/v2'


def get_user_token(username, password):
    """获取指定用户名密码的TOKEN,返回json"""
    credential = CREDENTIAL_PASSWORD % ('', username, password)
    headers = {"Content-type": "application/json", "Accept": "application/json"}
    r = requests.post(KEYSTONE_ENDPOINT+'/tokens', data=credential, headers=headers)
    return r.json()


def get_tenant_token(tenantname, token):
    """获取指定租户、用户名、密码的TOKEN,返回json"""
    credential = CREDENTIAL_TOKEN % (tenantname, token)
    headers = {"Content-type": "application/json", "Accept": "application/json"}
    r = requests.post(KEYSTONE_ENDPOINT+'/tokens', data=credential, headers=headers)
    response_json = r.json()
    return response_json


def get_tenants(token_id):
    """获取指定TOKEN下的所有租户，返回一个租户字典,通过['tenants'][0 1 ... n]['id']取得租户id,返回样例如下"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    r = requests.get(KEYSTONE_ENDPOINT+'/tenants', headers=headers)
    return r.json()


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


def get_tenant_limits(token_id, tenant_id):
    """获取租户的资源配额限制"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id)
    r = requests.get(url+'/limits', headers=headers)
    return r.json()


def get_tenant_flavors(token_id, tenant_id):
    """获取租户的flavor"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id)
    r = requests.get(url+'/flavors/detail', headers=headers)
    return r.json()


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


def get_tenant_resources(token_id):
    """获取某一租户下面的资源"""
    # payload = {"q": [{"field": "timestamp", "op": "ge", "value": "2016-01-12T13:34:17"}]}
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    r = requests.get(CEILOMETER_ENDPOINT+'/resources', headers=headers)
    return r.json()


def _get_instance_resource_url(token_id, instance_id, meter_name):
    """获取跟主机相关的meter的url"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    r = requests.get(CEILOMETER_ENDPOINT+'/resources', headers=headers)
    for resource in r.json():
        if resource['resource_id'] == instance_id:
            for link in resource['links']:
                if link['rel'] == meter_name:
                    return link['href']
    return None


def _get_instance_network_resource_url(token_id, instance_id, meter_name):
    """获取主机网络相关meter的url"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    r = requests.get(CEILOMETER_ENDPOINT+'/resources', headers=headers)

    for resource in r.json():
        regex = instance_id + '-' + resource['metadata']['vnic_name']
        if resource['resource_id'].endswith(regex):
            for link in resource['links']:
                if link['rel'] == meter_name:
                    return link['href']
    return None


def get_tenant_instance_meter(token_id, instance_id, meter_name):
    # 参数问题
    payload = {"q": [{"field": "timestamp", "op": "ge", "value": "2016-01-13T02:34:17"},
                     {"field": "timestamp", "op": "le", "value": "2016-01-13T04:00:17"}]}
    url = _get_instance_resource_url(token_id, instance_id, meter_name)
    url_list = [url, '&q.op=eq&']

    for key, value in payload.items():
        if isinstance(value, list):
            for val in value:
                for k1, v1 in val.items():
                    url_list.append(key+'.'+k1+'='+v1+'&')
        else:
            url_list.append(key+'='+str(value)+'&')

    url = ''.join(url_list).rstrip('&')
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    r = requests.get(url, headers=headers)
    return r.json()


def get_tenant_instance_network_meter(token_id, instance_id, meter_name):
    # 参数问题
    payload = {"q": [{"field": "timestamp", "op": "ge", "value": "2016-01-13T02:34:17"},
                     {"field": "timestamp", "op": "le", "value": "2016-01-13T04:00:17"}]}
    url = _get_instance_network_resource_url(token_id, instance_id, meter_name)
    url_list = [url, '&q.op=eq&']

    for key, value in payload.items():
        if isinstance(value, list):
            for val in value:
                for k1, v1 in val.items():
                    url_list.append(key+'.'+k1+'='+v1+'&')
        else:
            url_list.append(key+'='+str(value)+'&')

    url = ''.join(url_list).rstrip('&')
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    r = requests.get(url, headers=headers)
    return r.json()


if __name__ == "__main__":

    # 通过用户和密码获取token
    token_json = get_user_token("user01", "user01")
    print token_json

    token_id = token_json['access']['token']['id']

    # 获取租户
    print get_tenants(token_id)
    tenant_name = get_tenants(token_id)['tenants'][0]['name']
    tenant_id = get_tenants(token_id)['tenants'][0]['id']

    # 获取租户的tonken
    token_json = get_tenant_token(tenant_name, "user01", "user01")
    token_id = token_json['access']['token']['id']

    # print get_tenant_vms(token, tenant_id)

    # 获取某一租户下面的资源

    print get_tenant_instance_meter(token_id, "0443f44e-2364-4211-803c-08afbe65b26e", "cpu_util")



