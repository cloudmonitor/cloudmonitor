# _*_ coding:utf-8 _*_

from flask import Flask
from flask.ext.login import login_required


from . import main


@main.route('/')
@login_required
def index():
    return 'Hello World!'