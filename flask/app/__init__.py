from flask import Flask
from flask.ext.bootstrap import Bootstrap
from config import config
from flask_util_js import FlaskUtilJs
from flask.ext.mail import Mail

bootstrap = Bootstrap()
fujs = FlaskUtilJs()
mail = Mail()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    bootstrap.init_app(app)
    fujs.init_app(app)
    mail.init_app(app)

    from .main import mainBlueprint
    app.register_blueprint(mainBlueprint)
    return app
