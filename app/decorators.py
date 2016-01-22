# _*_ coding:utf-8 _*_

from functools import wraps
from flask import session, redirect, url_for


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('log_user', None) is not None:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('auth.login'))
    return decorated_function
