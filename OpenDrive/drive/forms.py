from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms.fields.core import StringField
from wtforms.fields.simple import MultipleFileField

from wtforms.fields import SubmitField
from wtforms.validators import InputRequired, Length


class UploadNewFile(FlaskForm):
    file = MultipleFileField('New file(s)')
    submit = SubmitField('Upload')


class RenameFile(FlaskForm):
    filename = StringField('New filename', validators=[
                           InputRequired(), Length(1, 255)])
    submit = SubmitField('Change')
