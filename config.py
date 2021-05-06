from os import environ, path
import sys

basedir = path.abspath(path.dirname(__file__))


class Config:
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

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    FLASK_ENV = 'production'
    SQLALCHEMY_DATABASE_URI = 'mysql://user@localhost/foo'

    @classmethod
    def init_app(cls, app):
        print('THIS APP IS IN DEBUG MODE. \
                YOU SHOULD NOT SEE THIS IN PRODUCTION.')


class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    PORT = 10000
    DEBUG = True
    ASSETS_DEBUG = True

    @classmethod
    def init_app(cls, app):
        print('THIS APP IS IN DEBUG MODE. \
                YOU SHOULD NOT SEE THIS IN PRODUCTION.')


class TestingConfig(Config):
    TESTING = True

    @classmethod
    def init_app(cls, app):
        print('THIS APP IS IN DEBUG MODE. \
                YOU SHOULD NOT SEE THIS IN PRODUCTION.')


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
}
