#!/usr/bin/env python
import os
import subprocess

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell, Server
from redis import Redis
from rq import Connection, Queue, Worker

from OpenDrive import create_app, db
from OpenDrive.models import Role, User
from config import Config

app = create_app(os.getenv('APP_SETTINGS') or 'development')
manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host="0.0.0.0"))


@manager.command
def test():
    """Run the unit tests."""
    import unittest

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def setup_dev():
    """Runs the set-up needed for local development."""
    setup_general()


# @manager.command
# def setup_prod():
#     """Runs the set-up needed for production."""
#     setup_general()


def setup_general():
    """Runs the set-up needed for both local development and production.
       Also sets up first admin user."""
    Role.insert_roles()
    admin_query = Role.query.filter_by(name='Administrator')
    if admin_query.first() is not None:
        if User.query.filter_by(email=Config.ADMIN_EMAIL).first() is None:
            user = User(
                first_name='Admin',
                last_name='Account',
                password=Config.ADMIN_PASSWORD,
                confirmed=True,
                email=Config.ADMIN_EMAIL)
            db.session.add(user)
            db.session.commit()
            print('Added administrator {}'.format(user.full_name()))


@manager.command
def run_worker():
    """Initializes a slim rq task queue."""
    listenQueue = ['default', 'cryptography']
    conn = Redis(
        host=Config.RQ_DEFAULT_HOST,
        port=Config.RQ_DEFAULT_PORT,
        db=Config.RQ_DEFAULT_DB,
        password=Config.RQ_DEFAULT_PASSWORD)

    with Connection(conn):
        worker = Worker(map(Queue, listenQueue))
        worker.work()


@manager.command
def format():
    """Runs the yapf and isort formatters over the project."""
    isort = 'isort -rc *.py app/'
    yapf = 'yapf -r -i *.py app/'

    print('Running {}'.format(isort))
    subprocess.call(isort, shell=True)

    print('Running {}'.format(yapf))
    subprocess.call(yapf, shell=True)


if __name__ == '__main__':
    manager.run()