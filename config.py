from os import environ, path

basedir = path.abspath(path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    FLASK_ENV = 'production'
    DATABASE_URI = 'mysql://user@localhost/foo'


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
