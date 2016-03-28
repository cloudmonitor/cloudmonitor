# _*_ coding:utf-8 _*_

from flask import request
import json

from . import main
from collect.monitor import *
# from collect.monitor import get_tenant_token, get_tenants, get_tenant_instances, get_tenant_instance,\
#                             get_tenant_limits, get_user_token, get_tenant_flavors, get_tenant_ports, \
#                             get_tenant_networks, get_tenant_subnets, get_tenant_routers, get_one_firewalls_info,\
#                             get_all_firewalls_info, get_floating_ips, get_security_groups, get_all_policies, \
#                             get_all_rules, get_meter_func_data, get_tuopu_info, create_fw_rule, delete_fw_rule, \
#                             update_fw_rule


@main.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
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


@main.route('/ports')
def front_get_tenant_ports():
    token = json.loads(request.args.get('token'))
    ports_json = get_tenant_ports(token['id'])
    return json.dumps(ports_json)


@main.route('/routers')
def front_get_tenant_routers():
    token = json.loads(request.args.get('token'))
    routers_json = get_tenant_routers(token['id'])
    return json.dumps(routers_json)


@main.route('/floatingips')
def get_floatingips_info():
    token = json.loads(request.args.get('token'))
    floatingip_json = get_floating_ips(token["id"])
    return json.dumps(floatingip_json)


@main.route('/security_groups')
def get_security_groups_info():
    token = json.loads(request.args.get('token'))
    security_groups_json = get_security_groups(token["id"])
    return json.dumps(security_groups_json)


@main.route('/security_groups/create', methods=['POST'])
def create_sgs():
    token = json.loads(request.args.get('token'))
    sg = request.json
    sg_json = create_security_group(token['id'], sg)
    return json.dumps(sg_json)


@main.route('/security_groups/delete', methods=["POST"])
def delete_sgs():
    token = json.loads(request.args.get('token'))
    sg_id_list = request.json
    print sg_id_list
    sg_delete_json = delete_security_group(token['id'], sg_id_list)
    return json.dumps(sg_delete_json)


@main.route('/security_groups/update/<sg_id>', methods=['POST'])
def update_sg(sg_id):
    token = json.loads(request.args.get('token'))
    sg = request.json
    sg_json = update_security_group(token['id'], json.dumps(sg), sg_id)
    return json.dumps(sg_json)


@main.route('/sg_rules/delete', methods=["POST"])
def delete_sgs_rules():
    token = json.loads(request.args.get('token'))
    sg_rules_id_list = request.json
    sg_rules_delete_json = delete_security_group_rules(token['id'], sg_rules_id_list)
    return json.dumps(sg_rules_delete_json)


@main.route('/sg_rules/create', methods=["POST"])
def create_sgs_rules():
    token = json.loads(request.args.get('token'))
    rule = request.json
    rule_json = create_security_group_rules(token['id'], rule)
    return json.dumps(rule_json)


@main.route('/firewalls')
def get_all_firewall():
    token = json.loads(request.args.get('token'))
    firewall_json = get_tenant_firewalls(token['id'])
    return json.dumps(firewall_json)


@main.route('/firewall_rules')
def get_fw_rules():
    token = json.loads(request.args.get('token'))
    rule_json = get_tenant_firewall_rules(token['id'])
    return json.dumps(rule_json)


@main.route('/firewall_rules/create', methods=["POST"])
def create_f_rule():
    token = json.loads(request.args.get('token'))
    rule = request.json
    rule_json = create_firewall_rule(token['id'], rule)
    return json.dumps(rule_json)


@main.route('/firewall_rules/delete', methods=["POST"])
def delete_fw_rule():
    token = json.loads(request.args.get('token'))
    rule_id_list = request.json
    rule_delete_json = delete_firewall_rule(token['id'], rule_id_list)
    return json.dumps(rule_delete_json)


@main.route('/firewall_rules/update/<firewall_rules_id>', methods=["POST"])
def update_fw_rule(firewall_rules_id):
    token = json.loads(request.args.get('token'))
    rule = request.json
    print json.dumps(rule)
    rule_json = update_firewall_rule(token['id'], json.dumps(rule), firewall_rules_id)
    return json.dumps(rule_json)


@main.route('/firewall_policies')
def get_all_policy():
    token = json.loads(request.args.get('token'))
    policy_json = get_tenant_firewall_policies(token['id'])
    return json.dumps(policy_json)


@main.route('/firewall/<firewall_id>')
def get_firewall_info(firewall_id):
    token = json.loads(request.args.get('token'))
    firewall_info_json = get_tenant_firewall(token['id'], firewall_id)
    return json.dumps(firewall_info_json)


@main.route('/monitor/<instance_id>/<meter_name>/<type>')
def get_monitor_network(instance_id, meter_name, type):
    token = json.loads(request.args.get('token'))
    r = get_meter_func_data(token['id'], instance_id, meter_name, type)
    return json.dumps(r)


@main.route('/tuopu')
def get_tuopu():
    token = json.loads(request.args.get('token'))
    r = get_last_network_topology(token['id'], token["tenant"]["id"])
    return json.dumps(r)
