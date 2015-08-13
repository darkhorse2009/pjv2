from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.mysqldb import MySQL
from config import config
from flask_util_js import FlaskUtilJs


bootstrap = Bootstrap()
mysql = MySQL()
fujs = FlaskUtilJs()

#app initial
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    bootstrap.init_app(app)
    mysql.init_app(app)
    fujs.init_app(app)
    from .main import mainBlueprint
    app.register_blueprint(mainBlueprint)
    return app


