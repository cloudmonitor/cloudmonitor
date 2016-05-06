# _*_ coding:utf-8 _*_

from settings import *


def get_localtime():
    """获取当前时间"""
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    total_time = time.strftime(ISOTIMEFORMAT, time.localtime())
    return total_time


def time_to_isostring(s):
    """把一个时间转换成秒"""
    d = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
    return time.mktime(d.timetuple())


def isostring_to_time(s):
    """把秒数转换成一个时间"""
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(s)))


def get_meter_func_data(token_id, instance_id, meter_name, type):
    resource_id = get_instance_resource_id(token_id, instance_id, meter_name)
    func_name = "get_list_meter_"+type
    # print func_name
    return eval(func_name)(token_id, meter_name, resource_id)


def get_instance_resource_id(token_id, instance_id, meter_name):
    headers = {"Content-type": "application/json", "X-Auth-Token": token_id, "Accept": "application/json"}
    r = requests.get(CEILOMETER_ENDPOINT+'/resources', headers=headers)
    for resource in r.json():
        if meter_name.startswith("network."):
            if resource['metadata'].has_key('vnic_name'):
                regex = instance_id + '-' + resource['metadata']['vnic_name']
                if resource['resource_id'].endswith(regex):
                    return resource['resource_id']
        else:
            if resource['resource_id'] == instance_id:
                return resource['resource_id']


def localtime_to_utc(s):
    seconds = int(time_to_isostring(s))-28800
    return isostring_to_time(seconds)


def get_one_meter(token_id, time, meter_name ,resource_id ):
    """根据时间来删选数据"""
    time_reduce = isostring_to_time(time_to_isostring(time)-60)
    headers = {"X-Auth-Token":token_id, "Accept": "application/json"}
    url = CEILOMETER_ENDPOINT + '/meters/'+meter_name+'/?'
    # print url
    url_list = [url, ]
    payload = {"q": [{"field": "timestamp", "op": "gt", "value": time_reduce},
                     {"field": "timestamp", "op": "lt", "value": time},
                     {"field": "resource_id","value": resource_id}
                    ]}
    for key, value in payload.items():
        if isinstance(value, list):
            for val in value:
                for k1, v1 in val.items():
                    url_list.append(key+'.'+k1+'='+v1+'&')
        else:
            url_list.append(key+'='+str(value)+'&')
    url_list.append("limit=1")
    # print url_list
    url = ''.join(url_list)
    r = requests.get(url, headers=headers)
    return r.json()


def get_list_meter_minute(token_id, meter_name, resource_id):
    """以分钟得到某一组数据"""
    localtime = localtime_to_utc(get_localtime())
    meter_info_list = []
    for i in range(0, 7):
        r = get_one_meter(token_id, localtime, meter_name, resource_id)
        # print r
        if len(r) == 0:
            meter_info_list.append(r)
        else:
            meter_info_list.append(r[0])
        localtime = isostring_to_time(time_to_isostring(localtime)-180)
    r = {meter_name:meter_info_list}

    return r


def get_list_meter_hour(token_id,meter_name, resource_id):
    """以小时得到某一组数据"""
    localtime = localtime_to_utc(get_localtime())
    meter_info_list = []
    for i in range(0, 7):
        r = get_one_meter(token_id, localtime, meter_name, resource_id)
        if len(r) == 0:
            meter_info_list.append(r)
        else:
            meter_info_list.append(r[0])
        localtime01 = datetime.datetime.strptime(localtime,"%Y-%m-%d %H:%M:%S")
        times = localtime01 + datetime.timedelta(hours=-1)
        localtime = datetime.datetime.strftime(times, "%Y-%m-%d %H:%M:%S")
    r = {meter_name:meter_info_list}
    return r


def get_list_meter_day(token_id,meter_name, resource_id):
    """以天得到某一组数据"""
    localtime = localtime_to_utc(get_localtime())
    meter_info_list = []
    for i in range(0, 7):
        r = get_one_meter(token_id, localtime, meter_name, resource_id)
        if len(r) == 0:
            meter_info_list.append(r)
        else:
            meter_info_list.append(r[0])
        print localtime
        localtime01 = datetime.datetime.strptime(localtime,"%Y-%m-%d %H:%M:%S")
        times = localtime01 + datetime.timedelta(days=-1)
        localtime = datetime.datetime.strftime(times, "%Y-%m-%d %H:%M:%S")
        #print localtime
    r = {meter_name:meter_info_list}
    return r