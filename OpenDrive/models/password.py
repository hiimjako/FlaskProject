from flask import current_app

from sqlalchemy.sql import func

import os
import datetime

from OpenDrive.db import db


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
        # TODO: da cryptare
        self.password = password
        self.user_id = user_id

    def save(self):
        db.session.add(self)
        return db.session.commit()

    def __repr__(self):
        return f'<Password \'{self.site}\' \'{self.username}\'>'
