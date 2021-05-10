from flask import current_app
from flask_login import AnonymousUserMixin, UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import os

from .. import db, login_manager

import enum

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


# class extensionEnum(enum.Enum):
#     txt = 'txt'
#     pdf = 'pdf'
#     png = 'png'
#     jpg = 'jpg'
#     jpeg = 'jpeg'
#     gif = 'gif'


class File(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(64), index=True)
    # extension = db.Column(Enum(extensionEnum))
    path = db.Column(db.String(255), unique=True)
    insert_at = db.Column(db.DateTime(timezone=False))
    updated_at = db.Column(db.DateTime(timezone=False))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, filename, user_id):
        self.filename = secure_filename(filename)
        self.path = f'{UPLOAD_FOLDER}'
        self.user_id = user_id

    def __repr__(self):
        return f'<File \'{self.filename}\'>'
