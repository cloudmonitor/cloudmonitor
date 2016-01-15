# _*_ coding:utf-8 _*_

import requests
import json
import types

# 常量
TOKEN_URL = 'http://192.168.0.170:5000/v2.0/tokens'
USER_PWD = '{"auth": {"tenantName": "%s", "passwordCredentials": {"username": "%s", "password": "%s"}}}'
TENANT_URL = 'http://192.168.0.170:5000/v2.0/tenants'
TENANT_VM_URL = 'http://192.168.0.170:8774/v2/{tenant_id}/servers'
CEILOMETER_RESOURCE_URL = 'http://192.168.0.170:8777/v2/resources'
CEILOMETER_METER_SAMPLE = 'http://192.168.0.170:8777/v2/meters/{meter_name}'



def get_token(tenant_name, username, password):
    """获取指定用户名密码的TOKEN,返回TOKEN值"""
    user_pwd = str(USER_PWD) % (tenant_name, username, password)
    params = json.dumps(eval(user_pwd))
    headers = {"Content-type": "application/json", "Accept": "application/json"}
    r = requests.post(TOKEN_URL, data=params, headers=headers)
    resjson = r.json()
    return resjson["access"]["token"]["id"]


def get_tenants(token):
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
    headers = {"Content-type": "application/json", "X-Auth-Token": token, "Accept": "application/json"}
    r = requests.get(TENANT_URL, headers=headers)
    return r.json()


def get_tenant_vms(token, tenant_id):
    """获取某一租户下的所有vm"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token, "Accept": "application/json"}
    url = TENANT_VM_URL.format(tenant_id=tenant_id)
    r = requests.get(url, headers=headers)
    return r.json()


def get_tenant_resorces(token):
    """获取某一租户下面的资源"""
    # payload = {"q": [{"field": "timestamp", "op": "ge", "value": "2016-01-12T13:34:17"}]}
    headers = {"Content-type": "application/json", "X-Auth-Token": token, "Accept": "application/json"}
    r = requests.get(CEILOMETER_RESOURCE_URL, headers=headers)
    return r.json()


def get_meter_sample(token, meter_name):

    # 参数问题
    payload = {"q": [{"field": "timestamp", "op": "ge", "value": "2016-01-13T02:34:17"},
                     {"field": "timestamp", "op": "le", "value": "2016-01-13T04:00:17"},
                     {"field": "timestamp", "op": "le", "value": "2016-01-13T04:00:17"}]}
    urllist = [CEILOMETER_METER_SAMPLE.format(meter_name=meter_name), '?']

    for key, value in payload.items():
        if type(value) is types.ListType:
            for val in value:
                for k1, v1 in val.items():
                    urllist.append(key+'.'+k1+'='+v1+'&')
        else:
            urllist.append(key+'='+str(value)+'&')

    url = ''.join(urllist).rstrip('&')
    # ?q.field=timestamp&q.op=gt&q.value=2016-01-12T13:34:17
    headers = {"Content-type": "application/json", "X-Auth-Token": token, "Accept": "application/json"}
    r = requests.get(url, headers=headers)
    return r.json()


def get_vm_meter():
    pass


if __name__ == "__main__":

    # 通过用户和密码获取token
    token = get_token("", "user01", "user01")

    # 获取租户
    tenant_name = get_tenants(token)['tenants'][0]['name']
    tenant_id = get_tenants(token)['tenants'][0]['id']

    # 获取某一租户下的所有vm
    token = get_token(tenant_name, "user01", "user01")
 

    # print get_tenant_vms(token, tenant_id)

    # 获取某一租户下面的资源
    print get_tenant_resorces(token)

    print get_meter_sample(token, 'disk.usage')