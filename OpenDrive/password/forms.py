from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms import ValidationError


from OpenDrive import db
from OpenDrive.models import User, File
from wtforms.fields import SubmitField, StringField
from wtforms.fields.simple import PasswordField
from wtforms.validators import Email, EqualTo, InputRequired, Length, URL


class CreateNewPassword(FlaskForm):
    site = StringField('Site', [InputRequired(), URL(False, 'It isn\'t a valid site URL')])
    username = StringField('Username', [InputRequired(), Length(1, -1, 'Username too short')])
    password = PasswordField('Password', [InputRequired()])  # , EqualTo('confirm', message='Passwords must match')])
    # confirm = PasswordField('Repeat Password')
    submit = SubmitField('Upload')
