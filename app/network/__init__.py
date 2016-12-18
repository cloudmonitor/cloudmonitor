# _*_ coding:utf-8 _*_

from flask import Blueprint

network = Blueprint('network', __name__)

from . import views


