# _*_ coding:utf-8 _*_

from neutron import get_all_networks, get_tenant_subnets, get_tenant_routers, get_tenant_ports
from nova import get_tenant_instances


SERVER_NUM = 0
NET_NUM = 0
ROUTER_NUM = 0
EXNET_NUM = 0


def _get_tuopu_port_info(token_id):
    """获取拓扑的端口信息"""
    ports_list = []

    all_port_info = get_tenant_ports(token_id)
    #print json.dumps(all_port_info)
    for i in range(len(all_port_info['ports'])):
        port_info = {}
        if not all_port_info['ports'][i]['device_id'].startswith('dhcp'):
            port_info["status"] = all_port_info['ports'][i]['status']
            port_info["srcDeviceId"] = all_port_info['ports'][i]['network_id']
            port_info["url"] = ""
            port_info["device_owner"] = all_port_info['ports'][i]["device_owner"]
            port_info["fixed_ips"] = all_port_info['ports'][i]["fixed_ips"]
            port_info["id"] = all_port_info['ports'][i]["id"]
            port_info["dstDeviceId"] = all_port_info['ports'][i]["device_id"]
            port_info["stroke"] = "black"
            port_info["strokeWidth"] = 1
            ports_list.append(port_info)
    all_routers_info = get_tenant_routers(token_id)
    for i in range(len(all_routers_info["routers"])):
        # router_id = all_routers_info['routers'][i]['id']
        # one_router_info = get_one_routers_info(token_id, router_id)
        if all_routers_info['routers'][i]["external_gateway_info"]:
            ex_port_info = {}
            ex_port_info["srcDeviceId"] = all_routers_info['routers'][i]["external_gateway_info"]["network_id"]
            ex_port_info["fixed_ips"] = all_routers_info['routers'][i]["external_gateway_info"]["external_fixed_ips"]
            ex_port_info["id"] = "gateway"+all_routers_info['routers'][i]["external_gateway_info"]["network_id"]
            ex_port_info["dstDeviceId"] = all_routers_info['routers'][i]["id"]
            ex_port_info["stroke"] = "black"
            ex_port_info["strokeWidth"] = 1
            ports_list.append(ex_port_info)
    return ports_list


def _get_tuopu_router_info(token_id):
    """ 获取路由器的tuopu信息 """
    routers_list = []
    x = 240
    y = 240
    width = 100
    height = 100
    all_routers_info = get_tenant_routers(token_id)
    for i in range(len(all_routers_info['routers'])):
        router_info = {}
        router_info["status"] = all_routers_info["routers"][i]["status"]
        router_info["external_gateway_info"] = all_routers_info["routers"][i]["external_gateway_info"]
        router_info["url"] = ""
        router_info["id"] = all_routers_info["routers"][i]["id"]
        router_info["name"] = all_routers_info["routers"][i]["name"]
        router_info["src"] = "./icon/device/router.png"
        router_info["device_name"] = "router"
        global ROUTER_NUM
        ROUTER_NUM += 1
        # router_info["x"] = "%s" %(x+i*width)
        # router_info["y"] = "%s" %(y + i*height)
        router_info["width"] = "%s" %(70)
        router_info["height"] = "%s" %(70)
        routers_list.append(router_info)
    return routers_list


def _get_tuopu_network_info(network_info, subnet_info):
    net_info = []
    x = 360
    y = 360
    width = 100
    height = 100
    for i in range(len(network_info["networks"])):
        _net_info = {}
        _net_info["status"] = network_info["networks"][i]["status"]
        _net_info["subnets"] = _get_subnet_detail(network_info["networks"][i]["id"], subnet_info)
        _net_info["name"] = network_info["networks"][i]["name"]
        _net_info["router:external"] = network_info["networks"][i]["router:external"]
        _net_info["url"] = ""
        _net_info["id"] = network_info["networks"][i]["id"]
        if network_info["networks"][i]["router:external"]:
            _net_info["src"] = "./icon/device/extnet.png"
            _net_info["device_name"] = "ext_net"
            global EXNET_NUM
            EXNET_NUM +=1
        else:
             _net_info["src"] = "./icon/device/network.png"
             _net_info["device_name"] = "network"
             global NET_NUM
             NET_NUM  +=1
        # _net_info["x"] = "%s" %(x+i*width)
        # _net_info["y"] = "%s" %(y + i*height)
        _net_info["width"] = "%s" %(70)
        _net_info["height"] = "%s" %(70)
        net_info.append(_net_info)
    return net_info


