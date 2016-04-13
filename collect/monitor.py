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
from floatingip import *

if __name__ == "__main__":

    # 通过用户和密码获取token
    token_json = get_user_token("user01", "user01")
    #print json.dumps(token_json)

    token_id = token_json['access']['token']['id']
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
    #print create2_servers(token_id, tenant_id, '{"server": {"flavorRef": "1","imageRef": "879bef2e-565f-46fa-9344-a99862b13afe","max_count": 1,"min_count": 1,"name": "api-test-1","networks": [{"uuid": "a62ccae1-4e60-4de3-8233-4f35420197b5"}],"network_id": "a62ccae1-4e60-4de3-8233-4f35420197b5","subnet_id": "98f80625-6d12-474a-9420-88c74269ee4c"}}')
    #print get_router_ports(token_id,"0d240a36-2a97-4101-90f0-46157fad48be")
    #print delete_port(token_id, {"port_ids":['8a81de6d-d43e-4cfd-9fc5-178d35fab889']})
    #print remove_router_interface()
    #print json.dumps(disconnect_subnet(token_id))
    #print json.dumps(get_tenant_networks(token_id))\
    #print json.dumps(create_network(token_id,'[{"network": {"name": "222", "admin_state_up": true}}, {"subnet": {"ip_version": 4, "cidr": "192.168.0.0/24", "name": "111"}}]'))
    #print json.dumps(create_network(token_id,'[{"network": {"name": "111", "admin_state_up": true}}, {"subnet": {"ip_version": 4, "cidr": "10.1.2.3/24", "name": "222"}}]'))
    #print json.dumps(get_tenant_limits(token_id,tenant_id))
    #print create3_servers(token_id, tenant_id, '{"server": {"security_groups": [],"availability-zone": "compute01","name": "123","imageRef": "d52fa4c8-dcbe-433c-8ee6-99b9f669e1ce","flavorRef": "1","max_count": "3","network_info": [{"network_id": "20f23a71-badc-43be-8f96-5422f2c9dc2c","subnet_id": "73ab5a15-9741-4772-8543-9c915dd08895"},{"network_id": "a62ccae1-4e60-4de3-8233-4f35420197b5","subnet_id": "98f80625-6d12-474a-9420-88c74269ee4c"}],"networks": [{"uuid": "20f23a71-badc-43be-8f96-5422f2c9dc2c"},{"uuid": "a62ccae1-4e60-4de3-8233-4f35420197b5"}]}}')
    #print json.dumps(get_new_subnets(token_id))
    #print json.dumps(disserver_security_group(token_id, tenant_id, "5cb4c811-36de-4dd1-bf0e-e364db4ebc6e"))
    #print server_update_sg(token_id, tenant_id, "5cb4c811-36de-4dd1-bf0e-e364db4ebc6e", '{"security_groups": ["test","asda"]}')
    #print json.dumps(server_security_group(token_id, tenant_id, "5cb4c811-36de-4dd1-bf0e-e364db4ebc6e"))
    #print json.dumps(disserver_security_group(token_id, tenant_id, "5cb4c811-36de-4dd1-bf0e-e364db4ebc6e"))
    #print action_server(token_id, tenant_id, '8a397967-a203-41e6-9755-1cbf58268845', '{"pause": null}')
    print action_server(token_id, tenant_id, '8a397967-a203-41e6-9755-1cbf58268845', '{"reboot": {"type": "HARD"}}')