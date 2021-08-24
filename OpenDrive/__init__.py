"""init for OpenDrive project"""
import os
import click

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf import CSRFProtect
from flask_mobility import Mobility
from redis import Redis
from rq import Connection, Queue, Worker
from config import config as Config
from OpenDrive.db import db, migrate, rq
from OpenDrive.models import AnonymousUser, User, Role

# blueprints
from .utils import register_template_utils
from .main import main as main_blueprint
from .account import account as account_blueprint
from .admin import admin as admin_blueprint
from .drive import drive as drive_blueprint
from .password import password as password_blueprint


basedir = os.path.abspath(os.path.dirname(__file__))

csrf = CSRFProtect()
mail = Mail()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'account.login'
login_manager.anonymous_user = AnonymousUser
@login_manager.user_loader
def load_user(user_id):
    """Retrives the user from the id saved into cookie"""
    return User.query.get(int(user_id))

def create_app(config):
    """Creates the main flask app"""
    app = Flask(__name__, static_url_path='/static')

    config_name = config
    if not isinstance(config, str):
        config_name = os.environ.get("FLASK_ENV", default="development")

    app.config.from_object(Config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    Config[config_name].init_app(app)

    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    Mobility(app)
    rq.init_app(app)
    rq.redis_url = Config[config_name].REDIS_URL

    create_cli(app)

    # Register Jinja template functions
    register_template_utils(app)

    # Blueprints
    app.register_blueprint(main_blueprint)
    app.register_blueprint(account_blueprint, url_prefix='/account')
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    app.register_blueprint(drive_blueprint, url_prefix='/drive')
    app.register_blueprint(password_blueprint, url_prefix='/password')

    return app

def create_cli(app):
    """Custom commands for flask cli"""
    if app:
        @app.cli.command("setup_dev")
        def setup_dev():
            Role.insert_roles()
            admin_query = Role.query.filter_by(name='Administrator')
            if admin_query.first() is not None:
                if User.query.filter_by(email=app.config["ADMIN_EMAIL"]).first() is None:
                    user = User(
                        first_name='Admin',
                        last_name='Account',
                        password=app.config["ADMIN_PASSWORD"],
                        email=app.config["ADMIN_EMAIL"])
                    db.session.add(user)
                    db.session.commit()
                    print('Added administrator {}'.format(user.full_name()))

        @app.cli.command("run_worker")
        @click.argument('config')
        def run_worker(config):
            """Initializes a slim rq task queue."""

            if not isinstance(config, str):
                config = "development"

            app.config.from_object(Config[config])
            app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

            listen_queue = ['default', 'cryptography', 'email']
            conn = Redis(
                host=app.config["RQ_DEFAULT_HOST"],
                port=app.config["RQ_DEFAULT_PORT"],
                db=app.config["RQ_DEFAULT_DB"],
                password=app.config["RQ_DEFAULT_PASSWORD"])

            with Connection(conn):
                worker = Worker(map(Queue, listen_queue))
                worker.work()
