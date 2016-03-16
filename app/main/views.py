# _*_ coding:utf-8 _*_

from flask import Flask, session, render_template, request
# from flask.ext.login import login_required
import json

from ..decorators import login_required, allow_cross_domain


from . import main
from ..models import User
from collect.monitor import get_tenant_token, get_tenants, get_tenant_instances, get_tenant_instance, get_tenant_resources,\
                            get_tenant_instance_meter, get_tenant_limits, get_user_token, get_tenant_flavors, \
                            get_tenant_networks, get_tenant_subnets, get_tenant_routers,get_one_firewalls_info,get_all_rules, \
                            get_all_policies, get_all_firewalls_info, get_floatingips, get_security_groups,get_port_all_info,get_all_policies, \
                            get_all_rules,get_list_meter_minute,get_instance_network_resource_id,get_meter_func_data,get_tuopu_info






@main.route('/login', methods=['POST'])
def login():
    # print "hello"
    # print request.form.get('data')
    data = json.loads(request.form.get('data'))
    username = data['username']
    password = data['password']
    token_json = get_user_token(username, password)
    return json.dumps(token_json)


@main.route('/tenants')
def front_get_tenants():
    token = json.loads(request.args.get('token'))
    tenants_json = get_tenants(token['id'])
    return json.dumps(tenants_json)


@main.route('/tenant/login')
def front_get_tenant_token():
    token = json.loads(request.args.get('token'))
    tenantname = request.args.get('tenantname')
    tenant_token_json = get_tenant_token(tenantname, token['id'])
    return json.dumps(tenant_token_json)


@main.route('/limits')
@allow_cross_domain
def front_get_tenant_limits():
    token = json.loads(request.args.get('token'))
    limits_json = get_tenant_limits(token['id'], token['tenant']['id'])
    return json.dumps(limits_json)


@main.route('/instances')
def front_get_tenant_instances():
    token = json.loads(request.args.get('token'))
    vms_json = get_tenant_instances(token['id'], token['tenant']['id'])
    return json.dumps(vms_json)


@main.route('/flavors')
def front_get_tenant_flavors():
    token = json.loads(request.args.get('token'))
    flavors_json = get_tenant_flavors(token['id'], token['tenant']['id'])
    return json.dumps(flavors_json)


@main.route('/instances/<instance_id>')
def front_get_tenant_instance(instance_id):
    token = json.loads(request.args.get('token'))
    vm_json = get_tenant_instance(token['id'], token['tenant']['id'], instance_id)
    return json.dumps(vm_json)


@main.route('/networks')
def front_get_tenant_networks():
    token = json.loads(request.args.get('token'))
    networks_json = get_tenant_networks(token['id'])
    return json.dumps(networks_json)


@main.route('/subnets')
def front_get_tenant_subnets():
    token = json.loads(request.args.get('token'))
    subnets_json = get_tenant_subnets(token['id'])
    return json.dumps(subnets_json)


@main.route('/routers')
def front_get_tenant_routers():
    token = json.loads(request.args.get('token'))
    routers_json = get_tenant_routers(token['id'])
    return json.dumps(routers_json)


@main.route('/resources')
def front_get_tenant_resources():
    token = json.loads(request.args.get('token'))
    resources_json = get_tenant_resources(token['id'])
    return json.dumps(resources_json)


@main.route('/meters/<instance_id>/<meter_name>')
def front_get_tenant_vm_meters(instance_id, meter_name):
    token = json.loads(request.args.get('token'))
    meter_json = get_tenant_instance_meter(token['id'], instance_id, meter_name)
    return json.dumps(meter_json)


@main.route('/floatingips')
def get_floatingips_info():
    token = json.loads(request.args.get('token'))
    floatingip_json = get_floatingips(token["id"])
    return json.dumps(floatingip_json)


@main.route('/security_groups')
def get_security_groups_info():
    token = json.loads(request.args.get('token'))
    security_groups_json = get_security_groups(token["id"])
    return json.dumps(security_groups_json)


@main.route('/firewalls')
def get_all_firewall():
    token = json.loads(request.args.get('token'))
    firewall_json = get_all_firewalls_info(token['id'])
    return json.dumps(firewall_json)


@main.route('/firewall_rules')
def get_all_rule():
    token = json.loads(request.args.get('token'))
    rule_json = get_all_rules(token['id'])
    return json.dumps(rule_json)


@main.route('/firewall_policies')
def get_all_policy():
    token = json.loads(request.args.get('token'))
    policy_json = get_all_policies(token['id'])
    return json.dumps(policy_json)


@main.route('/firewall/<firewall_id>')
def get_firewall_info(firewall_id):
    token = json.loads(request.args.get('token'))
    firewall_info_json = get_one_firewalls_info(token['id'], firewall_id)
    return json.dumps(firewall_info_json)


@main.route('/ports')
def get_ports_info():
    token = json.loads(request.args.get('token'))
    ports_info_json = get_port_all_info(token['id'])
    return json.dumps(ports_info_json)


@main.route('/policy')
def get_policy_info():
    token = json.loads(request.args.get('token'))
    policy_info_json = get_all_policies(token['id'])
    return json.dumps(policy_info_json)


@main.route('/rules')
def get_rules_info():
    token = json.loads(request.args.get('token'))
    rules_info = get_all_rules(token['id'])
    return json.dumps(rules_info)


@main.route('/monitor/<instance_id>/cpu_util')
def get_monitor_cpu_util(instance_id):
    token = json.loads(request.args.get('token'))
    cpu_util_info = get_list_meter_minute(token['id'],'cpu_util',instance_id)
    return json.dumps(cpu_util_info)


@main.route('/monitor/<instance_id>/<meter_name>/<type>')
def get_monitor_network(instance_id,meter_name, type):
    token = json.loads(request.args.get('token'))
    r = get_meter_func_data(token['id'],instance_id, meter_name,type)
    # monitor_network_outgoing = get_list_meter_minute(token['id'],"network.outgoing.bytes.rate",resource_id)
    # r = {"monitor_network_incoming":monitor_network_incoming,"monitor_network_outgoing":monitor_network_outgoing}
    return json.dumps(r)


@main.route('/monitor/<instance_id>/disk_info')
def get_disk_info(instance_id):
    token = json.loads(request.args.get('token'))
    disk_read_rate = get_list_meter_minute(token['id'],"disk.read.bytes.rate",instance_id)
    disk_write_rate = get_list_meter_minute(token['id'],"disk.write.bytes.rate",instance_id)
    r = dict(disk_read_rate, **disk_write_rate)
    return json.dumps(r)


@main.route('/tuopu')
def get_tuopu():
    token = json.loads(request.args.get('token'))
    r = get_tuopu_info(token['id'], token["tenant"]["id"])
    return json.dumps(r)
