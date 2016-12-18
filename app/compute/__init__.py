# _*_ coding:utf-8 _*_

from flask import Blueprint

compute = Blueprint('compute', __name__)

from . import views



