from flask import Blueprint, render_template, redirect, request, flash

import os

from werkzeug.utils import secure_filename
from flask.helpers import send_file, url_for

from OpenDrive.drive.forms import (
    UploadNewFile,
    RenameFile
)

from OpenDrive import db
from OpenDrive.models import File
from flask_login import (current_user, login_required)

from OpenDrive.decorators import get_hash_cookie_required
from OpenDrive.utils import symmetricDecryptFile
import io

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
        path = file.getFilePath()
        if path:
            mimetype = file.getMimeType()
            as_attachment = request.args.get('as_attachment')
            show = request.args.get('show')

            fileBin = path
            if as_attachment == 'True':
                # Quando scarico il file lo voglio sempre dectyptato
                fileBin = io.BytesIO(symmetricDecryptFile(path, current_user.cookieHash))
                return send_file(fileBin, mimetype=mimetype, attachment_filename=file.filename, as_attachment=True)

            if show == 'True':
                # Quando lo apro in una nuova tab lo voglio decryptato
                # TODO: far si che quando si apre in una nuova tab ci sia il nome corretto
                fileBin = io.BytesIO(symmetricDecryptFile(path, current_user.cookieHash))
                return send_file(fileBin, mimetype=mimetype)

            # per le anteprime decrypto solo le immagini, per mostrarle in anteprima
            # gli altri file non sono utili
            if mimetype is not None and mimetype.startswith("image"):
                fileBin = io.BytesIO(symmetricDecryptFile(path, current_user.cookieHash))
            return send_file(fileBin, mimetype=mimetype)
        else:
            flash(f'Error: file {file.filename.strip()} not found. Ask to admin', 'bg-danger')

    if request.method == 'DELETE':
        file = File.query.filter_by(id=file_id, user_id=current_user.id).first()
        path = file.getFilePath()

        if path:
            os.remove(path)

        db.session.delete(file)
        db.session.commit()

        return {'status': True, 'message': 'Correctly deleted'}

    return {'status': False, 'message': 'Error'}


@drive.route('/file/<int:file_id>/rename', methods=['GET', 'POST'])
@login_required
def rename_file(file_id):
    form = RenameFile()
    if request.method == 'POST':
        if form.validate_on_submit():
            file = File.query.filter_by(
                id=file_id, user_id=current_user.id).first()
            if file:
                file.filename = os.path.splitext(form.filename.data)[0] + os.path.splitext(file.filename)[1]
                db.session.add(file)
                db.session.commit()
                flash('Correctly updated', 'bg-primary')
                return redirect(url_for('drive.index'))
 
        else:
            for error in form.errors:
                flash(form.errors[error][0], 'bg-danger')

    file = File.query.filter_by(id=file_id, user_id=current_user.id).first()
    return render_template('drive/rename_file.html', form=form, file=file)

@drive.route('/file/<int:file_id>/share', methods=['GET'])
@login_required
def share_file(file_id):
    flash("Feature work in progress :)", 'bg-danger')
    return redirect(url_for('drive.index'))

