from flask import Blueprint, render_template, request, flash, redirect, current_app

import os

from OpenDrive.models import EditableHTML

from werkzeug.utils import secure_filename
from flask.helpers import url_for

from OpenDrive.drive.forms import (
    UploadNewFile
)

from OpenDrive import db
from OpenDrive.models import File
from flask_login import (current_user, login_required)

drive = Blueprint('drive', __name__)


@drive.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = UploadNewFile()
    if form.validate_on_submit():
        f = form.file.data
        filename = secure_filename(f.filename)
        basePath = current_app.config['UPLOAD_PATH']
        if not os.path.exists(basePath):
            os.makedirs(basePath)
        uploadPath = os.path.join(basePath, filename)
        f.save(uploadPath)
        file = File(
            filename=filename,
            path=uploadPath,
            user_id=current_user.id
        )
        db.session.add(file)
        db.session.commit()

        return redirect(url_for('drive.index'))

    # Getting all user files

    # return render_template('drive/upload.html', form=form)

    return render_template('drive/index.html', form=form)


# @drive.route('/upload', methods=['GET', 'POST'])
# def upload_file():
#     form = UploadNewFile()
#     if form.validate_on_submit():
#         f = form.file.data
#         filename = secure_filename(f.filename)
#         uploadPath = current_app.config['UPLOAD_PATH']
#         if not os.path.exists(uploadPath):
#             os.makedirs(uploadPath)
#         f.save(os.path.join(uploadPath, filename))
#         return redirect(url_for('drive.index'))

#     return render_template('drive/upload.html', form=form)
