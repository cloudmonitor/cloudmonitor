# _*_ coding:utf-8 _*_

from flask import request
import json

from . import main
from collect.monitor import *


@main.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    token_json = get_user_token(username, password)
    return json.dumps(token_json)


@main.route('/tenants')
@auth_is_available
def front_get_tenants():
    token = json.loads(request.args.get('token'))
    tenants_json = get_tenants(token['id'])
    return json.dumps(tenants_json)


@main.route('/tenant/login')
@auth_is_available
def front_get_tenant_token():
    token = json.loads(request.args.get('token'))
    tenantname = request.args.get('tenantname')
    tenant_token_json = get_tenant_token(tenantname, token['id'])
    return json.dumps(tenant_token_json)


@main.route('/limits')
@auth_is_available
def front_get_tenant_limits():
    token = json.loads(request.args.get('token'))
    limits_json = get_tenant_limits(token['id'], token['tenant']['id'])
    return json.dumps(limits_json)


@main.route('/instances')
@auth_is_available
def front_get_tenant_instances():
    token = json.loads(request.args.get('token'))
    vms_json = get_tenant_instances_image(token['id'], token['tenant']['id'])
    return json.dumps(vms_json)


@main.route('/instance/interfaces/<servers_id>')
@auth_is_available
def front_get_instance_interfaces(servers_id):
    token = json.loads(request.args.get('token'))
    inter_json = get_server_interface(token['id'], token['tenant']['id'], servers_id)
    return json.dumps(inter_json)


@main.route('/servers/create', methods=["POST"])
@auth_is_available
def create_servers_info():
    token = json.loads(request.args.get('token'))
    servers_data = request.json
    print json.dumps(servers_data)
    servers_json = create3_servers(token['id'], token['tenant']['id'], json.dumps(servers_data))
    return json.dumps(servers_json)


@main.route('/servers/update/<servers_id>', methods=["POST"])
@auth_is_available
def update_servers_info(servers_id):
    token = json.loads(request.args.get('token'))
    server = request.json
    server_json = update_servers(token['id'], token['tenant']['id'], json.dumps(server), servers_id)
    return json.dumps(server_json)


@main.route('/servers/delete', methods=["POST"])
@auth_is_available
def delete_servers_info():
    token = json.loads(request.args.get('token'))
    servers_id_list = request.json
    print servers_id_list
    servers_delete_json = delete_servers(token['id'], token['tenant']['id'], servers_id_list)
    return json.dumps(servers_delete_json)


@main.route('/interfaces/bind/<servers_id>', methods=["POST"])
@auth_is_available
def bind_interfaces_info(servers_id):
    token = json.loads(request.args.get('token'))
    data = request.json
    print data
    bind_port_json = bind_interface(token['id'], token['tenant']['id'], data, servers_id)
    return json.dumps(bind_port_json)


@main.route('/touch_interface/<servers_id>', methods=["POST"])
@auth_is_available
def bind_interface2_info(servers_id):
    token = json.loads(request.args.get('token'))
    data = request.json
    bind_port_json = touch_interface(token['id'], token['tenant']['id'], data, servers_id)
    return json.dumps(bind_port_json)


@main.route('/detach_interface/<servers_id>/<port_id>')
@auth_is_available
def detach_interface_info(servers_id,port_id):
    token = json.loads(request.args.get('token'))
    del_port = detach_interface(token['id'], token['tenant']['id'], servers_id, port_id)
    return json.dumps(del_port)


@main.route('/interfaces/delete/<servers_id>', methods=["POST"])
@auth_is_available
def delete_interfaces_info(servers_id):
    token = json.loads(request.args.get('token'))
    interfaces = request.json
    del_port = delete_interface(token['id'], token['tenant']['id'], servers_id, interfaces)
    return json.dumps(del_port)


