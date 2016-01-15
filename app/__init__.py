# _*_ coding:utf-8 _*_


from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.bootstrap import Bootstrap

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message = None
bootstrap = Bootstrap()



def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "try to guess"
    login_manager.init_app(app)
    bootstrap.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app