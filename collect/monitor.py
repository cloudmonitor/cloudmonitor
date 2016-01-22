# _*_ coding:utf-8 _*_

import requests
import json
import types

# 常量

CREDENTIAL = '{"auth": {"tenantName": "%s", "passwordCredentials": {"username": "%s", "password": "%s"}}}'

CEILOMETER_METER_SAMPLE = 'http://192.168.0.170:8777/v2/meters/{meter_name}'

KEYSTONE_ENDPOINT = 'http://controller:5000/v2.0'
GLANCE_ENDPOINT = 'http://controller:9292/v2/'
NOVA_ENDPOINT = 'http://controller:8774/v2/{tenant_id}'
NEUTRON_ENDPOINT = 'http://controller:9696/v2.0'
CEILOMETER_ENDPOINT = 'http://controller:8777/v2'


def get_user_token(username, password):
    """获取指定用户名密码的TOKEN,返回json"""
    user_pwd = str(CREDENTIAL) % ('', username, password)
    params = json.dumps(eval(user_pwd))
    headers = {"Content-type": "application/json", "Accept": "application/json"}
    r = requests.post(KEYSTONE_ENDPOINT+'/tokens', data=params, headers=headers)
    return r.json()


def get_tenant_token(tenant_name, username, password):
    """获取指定租户、用户名、密码的TOKEN,返回json"""
    user_pwd = str(CREDENTIAL) % (tenant_name, username, password)
    params = json.dumps(eval(user_pwd))
    headers = {"Content-type": "application/json", "Accept": "application/json"}
    r = requests.post(KEYSTONE_ENDPOINT+'/tokens', data=params, headers=headers)
    response_json = r.json()
    return response_json


# def _set_service_endpoint(token_json):
#     """设置相应服务的endpoint"""
#     for endpoint in token_json['access']['serviceCatalog']:
#         if endpoint['name'] == 'nova':
#             NOVA_ENDPOINT = endpoint['endpoints'][0]['publicURL']
#         elif endpoint['name'] == 'glance':
#             GLANCE_ENDPOINT = endpoint['endpoints'][0]['publicURL']
#         elif endpoint['name'] == 'neutron':
#             NEUTRON_ENDPOINT = endpoint['endpoints'][0]['publicURL']
#         elif endpoint['name'] == 'ceilometer':
#             CEILOMETER_ENDPOINT = endpoint['endpoints'][0]['publicURL']
#         else:
#             pass


def get_tenants(token_id):
    """获取指定TOKEN下的所有租户，返回一个租户字典,通过['tenants'][0 1 ... n]['id']取得租户id,返回样例如下
        {
          "tenants_links": [],
          "tenants": [
            {
              "description": "tenant01 testing",
              "enabled": true,
              "id": "e74268a4e2f84bf9bf280e252d1c158e",
              "name": "tenant01"
            },
            {
              "description": "tenant02",
              "enabled": true,
              "id": "fa77ba26908b4f1baefed7c2ae8a63ef",
              "name": "tenant02"
            }
          ]
        }
    """
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    r = requests.get(KEYSTONE_ENDPOINT+'/tenants', headers=headers)
    return r.json()


def get_tenant_instances(token_id, tenant_id):
    """获取某一租户下的所有vm"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id)
    r = requests.get(url+'/servers', headers=headers)
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