@main.route('/sever_sg/<servers_id>')
@auth_is_available
def server_sg(servers_id):
    token = json.loads(request.args.get('token'))
    server_sg_json = server_security_group(token['id'], token['tenant']['id'], servers_id)
    return json.dumps(server_sg_json)


@main.route('/disserver_sg/<servers_id>')
@auth_is_available
def disserver_sg(servers_id):
    token = json.loads(request.args.get('token'))
    disserver_sg_json = disserver_security_group(token['id'], token['tenant']['id'], servers_id)
    return json.dumps(disserver_sg_json)


@main.route('/sever_sg/update/<server_id>', methods=["POST"])
@auth_is_available
def bind_security_group_info(server_id):
    token = json.loads(request.args.get('token'))
    data = request.json
    update_sg = server_update_sg(token['id'], token['tenant']['id'], server_id, data)
    return json.dumps(update_sg)


@main.route('/servers_action/<servers_id>', methods=["POST"])
@auth_is_available
def servers_action_info(servers_id):
    token = json.loads(request.args.get('token'))
    data = request.json
    print json.dumps(data)
    remove_json = action_server(token['id'], token['tenant']['id'], servers_id, json.dumps(data))
    return json.dumps(remove_json)


@main.route('/servers_console/<servers_id>', methods=["POST"])
@auth_is_available
def servers_console_info(servers_id):
    token = json.loads(request.args.get('token'))
    data = request.json
    print json.dumps(data)
    console_json = get_server_console(token['id'], token['tenant']['id'], servers_id, json.dumps(data))
    return json.dumps(console_json)


@main.route('/flavors')
@auth_is_available
def front_get_tenant_flavors():
    token = json.loads(request.args.get('token'))
    flavors_json = get_tenant_flavors(token['id'], token['tenant']['id'])
    return json.dumps(flavors_json)


@main.route('/tenant_limits')
@auth_is_available
def front_get_limits():
    token = json.loads(request.args.get('token'))
    limits_json = get_tenant_limits(token['id'], token['tenant']['id'])
    return json.dumps(limits_json)


@main.route('/os_availability_zone')
@auth_is_available
def front_get_os_availability_zone():
    token = json.loads(request.args.get('token'))
    zone_json = get_tenant_os_availability_zone(token['id'], token['tenant']['id'])
    return json.dumps(zone_json)


@main.route('/images')
@auth_is_available
def front_get_images():
    token = json.loads(request.args.get('token'))
    images_json = get_tenant_images(token['id'])
    return json.dumps(images_json)


@main.route('/instances/<instance_id>')
@auth_is_available
def front_get_tenant_instance(instance_id):
    token = json.loads(request.args.get('token'))
    vm_json = get_tenant_instance(token['id'], token['tenant']['id'], instance_id)
    return json.dumps(vm_json)


@main.route('/networks')
@auth_is_available
def front_get_tenant_networks():
    token = json.loads(request.args.get('token'))
    networks_json = get_tenant_networks(token['id'])
    return json.dumps(networks_json)


@main.route('/all_networks')
@auth_is_available
def front_get_all_networks():
    token = json.loads(request.args.get('token'))
    networks_json = get_all_networks(token['id'])
    return json.dumps(networks_json)


@main.route('/extnet')
@auth_is_available
def front_get_tenant_extnet():
    token = json.loads(request.args.get('token'))
    extnet_json = get_tenant_ext_net(token['id'])
    return json.dumps(extnet_json)


@main.route('/subnets')
@auth_is_available
def front_get_tenant_subnets():
    token = json.loads(request.args.get('token'))
    subnets_json = get_tenant_subnets(token['id'])
    return json.dumps(subnets_json)


# @main.route('/new_subnets')
# @auth_is_available
# def front_get_tenant_new_subnets():
#     token = json.loads(request.args.get('token'))
#     subnets_json = get_new_subnets(token['id'])
#     return json.dumps(subnets_json)


@main.route('/ports')
@auth_is_available
def front_get_tenant_ports():
    token = json.loads(request.args.get('token'))
    ports_json = get_tenant_ports(token['id'])
    return json.dumps(ports_json)


