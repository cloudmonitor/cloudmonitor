# _*_ coding:utf-8 _*_

from . import monitor
from osapi import *


@monitor.route('/monitor/<instance_id>/<meter_name>/<curr_type>')
@auth_is_available
def get_monitor_data(instance_id, meter_name, curr_type):
    token = json.loads(request.args.get('token'))
    limit = int(request.args.get('limit'))
    r = get_meter_func_data(token['id'], instance_id, meter_name, curr_type, limit)
    return json.dumps(r)



