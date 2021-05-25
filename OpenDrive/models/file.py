from flask import current_app
from werkzeug.utils import secure_filename
import urllib.parse
import posixpath

from sqlalchemy.sql import func

import os
import datetime

from OpenDrive.db import db, rq
from OpenDrive.jobs.cryptography import add as queue
from OpenDrive.utils import symmetricEncryptFile

import enum
import uuid

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


# class extensionEnum(enum.Enum):
#     txt = 'txt'
#     pdf = 'pdf'
#     png = 'png'
#     jpg = 'jpg'
#     jpeg = 'jpeg'
#     gif = 'gif'

def test():
    print('funzione passata')


class File(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), index=True)
    # extension = db.Column(Enum(extensionEnum))
    path = db.Column(db.String(512), unique=True)
    insert_at = db.Column(db.DateTime(timezone=False),
                          server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=False), onupdate=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, file, user_id):
        self.filename = secure_filename(file.filename)

        basePath = current_app.config['UPLOAD_PATH']
        if not os.path.exists(basePath):
            os.makedirs(basePath)
        self.path = os.path.join(basePath, str(uuid.uuid4()))

        try:
            file.save(self.path)
        except:
            print("file non caricato")

        self.user_id = user_id

    def save(self, key: None):
        db.session.add(self)
        # rq.get_queue('cryptography').enqueue(
        #     test,
        #     arg1='ciao'
        # )
        symmetricEncryptFile(self.path, key)
        return db.session.commit()

    def __repr__(self):
        return f'<File \'{self.filename}\'>'

    def getImageUrl(self):
        # return urllib.parse.urljoin(current_app.config['APP_URL'], posixpath.join('drive', 'file', str(self.id)))
        return posixpath.join('file', str(self.id))
