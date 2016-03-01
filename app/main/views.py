# _*_ coding:utf-8 _*_

from flask import Flask, session, render_template, request
# from flask.ext.login import login_required
import json

from ..decorators import login_required, allow_cross_domain


from . import main
from ..models import User
from collect.monitor import get_tenant_token, get_tenants, get_tenant_instances, get_tenant_instance, get_tenant_resources,\
                            get_tenant_instance_meter, get_tenant_limits, get_user_token


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
    print token
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


@main.route('/')
def index():
    user = session.get('log_user')
    tenants_json = get_tenants(user['token_id'])
    token_json = get_tenant_token(tenants_json['tenants'][0]['name'], user['username'], session.get('log_pwd'))
    user = User(token_json)
    session['log_user'] = user.to_json()
    return render_template('index.html')


@main.route('/instances')
def front_get_tenant_instances():
    user = session.get('log_user')
    vms_json = get_tenant_instances(user['token_id'], user['tenant_id'])
    return json.dumps(vms_json)


@main.route('/instances/<instance_id>')
def front_get_tenant_instance(instance_id):
    user = session.get('log_user')
    vm_json = get_tenant_instance(user['token_id'], user['tenant_id'], instance_id)
    return json.dumps(vm_json)


@main.route('/resources')
def front_get_tenant_resources():
    user = session.get('log_user')
    resources_json = get_tenant_resources(user['token_id'])
    return json.dumps(resources_json)


@main.route('/meters/<instance_id>/<meter_name>')
def front_get_tenant_vm_meters(instance_id, meter_name):
    user = session.get('log_user')
    meter_json = get_tenant_instance_meter(user['token_id'], instance_id, meter_name)
    return json.dumps(meter_json)
