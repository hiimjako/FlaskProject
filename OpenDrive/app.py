import os
from db import db, migrate

from flask import Flask
from config import configDict
from flask_migrate import Migrate


def create_app(config='DevelopmentConfig'):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(configDict.get(config))

    db.init_app(app)
    migrate.init_app(app, db)
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app


if __name__ == "__main__":
    print('QUA 1')
    app = create_app()
    app.run()
