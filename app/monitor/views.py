# _*_ coding:utf-8 _*_

from . import monitor
from osapi import *


@monitor.route('/top_tenant/<curr_type>')
@auth_is_available
def get_top_tenant_data(curr_type):
    r = get_top_tenant(curr_type)
    return json.dumps(r)


@monitor.route('/<tenant_id>/tenant_top_instance/<curr_type>')
@auth_is_available
def get_tenant_top_instance_data(tenant_id, curr_type):
    r = get_tenant_top_instance(tenant_id, curr_type)
    return json.dumps(r)


@monitor.route('/<tenant_id>/tenant_top_protocol/<curr_type>')
@auth_is_available
def get_tenant_top_protocol_data(tenant_id, curr_type):
    r = get_tenant_top_protocol(tenant_id, curr_type)
    return json.dumps(r)


@monitor.route('/<tenant_id>/tenant_top_ip/<curr_type>')
@auth_is_available
def get_tenant_top_ip_data(tenant_id, curr_type):
    r = get_tenant_top_ip(tenant_id, curr_type)
    return json.dumps(r)


@monitor.route('/<tenant_id>/tenant_top_ip_link/<curr_type>')
@auth_is_available
def get_tenant_top_ip_link_data(tenant_id, curr_type):
    r = get_tenant_top_ip_link(tenant_id, curr_type)
    return json.dumps(r)


@monitor.route('/<tenant_id>/tenant_top_port/<curr_type>')
@auth_is_available
def get_tenant_top_port_data(tenant_id, curr_type):
    r = get_tenant_top_port(tenant_id, curr_type)
    return json.dumps(r)


@monitor.route('/<tenant_id>/tenant_top_protocol_port/<curr_type>')
@auth_is_available
def get_tenant_top_protocol_port_data(tenant_id, curr_type):
    r = get_tenant_top_protocol_port(tenant_id, curr_type)
    return json.dumps(r)


@monitor.route('/<tenant_id>/tenant_top_session/<curr_type>')
@auth_is_available
def get_tenant_top_session_data(tenant_id, curr_type):
    r = get_tenant_top_session(tenant_id, curr_type)
    return json.dumps(r)


@monitor.route('/<instance_id>/<meter_name>/<curr_type>')
@auth_is_available
def get_monitor_data(instance_id, meter_name, curr_type):
    token = json.loads(request.args.get('token'))
    limit = int(request.args.get('limit'))
    r = get_meter_func_data(token['id'], instance_id, meter_name, curr_type, limit)
    return json.dumps(r)


@monitor.route('/<instance_id>/instance_active_flow')
@auth_is_available
def get_instance_active_flow_data(instance_id):
    r = get_instance_active_flow(instance_id)
    return json.dumps(r)


@monitor.route('/<tenant_id>/<instance_id>/instance_top_protocol_port/<curr_type>')
@auth_is_available
def get_instance_top_protocol_port_data(tenant_id, instance_id, curr_type):
    r = get_instance_top_protocol_port(tenant_id, instance_id, curr_type)
    return json.dumps(r)


@monitor.route('/<tenant_id>/<instance_id>/instance_top_ip_link/<curr_type>')
@auth_is_available
def get_instance_top_ip_link_data(tenant_id, instance_id, curr_type):
    r = get_instance_top_ip_link(tenant_id, instance_id, curr_type)
    return json.dumps(r)


@monitor.route('/<tenant_id>/<instance_id>/instance_top_session/<curr_type>')
@auth_is_available
def get_instance_top_session_data(tenant_id, instance_id, curr_type):
    r = get_instance_top_session(tenant_id, instance_id, curr_type)
    return json.dumps(r)


@monitor.route('/<tenant_id>/<instance_id>/instance_top_src_ip/<curr_type>')
@auth_is_available
def get_instance_top_src_ip_data(tenant_id, instance_id, curr_type):
    r = get_instance_top_src_ip(tenant_id, instance_id, curr_type)
    return json.dumps(r)


@monitor.route('/<tenant_id>/<instance_id>/instance_top_dst_ip/<curr_type>')
@auth_is_available
def get_instance_top_dst_ip_data(tenant_id, instance_id, curr_type):
    r = get_instance_top_dst_ip(tenant_id, instance_id, curr_type)
    return json.dumps(r)


@monitor.route('/<tenant_id>/<instance_id>/instance_top_src_port/<curr_type>')
@auth_is_available
def get_instance_top_src_port_data(tenant_id, instance_id, curr_type):
    r = get_instance_top_src_port(tenant_id, instance_id, curr_type)
    return json.dumps(r)


@monitor.route('/<tenant_id>/<instance_id>/instance_top_dst_port/<curr_type>')
@auth_is_available
def get_instance_top_dst_port_data(tenant_id, instance_id, curr_type):
    r = get_instance_top_dst_port(tenant_id, instance_id, curr_type)
    return json.dumps(r)









