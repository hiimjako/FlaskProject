from flask import url_for, current_app as app
from wtforms.fields import Field
from wtforms.widgets import HiddenInput
from wtforms.compat import text_type
from cryptography.fernet import Fernet, InvalidToken
import base64
import hashlib


def register_template_utils(app):
    """Register Jinja 2 helpers (called from __init__.py)."""

    @app.template_test()
    def equalto(value, other):
        return value == other

    @app.template_global()
    def is_hidden_field(field):
        from wtforms.fields import HiddenField
        return isinstance(field, HiddenField)

    app.add_template_global(index_for_role)


def index_for_role(role):
    return url_for(role.index)


def symmetricDecrypt(psw: str, key=None):
    if key is None:
        try:
            key = app.config['ENCRTYPTION_KEY']
        except:
            with app.app_context():
                key = app.config['ENCRTYPTION_KEY']

    keyHex = hashlib.md5(str.encode(key)).hexdigest()
    key = base64.urlsafe_b64encode(keyHex.encode())
    f = Fernet(key)
    try:
        decrypted_data = f.decrypt(str.encode(psw))
    except InvalidToken:
        return "Invalid key"
    return decrypted_data.decode("utf-8")


def symmetricEncrypt(psw: str,  key=None):
    if key is None:
        try:
            key = app.config['ENCRTYPTION_KEY']
        except:
            with app.app_context():
                key = app.config['ENCRTYPTION_KEY']

    keyHex = hashlib.md5(str.encode(key)).hexdigest()
    key = base64.urlsafe_b64encode(keyHex.encode())
    f = Fernet(key)
    try:
        encrypted_data = f.encrypt(str.encode(psw))
    except InvalidToken:
        return "Invalid key"
    return encrypted_data.decode("utf-8")


def symmetricDecryptFile(path: str, key=None):
    if key is None:
        try:
            key = app.config['ENCRTYPTION_KEY']
        except:
            with app.app_context():
                key = app.config['ENCRTYPTION_KEY']

    keyHex = hashlib.md5(str.encode(key)).hexdigest()
    key = base64.urlsafe_b64encode(keyHex.encode())
    f = Fernet(key)

    with open(path, "rb") as file:
        encrypted_data = file.read()
    try:
        decrypted_data = f.decrypt(encrypted_data)
    except InvalidToken:
        return bytes()

    return decrypted_data


def symmetricEncryptFile(path: str,  key=None):
    if key is None:
        try:
            key = app.config['ENCRTYPTION_KEY']
        except:
            with app.app_context():
                key = app.config['ENCRTYPTION_KEY']

    keyHex = hashlib.md5(str.encode(key)).hexdigest()
    key = base64.urlsafe_b64encode(keyHex.encode())
    f = Fernet(key)

    with open(path, "rb") as file:
        file_data = file.read()

    try:
        encrypted_data = f.encrypt(file_data)
    except InvalidToken:
        return bytes()

    with open(path, "wb") as file:
        file.write(encrypted_data)
