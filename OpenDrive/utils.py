"""Utils file, with common function"""
import base64
import hashlib

from cryptography.fernet import Fernet, InvalidToken
from flask import current_app as app
from flask import url_for
from flask.helpers import flash


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
    """Page index based on role"""
    return url_for(role.index)


def symmetric_decrypt(psw: str, key=None):
    """symmetric Decryption"""
    if key is None:
        try:
            key = app.config['ENCRTYPTION_KEY']
        except Exception:
            with app.app_context():
                key = app.config['ENCRTYPTION_KEY']

    key_hex = hashlib.md5(str.encode(key)).hexdigest()
    key = base64.urlsafe_b64encode(key_hex.encode())
    fernet_key = Fernet(key)
    try:
        decrypted_data = fernet_key.decrypt(str.encode(psw))
    except InvalidToken:
        return "Invalid key"
    return decrypted_data.decode("utf-8")


def symmetric_encrypt(psw: str,  key=None):
    """symmetric Encrypt"""
    if key is None:
        try:
            key = app.config['ENCRTYPTION_KEY']
        except Exception:
            with app.app_context():
                key = app.config['ENCRTYPTION_KEY']

    key_hex = hashlib.md5(str.encode(key)).hexdigest()
    key = base64.urlsafe_b64encode(key_hex.encode())
    fernet_key = Fernet(key)
    try:
        encrypted_data = fernet_key.encrypt(str.encode(psw))
    except InvalidToken:
        return "Invalid key"
    return encrypted_data.decode("utf-8")


def symmetric_decrypt_file(path: str, key=None):
    """symmetric Decrypt File for files"""
    if key is None:
        try:
            key = app.config['ENCRTYPTION_KEY']
        except Exception:
            with app.app_context():
                key = app.config['ENCRTYPTION_KEY']

    key_hex = hashlib.md5(str.encode(key)).hexdigest()
    key = base64.urlsafe_b64encode(key_hex.encode())
    fernet_key = Fernet(key)

    with open(path, "rb") as file:
        encrypted_data = file.read()
    try:
        decrypted_data = fernet_key.decrypt(encrypted_data)
    except InvalidToken:
        return bytes()

    return decrypted_data


def symmetric_encrypt_file(path: str,  key=None):
    """symmetric Ecrypt File for files"""
    if key is None:
        try:
            key = app.config['ENCRTYPTION_KEY']
        except Exception:
            with app.app_context():
                key = app.config['ENCRTYPTION_KEY']

    key_hex = hashlib.md5(str.encode(key)).hexdigest()
    key = base64.urlsafe_b64encode(key_hex.encode())
    fernet_key = Fernet(key)

    with open(path, "rb") as file:
        file_data = file.read()

    try:
        encrypted_data = fernet_key.encrypt(file_data)
    except InvalidToken:
        return bytes()

    with open(path, "wb") as file:
        file.write(encrypted_data)

def render_errors(form_errors):
    """Renders all form errors as flashes"""
    for error in form_errors:
        err = form_errors[error]
        if len(err) > 0:
            flash(form_errors[error][0], 'bg-danger')

def format_path(path):
    """Function that standardize a path for the application"""
    if not isinstance(path, str):
        path = "/"
    if not path.startswith("/"):
        path  = "/" + path
    if  not path.startswith("/h"):
        path  = "/h" + path
    if path[len(path )-1] != "/":
        path  = path  + "/"
    path = path.lower()
    return path
