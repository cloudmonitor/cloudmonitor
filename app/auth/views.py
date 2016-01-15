# _*_ coding:utf-8 _*_

from flask import render_template

from . import auth


@auth.route('/login', methods=['GET', 'POST'])
def login():
    pass