from flask import Blueprint, render_template, send_from_directory, current_app, request, flash

import os

from werkzeug.utils import secure_filename
from flask.helpers import send_file, url_for

from OpenDrive.drive.forms import (
    UploadNewFile
)

from OpenDrive import db
from OpenDrive.models import File
from flask_login import (current_user, login_required)

from OpenDrive.drive.utils import getFilePath
from OpenDrive.decorators import get_hash_cookie_required
from OpenDrive.utils import symmetricDecryptFile
import io
import mimetypes

drive = Blueprint('drive', __name__)


@drive.route('/', methods=['GET', 'POST'])
@login_required
@get_hash_cookie_required
def index():
    form = UploadNewFile()
    if form.validate_on_submit():
        fileBin = form.file.data
        file = File(
            file=fileBin,
            user_id=current_user.id
        )
        file.save(current_user.cookieHash)
        message = 'Correctly added'
        flash(message, 'bg-primary')
        return {'status': True, 'message': message}
        # return redirect(url_for('drive.index'))

    # Getting all user files
    # No need to be decrypted
    files = File.query.filter_by(user_id=current_user.id).all()
    return render_template('drive/index.html', form=form, files=files)


@drive.route('/file/<int:file_id>', methods=['GET', 'DELETE'])
@login_required
@get_hash_cookie_required
def serve_file(file_id):
    if request.method == 'GET':
        file = File.query.filter_by(id=file_id, user_id=current_user.id).first()
        path = getFilePath(file)
        if path:
            mimetype = mimetypes.MimeTypes().guess_type(file.filename)[0]
            as_attachment = request.args.get('as_attachment')

            fileBin = path
            if as_attachment == 'True':
                # Quando scarico il file lo voglio sempre dectyptato
                fileBin = io.BytesIO(symmetricDecryptFile(path, current_user.cookieHash))
                return send_file(fileBin, mimetype=mimetype, attachment_filename=file.filename, as_attachment=True)

            # per le anteprime decrypto solo le immagini, per mostrarle in anteprima
            # gli altri file non sono utili
            if mimetype.startswith("image"):
                fileBin = io.BytesIO(symmetricDecryptFile(path, current_user.cookieHash))
            return send_file(fileBin, mimetype=mimetype)

    if request.method == 'DELETE':
        file = File.query.filter_by(id=file_id, user_id=current_user.id).first()
        path = getFilePath(file)

        if path:
            os.remove(path)

        db.session.delete(file)
        db.session.commit()

        return {'status': True, 'message': 'Correctly deleted'}

    return {'status': False, 'message': 'Error'}

# TODO: parte dei file condivisi
# @drive.route('/shared/<int:file_id>', methods=['GET', 'POST'])
# @login_required
# def serve_file(file_id):
#     file = File.query.filter_by(id=file_id).first()
#     path = file.path
#     if os.path.isfile(file.path):
#         path = file.path
#     elif os.path.isfile(os.path.join(current_app.config['UPLOAD_PATH'], file.filename)):
#         path = os.path.join(current_app.config['UPLOAD_PATH'], file.filename)
#     else:
#         return None

#     return send_file(path)
