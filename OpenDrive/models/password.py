from flask import current_app

from sqlalchemy.sql import func

from OpenDrive.db import db
from OpenDrive.utils import symmetric_encrypt


class Password(db.Model):
    __tablename__ = 'passwords'
    id = db.Column(db.Integer, primary_key=True)
    site = db.Column(db.String(255), index=True)
    username = db.Column(db.String(255), index=True)
    password = db.Column(db.String(255), index=True)
    insert_at = db.Column(db.DateTime(timezone=False),
                          server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=False), onupdate=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, site, username, password, user_id):
        self.site = site
        self.username = username
        self.password = password
        self.user_id = user_id

    def save(self, key: None):
        self.password = symmetric_encrypt(self.password, key)
        db.session.add(self)
        return db.session.commit()

    def __repr__(self):
        return f'<Password \'{self.site}\' \'{self.username}\'>'

    @property
    def serialized(self):
        """Return object data in serializeable format"""
        return {
            'site': self.site,
            'username': self.username,
            'password': self.password,
            'user_id': self.user_id
        }