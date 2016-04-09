# _*_ coding:utf-8 _*_

from settings import *
from neutron import *


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


# def get_flavor_detail(token_id, tenant_id, flavor_id):
#     """获取某一具体的flavor"""
#     headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
#     url = NOVA_ENDPOINT.format(tenant_id=tenant_id) + "/flavors/" + flavor_id
#     r = requests.get(url=url, headers=headers)
#     return r.json()


def get_tenant_os_availability_zone(token_id,tenant_id):
    """获取可分配的域"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id) + "/os-availability-zone"
    r = requests.get(url=url, headers=headers)
    return r.json()


def create_servers(token_id, tenant_id, data):
    """创建一个虚拟机"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id) + "/servers"
    r = requests.post(url=url, data=data, headers=headers)
    return r.json()


def update_servers(token_id, tenant_id, data, servers_id):
    """更新虚拟机"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id) + "/servers/" + servers_id
    r = requests.put(url=url, data=data, headers=headers)
    return r.json()


def delete_servers(token_id, tenant_id, servers_id_list):
    """终止虚拟机"""
    delete_status = {}
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    for i in range(len(servers_id_list["servers_ids"])):
        url = NOVA_ENDPOINT.format(tenant_id=tenant_id) + "/servers/" + servers_id_list["servers_ids"][i]
        r = requests.delete(url=url, headers=headers)
        delete_status[servers_id_list["servers_ids"][i]] = r.status_code
    return delete_status


def bind_interface(token_id, tenant_id, data, servers_id):
    """绑定虚拟网卡"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id) + "/servers/" + servers_id + "/os-interface"
    r = requests.post(url=url, data=data, headers=headers)
    return r.json()


def delete_interface(token_id, tenant_id, servers_id, port_id):
    """解绑虚拟网卡"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id) + "/servers/" + servers_id + "/os-interface/" + port_id
    r = requests.post(url=url, headers=headers)
    print r.json()


def create2_servers(token_id, tenant_id, servers_data):
    """创建指定子网的虚拟机"""
    servers_data = json.loads(servers_data)
    print type(servers_data)
    network_id = servers_data['server'].pop('network_id')
    subnet_id = servers_data['server'].pop('subnet_id')
    port_data = '{"port": {"network_id": "%s","fixed_ips": [{"subnet_id": "%s"}]}}' % (network_id, subnet_id)
    port_r = create_port(token_id, port_data)
    port_id = port_r['port']['id']
    print port_id
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id) + "/servers"
    servers_data['server']['networks'][0]['port_id'] = port_id
    server_r = requests.post(url=url, data=json.dumps(servers_data), headers=headers)
    server_r = server_r.json()
    print server_r
    return server_r


#
# def bind_floatingips(token_id, tenant_id, servers_id, data):
#     """增加浮动ip"""
#     headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
#     url = NOVA_ENDPOINT.format(tenant_id=tenant_id) + "/servers/" + servers_id + "/action"
#     print url
#     r = requests.post(url=url, data=data, headers=headers)
#     return r.json()
#
#
# def remove_floatingips(token_id, tenant_id, servers_id, data):
#     """解除浮动ip"""
#     headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
#     url = NOVA_ENDPOINT.format(tenant_id=tenant_id) + "/servers/" + servers_id + "/action"
#     print url
#     r = requests.post(url=url, data=data, headers=headers)
#     return r.json()
#
#
# def bind_security_group(token_id, tenant_id, data, servers_id):
#     """绑定安全组"""
#     headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
#     url = NOVA_ENDPOINT.format(tenant_id=tenant_id) + "/servers/" + servers_id + "/action"
#     print url
#     r = requests.post(url=url, data=data, headers=headers)
#     return r.json()
#
#
# def remove_security_group(token_id, tenant_id, servers_id):
#     """解绑安全组"""
#     headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
#     url = NOVA_ENDPOINT.format(tenant_id=tenant_id) + "/servers/" + servers_id + "/action"
#     print url
#     r = requests.post(url=url, headers=headers)
#     print r.json()


def action_server(token_id, tenant_id, servers_id, data):
    """对于虚拟机的安全组、floatingips、中止虚拟机、暂停之后的恢复虚拟机、挂起、挂起恢复、\
    锁定和解锁虚拟机、硬重启、软重启、关闭虚拟机、重建虚拟机、启动虚拟机"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NOVA_ENDPOINT.format(tenant_id=tenant_id) + "/servers/" + servers_id + "/action"
    print url
    r = requests.post(url=url, data=data, headers=headers)
    print r.json()


