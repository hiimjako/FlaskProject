from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from wtforms import ValidationError
from wtforms.fields.core import StringField

from OpenDrive import db
from OpenDrive.models import User, File
from wtforms.fields import SubmitField
from wtforms.validators import InputRequired, Length


class UploadNewFile(FlaskForm):
    file = FileField('New file', validators=[FileRequired()])
    submit = SubmitField('Upload')


class RenameFile(FlaskForm):
    filename = StringField('New filename', validators=[
                           InputRequired(), Length(1, 255)])
    submit = SubmitField('Change')
