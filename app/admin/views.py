# _*_ coding:utf-8 _*_

from flask import request

from osapi import auth_is_available, get_admin_token
from osapi.admin import *

from . import admin


@admin.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    token_json = get_admin_token(username, password)
    return json.dumps(token_json)


@admin.route('/abstract')
@auth_is_available
def abstract():
    """获取概要信息"""
    token = json.loads(request.args.get('token'))
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    # print request.args
    # print json.dumps(token)
    # print start_time
    # print end_time
    abstract_info = get_abstarct_info(token["id"], start_time, end_time, token["tenant"]["id"])
    print json.dumps(abstract_info)
    return json.dumps(abstract_info)


@admin.route('/hypervisor')
@auth_is_available
def hypervisor():
    """获取物理主机的信息"""
    token = json.loads(request.args.get('token'))
    hypervisor_info = get_physical_usage(token["id"], token["tenant"]["id"])
    return json.dumps(hypervisor_info)


@admin.route('/all_instances')
@auth_is_available
def get_all_instances_data():
    """获取所有云主机的信息"""
    token = json.loads(request.args.get('token'))
    instances_info = get_all_tenant_instances(token["id"], token["tenant"]["id"])
    return json.dumps(instances_info)


@admin.route('/tenants')
@auth_is_available
def get_all_tenants_data():
    token = json.loads(request.args.get('token'))
    tenants_json = get_all_tenants(token['id'])
    return json.dumps(tenants_json)


@admin.route('/create/tenant', methods=['POST'])
@auth_is_available
def create_tenant_data():
    token = json.loads(request.args.get('token'))
    tenant_json = request.json
    create_tenant_json = create_tenant(token["id"], json.dumps(tenant_json))
    return json.dumps(create_tenant_json)


@admin.route('/delete/tenant/<tenant_id>')
@auth_is_available
def delete_tenant_data(tenant_id):
    token = json.loads(request.args.get('token'))
    status = delete_tenant(token["id"], tenant_id)
    return json.dumps(status)


@admin.route('/delete/tenant_list', methods=['POST'])
@auth_is_available
def delete_tenant_list_data():
    token = json.loads(request.args.get('token'))
    tenant_list_id = request.json
    delete_tanant_list_status = delete_tanant_list(token["id"], tenant_list_id)
    return json.dumps(delete_tanant_list_status)


@admin.route('/update/tenant/<tenant_id>', methods=['POST'])
@auth_is_available
def update_tenant_data(tenant_id):
    token = json.loads(request.args.get('token'))
    tenant_json = request.json
    new_tenant_json = update_tenant(token["id"], tenant_id, json.dumps(tenant_json))
    return json.dumps(new_tenant_json)


@admin.route('/tenant/<tenant_id>/basic_quota')
@auth_is_available
def get_tenant_basic_quota_data(tenant_id):
    """更新用户配额"""
    token = json.loads(request.args.get('token'))
    quota_json = get_tenant_basic_quota(token["id"], token["tenant"]["id"], tenant_id)
    return json.dumps(quota_json)


@admin.route('/update/tenant/<tenant_id>/basic_quota', methods=['POST'])
@auth_is_available
def update_tenant_basic_quota_data(tenant_id):
    """更新用户基本配额"""
    token = json.loads(request.args.get('token'))
    quota_json = request.json
    new_quota_json = update_tenant_basic_quota(token["id"], token["tenant"]["id"], tenant_id, json.dumps(quota_json))
    return json.dumps(new_quota_json)


@admin.route('/tenant/<tenant_id>/neutron_quota')
@auth_is_available
def get_tenant_neutron_quota_data(tenant_id):
    """获取用户网络相关配额"""
    token = json.loads(request.args.get('token'))
    quota_json = get_tenant_neutron_quota(token["id"], token["tenant"]["id"], tenant_id)
    return json.dumps(quota_json)


@admin.route('/update/tenant/<tenant_id>/neutron_quota', methods=['POST'])
@auth_is_available
def update_tenant_neutron_quota_data(tenant_id):
    """更新用户网络相关配额"""
    token = json.loads(request.args.get('token'))
    quota_json = request.json
    new_quota_json = update_tenant_neutron_quota(token["id"], token["tenant"]["id"], tenant_id, json.dumps(quota_json))
    return json.dumps(new_quota_json)


