from os import environ, path
import sys

basedir = path.abspath(path.dirname(__file__))

# Try better handling
if path.exists(".env"):
    for line in open(".env"):
        var = line.strip().split("=")
        if len(var) == 2:
            environ[var[0]] = var[1].replace("\"", "")


class Config:
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = False

    APP_NAME = "Open drive"
    UPLOAD_PATH = path.join(basedir, "upload")

    ENCRTYPTION_KEY = environ.get("ENCRTYPTION_KEY", default="secret")

    POSTGRES_USER = environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD = environ.get("POSTGRES_PASSWORD")
    POSTGRES_URL = environ.get("POSTGRES_URL", default="127.0.0.1")
    POSTGRES_PORT = environ.get("POSTGRES_PORT", default=5432)
    POSTGRES_DB = environ.get("POSTGRES_DB")

    RQ_DEFAULT_HOST = environ.get("RQ_DEFAULT_HOST", default="127.0.0.1")
    RQ_DEFAULT_PORT = environ.get("RQ_DEFAULT_PORT", default=6379)
    RQ_DEFAULT_PASSWORD = environ.get("RQ_DEFAULT_PASSWORD")
    RQ_DEFAULT_DB = environ.get("RQ_DEFAULT_DB")
    REDIS_URL = f'redis://:{RQ_DEFAULT_PASSWORD}@{RQ_DEFAULT_HOST}:{RQ_DEFAULT_PORT}/{RQ_DEFAULT_DB}'

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = environ.get("MAIL_USERNAME", default="opendrive.noreply@gmail.com")
    MAIL_PASSWORD = environ.get("MAIL_PASSWORD", default="ccvrbslplzykdjbm")

    SECRET_KEY = environ.get("SECRET_KEY", default="secret_key_pass")
    ADMIN_EMAIL = environ.get("ADMIN_EMAIL")
    ADMIN_PASSWORD = environ.get("ADMIN_PASSWORD")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_URL}:{POSTGRES_PORT}/{POSTGRES_DB}"

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    FLASK_ENV = "production"
    # SESSION_COOKIE_SECURE = True
    # SQLALCHEMY_DATABASE_URI = "mysql://user@localhost/foo"

    @classmethod
    def init_app(cls, app):
        print("PRODUCTION")


class DevelopmentConfig(Config):
    FLASK_ENV = "development"
    POSTGRES_URL = "127.0.0.1"
    RQ_DEFAULT_HOST = "127.0.0.1"
    REDIS_URL = f'redis://:{Config.RQ_DEFAULT_PASSWORD}@{RQ_DEFAULT_HOST}:{Config.RQ_DEFAULT_PORT}/{Config.RQ_DEFAULT_DB}'
    SQLALCHEMY_DATABASE_URI = f"postgresql://{Config.POSTGRES_USER}:{Config.POSTGRES_PASSWORD}@{POSTGRES_URL}:{Config.POSTGRES_PORT}/{Config.POSTGRES_DB}"
    DEBUG = True

    @classmethod
    def init_app(cls, app):
        print("THIS APP IS IN DEBUG MODE. \
                YOU SHOULD NOT SEE THIS IN PRODUCTION.")


class TestingConfig(Config):
    TESTING = True

    @classmethod
    def init_app(cls, app):
        print("THIS APP IS IN DEBUG MODE. \
                YOU SHOULD NOT SEE THIS IN PRODUCTION.")


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