@main.route('/server_ports')
@auth_is_available
def front_get_tenant_server_ports():
    token = json.loads(request.args.get('token'))
    ports_json = get_server_port(token['id'], token["tenant"]["id"])
    return json.dumps(ports_json)


@main.route('/router_ports/<router_id>')
@auth_is_available
def front_get_router_ports(router_id):
    token = json.loads(request.args.get('token'))
    router_ports_json = get_router_ports(token['id'], router_id)
    return json.dumps(router_ports_json)


@main.route('/routers')
@auth_is_available
def front_get_tenant_routers():
    token = json.loads(request.args.get('token'))
    routers_json = get_tenant_routers(token['id'])
    return json.dumps(routers_json)


@main.route('/router_table/<router_id>')
@auth_is_available
def front_get_routers(router_id):
    token = json.loads(request.args.get('token'))
    tables_json = get_route_table(token['id'], router_id)
    return json.dumps(tables_json)


@main.route('/floatingips')
@auth_is_available
def get_floatingips_info():
    token = json.loads(request.args.get('token'))
    floatingip_json = get_floating_ips(token["id"])
    return json.dumps(floatingip_json)


@main.route('/dis_floatingips')
@auth_is_available
def get_dis_floatingips_info():
    token = json.loads(request.args.get('token'))
    floatingip_json = get_disallocate_floating_ips(token["id"])
    return json.dumps(floatingip_json)


@main.route('/floatingips/allocate', methods=["POST"])
@auth_is_available
def allocate_floatingips():
    token = json.loads(request.args.get('token'))
    data = json.dumps(request.json)
    print data
    floatingip_json = allocate_floating_ips(token["id"], data)
    return json.dumps(floatingip_json)


@main.route('/floatingips/release', methods=["POST"])
@auth_is_available
def release_floatingips():
    token = json.loads(request.args.get('token'))
    data = request.json
    release_json = release_floating_ips(token["id"], data)
    return json.dumps(release_json)


@main.route('/floatingips/associate/<floatingip_id>', methods=["POST"])
@auth_is_available
def associate_floatingips(floatingip_id):
    token = json.loads(request.args.get('token'))
    data = json.dumps(request.json)
    associate_json = associate_floatingip_prot(token["id"], floatingip_id, data)
    return json.dumps(associate_json)


@main.route('/floatingips/disassociateport')
@auth_is_available
def disassociate_floatingips_port():
    token = json.loads(request.args.get('token'))
    disassociateport_json = get_disassociate_floatingip_port(token["id"])
    return json.dumps(disassociateport_json)


@main.route('/security_groups')
@auth_is_available
def get_security_groups_info():
    token = json.loads(request.args.get('token'))
    security_groups_json = get_security_groups(token["id"])
    return json.dumps(security_groups_json)


@main.route('/security_groups/create', methods=['POST'])
@auth_is_available
def create_sgs():
    token = json.loads(request.args.get('token'))
    sg = request.json
    sg_json = create_security_group(token['id'], sg)
    return json.dumps(sg_json)


@main.route('/security_groups/delete', methods=["POST"])
@auth_is_available
def delete_sgs():
    token = json.loads(request.args.get('token'))
    sg_id_list = request.json
    print sg_id_list
    sg_delete_json = delete_security_group(token['id'], sg_id_list)
    return json.dumps(sg_delete_json)


@main.route('/security_groups/update/<sg_id>', methods=['POST'])
@auth_is_available
def update_sg(sg_id):
    token = json.loads(request.args.get('token'))
    sg = request.json
    sg_json = update_security_group(token['id'], json.dumps(sg), sg_id)
    return json.dumps(sg_json)


@main.route('/sg_rules/delete', methods=["POST"])
@auth_is_available
def delete_sgs_rules():
    token = json.loads(request.args.get('token'))
    sg_rules_id_list = request.json
    sg_rules_delete_json = delete_security_group_rules(token['id'], sg_rules_id_list)
    return json.dumps(sg_rules_delete_json)


