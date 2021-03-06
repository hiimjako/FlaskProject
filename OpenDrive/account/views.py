"""Views for account section"""
from datetime import timedelta

from flask import (Blueprint, current_app, flash, make_response, redirect,
                   render_template, request, url_for)
from flask_login import current_user, login_required, login_user, logout_user
from OpenDrive import db, rq
from OpenDrive.account.forms import (ChangeUserEmailForm, CreatePasswordForm, LoginForm)
from OpenDrive.models import User
from OpenDrive.queue import send_email
from OpenDrive.utils import render_errors, symmetric_encrypt

account = Blueprint('account', __name__)


@account.route('/login', methods=['GET', 'POST'])
def login():
    """Route that manages the user login"""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.password_hash is not None and \
                user.verify_password(form.password.data):
            duration = timedelta(weeks=1)
            expires = None
            login_user(user, form.remember_me.data, duration)
            encrypted_pass = symmetric_encrypt(form.password.data)
            response = make_response(redirect(request.args.get('next') or url_for('main.index')))
            if form.remember_me.data:
                expires = (duration.microseconds + (duration.seconds + duration.days * 24 * 3600) * 10**6) / 10.0**6
            response.set_cookie('hash',
                            encrypted_pass,
                            secure=current_app.config["SESSION_COOKIE_SECURE"],
                            httponly=True,
                            max_age=expires)
            # , samesite="Strict")
            flash('You are now logged in. Welcome back!', 'bg-primary')
            return response
        else:
            flash('Invalid email or password.', 'bg-danger')
    return render_template('account/login.html', form=form)


@account.route('/logout')
@login_required
def logout():
    """Route that manages the user logout"""
    logout_user()
    flash('You have been logged out.', 'bg-danger')
    response = make_response(redirect(url_for('main.index')))
    response.set_cookie("hash", '', expires=0)
    return response


@account.route('/manage', methods=['GET', 'POST'])
@account.route('/manage/info', methods=['GET', 'POST'])
@login_required
def manage():
    """Route that renders the user informations"""
    return render_template('account/manage.html', user=current_user, form=None)


@account.route('/manage/new-email', methods=['GET', 'POST'])
@login_required
def change_email():
    """Route that manages the email change for the user"""
    form = ChangeUserEmailForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        db.session.add(current_user)
        db.session.commit()
        flash(f'Email successfully changed to {current_user.email}.', 'bg-primary')
    else:
        render_errors(form.errors) # pylint: disable=maybe-no-member

    return render_template('account/manage.html', user=current_user, form=form)

@account.route('/join-from-invite/<int:user_id>/<token>', methods=['GET', 'POST'])
def join_from_invite(user_id, token):
    """
    Confirm new user's account with provided token and prompt them to set
    a password.
    """
    if current_user is not None and current_user.is_authenticated:
        flash('You are already logged in.', 'bg-danger')
        return redirect(url_for('main.index'))

    new_user = User.query.get(user_id)
    if new_user is None:
        return redirect(404)

    if new_user.password_hash is not None:
        flash('You have already joined.', 'bg-danger')
        return redirect(url_for('main.index'))

    if new_user.is_valid_token(token):
        form = CreatePasswordForm()
        if form.validate_on_submit():
            new_user.password = form.password.data
            db.session.add(new_user)
            db.session.commit()
            flash('Your password has been set, if it\'s needed to '
                  'check your settings go to "account", "settings" ', 'bg-primary')
            return redirect(url_for('account.login'))
        else:
            render_errors(form.errors) # pylint: disable=maybe-no-member
        return render_template('account/join_invite.html', form=form)
    else:
        flash('The confirmation link is invalid or has expired. Another '
              'invite email with a new link has been sent to you.', 'bg-danger')
        token = new_user.generate_confirmation_token()
        invite_link = url_for(
            'account.join_from_invite',
            user_id=user_id,
            token=token,
            _external=True)
        rq.get_queue("email").enqueue(
            send_email, 
            recipient=new_user.email,
            subject='You Are Invited To Join',
            template='email/invite',
            user=new_user,
            invite_link=invite_link,)
    return redirect(url_for('main.index'))

@account.route('/api/id', methods=['GET'])
def get_id_by_email_no_login():
    email = request.args['email']
    user = User.query.filter_by(email=email).first()
    if user is not None:
        return {'status': True, 'data': user.id}
    return {'status': False, 'data': None}

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
