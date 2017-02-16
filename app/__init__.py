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
    app.config["UPLOAD_FOLDER"] = "upload/"
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/v1.0/auth")

    from .monitor import monitor as monitor_blueprint
    app.register_blueprint(monitor_blueprint, url_prefix="/v1.0/monitor")

    from .sdn import sdn as sdn_blueprint
    app.register_blueprint(sdn_blueprint, url_prefix="/v1.0/sdn")

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix="/v1.0/admin")

    return app

