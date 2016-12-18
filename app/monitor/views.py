# _*_ coding:utf-8 _*_

from . import monitor
from osapi import *


@monitor.route('/<instance_id>/<meter_name>/<curr_type>')
@auth_is_available
def get_monitor_data(instance_id, meter_name, curr_type):
    token = json.loads(request.args.get('token'))
    limit = int(request.args.get('limit'))
    r = get_meter_func_data(token['id'], instance_id, meter_name, curr_type, limit)
    return json.dumps(r)


@monitor.route('/<tenant_id>/<curr_type>')
@auth_is_available
def get_tenant_top_instance_data(tenant_id, curr_type):
    r = get_tenant_top_instance(tenant_id, curr_type)
    return json.dumps(r)




