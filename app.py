from os import environ
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import configDict

app = Flask(__name__)
app.config.from_object(configDict.get(environ.get('FLASK_CONFIG', default='DevelopmentConfig')))

db = SQLAlchemy()
db.init_app(app)


# @app.before_first_request
# def create_tables():
#     db.create_all()


@ app.route('/')
def hello_world():
    print(app.config)
    return render_template('base.html')


if __name__ == "__main__":
    app.run()
