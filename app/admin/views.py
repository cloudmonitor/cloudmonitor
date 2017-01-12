# _*_ coding:utf-8 _*_

from flask import request
import json

from osapi import auth_is_available, get_admin_token
from osapi.admin import *

from . import admin


@admin.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    token_json = get_admin_token(username, password)
    return json.dumps(token_json)

