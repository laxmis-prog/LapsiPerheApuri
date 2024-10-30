import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
        ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    print("MAIL_USERNAME: "+MAIL_USERNAME)
    SOVELLUSMALLI_MAIL_SUBJECT_PREFIX = '[Flasky]'
    SOVELLUSMALLI_MAIL_SENDER = 'Sovellusmalli Admin <flasky@example.com>'
    SOVELLUSMALLI_ADMIN = os.environ.get('FLASKY_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class XamppConfig(Config):
    DEBUG = True
    DB_USERNAME= os.environ.get('DB_USERNAME') or 'root'
    DB_PASSWORD= os.environ.get('DB_PASSWORD') or ''
    DB_HOST= os.environ.get('DB_HOST') or 'localhost'
    DB_PORT= os.environ.get('DB_PORT') or '3306'
    DB_NAME= os.environ.get('DB_NAME') or 'flasky'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://'+DB_USERNAME+':'+DB_PASSWORD+'@'+DB_HOST+':'+DB_PORT+'/'+DB_NAME
    print("SQLALCHEMY_DATABASE_URI: "+SQLALCHEMY_DATABASE_URI)

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'xampp': XamppConfig,

    'default': DevelopmentConfig
}