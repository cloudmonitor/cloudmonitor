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
    return status


@admin.route('/update/tenant/<tenant_id>', methods=['POST'])
@auth_is_available
def update_tenant_data(tenant_id):
    token = json.loads(request.args.get('token'))
    tenant_json = request.json
    new_tenant_json = update_tenant(token["id"], tenant_id, json.dumps(tenant_json))
    return json.dumps(new_tenant_json)


@admin.route('/update/tenant/<tenant_id>/quota', methods=['POST'])
@auth_is_available
def update_tenant_quota_data(tenant_id):
    token = json.loads(request.args.get('token'))
    admin_tenant_id = request.args.get('admin_tenant_id')
    quota_json = request.json
    new_quota_json = update_tenant_quota(token["id"], admin_tenant_id, tenant_id, json.dumps(quota_json))
    return json.dumps(new_quota_json)


@admin.route('/users')
@auth_is_available
def get_all_users_data():
    token = json.loads(request.args.get('token'))
    users_json = get_all_users(token['id'])
    return json.dumps(users_json)


@admin.route('/create/user', methods=['POST'])
@auth_is_available
def create_user_data():
    token = json.loads(request.args.get('token'))
    user_json = request.json
    create_user_json = create_user(token["id"], json.dumps(user_json))
    return json.dumps(create_user_json)


@admin.route('/delete/user/<user_id>')
@auth_is_available
def delete_user_data(user_id):
    token = json.loads(request.args.get('token'))
    status = delete_user(token["id"], user_id)
    return status


@admin.route('/update/user/<user_id>', methods=['POST'])
@auth_is_available
def update_user_data(user_id):
    token = json.loads(request.args.get('token'))
    user_json = request.json
    new_user_json = update_user(token["id"], user_id, json.dumps(user_json))
    return json.dumps(new_user_json)

