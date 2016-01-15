# _*_ coding:utf-8 _*_

from flask import render_template, request, redirect, url_for
from flask.ext.login import login_user, logout_user, login_required, current_user

from . import auth
from .forms import LoginFrom
from ..models import User, USER
from collect.monitor import get_token


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginFrom()
    if form.validate_on_submit():
        attrdict = get_token('', form.username.data, form.password.data)
        if attrdict is not None:
            user = User(attrdict)
            login_user(user)
            print user.id, user.token_id
            return redirect(request.args.get('next') or url_for('main.index'))
    return render_template('auth/login.html', form=form)
