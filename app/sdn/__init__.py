# _*_ coding:utf-8 _*_

from flask import Blueprint

sdn = Blueprint('sdn', __name__)

from . import views
