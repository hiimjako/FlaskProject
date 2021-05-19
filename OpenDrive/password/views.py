from flask import Blueprint, render_template, send_from_directory, current_app, request, flash

import os

from werkzeug.utils import secure_filename
from flask.helpers import send_file, url_for

from OpenDrive.password.forms import (
    CreateNewPassword
)

from OpenDrive import db
from OpenDrive.models import File
from flask_login import (current_user, login_required)


password = Blueprint('password', __name__)


@password.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('password/index.html')
