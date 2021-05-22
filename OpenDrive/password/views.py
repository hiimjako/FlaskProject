from flask import Blueprint, render_template, send_from_directory, current_app, request, flash

import os

from werkzeug.utils import secure_filename
from flask.helpers import send_file, url_for

from OpenDrive.password.forms import (
    CreateNewPassword
)

from OpenDrive import db
from OpenDrive.models import Password
from flask_login import (current_user, login_required)


password = Blueprint('password', __name__)


@password.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = CreateNewPassword()
    # TODO: handle errors
    if form.validate_on_submit():
        password = Password(
            site=form.site.data,
            username=form.username.data,
            password=form.password.data,
            user_id=current_user.id
        )
        password.save()
        message = 'Correctly password added'
        flash(message, 'bg-primary')
    else:
        for error in form.errors:
            flash(form.errors[error][0], 'bg-danger')

    passwords = Password.query.filter_by(user_id=current_user.id).all()
    return render_template('password/index.html', form=form, passwords=passwords)
