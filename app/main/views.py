# _*_ coding:utf-8 _*_

from flask import Flask, session, render_template, request
# from flask.ext.login import login_required
import json

from ..decorators import login_required, allow_cross_domain


from . import main
from ..models import User
from collect.monitor import get_tenant_token, get_tenants, get_tenant_instances, get_tenant_instance, get_tenant_resources,\
                            get_tenant_instance_meter, get_tenant_limits, get_user_token, get_tenant_flavors, \
                            get_tenant_networks, get_tenant_subnets, get_tenant_routers



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
