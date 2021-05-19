from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from wtforms import ValidationError

from wtforms.fields.html5 import EmailField

from OpenDrive import db
from OpenDrive.models import User, File
from wtforms.fields import SubmitField


class CreateNewPassword(FlaskForm):
    file = FileField(validators=[FileRequired()])
    submit = SubmitField('Upload')
