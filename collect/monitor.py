# _*_ coding:utf-8 _*_

from identify import *
from nova import *
from topology import *
from neutron import *
from ceilometer import *
from firewall import *


if __name__ == "__main__":

    # 通过用户和密码获取token
    token_json = get_user_token("user01", "user01")
    #print token_json

    token_id = token_json['access']['token']['id']

    # 获取租户
    # print get_tenants(token_id)
    # tenant_name = get_tenants(token_id)['tenants'][0]['name']
    # tenant_id = get_tenants(token_id)['tenants'][0]['id']

    # 获取租户的tonken
    token_json = get_tenant_token("project01", token_id)
    token_id = token_json['access']['token']['id']

    print json.dumps(get_last_network_topology(token_id, 'd0b8bf58c42a4f8b92bb67073a1af2b1'))

    # print delete_fw_rule(token_id, "7372a0fb-1ad4-4581-ad6e-3af645383b5d")






# # _*_ coding:utf-8 _*_
#
# import requests
# import json
# import time
# import datetime
#
# # 常量
#
# CREDENTIAL_PASSWORD = '{"auth": {"tenantName": "%s", "passwordCredentials": {"username": "%s", "password": "%s"}}}'
# CREDENTIAL_TOKEN = '{"auth":{"tenantName":"%s","token":{"id":"%s"}}}'
#
# KEYSTONE_ENDPOINT = 'http://controller:5000/v2.0'
# GLANCE_ENDPOINT = 'http://controller:9292/v2'
# NOVA_ENDPOINT = 'http://controller:8774/v2/{tenant_id}'
# NEUTRON_ENDPOINT = 'http://controller:9696/v2.0'
# CEILOMETER_ENDPOINT = 'http://controller:8777/v2'
#
# SERVER_NUM = 0
# NET_NUM = 0
# ROUTER_NUM = 0
# EXNET_NUM = 0
#
#
# def get_user_token(username, password):
#     """获取指定用户名密码的TOKEN,返回json"""
#     credential = CREDENTIAL_PASSWORD % ('', username, password)
#     headers = {"Content-type": "application/json", "Accept": "application/json"}
#     r = requests.post(KEYSTONE_ENDPOINT+'/tokens', data=credential, headers=headers)
#     return r.json()
#
#
# def get_tenant_token(tenantname, token):
#     """获取指定租户、用户名、密码的TOKEN,返回json"""
#     credential = CREDENTIAL_TOKEN % (tenantname, token)
#     headers = {"Content-type": "application/json", "Accept": "application/json"}
#     r = requests.post(KEYSTONE_ENDPOINT+'/tokens', data=credential, headers=headers)
#     response_json = r.json()
#     return response_json
#
#
# def get_tenants(token_id):
#     """获取指定TOKEN下的所有租户，返回一个租户字典,通过['tenants'][0 1 ... n]['id']取得租户id,返回样例如下"""
#     headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
#     r = requests.get(KEYSTONE_ENDPOINT+'/tenants', headers=headers)
#     return r.json()
#
#
# def get_tenant_instances(token_id, tenant_id):
#     """获取某一租户下的所有vm"""
#     headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
#     url = NOVA_ENDPOINT.format(tenant_id=tenant_id)
#     r = requests.get(url+'/servers/detail', headers=headers)
#     return r.json()
#
#
# def get_tenant_instance(token_id, tenant_id, instance_id):
#     """获取某一租户下的某一vm"""
#     headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
#     url = NOVA_ENDPOINT.format(tenant_id=tenant_id)
#     r = requests.get(url+'/servers/'+instance_id, headers=headers)
#     return r.json()
#
#
# def get_tenant_limits(token_id, tenant_id):
#     """获取租户的资源配额限制"""
#     headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
#     url = NOVA_ENDPOINT.format(tenant_id=tenant_id)
#     r = requests.get(url+'/limits', headers=headers)
#     return r.json()
#
#
# def get_tenant_flavors(token_id, tenant_id):
#     """获取租户的flavor"""
#     headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
#     url = NOVA_ENDPOINT.format(tenant_id=tenant_id)
#     r = requests.get(url+'/flavors/detail', headers=headers)
#     return r.json()
#
#
# def get_tenant_networks(token_id):
#     """获取租户的flavor"""
#     headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
#     url = NEUTRON_ENDPOINT
#     r = requests.get(url+'/networks', headers=headers)
#     return r.json()
#
#
# def get_tenant_subnets(token_id):
#     """获取租户的flavor"""
#     headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
#     url = NEUTRON_ENDPOINT
#     r = requests.get(url+'/subnets', headers=headers)
#     return r.json()
#
#
# def get_tenant_routers(token_id):
#     """获取租户的flavor"""
#     headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
#     url = NEUTRON_ENDPOINT
#     r = requests.get(url+'/routers', headers=headers)
#     return r.json()
#
#
# def get_floating_ips(token_id):
#     """ 列出floating ip"""
#     headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
#     url = NEUTRON_ENDPOINT + '/floatingips'
#     r = requests.get(url, headers=headers)
#     return r.json()
#
#
# def get_tenant_ports(token_id):
#     """ 获取所有的端口的信息"""
#     headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
#     url = NEUTRON_ENDPOINT + "/ports"
#     r = requests.get(url=url, headers=headers)
#     return r.json()
#
#
# def get_security_groups(token_id):
#     """列出安全组的信息"""
#     headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
#     url = NEUTRON_ENDPOINT + '/security-groups'
#     r = requests.get(url, headers=headers)
#     return r.json()
#
#
# def get_all_rules(token_id):
#     """ 获取所有的rule的信息"""
#     headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
#     url = NEUTRON_ENDPOINT + '/fw/firewall_rules'
#     r = requests.get(url=url, headers=headers)
#     return r.json()
#
#
# def get_one_rules(token_id, rule_id):
#     """ 获取某一的rule的信息"""
#     headers = {"X-Auth-Token": token_id, "Accept": "application/json"}
#     url = NEUTRON_ENDPOINT + '/fw/firewall_rules/'+rule_id
#     r = requests.get(url=url, headers= headers)
#     return r.json()
#
#
# def get_all_policies(token_id):
#     """获取所有的policys的信息"""
#     headers = {"X-Auth-Token": token_id, "Accept": "application/json"}
#     url = NEUTRON_ENDPOINT + '/fw/firewall_policies'
#     r = requests.get(url=url, headers=headers)
#     return r.json()
#
#
# def get_one_policies(token_id, policies_id):
#     """获取某一个policy的信息"""
#     headers = {"X-Auth-Token": token_id, "Accept": "application/json"}
#     url = NEUTRON_ENDPOINT + '/fw/firewall_policies/'+policies_id
#     r = requests.get(url=url, headers=headers)
#     return r.json()
#
#
# def get_all_firewalls_info(token_id):
#     """获取所有的Firewalls信息"""
#     headers = {"X-Auth-Token": token_id, "Accept": "application/json"}
#     url = NEUTRON_ENDPOINT + '/fw/firewalls'
#     r = requests.get(url=url, headers=headers)
#     return r.json()
#
#
# def get_one_firewalls_info(token_id, firewalls_id):
#     """获取某一具体Firewalls的信息"""
#     headers = {"X-Auth-Token": token_id, "Accept": "application/json"}
#     url = NEUTRON_ENDPOINT + '/fw/firewalls/'+firewalls_id
#     r = requests.get(url=url, headers=headers)
#     firewall_info = r.json()
#     print firewall_info
#     policy_id = firewall_info['firewall']['firewall_policy_id']
#     print policy_id
#     policy_all_info = get_all_policies(token_id)
#     for item in policy_all_info['firewall_policies']:
#         if policy_id == item['id']:
#             rule_id = item['firewall_rules']
#     for firewall_rule_id in rule_id:
#         rule_info = get_one_rules(token_id, firewall_rule_id)
#     # print rule_info
#     return rule_info
#
#
# def get_all_policies(token_id):
#     """获取所有的policys的信息"""
#     headers = {"X-Auth-Token": token_id, "Accept": "application/json"}
#     url = NEUTRON_ENDPOINT + '/fw/firewall_policies'
#     r = requests.get(url=url, headers=headers)
#     return r.json()
#
#
# def get_all_rules(token_id):
#     """获取所有的rule的信息"""
#     headers = {"X-Auth-Token": token_id, "Accept": "application/json"}
#     url = NEUTRON_ENDPOINT + '/fw/firewall_rules'
#     r = requests.get(url=url, headers=headers)
#     return r.json()
#
#
# def create_fw_rule(token_id, rule):
#     """创建防火墙规则"""
#     headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
#     url = NEUTRON_ENDPOINT + '/fw/firewall_rules'
#     r = requests.post(url=url, data=json.dumps(rule), headers=headers)
#     return r.json()
#
#
# def delete_fw_rule(token_id, rule_id_list):
#     """删除防火墙规则"""
#     delete_status = {}
#     headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
#     for i in range(len(rule_id_list["firewall_rule_ids"])):
#         url = NEUTRON_ENDPOINT + '/fw/firewall_rules/' + rule_id_list["firewall_rule_ids"][i]
#         r = requests.delete(url=url, headers=headers)
#         delete_status[rule_id_list["firewall_rule_ids"][i]] = r.status_code
#     return delete_status
#
#
# def update_fw_rule(token_id, rule, fw_rule_id):
#     """更新防火墙规则"""
#     headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
#     url = NEUTRON_ENDPOINT + '/fw/firewall_rules/' + fw_rule_id
#     r = requests.put(url=url, data=rule, headers=headers)
#     return r.json()
#
#
# def create_security_group(token_id, data):
#     """根据token_id和安全组名字创建安全组"""
#     headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
#     url = NEUTRON_ENDPOINT + "/security-groups"
#     r = requests.post(url=url, headers=headers, data=json.dumps(data))
#     return r.json()
#
#
# def update_security_group(token_id, security_group, security_group_id):
#     """更新安全组"""
#     headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
#     url = NEUTRON_ENDPOINT + '/security-groups/' + security_group_id
#     r = requests.put(url=url, data=security_group, headers=headers)
#     return r.json()
#
#
# def delete_security_group(token_id, sg_id_list):
#     """根据security_group_id删除安全组"""
#     sg_del_status = {}
#     headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
#     for i in range(len(sg_id_list["sg_ids"])):
#         url = NEUTRON_ENDPOINT + "/security-groups/"+sg_id_list["sg_ids"][i]
#         r = requests.delete(url=url, headers=headers)
#         sg_del_status[sg_id_list["sg_ids"][i]] = r.status_code
#     return sg_del_status
#
#
# def create_security_group_rules(token_id, data):
#     """创建安全组规则"""
#     headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
#     url = NEUTRON_ENDPOINT + "/security-groups-rules"
#     r = requests.post(url=url, headers=headers, data=json.dumps(data))
#     return r.json()
#
#
# def delete_security_group_rules(token_id,sg_id_rules_list):
#     sg_rules_del_status = {}
#     headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
#     for i in range(len(sg_id_rules_list["sg_rules_ids"])):
#         url = NEUTRON_ENDPOINT + "/security-groups_rules/"+sg_id_rules_list["sg_rules_ids"][i]
#         r = requests.delete(url=url, headers=headers)
#         sg_rules_del_status[sg_id_rules_list["sg_rules_ids"][i]] = r.status_code
#     return sg_rules_del_status
#
#
# def get_localtime():
#     """获取当前时间"""
#     ISOTIMEFORMAT = '%Y-%m-%d %X'
#     total_time = time.strftime(ISOTIMEFORMAT,time.localtime())
#     return total_time
#
#
# def time_to_isostring(s):
#     """把一个时间转换成秒"""
#     d = datetime.datetime.strptime(s,"%Y-%m-%d %H:%M:%S")
#     return time.mktime(d.timetuple())
#
#
# def isostring_to_time(s):
#     """把秒数转换成一个时间"""
#     return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(float(s)))
#
#
# def get_meter_func_data(token_id, instance_id, meter_name, type):
#     resource_id = get_instance_resource_id(token_id, instance_id, meter_name)
#     func_name = "get_list_meter_"+type
#     # print func_name
#     return eval(func_name)(token_id, meter_name, resource_id)
#
#
# def get_instance_resource_id(token_id, instance_id, meter_name):
#     headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
#     r = requests.get(CEILOMETER_ENDPOINT+'/resources', headers=headers)
#     for resource in r.json():
#         if meter_name.startswith("network."):
#             if resource['metadata'].has_key('vnic_name'):
#                 regex = instance_id + '-' + resource['metadata']['vnic_name']
#                 if resource['resource_id'].endswith(regex):
#                     return resource['resource_id']
#         else:
#             if resource['resource_id'] == instance_id:
#                 return resource['resource_id']
#
#
# def localtime_to_utc(s):
#     seconds = int(time_to_isostring(s))-28800
#     return isostring_to_time(seconds)
#
#
# def get_one_meter(token_id, time, meter_name ,resource_id ):
#     """根据时间来删选数据"""
#     time_reduce = isostring_to_time(time_to_isostring(time)-60)
#     headers = {"X-Auth-Token":token_id, "Accept": "application/json"}
#     url = CEILOMETER_ENDPOINT + '/meters/'+meter_name+'/?'
#     url_list = [url, ]
#     payload = {"q": [{"field": "timestamp", "op": "gt", "value": time_reduce},
#                      {"field": "timestamp", "op": "lt", "value": time},
#                      {"field": "resource_id","value": resource_id}
#                     ]}
#     for key, value in payload.items():
#         if isinstance(value, list):
#             for val in value:
#                 for k1, v1 in val.items():
#                     url_list.append(key+'.'+k1+'='+v1+'&')
#         else:
#             url_list.append(key+'='+str(value)+'&')
#     url_list.append("limit=1")
#     url = ''.join(url_list)
#     r = requests.get(url, headers=headers)
#     return r.json()
#
#
# def get_list_meter_minute(token_id, meter_name, resource_id):
#     """以分钟得到某一组数据"""
#     localtime = localtime_to_utc(get_localtime())
#     meter_info_list = []
#     for i in range(0, 7):
#         r = get_one_meter(token_id, localtime, meter_name, resource_id)
#         # print r
#         if len(r) == 0:
#             meter_info_list.append(r)
#         else:
#             meter_info_list.append(r[0])
#         localtime = isostring_to_time(time_to_isostring(localtime)-180)
#     r = {meter_name:meter_info_list}
#
#     return r
#
#
# def get_list_meter_hour(token_id,meter_name, resource_id):
#     """以小时得到某一组数据"""
#     localtime = localtime_to_utc(get_localtime())
#     meter_info_list = []
#     for i in range(0, 7):
#         r = get_one_meter(token_id, localtime, meter_name, resource_id)
#         if len(r) == 0:
#             meter_info_list.append(r)
#         else:
#             meter_info_list.append(r[0])
#         localtime01 = datetime.datetime.strptime(localtime,"%Y-%m-%d %H:%M:%S")
#         times = localtime01 + datetime.timedelta(hours=-1)
#         localtime = datetime.datetime.strftime(times, "%Y-%m-%d %H:%M:%S")
#     r = {meter_name:meter_info_list}
#     return r
#
#
# def get_list_meter_day(token_id,meter_name, resource_id):
#     """以天得到某一组数据"""
#     localtime = localtime_to_utc(get_localtime())
#     meter_info_list = []
#     for i in range(0, 7):
#         r = get_one_meter(token_id, localtime, meter_name, resource_id)
#         if len(r) == 0:
#             meter_info_list.append(r)
#         else:
#             meter_info_list.append(r[0])
#         print localtime
#         localtime01 = datetime.datetime.strptime(localtime,"%Y-%m-%d %H:%M:%S")
#         times = localtime01 + datetime.timedelta(days=-1)
#         localtime = datetime.datetime.strftime(times, "%Y-%m-%d %H:%M:%S")
#         #print localtime
#     r = {meter_name:meter_info_list}
#     return r
#
#
# def _get_tuopu_port_info(token_id):
#     """获取拓扑的端口信息"""
#     ports_list = []
#
#     all_port_info = get_tenant_ports(token_id)
#     #print json.dumps(all_port_info)
#     for i in range(len(all_port_info['ports'])):
#         port_info = {}
#         if not all_port_info['ports'][i]['device_id'].startswith('dhcp'):
#             port_info["status"] = all_port_info['ports'][i]['status']
#             port_info["srcDeviceId"] = all_port_info['ports'][i]['network_id']
#             port_info["url"] = ""
#             port_info["device_owner"] = all_port_info['ports'][i]["device_owner"]
#             port_info["fixed_ips"] = all_port_info['ports'][i]["fixed_ips"]
#             port_info["id"] = all_port_info['ports'][i]["id"]
#             port_info["dstDeviceId"] = all_port_info['ports'][i]["device_id"]
#             port_info["stroke"] = "black"
#             port_info["strokeWidth"] = 1
#             ports_list.append(port_info)
#     all_routers_info = get_tenant_routers(token_id)
#     for i in range(len(all_routers_info["routers"])):
#         # router_id = all_routers_info['routers'][i]['id']
#         # one_router_info = get_one_routers_info(token_id, router_id)
#         if all_routers_info['routers'][i]["external_gateway_info"]:
#             ex_port_info = {}
#             ex_port_info["srcDeviceId "] = all_routers_info['routers'][i]["external_gateway_info"]["network_id"]
#             ex_port_info["fixed_ips"] = all_routers_info['routers'][i]["external_gateway_info"]["external_fixed_ips"]
#             ex_port_info["id"] = "gateway"+all_routers_info['routers'][i]["external_gateway_info"]["network_id"]
#             ex_port_info["dstDeviceId"] = all_routers_info['routers'][i]["id"]
#             ex_port_info["stroke"] = "black"
#             ex_port_info["strokeWidth"] = 1
#             ports_list.append(ex_port_info)
#     return ports_list
#
#
# def _get_tuopu_router_info(token_id):
#     """ 获取路由器的tuopu信息 """
#     routers_list = []
#     x = 240
#     y = 240
#     width = 100
#     height = 100
#     all_routers_info = get_tenant_routers(token_id)
#     for i in range(len(all_routers_info['routers'])):
#         router_info = {}
#         router_info["status"] = all_routers_info["routers"][i]["status"]
#         router_info["external_gateway_info"] = all_routers_info["routers"][i]["external_gateway_info"]
#         router_info["url"] = ""
#         router_info["id"] = all_routers_info["routers"][i]["id"]
#         router_info["name"] = all_routers_info["routers"][i]["name"]
#         router_info["src"] = "./icon/device/router.png"
#         router_info["device_name"] = "router"
#         global ROUTER_NUM
#         ROUTER_NUM += 1
#         # router_info["x"] = "%s" %(x+i*width)
#         # router_info["y"] = "%s" %(y + i*height)
#         router_info["width"] = "%s" %(70)
#         router_info["height"] = "%s" %(70)
#         routers_list.append(router_info)
#     return routers_list
#
#
# def _get_tuopu_network_info(network_info, subnet_info):
#     net_info = []
#     x = 360
#     y = 360
#     width = 100
#     height = 100
#     for i in range(len(network_info["networks"])):
#         _net_info = {}
#         _net_info["status"] = network_info["networks"][i]["status"]
#         _net_info["subnets"] = _get_subnet_detail(network_info["networks"][i]["id"], subnet_info)
#         _net_info["name"] = network_info["networks"][i]["name"]
#         _net_info["router:external"] = network_info["networks"][i]["router:external"]
#         _net_info["url"] = ""
#         _net_info["id"] = network_info["networks"][i]["id"]
#         if network_info["networks"][i]["router:external"]:
#             _net_info["src"] = "./icon/device/extnet.png"
#             _net_info["device_name"] = "ext_net"
#             global EXNET_NUM
#             EXNET_NUM +=1
#         else:
#              _net_info["src"] = "./icon/device/network.png"
#              _net_info["device_name"] = "network"
#              global NET_NUM
#              NET_NUM  +=1
#         # _net_info["x"] = "%s" %(x+i*width)
#         # _net_info["y"] = "%s" %(y + i*height)
#         _net_info["width"] = "%s" %(70)
#         _net_info["height"] = "%s" %(70)
#         net_info.append(_net_info)
#     return net_info
#
#
# def _get_tuopu_servers_info(severs_info_detail):
#     servers_list = []
#     x = 120
#     y = 123
#     width = 100
#     height = 100
#     for i in range(len(severs_info_detail["servers"])):
#         one_servers_info = {}
#         one_servers_info["status"] = severs_info_detail["servers"][i]["status"]
#         one_servers_info["task"] = "null"
#         one_servers_info["console"] = "vnc"
#         one_servers_info["name"] = severs_info_detail["servers"][i]["name"]
#         one_servers_info["url"] = ""
#         one_servers_info["id"] = severs_info_detail["servers"][i]["id"]
#         one_servers_info["src"] = "./icon/device/server.png"
#         one_servers_info["device_name"] = "server"
#         # one_servers_info["x"] = "%s" %(x+i*width)
#         # one_servers_info["y"] = "%s" %(y + i*height)
#         one_servers_info["width"] = "%s" %(70)
#         one_servers_info["height"] = "%s" %(70)
#         global SERVER_NUM
#         SERVER_NUM += 1
#         servers_list.append(one_servers_info)
#     return servers_list
#
#
# def _get_subnet_detail(network_id, subnet_info):
#     simple_subnet_info = []
#     for i in range(len(subnet_info["subnets"])):
#         _simple_subnet_info = {}
#         if subnet_info["subnets"][i]["network_id"] == network_id:
#             _simple_subnet_info["url"] = ""
#             _simple_subnet_info["cidr"] = subnet_info["subnets"][i]["cidr"]
#             _simple_subnet_info["id"] = subnet_info["subnets"][i]["id"]
#             simple_subnet_info.append(_simple_subnet_info)
#     return simple_subnet_info
#
#
# def get_tuopu_info(token_id, tenant_id):
#     """这里是获取拓扑信息"""
#     tuopu_info = {}
#     tuopu_port = _get_tuopu_port_info(token_id)
#     tuopu_router = _get_tuopu_router_info(token_id)
#     network_info = get_tenant_networks(token_id)
#     subnet_info = get_tenant_subnets(token_id)
#     tuopu_network = _get_tuopu_network_info(network_info,subnet_info)
#     _servers_detail = get_tenant_instances(token_id, tenant_id)
#     tuopu_server = _get_tuopu_servers_info(_servers_detail)
#     tuopu_server += tuopu_router
#     tuopu_server += tuopu_network
#     tuopu_info['devices'] = tuopu_server
#     tuopu_info['lines'] = tuopu_port
#     return tuopu_info
#
#
# def get_last_tuopu_info(token_id, tenant_id):
#     global ROUTER_NUM
#     global NET_NUM
#     global EXNET_NUM
#     global SERVER_NUM
#     tuopu_info = get_tuopu_info(token_id, tenant_id)
#     max_num = max(ROUTER_NUM, NET_NUM, EXNET_NUM, SERVER_NUM)
#     print max_num
#     x = 100
#     y = 60
#     width = (max_num+1)*20
#     height = 150
#     router_num = 0
#     server_nmu = 0
#     net_exnet_num = 0
#     for i in range(len(tuopu_info['devices'])):
#         if tuopu_info['devices'][i]['src'].endswith("server.png"):
#             tuopu_info['devices'][i]['x'] = x + server_nmu*width
#             tuopu_info['devices'][i]['y'] = y
#             server_nmu += 1
#         if tuopu_info['devices'][i]['src'].endswith("router.png"):
#             tuopu_info['devices'][i]['x'] = x + router_num*width
#             tuopu_info['devices'][i]['y'] = y + height
#             router_num += 1
#         if tuopu_info['devices'][i]['src'].endswith("network.png") or tuopu_info['devices'][i]['src'].endswith("extnet.png"):
#             tuopu_info['devices'][i]['x'] = x + net_exnet_num*width
#             tuopu_info['devices'][i]['y'] = y + height*2
#             net_exnet_num += 1
#     # global ROUTER_NUM
#     ROUTER_NUM = 0
#     # global NET_NUM
#     NET_NUM = 0
#     # global EXNET_NUM
#     EXNET_NUM = 0
#     # global SERVER_NUM
#     SERVER_NUM = 0
#     return tuopu_info
#
#
# if __name__ == "__main__":
#
#     # 通过用户和密码获取token
#     token_json = get_user_token("user01", "user01")
#     #print token_json
#
#     token_id = token_json['access']['token']['id']
#
#     # 获取租户
#     #print get_tenants(token_id)
#     tenant_name = get_tenants(token_id)['tenants'][0]['name']
#     tenant_id = get_tenants(token_id)['tenants'][0]['id']
#
#     # 获取租户的tonken
#     token_json = get_tenant_token("project01", token_id)
#     token_id = token_json['access']['token']['id']
#
#     # print delete_fw_rule(token_id, "7372a0fb-1ad4-4581-ad6e-3af645383b5d")
#
#
#
#     # print get_tenant_vms(token, tenant_id)
#
#     # 获取某一租户下面的资源
#
#     #print get_tenant_instance_meter(token_id, "0443f44e-2364-4211-803c-08afbe65b26e", "cpu_util")
#     #get_one_firewalls_info(token_id,'f4812b3f-1f49-4271-96ad-5433bcf68cfd')
#     #print get_all_firewalls_info(token_id)
#     #print list_floatingips(token_id)
#     #print get_all_rules(token_id)
#     #print get_list_meter_minute(token_id,'cpu_util','d3e91881-f450-4842-8c40-0af2052b14fe')
#     #print get_list_meter_minute(token_id,"network.incoming.bytes.rate","instance-00000003-790d82c0-bbea-44cc-8ab8-91d121f48fac-tap7ae9c9fc-2a")
#     #monitor_network_incoming = get_list_meter_minute(token_id,"network.incoming.bytes.rate","instance-00000003-790d82c0-bbea-44cc-8ab8-91d121f48fac-tap7ae9c9fc-2a")
#     #monitor_network_outgoing = get_list_meter_minute(token_id,"network.outgoing.bytes.rate","instance-00000003-790d82c0-bbea-44cc-8ab8-91d121f48fac-tap7ae9c9fc-2a")
#     #r = {"monitor_network_incoming":monitor_network_incoming,"monitor_network_outgoing":monitor_network_outgoing}
#     #print r
#     #disk_read_rate = get_list_meter_minute(token_id,"disk.read.bytes.rate","5cb4c811-36de-4dd1-bf0e-e364db4ebc6e")
#     #disk_write_rate = get_list_meter_minute(token_id,"disk.write.bytes.rate","5cb4c811-36de-4dd1-bf0e-e364db4ebc6e")
#     #r = dict(disk_read_rate, **disk_write_rate)
#     #print json.dumps(r)
#     #resource_id =  get_instance_network_resource_id(token_id, "5cb4c811-36de-4dd1-bf0e-e364db4ebc6e","network.incoming.bytes.rate")
#     #print get_list_meter_minute(token_id,"network.incoming.bytes.rate",resource_id)
#     #print get_list_meter_minute(token_id,'disk.read.bytes.rate','5cb4c811-36de-4dd1-bf0e-e364db4ebc6e')
#     # def get_meter_func_data(token_id, instance_id, meter_name, type):
#     #print json.dumps(get_meter_func_data(token_id, '5cb4c811-36de-4dd1-bf0e-e364db4ebc6e', "network.incoming.bytes.rate", "minute"))
#     print json.dumps(get_last_tuopu_info(token_id, "d0b8bf58c42a4f8b92bb67073a1af2b1"))
#     print json.dumps(get_last_tuopu_info(token_id,"d0b8bf58c42a4f8b92bb67073a1af2b1"))
#
