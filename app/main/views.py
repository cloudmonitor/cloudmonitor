# _*_ coding:utf-8 _*_

from flask import Flask


from . import main


@main.route('/')
def hello_world():
    return 'Hello World!'