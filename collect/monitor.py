# _*_ coding:utf-8 _*_

from identify import *
from nova import *
from topology import *
from neutron import *
from ceilometer import *
from firewall import *
from settings import *
from securitygroup import *
from floatingip import *
from quota import *



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

    # print json.dumps(get_last_network_topology(token_id, 'd0b8bf58c42a4f8b92bb67073a1af2b1'))
