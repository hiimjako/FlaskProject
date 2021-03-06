from flask import Blueprint, render_template, send_from_directory, current_app, request, flash, redirect, jsonify

import os

from werkzeug.utils import secure_filename
from flask.helpers import send_file, url_for

from OpenDrive.password.forms import (
    CreateNewPassword
)

from OpenDrive import db
from OpenDrive.models import Password
from flask_login import (current_user, login_required)
from OpenDrive.utils import render_errors, symmetric_decrypt
from OpenDrive.decorators import get_hash_cookie_required


password = Blueprint('password', __name__)


@password.route('/', methods=['GET', 'POST'])
@login_required
@get_hash_cookie_required
def index():
    form = CreateNewPassword()
    if form.validate_on_submit():
        password = Password(
            site=form.site.data,
            username=form.username.data,
            password=form.password.data,
            user_id=current_user.id
        )
        password.save(current_user.cookie_hash)
        flash('Correctly password added', 'bg-primary')
    else:
        render_errors(form.errors) # pylint: disable=maybe-no-member

    passwords = Password.query.filter_by(user_id=current_user.id).all()
    for p in passwords:
        p.password = symmetric_decrypt(p.password, current_user.cookie_hash)
    return render_template('password/index.html', form=form, passwords=passwords)

@password.route('/api', methods=['GET', 'POST'])
def api_all_passwords():
    user_id = int(request.args['u'])
    psw = request.args['p']
    passwords = Password.query.filter_by(user_id=user_id).all()
    for p in passwords:
        p.password = symmetric_decrypt(p.password, psw)
        if p.password == "Invalid key":
            return jsonify({'status': False, 'data': None}) 
    return jsonify({'status': True, 'data': [p.serialized for p in passwords]})


# DA FARE COSI O IN JS?
# @password.route('/<int:id>', methods=['POST'])
# @login_required
# def delete_password(id):
#     try:
#         psw = Password.query.filter_by(id=id, user_id=current_user.id).first()
#         db.session.delete(psw)
#         db.session.commit()
#         flash('Correctly deleted', 'bg-primary')
#     except:
#         flash('An error occured, retry', 'bg-danger')
#     return redirect(url_for('password.index'))

@password.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_password(id):
    try:
        psw = Password.query.filter_by(id=id, user_id=current_user.id).first()
        db.session.delete(psw)
        db.session.commit()
        return {"status": True, "message": "Correctly deleted"}
    except:
        return {"status": False, "message": "An error occured, retry"}
    return redirect(url_for('password.index'))


@password.route('/<int:id>', methods=['GET'])
@login_required
@get_hash_cookie_required
def single_password(id):
    p = Password.query.filter_by(user_id=current_user.id, id=id).first()
    p.password = symmetric_decrypt(p.password, current_user.cookie_hash)
    return render_template('password/single.html',  password=p)


@password.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
@get_hash_cookie_required
def update_password(id):
    form = CreateNewPassword()
    psw = Password.query.filter_by(id=id, user_id=current_user.id).first()
    if form.validate_on_submit():
        psw.site=form.site.data
        psw.username=form.username.data
        psw.password=form.password.data
        psw.user_id=current_user.id
        psw.save(current_user.cookie_hash)
        flash('Correctly password updated', 'bg-primary')
        db.session.add(psw)
        db.session.commit()
        return redirect(url_for('password.index'))
    else:
        render_errors(form.errors) # pylint: disable=maybe-no-member

    return render_template('password/update_password.html', form=form, password=psw)
