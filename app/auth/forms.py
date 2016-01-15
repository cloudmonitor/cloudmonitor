# _*_ coding:utf-8 _*_

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

import sys
reload(sys)
sys.setdefaultencoding('utf8')


class LoginFrom(Form):
    username = StringField('用户名', validators=[DataRequired(), Length(1,64)])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('登录')


