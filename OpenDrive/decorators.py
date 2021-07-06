from functools import wraps

from flask import abort, flash, redirect, request, url_for
from flask_login import current_user

from OpenDrive.models import Permission
from OpenDrive.utils import symmetricDecrypt


def permission_required(permission):
    '''Check if the current user has the requested permissions'''
    def decorator(f):
        '''Decorator'''
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)


def get_hash_cookie_required(f):
    '''adds a cookie_hash param to current_user'''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        '''Decorator'''
        cookie_hash = request.cookies.get('hash')
        if not cookie_hash:
            flash('An error occured, try to login again', 'bg-danger')
            return redirect(url_for('account.logout'))
        token = symmetricDecrypt(cookie_hash)
        if not current_user.verify_password(token):
            flash('Invalid cookie, relog to refresh', 'bg-danger')
            return redirect(url_for('account.logout'))
        current_user.cookie_hash = token
        return f(*args, **kwargs)
    return decorated_function
