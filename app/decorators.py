# _*_ coding:utf-8 _*_

from functools import wraps
from flask import session, redirect, url_for, make_response


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('log_user', None) is not None:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('auth.login'))
    return decorated_function


def allow_cross_domain(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        rst = make_response(fun(*args, **kwargs))
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        allow_headers = "Referer,Accept,Origin,User-Agent"
        rst.headers['Access-Control-Allow-Headers'] = allow_headers
        return rst
    return wrapper_fun
