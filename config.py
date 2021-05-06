from os import environ, path

basedir = path.abspath(path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    POSTGRES_USER = environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD = environ.get("POSTGRES_PASSWORD")
    POSTGRES_URL = environ.get("POSTGRES_URL")
    POSTGRES_PORT = environ.get("POSTGRES_PORT")
    POSTGRES_DB = environ.get("POSTGRES_DB")
    SECRET_KEY = environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_URL}:{POSTGRES_PORT}/{POSTGRES_DB}'


class ProductionConfig(Config):
    FLASK_ENV = 'production'
    SQLALCHEMY_DATABASE_URI = 'mysql://user@localhost/foo'


class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    PORT = 10000
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


configDict = {
    'DevelopmentConfig': DevelopmentConfig,
    'ProductionConfig': ProductionConfig,
    'TestingConfig': TestingConfig,
}
