# coding:utf-8


import time
import json

from osapi.sdnapi import StaticFlowPusher, Controller, BASE_URL


def get_localtime():
    """获取当前时间"""
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    total_time = time.strftime(ISOTIMEFORMAT, time.localtime())
    return total_time


if __name__ == "__main__":
    controller = Controller(BASE_URL)
    print json.dumps(controller.get_switches())
    staticflowpusher = StaticFlowPusher(BASE_URL)
    print json.dumps(staticflowpusher.get_flow("all"))
