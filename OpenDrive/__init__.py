import os

from flask import Flask
# from flask_assets import Environment
# from flask_compress import Compress
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_mobility import Mobility
from OpenDrive.db import db, migrate, rq

from config import config as Config

basedir = os.path.abspath(os.path.dirname(__file__))

csrf = CSRFProtect()
# compress = Compress()

# Set up Flask-Login
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'account.login'


def create_app(config):
    app = Flask(__name__,
                static_url_path='/static')

    config_name = config
    if not isinstance(config, str):
        config_name = os.environ.get("FLASK_ENV", default="development")

    app.config.from_object(Config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # not using sqlalchemy event system, hence disabling it
    Config[config_name].init_app(app)

    # Set up extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    Mobility(app)
    # compress.init_app(app)
    rq.init_app(app)
    rq.redis_url = Config[config_name].REDIS_URL

    # Register Jinja template functions
    from .utils import register_template_utils
    register_template_utils(app)

    # Set up asset pipeline
    # assets_env = Environment(app)
    # dirs = ['assets/styles', 'assets/scripts']
    # for path in dirs:
    #     assets_env.append_path(os.path.join(basedir, path))
    # assets_env.url_expire = True

    # assets_env.register('app_css', app_css)
    # assets_env.register('app_js', app_js)
    # assets_env.register('vendor_css', vendor_css)
    # assets_env.register('vendor_js', vendor_js)

    # Configure SSL if platform supports it
    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        pass
        # TODO: da abilitare quando avrò i certificati
        # from flask_sslify import SSLify
        # SSLify(app)

        # Create app blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .account import account as account_blueprint
    app.register_blueprint(account_blueprint, url_prefix='/account')

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .drive import drive as drive_blueprint
    app.register_blueprint(drive_blueprint, url_prefix='/drive')

    from .password import password as password_blueprint
    app.register_blueprint(password_blueprint, url_prefix='/password')

    return app
