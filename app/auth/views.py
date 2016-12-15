# _*_ coding:utf-8 _*_

from . import auth
from osapi import *


@auth.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    token_json = get_user_token(username, password)
    return json.dumps(token_json)


@auth.route('/tenants')
@auth_is_available
def front_get_tenants():
    token = json.loads(request.args.get('token'))
    tenants_json = get_tenants(token['id'])
    return json.dumps(tenants_json)


@auth.route('/tenant/login')
@auth_is_available
def front_get_tenant_token():
    token = json.loads(request.args.get('token'))
    tenantname = request.args.get('tenantname')
    tenant_token_json = get_tenant_token(tenantname, token['id'])
    return json.dumps(tenant_token_json)