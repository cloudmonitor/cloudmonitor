# _*_ coding:utf-8 _*_

from flask import Flask, session, render_template
# from flask.ext.login import login_required

from ..decorators import login_required


from . import main
from ..models import User
from collect.monitor import get_tenant_token, get_tenants, get_tenant_instances, get_tenant_instance, get_tenant_resources,\
                            get_tenant_instance_meter, get_tenant_limits


@main.route('/')
@login_required
def index():
    user = session.get('log_user')
    tenants_json = get_tenants(user['token_id'])
    token_json = get_tenant_token(tenants_json['tenants'][0]['name'], user['username'], session.get('log_pwd'))
    user = User(token_json)
    session['log_user'] = user.to_json()
    return render_template('index.html')


@main.route('/tenants')
@login_required
def front_get_tenants():
    user = session.get('log_user', None)
    if user is not None:
        tenants_json = get_tenants(user['token_id'])
        token_json = get_tenant_token(tenants_json['tenants'][0]['name'], user['username'], session.get('log_pwd'))
        user = User(token_json)
        session['log_user'] = user.to_json()
        return str(tenants_json)
    return None


@main.route('/limits')
@login_required
def front_get_tenant_limits():
    user = session.get('log_user')
    limits_json = get_tenant_limits(user['token_id'], user['tenant_id'])
    return str(limits_json)


@main.route('/instances')
@login_required
def front_get_tenant_instances():
    user = session.get('log_user')
    vms_json = get_tenant_instances(user['token_id'], user['tenant_id'])
    return str(vms_json)


@main.route('/instances/<instance_id>')
@login_required
def front_get_tenant_instance(instance_id):
    user = session.get('log_user')
    vm_json = get_tenant_instance(user['token_id'], user['tenant_id'], instance_id)
    return str(vm_json)


@main.route('/resources')
@login_required
def front_get_tenant_resources():
    user = session.get('log_user')
    resources_json = get_tenant_resources(user['token_id'])
    return str(resources_json)


@main.route('/meters/<instance_id>/<meter_name>')
@login_required
def front_get_tenant_vm_meters(instance_id, meter_name):
    user = session.get('log_user')
    meter_json = get_tenant_instance_meter(user['token_id'], instance_id, meter_name)
    return str(meter_json)
