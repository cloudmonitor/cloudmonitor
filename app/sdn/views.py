# _*_ coding:utf-8 _*_

from flask import request
import requests
import json
from . import sdn
from osapi import auth_is_available, get_tenant_instance_host_ip
from osapi.sdnapi import StaticFlowPusher, Controller, BASE_URL


@sdn.route('/get_flow_entries')
@auth_is_available
def get_flow_entries():
    staticflowpusher = StaticFlowPusher(BASE_URL)
    flow_entries = staticflowpusher.get_flow("all")
    return json.dumps(flow_entries)


@sdn.route('/add_flow_entry', methods=["POST"])
@auth_is_available
def add_flow_entry():
    flow_entry = request.json
    token = json.loads(request.args.get('token'))
    # 获取虚拟信息（包括端口信息以及对应物理主机IP）
    server_json = get_tenant_instance_host_ip(token['id'], token['tenant']['id'], flow_entry["instance_id"])
    # 虚拟机对应OVS网卡名称
    ifname = "qvo" + server_json["server"]["interfaceAttachments"][0]["port_id"][0:11]
    # 虚拟机对应物理主机IP
    host_ip = server_json["server"]["hostIP"]
    # 通过sFlow-RT获取对应物理主机上的br-int的Metric信息
    metric_json = requests.get("http://192.168.1.180:8008/metric/"+host_ip+"/json").json()
    # 虚拟机对应在OVS上的ifindex
    index = ""
    for key, val in metric_json.items():
        if val == ifname:
            index = key.split('.')[0]
            break
    # 虚拟机对应在OVS上的of_port
    of_port = metric_json[index + ".of_port"]
    # 获取Floodlight管理的OVS信息
    controller = Controller(BASE_URL)
    switch_json = controller.get_switches()
    # 获取虚拟机对应的OVS的DPID
    of_dpid = ""
    for switch in switch_json:
        if switch["inetAddress"].startswith("/" + host_ip):
            of_dpid = switch["switchDPID"]
            break
    # 添加信息到flow_entry
    flow_entry["switch"] = of_dpid
    flow_entry["in_port"] = of_port
    flow_entry["active"] = "true"
    # 向虚拟机对应的OVS添加flow_entry
    staticflowpusher = StaticFlowPusher(BASE_URL)
    add_success = staticflowpusher.add_flow(json.dumps(flow_entry))
    if add_success:
        return json.dumps("success")
    else:
        return json.dumps("fail")


@sdn.route('/delete_flow_entry', methods=["DELETE"])
@auth_is_available
def delete_flow_entry():
    flow_name = request.json
    staticflowpusher = StaticFlowPusher(BASE_URL)
    del_success = staticflowpusher.delete_flow(json.dumps(flow_name))
    if del_success:
        return json.dumps("success")
    else:
        return json.dumps("fail")



