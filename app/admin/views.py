# _*_ coding:utf-8 _*_

from flask import request
import json

from osapi import auth_is_available, get_admin_token
from osapi.admin import *

from . import admin


@admin.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    token_json = get_admin_token(username, password)
    return json.dumps(token_json)


@admin.route('/abstract/<token_id>/<tenant_id>/<start_time>/<stop_time>')
def abstract(token_id , start_time, stop_time, tenant_id):
    """获取概要信息"""
    abstract_info = get_tenant_usage(token_id, start_time, stop_time, tenant_id)
    return json.dumps(abstract_info)


@admin.route('/hypervisor/<token_id>/<tenant_id>')
def hypervisor(token_id , tenant_id):
    """获取物理主机的信息"""
    hypervisor_info = get_physical_usage(token_id, tenant_id)
    return json.dumps(hypervisor_info)