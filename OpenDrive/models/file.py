import posixpath
import uuid
import mimetypes
import os
import re

from sqlalchemy.sql import func
from flask import current_app
from OpenDrive.db import db
from OpenDrive.utils import format_path, symmetric_encrypt_file

class File(db.Model):
    """File model"""
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), index=True)
    # extension = db.Column(Enum(extensionEnum))
    path = db.Column(db.String(512), unique=True)
    folder = db.Column(db.String(512))
    # bytes
    size = db.Column(db.Integer, default=0)
    insert_at = db.Column(db.DateTime(timezone=False), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=False), onupdate=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

    def __init__(self, file, folder, user_id):
        # self.filename = secure_filename(file.filename)
        if file:
            self.filename = os.path.splitext(file.filename)[0] + os.path.splitext(file.filename)[1].lower()
            base_path = current_app.config['UPLOAD_PATH']
            if not os.path.exists(base_path):
                os.makedirs(base_path)
            self.path = os.path.join(base_path, str(uuid.uuid4()))

            try:
                file.save(self.path)
                self.size = os.stat(self.path).st_size
            except Exception:
                # FIXME: da mettere token sbagliato
                # Oppure os error
                print("file non caricato")
                
        self.update_folder_secure(folder)
        self.user_id = user_id

    def save(self, key: None):
        db.session.add(self)
        if self.path:
            symmetric_encrypt_file(self.path, key)
        return db.session.commit()
   
    def hard_delete(self):
        """Deletes record and the file in HDD"""
        if self.path:
            os.remove(self.path)
        db.session.delete(self)
        return db.session.commit()

    def __repr__(self):
        return f'<File \'{self.filename}\'>'

    def getFilePath(self):
        path = None
        if os.path.isfile(self.path):
            path = self.path
        elif os.path.isfile(os.path.join(current_app.config['UPLOAD_PATH'], self.filename)):
            path = os.path.join(current_app.config['UPLOAD_PATH'], self.filename)
        return path

    def getImageUrl(self):
        return "/drive/" + posixpath.join('file', str(self.id))

    def getFolderUrl(self, path = None):
        return  "/drive/" + posixpath.join(path, self.getFolderName(path))

    def getFolderName(self, path = None):
        if path is None:
            return os.path.basename(self.folder)
        return re.search(r"^(.*?)(?=\/)",  self.folder.replace(path, "", 1)).group(1)

    def getMimeType(self):
        return mimetypes.MimeTypes().guess_type(self.filename)[0] or "application/octet-stream"

    def update_folder_secure(self, folder):
        self.folder = format_path(folder)
    
    def get_printable_folder(self):
        return self.folder.replace("/h", "", 1)