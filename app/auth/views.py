# _*_ coding:utf-8 _*_

from flask import render_template, request, redirect, url_for, current_app, session
# from flask.ext.login import login_user, logout_user, login_required, current_user

from . import auth
from .forms import LoginFrom
from ..models import User
from collect.monitor import get_user_token


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginFrom()
    if form.validate_on_submit():
        token_json = get_user_token(form.username.data, form.password.data)
        if token_json is not None:
            user = User(token_json)
            session['log_pwd'] = form.password.data
            session['log_user'] = user.to_json()
            return redirect(request.args.get('next') or url_for('main.index'))
    return render_template('auth/login.html', form=form)