@main.route('/sg_rules/create', methods=["POST"])
@auth_is_available
def create_sgs_rules():
    token = json.loads(request.args.get('token'))
    rule = request.json
    rule_json = create_security_group_rules(token['id'], rule)
    return json.dumps(rule_json)


@main.route('/firewalls')
@auth_is_available
def get_all_firewall():
    token = json.loads(request.args.get('token'))
    firewall_json = get_tenant_firewalls(token['id'])
    return json.dumps(firewall_json)


@main.route('/firewall_rules')
@auth_is_available
def get_fw_rules():
    token = json.loads(request.args.get('token'))
    rule_json = get_tenant_firewall_rules(token['id'])
    return json.dumps(rule_json)


@main.route('/firewall_rules/create', methods=["POST"])
@auth_is_available
def create_fw_rule():
    token = json.loads(request.args.get('token'))
    rule = request.json
    rule_json = create_firewall_rule(token['id'], rule)
    return json.dumps(rule_json)


@main.route('/firewall_rules/delete', methods=["POST"])
@auth_is_available
def delete_fw_rule():
    token = json.loads(request.args.get('token'))
    rule_id_list = request.json
    rule_delete_json = delete_firewall_rule(token['id'], rule_id_list)
    return json.dumps(rule_delete_json)


@main.route('/firewall_rules/update/<firewall_rules_id>', methods=["POST"])
@auth_is_available
def update_fw_rule(firewall_rules_id):
    token = json.loads(request.args.get('token'))
    rule = request.json
    print json.dumps(rule)
    rule_json = update_firewall_rule(token['id'], json.dumps(rule), firewall_rules_id)
    return json.dumps(rule_json)


@main.route('/firewall_policies')
@auth_is_available
def get_all_policy():
    token = json.loads(request.args.get('token'))
    policy_json = get_tenant_firewall_policies(token['id'])
    return json.dumps(policy_json)


@main.route('/firewall_policies/create', methods=["POST"])
@auth_is_available
def policy_create():
    token = json.loads(request.args.get('token'))
    policy_data = request.json
    policy_json = create_policy(token['id'], json.dumps(policy_data))
    return json.dumps(policy_json)


@main.route('/firewall_policies/update/<firewall_policies_id>', methods=["POST"])
@auth_is_available
def update_policies(firewall_policies_id):
    token = json.loads(request.args.get('token'))
    policy = request.json
    policy_json = update_policy(token['id'], json.dumps(policy), firewall_policies_id)
    return json.dumps(policy_json)


@main.route('/firewall_policies/delete', methods=["POST"])
@auth_is_available
def delete_policies():
    token = json.loads(request.args.get('token'))
    policies_id_list = request.json
    print policies_id_list
    policy_delete_json = delete_fw_policy(token['id'], policies_id_list)
    return json.dumps(policy_delete_json)


@main.route('/firewall_policies/insert_rule/<policy_id>', methods=["POST"])
@auth_is_available
def insert_rule(policy_id):
    token = json.loads(request.args.get('token'))
    rule_data = request.json
    insert_rule_json = insert_rule_policy(token['id'], policy_id, json.dumps(rule_data))
    return json.dumps(insert_rule_json)


@main.route('/firewall_policies/remove_rule/<policy_id>', methods=["POST"])
@auth_is_available
def remove_rule(policy_id):
    token = json.loads(request.args.get('token'))
    rule_data = request.json
    remove_rule_json = remove_rule_policy(token['id'], policy_id, json.dumps(rule_data))
    return json.dumps(remove_rule_json)


@main.route('/firewall/create', methods=["POST"])
@auth_is_available
def create_fw():
    token = json.loads(request.args.get('token'))
    firewll_info = request.json
    firewall_info_json = create_firewall(token['id'], json.dumps(firewll_info))
    return json.dumps(firewall_info_json)