def _get_tuopu_servers_info(severs_info_detail):
    servers_list = []
    x = 120
    y = 123
    width = 100
    height = 100
    for i in range(len(severs_info_detail["servers"])):
        one_servers_info = {}
        one_servers_info["status"] = severs_info_detail["servers"][i]["status"]
        one_servers_info["task"] = "null"
        one_servers_info["console"] = "vnc"
        one_servers_info["name"] = severs_info_detail["servers"][i]["name"]
        one_servers_info["url"] = ""
        one_servers_info["id"] = severs_info_detail["servers"][i]["id"]
        one_servers_info["src"] = "./icon/device/server.png"
        one_servers_info["device_name"] = "server"
        # one_servers_info["x"] = "%s" %(x+i*width)
        # one_servers_info["y"] = "%s" %(y + i*height)
        one_servers_info["width"] = "%s" %(70)
        one_servers_info["height"] = "%s" %(70)
        global SERVER_NUM
        SERVER_NUM += 1
        servers_list.append(one_servers_info)
    return servers_list


def _get_subnet_detail(network_id, subnet_info):
    simple_subnet_info = []
    for i in range(len(subnet_info["subnets"])):
        _simple_subnet_info = {}
        if subnet_info["subnets"][i]["network_id"] == network_id:
            _simple_subnet_info["url"] = ""
            _simple_subnet_info["cidr"] = subnet_info["subnets"][i]["cidr"]
            _simple_subnet_info["id"] = subnet_info["subnets"][i]["id"]
            simple_subnet_info.append(_simple_subnet_info)
    return simple_subnet_info


def get_network_topology(token_id, tenant_id):
    """这里是获取拓扑信息"""
    tuopu_info = {}
    tuopu_port = _get_tuopu_port_info(token_id)
    tuopu_router = _get_tuopu_router_info(token_id)
    network_info = get_all_networks(token_id)
    subnet_info = get_tenant_subnets(token_id)
    tuopu_network = _get_tuopu_network_info(network_info, subnet_info)
    _servers_detail = get_tenant_instances(token_id, tenant_id)
    tuopu_server = _get_tuopu_servers_info(_servers_detail)
    tuopu_server += tuopu_router
    tuopu_server += tuopu_network
    tuopu_info['devices'] = tuopu_server
    tuopu_info['lines'] = tuopu_port
    return tuopu_info


def get_last_network_topology(token_id, tenant_id):
    global ROUTER_NUM
    global NET_NUM
    global EXNET_NUM
    global SERVER_NUM
    tuopu_info = get_network_topology(token_id,tenant_id)
    max_num = max(ROUTER_NUM,NET_NUM,EXNET_NUM,SERVER_NUM)
    # print max_num
    x = 100
    y = 60
    width = (max_num+1)*20
    height = 150
    router_num = 0
    server_nmu = 0
    net_exnet_num = 0
    for i in range(len(tuopu_info['devices'])):
        if tuopu_info['devices'][i]['src'].endswith("server.png"):
            tuopu_info['devices'][i]['x'] = x + server_nmu*width
            tuopu_info['devices'][i]['y'] = y
            server_nmu += 1
        if tuopu_info['devices'][i]['src'].endswith("router.png"):
            tuopu_info['devices'][i]['x'] = x + router_num*width
            tuopu_info['devices'][i]['y'] = y + height
            router_num += 1
        if tuopu_info['devices'][i]['src'].endswith("network.png") or tuopu_info['devices'][i]['src'].endswith("extnet.png"):
            tuopu_info['devices'][i]['x'] = x + net_exnet_num*width
            tuopu_info['devices'][i]['y'] = y + height*2
            net_exnet_num += 1
    ROUTER_NUM = 0
    NET_NUM = 0
    EXNET_NUM = 0
    SERVER_NUM = 0
    return tuopu_info

