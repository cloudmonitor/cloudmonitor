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
from user import *


if __name__ == "__main__":

    # 通过用户和密码获取token
    token_json = get_user_token("user01", "user01")
    admin_json = get_admin_token()
    token = token_json['access']['token']
    token_id = token_json['access']['token']['id']
    admin_token_id = admin_json['access']['token']['id']
    # 获取租户
    # print get_tenants(token_id)
    # tenant_name = get_tenants(token_id)['tenants'][0]['name']
    tenant_id = get_tenants(token_id)['tenants'][0]['id']
    # 获取租户的tonken
    token_json = get_tenant_token("project02", token_id)
    token_id = token_json['access']['token']['id']

    # delete_port_list = get_dis_port(token_id)
    # print delete_port_list
    # print delete_port(token_id,delete_port_list)
    # print json.dumps(get_tenant_networks(token_id))
    # print json.dumps(get_last_network_topology(token_id, tenant_id))
    # print json.dumps(get_network_servers(token_id, tenant_id, "447e39f3-7710-48b4-9fd8-3356511f8c83"))
    # print json.dumps(get_tenant_instances(token_id, tenant_id))
    # print json.dumps(get_router_networks(token_id, "d2092658-6162-49c7-b5a5-94380256e995"))
    # print get_router_servers(token_id, tenant_id, "d2092658-6162-49c7-b5a5-94380256e995")
    print json.dumps(get_last_network_topology(token_id, tenant_id))
