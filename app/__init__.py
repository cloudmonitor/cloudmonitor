# _*_ coding:utf-8 _*_


from flask import Flask
# from flask.ext.login import LoginManager
# from flask.ext.bootstrap import Bootstrap
from flask.ext.cors import CORS

# login_manager = LoginManager()
# login_manager.session_protection = 'strong'
# login_manager.login_view = 'auth.login'
# login_manager.login_message = None
cors = CORS()


def create_app():
    app = Flask(__name__)
    # app.config["SECRET_KEY"] = "try to guess"
    # login_manager.init_app(app)
    cors.init_app(app)

    print app.root_path

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