@admin.route('/users')
@auth_is_available
def get_all_users_data():
    """获取所有用户"""
    token = json.loads(request.args.get('token'))
    users_json = get_all_users(token['id'])
    return json.dumps(users_json)


@admin.route('/tenants/<tenant_id>/users')
@auth_is_available
def grant_tenant_users_data(tenant_id):
    """授权租户的所有用户"""
    token = json.loads(request.args.get('token'))
    users_json = get_tenant_users(token['id'], tenant_id)
    return json.dumps(users_json)


@admin.route('/create/user', methods=['POST'])
@auth_is_available
def create_user_data():
    """创建用户"""
    token = json.loads(request.args.get('token'))
    user_json = request.json
    create_user_json = create_user(token["id"], json.dumps(user_json))
    return json.dumps(create_user_json)


@admin.route('/delete/user/<user_id>')
@auth_is_available
def delete_user_data(user_id):
    """删除指定用户"""
    token = json.loads(request.args.get('token'))
    status = delete_user(token["id"], user_id)
    return json.dumps(status)


@admin.route('/delete/user_list', methods=['POST'])
@auth_is_available
def delete_user_list_data():
    token = json.loads(request.args.get('token'))
    user_id_list = request.json
    delete_user_list_status = delete_user_list(token["id"], user_id_list)
    return json.dumps(delete_user_list_status)


@admin.route('/update/user/<user_id>', methods=['POST'])
@auth_is_available
def update_user_data(user_id):
    token = json.loads(request.args.get('token'))
    user_json = request.json
    new_user_json = update_user(token["id"], user_id, json.dumps(user_json))
    return json.dumps(new_user_json)


@admin.route('/roles')
@auth_is_available
def get_all_roles_data():
    """获取所有的角色"""
    token = json.loads(request.args.get('token'))
    roles_json = get_all_roles(token['id'])
    return json.dumps(roles_json)


@admin.route('/tenants/<tenant_id>/users/<user_id>/roles')
@auth_is_available
def get_tenant_user_roles_data(tenant_id, user_id):
    """获取租户某一用户的角色"""
    token = json.loads(request.args.get('token'))
    roles_json = get_tenant_user_role(token['id'], tenant_id, user_id)
    return json.dumps(roles_json)


@admin.route('/tenants/<tenant_id>/users/<user_id>/roles/<role_id>')
@auth_is_available
def grant_tenant_user_role_data(tenant_id, user_id, role_id):
    """授权租户某一用户指定角色"""
    token = json.loads(request.args.get('token'))
    roles_json = grant_tenant_user_role(token['id'], tenant_id, user_id, role_id)
    return json.dumps(roles_json)


@admin.route('/tenant/usage_abstract/<project_id>')
@auth_is_available
def get_tenant_usage_abstract_data(project_id):
    """获取租户的资源使用摘要"""
    token = json.loads(request.args.get('token'))
    tenant_usage_info = get_tenant_usage_abstract(token["id"], token["tenant"]["id"], project_id)
    return json.dumps(tenant_usage_info)


@admin.route('/tenant/instances/<project_id>')
@auth_is_available
def get_tenant_instances_data(project_id):
    """获取租户下虚拟机的基本情况"""
    token = json.loads(request.args.get('token'))
    tenant_instanes_info = get_tenant_instances(token["id"], token["tenant"]["id"], project_id)
    return json.dumps(tenant_instanes_info)


@admin.route('/tenant/networks/<project_id>')
@auth_is_available
def get_tenant_networks_data(project_id):
    """获取租户下网络基本情况"""
    token = json.loads(request.args.get('token'))
    tenant_networks_info = get_tenant_networks(token["id"], project_id)
    return json.dumps(tenant_networks_info)


@admin.route('/tenant/routers/<project_id>')
@auth_is_available
def get_tenant_routers_data(project_id):
    """获取租户的资源路由器"""
    token = json.loads(request.args.get('token'))
    tenant_routers_info = get_tenant_routers_info(token["id"], project_id)
    return json.dumps(tenant_routers_info)
