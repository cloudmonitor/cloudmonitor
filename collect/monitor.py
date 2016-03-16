# _*_ coding:utf-8 _*_

import requests
import json
import types
import time
import  datetime

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


def get_instance_network_resource_id(token_id, instance_id, meter_name):
    """获取主机网络相关meter的url"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    r = requests.get(CEILOMETER_ENDPOINT+'/resources', headers=headers)
    for resource in r.json():
        if resource['metadata'].has_key('vnic_name'):
            regex = instance_id + '-' + resource['metadata']['vnic_name']
            if resource['resource_id'].endswith(regex):
                return resource['resource_id']



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


def get_floatingips(token_id):
    #列出floating ip
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + '/floatingips'
    r = requests.get(url, headers=headers)
    return r.json()


def get_port_all_info(token_id):
    #获取所有的端口的信息
    headers = {"X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + "/ports"
    r = requests.get(url=url, headers=headers)
    return r.json()


def get_security_groups(token_id):
    #列出安全组的信息
    headers = {"X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + '/security-groups'
    r = requests.get(url, headers=headers)
    return r.json()


def get_all_rules(token_id):
    # 获取所有的rule的信息
    headers = {"X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + '/fw/firewall_rules'
    r = requests.get(url=url, headers=headers)
    return r.json()


def get_one_rules(token_id,rule_id):
    # 获取某一的rule的信息
    headers = {"X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + '/fw/firewall_rules/'+rule_id
    r = requests.get(url= url, headers= headers)
    return r.json()


def get_all_policies(token_id):
    #获取所有的policys的信息
    headers = {"X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + '/fw/firewall_policies'
    r = requests.get(url= url, headers= headers)
    return r.json()


def get_one_policies(token_id,policies_id):
    #获取某一个policy的信息
    headers = {"X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + '/fw/firewall_policies/'+policies_id
    r = requests.get(url= url, headers= headers)
    return r.json()


def get_all_firewalls_info(token_id):
    #获取所有的Firewalls信息
    headers = {"X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + '/fw/firewalls'
    r = requests.get(url=url, headers=headers)
    return r.json()


def get_one_firewalls_info(token_id,firewalls_id):
    # 获取某一具体Firewalls的信息
    headers = {"X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + '/fw/firewalls/'+firewalls_id
    r = requests.get(url=url, headers=headers)
    firewall_info = r.json()
    print firewall_info
    policy_id = firewall_info['firewall']['firewall_policy_id']
    print policy_id
    policy_all_info = get_all_policies(token_id)
    for item in policy_all_info['firewall_policies']:
        if policy_id == item['id']:
            rule_id = item['firewall_rules']
    for firewall_rule_id in rule_id:
        rule_info = get_one_rules(token_id, firewall_rule_id)
    print rule_info
    return rule_info


def get_all_policies(token_id):
    #获取所有的policys的信息
    headers = {"X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + '/fw/firewall_policies'
    r = requests.get(url= url, headers= headers)
    return r.json()


def get_all_rules(token_id):
    #获取所有的rule的信息
    headers = {"X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + '/fw/firewall_rules'
    r = requests.get(url= url, headers= headers)
    return r.json()

def get_localtime():
    #获取当前时间
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    total_time = time.strftime(ISOTIMEFORMAT,time.localtime())
    return total_time


def Time2ISOString(s):
    #把一个时间转换成秒
    d = datetime.datetime.strptime(s,"%Y-%m-%d %H:%M:%S")
    return time.mktime(d.timetuple())


def ISOString2Time(s):
    #把秒数转换成一个时间
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(float(s)))


def get_meter_func_data(token_id, instance_id, meter_name, type):
    resource_id = get_instance_resource_id(token_id, instance_id, meter_name)
    func_name = "get_list_meter_"+type
    # print func_name
    return eval(func_name)(token_id, meter_name, resource_id)


def get_instance_resource_id(token_id, instance_id, meter_name):
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    r = requests.get(CEILOMETER_ENDPOINT+'/resources', headers=headers)
    for resource in r.json():
        if meter_name.startswith("network."):
            if resource['metadata'].has_key('vnic_name'):
                regex = instance_id + '-' + resource['metadata']['vnic_name']
                if resource['resource_id'].endswith(regex):
                    return resource['resource_id']
        else:
            if resource['resource_id'] == instance_id:
                return resource['resource_id']


def localtime2UTC(s):
    seconds = int(Time2ISOString(s))-28800
    return ISOString2Time(seconds)


def get_one_meter(token_id, time, meter_name ,resource_id ):
    """根据时间来删选数据"""
    Time_reduce = ISOString2Time(Time2ISOString(time)-60)
    headers = {"X-Auth-Token":token_id, "Accept": "application/json"}
    url = CEILOMETER_ENDPOINT + '/meters/'+meter_name+'/?'
    url_list = [url,]
    payload = {"q": [{"field": "timestamp", "op": "gt", "value": Time_reduce},
                     {"field": "timestamp", "op": "lt", "value": time},
                     {"field": "resource_id","value": resource_id}
                    ]}
    for key, value in payload.items():
        if isinstance(value, list):
            for val in value:
                for k1, v1 in val.items():
                    url_list.append(key+'.'+k1+'='+v1+'&')
        else:
            url_list.append(key+'='+str(value)+'&')
    url_list.append("limit=1")
    url = ''.join(url_list)
    # print url
    r = requests.get(url, headers=headers)
    #print r.json()
    return r.json()


def get_list_meter_minute(token_id, meter_name, resource_id):
    #以分钟得到某一组数据
    localtime = localtime2UTC(get_localtime())
    meter_info_list = []
    for i in range(0, 7):
        r = get_one_meter(token_id, localtime, meter_name, resource_id)
        # print r
        if len(r) == 0:
            meter_info_list.append(r)
        else:
            meter_info_list.append(r[0])
        localtime = ISOString2Time(Time2ISOString(localtime)-180)
    r = {meter_name:meter_info_list}

    return r


def get_list_meter_hour(token_id,meter_name, resource_id):
    #以小时得到某一组数据
    localtime = localtime2UTC(get_localtime())
    meter_info_list = []
    for i in range(0, 7):
        r = get_one_meter(token_id, localtime, meter_name, resource_id)
        if len(r) == 0:
            meter_info_list.append(r)
        else:
            meter_info_list.append(r[0])
        localtime01 = datetime.datetime.strptime(localtime,"%Y-%m-%d %H:%M:%S")
        times = localtime01 + datetime.timedelta(hours=-1)
        localtime = datetime.datetime.strftime(times,"%Y-%m-%d %H:%M:%S")
    r = {meter_name:meter_info_list}
    return r


def get_list_meter_day(token_id,meter_name, resource_id):
    #以天得到某一组数据
    localtime = localtime2UTC(get_localtime())
    meter_info_list = []
    for i in range(0, 7):
        r = get_one_meter(token_id, localtime, meter_name, resource_id)
        if len(r) == 0:
            meter_info_list.append(r)
        else:
            meter_info_list.append(r[0])
        print localtime
        localtime01 = datetime.datetime.strptime(localtime,"%Y-%m-%d %H:%M:%S")
        times = localtime01 + datetime.timedelta(days=-1)
        localtime = datetime.datetime.strftime(times,"%Y-%m-%d %H:%M:%S")
        #print localtime
    r = {meter_name:meter_info_list}
    return r


def get_all_port_info(token_id):
    #获取所有的端口的信息
    headers = {"X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + "/ports"
    r = requests.get(url=url, headers=headers)
    return r.json()


def get_one_port_info(token_id,port_id):
    #获取某一端口的信息
    headers = {"X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + "/ports/"+port_id
    r = requests.get(url=url, headers=headers)
    return r.json()


def reduce_one_port_info(one_port_info):
    #简化port数据
    port_info = {}
    one_port_info = one_port_info['port']
    url = "/horizon/project/networks/ports/"+one_port_info["id"]+"/detail"
    port_info["status"]=one_port_info['status']
    port_info["network_id"]=one_port_info['network_id']
    port_info["url"]=url
    port_info["device_owner"]=one_port_info["device_owner"]
    port_info["fixed_ips"]=one_port_info["fixed_ips"]
    port_info["id"]=one_port_info["id"]
    port_info["device_id"]=one_port_info["device_id"]
    return port_info


def get_all_routers_info(token_id):
    #获取所有路由器的信息
    headers = {"X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + '/routers'
    r = requests.get(url=url, headers=headers)
    return r.json()


def get_one_routers_info(token_id, router_id):
    #获取某一具体路由器的信息
    headers = {"X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + '/routers/'+router_id
    r = requests.get(url=url, headers=headers)
    return r.json()


def _get_tuopu_port_info(token_id):
    #获取最终拓扑的端口信息
    ports_info = {}
    ports_list = []
    all_port_info = get_all_port_info(token_id)
    for i in range(len(all_port_info['ports'])):
        port_id = all_port_info['ports'][i]['id']
        one_port_info = get_one_port_info(token_id,port_id)
        ports_list.append(reduce_one_port_info(one_port_info))
    all_routers_info = get_all_routers_info(token_id)
    for i in range(len(all_routers_info["routers"])):
        router_id = all_routers_info['routers'][i]['id']
        one_router_info = get_one_routers_info(token_id,router_id)
        if one_router_info["router"]["external_gateway_info"]:
            ex_port_info = {}
            ex_port_info["network_id "] = one_router_info["router"]["external_gateway_info"]["network_id"]
            ex_port_info["fixed_ips"] = one_router_info["router"]["external_gateway_info"]["external_fixed_ips"]
            ex_port_info["id"] = "gateway"+one_router_info["router"]["external_gateway_info"]["network_id"]
            ex_port_info["device_id"] = one_router_info["router"]["id"]
            ports_list.append(ex_port_info)
    ports_info["ports"] = ports_list
    return ports_info


def reduce_one_router_info(one_router_info):
    #简化router数据
    router_info = {}
    one_router_info = one_router_info['router']
    router_info["status"] = one_router_info["status"]
    router_info["external_gateway_info"] = one_router_info["external_gateway_info"]
    url = "/horizon/project/routers/"+one_router_info["id"]+"/"
    router_info["url"] = url
    router_info["id"] = one_router_info["id"]
    router_info["name"] = one_router_info["name"]
    return router_info


def _get_tuopu_router_info(token_id):
    #获取路由器的拓扑图
    routers_info = {}
    routers_list = []
    all_routers_info = get_all_routers_info(token_id)
    for i in range(len(all_routers_info['routers'])):
        router_id = all_routers_info['routers'][i]['id']
        one_router_info = get_one_routers_info(token_id,router_id)
        routers_list.append(reduce_one_router_info(one_router_info))
    routers_info["routers"] = routers_list
    return routers_info


def _get_subnet_detail(network_id, subnet_info):
    simple_subnet_info = []
    for i in range(len(subnet_info["subnets"])):
        _simple_subnet_info = {}
        if subnet_info["subnets"][i]["network_id"] == network_id:
            _simple_subnet_info["url"] = ""
            _simple_subnet_info["cidr"] = subnet_info["subnets"][i]["cidr"]
            _simple_subnet_info["id"] = subnet_info["subnets"][i]["id"]
            simple_subnet_info.append(_simple_subnet_info)
    return simple_subnet_info


def _get_tuopu_network_info(network_info, subnet_info):
    reduce_net_info = {}
    net_info = []
    for i in range(len(network_info["networks"])):
        _net_info = {}
        _net_info["status"] = network_info["networks"][i]["status"]
        _net_info["subnets"] = _get_subnet_detail(network_info["networks"][i]["id"], subnet_info)
        _net_info["name"] = network_info["networks"][i]["name"]
        _net_info["router:external"] = network_info["networks"][i]["router:external"]
        _net_info["url"] = ""
        _net_info["id"] = network_info["networks"][i]["id"]
        net_info.append(_net_info)
    reduce_net_info["networks"] = net_info
    return reduce_net_info


def _get_servers_detail(token_id,tenant_id):
    #获取某一租户的servers的详细情况
    headers = {"X-Auth-Token": token_id, "Accept": "application/json"}
    url = "http://controller:8774/v2/" +tenant_id+"/servers/detail"
    r = requests.get(url=url, headers=headers)
    return r.json()


def _get_tuopu_servers_info(severs_info_detail):
    servers_list = []
    servers_info = {}
    for i in range(len(severs_info_detail["servers"])):
        one_servers_info = {}
        one_servers_info["status"] = severs_info_detail["servers"][i]["status"]
        one_servers_info["task"] = "null"
        one_servers_info["console"] = "vnc"
        one_servers_info["name"] = severs_info_detail["servers"][i]["name"]
        one_servers_info["url"] = ""
        one_servers_info["id"] = severs_info_detail["servers"][i]["id"]
        servers_list.append(one_servers_info)
    servers_info["servers"] = servers_list
    return servers_info


def get_network_all_info(token_id):
    #获取所有网络信息
    headers = {"X-Auth-Token":token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT+"/networks"
    r = requests.get(url,headers = headers)
    return r.json()


def get_network_one_info(token_id,network_id):
    #根据network_id获取某一特定的网络信息
    headers = {"X-Auth-Token":token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + '/networks/'+network_id
    r = requests.get(url, headers=headers)
    return r.json()


def get_subnet_all_info(token_id):
    #获取所有subnet信息
    headers = {"X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT+"/subnets"
    r = requests.get(url=url, headers=headers)
    return r.json()


def get_subnet_one_info(token_id,subnet_id):
    #获取具体某一子网的信息
    headers = {"X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT+"/subnets/"+subnet_id
    r = requests.get(url=url, headers=headers)
    return r.json()


def get_tuopu_info(token_id,tenant_id):
    tuopu_port = _get_tuopu_port_info(token_id)
    tuopu_router = _get_tuopu_router_info(token_id)
    network_info = get_network_all_info(token_id)
    subnet_info = get_subnet_all_info(token_id)
    tuopu_network = _get_tuopu_network_info(network_info,subnet_info)
    _servers_detail = _get_servers_detail(token_id,tenant_id)
    tuopu_server = _get_tuopu_servers_info(_servers_detail)
    tuopu_1 = dict(tuopu_port,**tuopu_network)
    tuopu_2 = dict(tuopu_router,**tuopu_server)
    tuopu_info = dict(tuopu_1,**tuopu_2)
    print json.dumps(tuopu_info)
    return tuopu_info




if __name__ == "__main__":

    # 通过用户和密码获取token
    token_json = get_user_token("user01", "user01")
    #print token_json

    token_id = token_json['access']['token']['id']

    # 获取租户
    #print get_tenants(token_id)
    tenant_name = get_tenants(token_id)['tenants'][0]['name']
    tenant_id = get_tenants(token_id)['tenants'][0]['id']

    # 获取租户的tonken
    token_json = get_tenant_token("project01", token_id)
    token_id = token_json['access']['token']['id']

    # print get_tenant_vms(token, tenant_id)

    # 获取某一租户下面的资源

    #print get_tenant_instance_meter(token_id, "0443f44e-2364-4211-803c-08afbe65b26e", "cpu_util")
    #get_one_firewalls_info(token_id,'f4812b3f-1f49-4271-96ad-5433bcf68cfd')
    #print get_all_firewalls_info(token_id)
    #print list_floatingips(token_id)
    #print get_all_rules(token_id)
    #print get_list_meter_minute(token_id,'cpu_util','d3e91881-f450-4842-8c40-0af2052b14fe')
    #print get_list_meter_minute(token_id,"network.incoming.bytes.rate","instance-00000003-790d82c0-bbea-44cc-8ab8-91d121f48fac-tap7ae9c9fc-2a")
    #monitor_network_incoming = get_list_meter_minute(token_id,"network.incoming.bytes.rate","instance-00000003-790d82c0-bbea-44cc-8ab8-91d121f48fac-tap7ae9c9fc-2a")
    #monitor_network_outgoing = get_list_meter_minute(token_id,"network.outgoing.bytes.rate","instance-00000003-790d82c0-bbea-44cc-8ab8-91d121f48fac-tap7ae9c9fc-2a")
    #r = {"monitor_network_incoming":monitor_network_incoming,"monitor_network_outgoing":monitor_network_outgoing}
    #print r
    #disk_read_rate = get_list_meter_minute(token_id,"disk.read.bytes.rate","5cb4c811-36de-4dd1-bf0e-e364db4ebc6e")
    #disk_write_rate = get_list_meter_minute(token_id,"disk.write.bytes.rate","5cb4c811-36de-4dd1-bf0e-e364db4ebc6e")
    #r = dict(disk_read_rate, **disk_write_rate)
    #print json.dumps(r)
    #resource_id =  get_instance_network_resource_id(token_id, "5cb4c811-36de-4dd1-bf0e-e364db4ebc6e","network.incoming.bytes.rate")
    #print get_list_meter_minute(token_id,"network.incoming.bytes.rate",resource_id)
    #print get_list_meter_minute(token_id,'disk.read.bytes.rate','5cb4c811-36de-4dd1-bf0e-e364db4ebc6e')
    # def get_meter_func_data(token_id, instance_id, meter_name, type):
    #print json.dumps(get_meter_func_data(token_id, '5cb4c811-36de-4dd1-bf0e-e364db4ebc6e', "network.incoming.bytes.rate", "minute"))
    get_tuopu_info(token_id,"d0b8bf58c42a4f8b92bb67073a1af2b1")

