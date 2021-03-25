import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD= 'app/upload/'
    DOWNLOAD= 'app/download/'
    # UPLOAD_CDMA = 'app/upload/cdma/'
    # UPLOAD_CSV = 'app/upload/csv/'
    CSRF_ENABLED = True
    MAIL_SERVER = 'smtp.163.com'
    MAIL_SENDER = 'fangww_uestc@163.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or ''
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or ''

class TestingConfig(Config):
    MONGO_URL = 'mongodb://localhost:27017/'
    MONGO_DB = 'data_test'


config = {
        'testing': TestingConfig,
        'default': TestingConfig
        }
