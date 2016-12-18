# _*_ coding:utf-8 _*_

from flask import Blueprint

monitor = Blueprint('monitor', __name__)

from . import views
