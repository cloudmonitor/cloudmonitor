# _*_ coding:utf-8 _*_

from . import compute
from osapi import *


@compute.route('/tenant_used_quota')
@auth_is_available
def get_tenant_used_quota_info():
    """租户所有资源的使用情况"""
    token = json.loads(request.args.get('token'))
    tenant_used_json = get_tenant_used_info(token['id'], token["tenant"]["id"])
    return json.dumps(tenant_used_json)


@compute.route('/limits')
@auth_is_available
def get_tenant_limits_info():
    """租户重要资源的使用情况"""
    token = json.loads(request.args.get('token'))
    limits_json = get_tenant_limits(token['id'], token['tenant']['id'])
    return json.dumps(limits_json)


@compute.route('/instances')
@auth_is_available
def front_get_tenant_instances():
    """获取某一租户下的所有vm,并将镜像的名字加入到了虚拟机的内容中"""
    token = json.loads(request.args.get('token'))
    vms_json = get_tenant_instances_image(token['id'], token['tenant']['id'])
    return json.dumps(vms_json)


@compute.route('/instance/interfaces/<instance_id>')
@auth_is_available
def front_get_instance_interfaces(instance_id):
    """获取某一虚拟机的interface信息"""
    token = json.loads(request.args.get('token'))
    inter_json = get_server_interface(token['id'], token['tenant']['id'], instance_id)
    return json.dumps(inter_json)


@compute.route('/instance/create', methods=["POST"])
@auth_is_available
def create_servers_info():
    token = json.loads(request.args.get('token'))
    servers_data = request.json
    print json.dumps(servers_data)
    servers_json = create3_servers(token['id'], token['tenant']['id'], json.dumps(servers_data))
    return json.dumps(servers_json)
