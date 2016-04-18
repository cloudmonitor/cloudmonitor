# _*_ coding:utf-8 _*_

from identify import *
from nova import *
from topology import *
from neutron import *
from ceilometer import *
from firewall import *
from settings import *
from securitygroup import *
from quota import *
from keypair import *
from util import *






if __name__ == "__main__":

    # 通过用户和密码获取token
    token_json = get_user_token("user01", "user01")
    #print json.dumps(token_json)
    admin_json = get_admin_token()
    token = token_json['access']['token']
    token_id = token_json['access']['token']['id']
    admin_token_id = admin_json['access']['token']['id']
    # 获取租户
    # print get_tenants(token_id)
    # tenant_name = get_tenants(token_id)['tenants'][0]['name']
    tenant_id = get_tenants(token_id)['tenants'][1]['id']

    # 获取租户的tonken
    token_json = get_tenant_token("project01", token_id)
    token_id = token_json['access']['token']['id']

    #print json.dumps(get_last_network_topology(token_id, 'd0b8bf58c42a4f8b92bb67073a1af2b1'))
    #print update_policy(token_id,'{"firewall_policy":{"name":"test","description":"111111111111","audited":false,"shared":true}}',"0b78d036-2efd-447b-8c84-95d2375b157e")
    #print json.dumps(get_tenant_ext_net(token_id))
    #print create2_servers(token_id, tenant_id, '{"server": {"name": "testtttttt", "imageRef": "879bef2e-565f-46fa-9344-a99862b13afe", "flavorRef": "1", "networks": [{"uuid": "20f23a71-badc-43be-8f96-5422f2c9dc2c"}], "max_count": "1", "network_info": [{"network_id": "20f23a71-badc-43be-8f96-5422f2c9dc2c", "subnet_id": "73ab5a15-9741-4772-8543-9c915dd08895"}], "availability-zone": "compute02", "security_groups": []}}')
    #print get_router_ports(token_id,"0d240a36-2a97-4101-90f0-46157fad48be")
    #print delete_port(token_id, {"port_ids":['8a81de6d-d43e-4cfd-9fc5-178d35fab889']})
    #print remove_router_interface()
    #print json.dumps(disconnect_subnet(token_id))
    #print json.dumps(get_tenant_networks(token_id))\
    #print json.dumps(create_network(token_id,'[{"network": {"name": "222", "admin_state_up": true}}, {"subnet": {"ip_version": 4, "cidr": "192.168.0.0/24", "name": "111"}}]'))
    #print json.dumps(create_network(token_id,'[{"network": {"name": "111", "admin_state_up": true}}, {"subnet": {"ip_version": 4, "cidr": "10.1.2.3/24", "name": "222"}}]'))
    #print json.dumps(get_tenant_limits(token_id,tenant_id))
    #print json.dumps(disconnect_subnet(token_id))
    # delete_port_list = get_dis_port(token_id)
    # print delete_port_list
    # print delete_port(token_id,delete_port_list)
    #print get_network_server(token_id, tenant_id,"project01-net02")
    #print json.dumps(get_last_network_topology(token_id,tenant_id))
    #print json.dumps(get_subnet_servers(token_id,tenant_id, "a5668f7b-7e92-4dae-9fda-537976fc7cd1"))
    #print json.dumps(get_tuopu_subnet_info(token_id))
    #print json.dumps(get_last_network_topology(token_id, tenant_id))
    #print json.dumps(network_subnet(token_id))
    # print admin_token_id
    # print json.dumps(get_users_list(admin_token_id))
    # print auth_is_available(token)
    print json.dumps(get_tenant_quota(tenant_id))