@main.route('/firewall/update/<firewall_id>', methods=["POST"])
@auth_is_available
def update_fw(firewall_id):
    token = json.loads(request.args.get('token'))
    firewall = request.json
    firewall_json = update_firewall(token['id'], json.dumps(firewall), firewall_id)
    return json.dumps(firewall_json)


@main.route('/firewall/delete', methods=["POST"])
@auth_is_available
def delete_fw():
    token = json.loads(request.args.get('token'))
    firewalls_id_list = request.json
    print firewalls_id_list
    firewall_delete_json = delete_firewll(token['id'], firewalls_id_list)
    return json.dumps(firewall_delete_json)


@main.route('/firewall/<firewall_id>')
@auth_is_available
def get_firewall_info(firewall_id):
    token = json.loads(request.args.get('token'))
    firewall_info_json = get_tenant_firewall(token['id'], firewall_id)
    return json.dumps(firewall_info_json)


@main.route('/monitor/<instance_id>/<meter_name>/<type>')
@auth_is_available
def get_monitor_network(instance_id, meter_name, type):
    token = json.loads(request.args.get('token'))
    r = get_meter_func_data(token['id'], instance_id, meter_name, type)
    return json.dumps(r)


@main.route('/tuopu')
@auth_is_available
def get_tuopu():
    token = json.loads(request.args.get('token'))
    r = get_last_network_topology(token['id'], token["tenant"]["id"])
    return json.dumps(r)


@main.route('/network/create', methods=["POST"])
@auth_is_available
def create_net():
    token = json.loads(request.args.get('token'))
    network_data = request.json
    network_json = create_network(token['id'], json.dumps(network_data))
    return json.dumps(network_json)


@main.route('/network/update/<network_id>', methods=["POST"])
@auth_is_available
def update_net(network_id):
    token = json.loads(request.args.get('token'))
    network = request.json
    network_json = update_network(token['id'], json.dumps(network), network_id)
    return json.dumps(network_json)


@main.route('/network/delete', methods=["POST"])
@auth_is_available
def delete_net():
    token = json.loads(request.args.get('token'))
    network_id_list = request.json
    network_delete_json = delete_network(token['id'], network_id_list)
    return json.dumps(network_delete_json)


@main.route('/subnet/create', methods=["POST"])
@auth_is_available
def create_subnet_info():
    token = json.loads(request.args.get('token'))
    subnet_data = request.json
    print json.dumps(subnet_data)
    subnet_json = create_subnet(token['id'], json.dumps(subnet_data))
    print json.dumps(subnet_json)
    return json.dumps(subnet_json)


@main.route('/subnet/update/<subnet_id>', methods=["POST"])
@auth_is_available
def update_subnet_info(subnet_id):
    token = json.loads(request.args.get('token'))
    subnet = request.json
    subnet_json = update_subnet(token['id'], json.dumps(subnet), subnet_id)
    return json.dumps(subnet_json)


@main.route('/subnet/delete', methods=["POST"])
@auth_is_available
def delete_subnet_info():
    token = json.loads(request.args.get('token'))
    subnet_id_list = request.json
    print subnet_id_list
    subnet_delete_json = delete_subnet(token['id'], subnet_id_list)
    return json.dumps(subnet_delete_json)


@main.route('/port/create', methods=["POST"])
@auth_is_available
def create_port_info():
    token = json.loads(request.args.get('token'))
    port_data = request.json
    port_json = create_port(token['id'], json.dumps(port_data))
    return json.dumps(port_json)


@main.route('/port/update/<port_id>', methods=["POST"])
@auth_is_available
def update_port_info(port_id):
    token = json.loads(request.args.get('token'))
    port = request.json
    port_json = update_port(token['id'], json.dumps(port), port_id)
    return json.dumps(port_json)


