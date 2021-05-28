from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    current_app,
    make_response
)
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)

from OpenDrive import db, rq
from OpenDrive.account.forms import (
    ChangeEmailForm,
    ChangePasswordForm,
    CreatePasswordForm,
    LoginForm,
    RegistrationForm,
    RequestResetPasswordForm,
    ResetPasswordForm,
)
from OpenDrive.utils import symmetricEncrypt
from OpenDrive.models import User

account = Blueprint('account', __name__)


@account.route('/login', methods=['GET', 'POST'])
def login():
    """Log in an existing user."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.password_hash is not None and \
                user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            encryptedPass = symmetricEncrypt(form.password.data)
            flash('You are now logged in. Welcome back!', 'bg-primary')
            response = make_response(redirect(request.args.get('next') or url_for('main.index')))
            response.set_cookie('hash', encryptedPass, secure=current_app.config["SESSION_COOKIE_SECURE"], httponly=True)  # , samesite="Strict")
            return response
        else:
            flash('Invalid email or password.', 'bg-danger')
    return render_template('account/login.html', form=form)


@account.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'bg-danger')
    response = make_response(redirect(url_for('main.index')))
    response.set_cookie("hash", '', expires=0)
    return response


@account.route('/manage', methods=['GET', 'POST'])
@account.route('/manage/info', methods=['GET', 'POST'])
@login_required
def manage():
    """Display a user's account information."""
    return render_template('account/manage.html', user=current_user, form=None)


# @account.before_app_request
# def before_request():
#     """Force user to confirm email before accessing login-required routes."""
#     if current_user.is_authenticated \
#             and request.endpoint[:8] != 'account.' \
#             and request.endpoint != 'static':
#         return redirect(url_for('account.unconfirmed'))


# @account.route('/unconfirmed')
# def unconfirmed():
#     """Catch users with unconfirmed emails."""
#     if current_user.is_anonymous:
#         return redirect(url_for('main.index'))
#     return render_template('account/unconfirmed.html')
