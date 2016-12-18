# _*_ coding:utf-8 _*_

from flask import Blueprint

info = Blueprint('info', __name__)

from . import views