@main.route('/port/delete', methods=["POST"])
@auth_is_available
def delete_port_info():
    token = json.loads(request.args.get('token'))
    port_id_list = request.json
    print port_id_list
    port_delete_json = delete_port(token['id'], port_id_list)
    return json.dumps(port_delete_json)


@main.route('/router/create', methods=["POST"])
@auth_is_available
def create_router_info():
    token = json.loads(request.args.get('token'))
    router_data = request.json
    router_json = create_router(token['id'], json.dumps(router_data))
    return json.dumps(router_json)


@main.route('/router/update/<router_id>', methods=["POST"])
@auth_is_available
def update_router_info(router_id):
    token = json.loads(request.args.get('token'))
    router = request.json
    router_json = update_router(token['id'], json.dumps(router), router_id)
    return json.dumps(router_json)


@main.route('/routers/disconnect_subnet')
@auth_is_available
def disconnect_subnet_info():
    token = json.loads(request.args.get('token'))
    dissubnet_json = disconnect_subnet(token['id'])
    return json.dumps(dissubnet_json)


@main.route('/router/delete', methods=["POST"])
@auth_is_available
def delete_router_info():
    token = json.loads(request.args.get('token'))
    router_id_list = request.json
    router_delete_json = delete_router(token['id'], router_id_list)
    return json.dumps(router_delete_json)


@main.route('/router/<router_id>/add_router_interface', methods=["POST"])
@auth_is_available
def add_router_inter(router_id):
    token = json.loads(request.args.get('token'))
    subnet = request.json
    inter_json = add_router_interface(token['id'], router_id, json.dumps(subnet))
    return json.dumps(inter_json)


@main.route('/router/<router_id>/remove_router_interface', methods=["POST"])
@auth_is_available
def remove_router_inter(router_id):
    token = json.loads(request.args.get('token'))
    inter_info = request.json
    dele_status = remove_router_interface(token['id'], router_id, json.dumps(inter_info))
    return json.dumps(dele_status)


@main.route('/keypairs')
@auth_is_available
def get_keypairs():
    token = json.loads(request.args.get('token'))
    keypairs = get_tenant_keypairs(token['id'], token["tenant"]["id"])
    return json.dumps(keypairs)


@main.route('/keypairs/create', methods=["POST"])
@auth_is_available
def create_keypairs():
    token = json.loads(request.args.get('token'))
    data = json.dumps(request.json)
    keypairs = create_tenant_keypair(token['id'], token["tenant"]["id"], data)
    return json.dumps(keypairs)


@main.route('/keypairs/delete', methods=["POST"])
@auth_is_available
def delete_keypairs():
    token = json.loads(request.args.get('token'))
    keypairs_name = request.json
    del_status = delete_tenant_keypair(token['id'], token["tenant"]["id"], keypairs_name)
    return json.dumps(del_status)


@main.route('/user/create', methods=["POST"])
@auth_is_available
def create_user_info():
    token = json.loads(request.args.get('token'))
    user_data = request.json
    user_json = create_user(token, json.dumps(user_data))
    return json.dumps(user_json)


@main.route('/user/update/<user_id>', methods=["POST"])
@auth_is_available
def update_user_info(user_id):
    token = json.loads(request.args.get('token'))
    data = request.json
    print json.dumps(data)
    user_json = update_user(token, user_id, data)
    return json.dumps(user_json)


@main.route('/user/delete/<user_id>')
@auth_is_available
def delete_user_info(user_id):
    token = json.loads(request.args.get('token'))
    delete_json = delete_user(token, user_id)
    return delete_json


@main.route('/user/detail/<user_id>')
@auth_is_available
def get_detail_user_info(user_id):
    token = json.loads(request.args.get('token'))
    detail_json = get_users_detail(token, user_id)
    return detail_json


@main.route('/tenant_used_quota')
@auth_is_available
def get_tenant_used_quota_info():
    token = json.loads(request.args.get('token'))
    tenant_used_json = get_tenant_used_info(token['id'], token["tenant"]["id"])
    return tenant_used_json
