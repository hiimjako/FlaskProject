from flask import Blueprint, render_template, redirect, request, flash

import os
from sqlalchemy.sql.elements import and_, or_

from werkzeug.utils import secure_filename
from flask.helpers import send_file, url_for

from OpenDrive.drive.forms import (
    UploadNewFile,
    RenameFile,
    changeFolder
)

from OpenDrive import db
from OpenDrive.models import File
from flask_login import (current_user, login_required)

from OpenDrive.decorators import get_hash_cookie_required
from OpenDrive.utils import render_errors, symmetricDecryptFile
import io
from sqlalchemy import func, distinct
from urllib.parse import unquote

drive = Blueprint('drive', __name__)

HOME_FOLDER = "/h/"

@drive.route('/<path:folder_path>', methods=['GET', 'POST'])
@login_required
@get_hash_cookie_required
def index(folder_path):
    form = UploadNewFile()
    folder_path = f"/{unquote(folder_path)}/" or HOME_FOLDER
    if form.validate_on_submit():
        for file in form.file.data:
            file_bin = file
            file = File(
                folder=folder_path,
                file=file_bin,
                user_id=current_user.id
            )
            file.save(current_user.cookieHash)

        message = 'Correctly added'
        flash(message, 'bg-primary')
        return {'status': True, 'message': message}
        # return redirect(url_for('drive.index'))

    # Getting all user files
    files = File.query.filter(and_(File.user_id==current_user.id, File.folder == folder_path))\
        .order_by(File.folder.desc()).all()

    folders = File.query.filter(and_(File.user_id==current_user.id, File.folder.op('~')(rf"^{folder_path}\/?\w")))\
        .order_by(File.folder.desc()).distinct(File.folder).all()

    if len(files) == 0 and len(folders) == 0:
        return redirect(url_for('drive.index', folder_path="/h"))

    return render_template('drive/index.html', form=form, files=files, folders=folders, folder_path=folder_path)

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
            preview = request.args.get('preview')

            file_bin = path
            if as_attachment == 'True':
                # Quando scarico il file lo voglio sempre dectyptato
                file_bin = io.BytesIO(symmetricDecryptFile(path, current_user.cookieHash))
                return send_file(file_bin, mimetype=mimetype, attachment_filename=file.filename, as_attachment=True)

            if preview == 'True':
                # per le anteprime decrypto solo le immagini, per mostrarle in anteprima
                # gli altri file non sono utili
                file_bin = io.BytesIO(bytes())
                if mimetype is not None and mimetype.startswith("image"):
                    file_bin = io.BytesIO(symmetricDecryptFile(path, current_user.cookieHash))
                return send_file(file_bin, mimetype=mimetype)

            # Quando lo apro in una nuova tab lo voglio decryptato
            # TODO: far si che quando si apre in una nuova tab ci sia il nome corretto
            file_bin = io.BytesIO(symmetricDecryptFile(path, current_user.cookieHash))
            return send_file(file_bin, mimetype=mimetype)
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
                return redirect(url_for('drive.index', folder_path="/h"))
        else:
            render_errors(form.errors)

    file = File.query.filter_by(id=file_id, user_id=current_user.id).first()
    return render_template('drive/rename_file.html', form=form, file=file)

@drive.route('/file/<int:file_id>/folder', methods=['GET', 'POST'])
@login_required
def folder_file(file_id):
    form = changeFolder()
    if request.method == 'POST':
        if form.validate_on_submit():
            file = File.query.filter_by(id=file_id, user_id=current_user.id).first()
            if file:
                file.update_folder_secure(form.folder.data)
                db.session.add(file)
                db.session.commit()
                flash('Correctly updated', 'bg-primary')
                return redirect(url_for('drive.index', folder_path="/h"))
        else:
            render_errors(form.errors)

    file = File.query.filter_by(id=file_id, user_id=current_user.id).first()
    return render_template('drive/change_folder.html', form=form, file=file)

@drive.route('/file/<int:file_id>/share', methods=['GET'])
@login_required
def share_file(file_id):
    flash("Feature work in progress :)", 'bg-danger')
    return redirect(url_for('drive.index', folder_path="/h"))
