# coding:utf-8
import time

def get_localtime():
    """获取当前时间"""
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    total_time = time.strftime(ISOTIMEFORMAT, time.localtime())
    return total_time


print get_localtime()