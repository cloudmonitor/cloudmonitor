# _*_ coding:utf-8 _*_

from settings import *


def get_tenant_firewall_rules(token_id):
    """ 获取所有的rule的信息"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + '/fw/firewall_rules'
    r = requests.get(url=url, headers=headers)
    return r.json()


def get_tenant_firewall_rule(token_id, rule_id):
    """ 获取某一的rule的信息"""
    headers = {"X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + '/fw/firewall_rules/'+rule_id
    r = requests.get(url=url, headers= headers)
    return r.json()


def get_tenant_firewall_policies(token_id):
    """获取所有的policys的信息"""
    headers = {"X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + '/fw/firewall_policies'
    r = requests.get(url=url, headers=headers)
    return r.json()


def get_tenant_firewall_policy(token_id, policies_id):
    """获取某一个policy的信息"""
    headers = {"X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + '/fw/firewall_policies/'+policies_id
    r = requests.get(url=url, headers=headers)
    return r.json()


def get_tenant_firewalls(token_id):
    """获取所有的Firewalls信息"""
    headers = {"X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + '/fw/firewalls'
    r = requests.get(url=url, headers=headers)
    return r.json()


def get_tenant_firewall(token_id, firewalls_id):
    """获取某一具体Firewalls的信息"""
    headers = {"X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + '/fw/firewalls/'+firewalls_id
    r = requests.get(url=url, headers=headers)
    firewall_info = r.json()
    print firewall_info
    policy_id = firewall_info['firewall']['firewall_policy_id']
    print policy_id
    policy_all_info = get_tenant_firewall_policies(token_id)
    for item in policy_all_info['firewall_policies']:
        if policy_id == item['id']:
            rule_id = item['firewall_rules']
    for firewall_rule_id in rule_id:
        rule_info = get_tenant_firewall_rule(token_id, firewall_rule_id)
    # print rule_info
    return rule_info


def create_firewall_rule(token_id, rule):
    """创建防火墙规则"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + '/fw/firewall_rules'
    r = requests.post(url=url, data=json.dumps(rule), headers=headers)
    return r.json()


def delete_firewall_rule(token_id, rule_id_list):
    """删除防火墙规则"""
    delete_status = {}
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    for i in range(len(rule_id_list["firewall_rule_ids"])):
        url = NEUTRON_ENDPOINT + '/fw/firewall_rules/' + rule_id_list["firewall_rule_ids"][i]
        r = requests.delete(url=url, headers=headers)
        delete_status[rule_id_list["firewall_rule_ids"][i]] = r.status_code
    return delete_status


def update_firewall_rule(token_id, rule, fw_rule_id):
    """更新防火墙规则"""
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    url = NEUTRON_ENDPOINT + '/fw/firewall_rules/' + fw_rule_id
    r = requests.put(url=url, data=rule, headers=headers)
    print r.json()
    return r.json()

