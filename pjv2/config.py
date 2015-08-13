import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_PATH_LTE = 'app/upload/lte/'
    UPLOAD_PATH_CDMA = 'app/upload/cdma/'
    UPLOAD_PATH_CSV = 'app/upload/csv/'
    CSRF_ENABLED = True

class DevelopmentConfig(Config):
    # DEBUG = True
    MYSQL_DB = 'data_dev'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'fangww'
    MYSQL_PORT = 3365


class TestingConfig(Config):
    TESTING = True
    MYSQL_DB = 'data_test'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'fangww'
    MYSQL_PORT = 3365


class ProductionConfig(Config):
    MYSQL_DB = 'data_production'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'fangww'
    MYSQL_PORT = 3365


class LteData(Config):
    MYSQL_DB = 'data_lte'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'fangww'
    MYSQL_PORT = 3365

class DevConfig(Config):
    MYSQL_DB = 'data_dev'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'fangww'
    MYSQL_PORT = 3365

config = {
    'development' : DevelopmentConfig,
    'testing' : TestingConfig,
    'production' : ProductionConfig,
    'default' : DevelopmentConfig,
    'ltedata' : LteData,
    'dev' :DevConfig
}