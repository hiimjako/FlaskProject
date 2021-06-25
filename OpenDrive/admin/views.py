from OpenDrive.utils import render_errors
from OpenDrive.queue import send_email
from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required
# from flask_rq2  import get_queue

from sqlalchemy import func, distinct
from hurry.filesize import size as bytesToHuman
from OpenDrive import db, rq
from OpenDrive.admin.forms import (
    ChangeAccountTypeForm,
    ChangeUserEmailForm,
    InviteUserForm,
    NewUserForm,
)
from OpenDrive.decorators import admin_required
from OpenDrive.models import Role, User, File, Password

admin = Blueprint('admin', __name__)


@admin.route('/')
@login_required
@admin_required
def index():
    """Admin dashboard page."""
    return render_template('admin/index.html')


@admin.route('/new-user', methods=['GET', 'POST'])
@login_required
@admin_required
def new_user():
    """Create a new user"""
    form = NewUserForm()
    if form.validate_on_submit():
        user = User(
            role=form.role.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User {} successfully created'.format(user.full_name()),
              'bg-primary')
    return render_template('admin/new_user.html', form=form)


@admin.route('/users')
@login_required
@admin_required
def registered_users():
    """Get registered user"""
    users = User.query.order_by(User.role_id.desc(), User.last_name).all()
    roles = Role.query.all()
    return render_template(
        'admin/registered_users.html', users=users, roles=roles)


@admin.route('/user/<int:user_id>')
@admin.route('/user/<int:user_id>/info')
@login_required
@admin_required
def user_info(user_id):
    """Get specific user info"""
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    return render_template('admin/manage_user.html', user=user)


@admin.route('/system-manager')
@login_required
@admin_required
def hardware_usage():
    """Retrives the space utilization for each user"""
    users = db.session.query(User.last_name, User.first_name, User.email,\
        func.count(distinct(File.id)).label("nFiles"),\
        func.count(distinct(Password.id)).label("nPassword"))\
        .join(File, isouter=True)\
        .join(Password, isouter=True)\
        .group_by(User.id)\
        .order_by(User.id)\
        .all()

    sizes = db.session.query(User.id, func.sum(File.size).label("size"))\
        .join(File, isouter=True)\
        .group_by(User.id)\
        .order_by(User.id)\
        .all()

    return render_template('admin/system_manager.html', users=users, sizes=sizes, bytesToHuman=bytesToHuman)


@admin.route('/user/<int:user_id>/change-email', methods=['GET', 'POST'])
@login_required
@admin_required
def change_user_email(user_id):
    """Route for change account email"""
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    form = ChangeUserEmailForm()
    if form.validate_on_submit():
        user.email = form.email.data
        db.session.add(user)
        db.session.commit()
        flash(f'Email for user {user.full_name()} successfully changed to {user.email}.', 'bg-primary')
    else:
        render_errors(form.errors)

    return render_template('admin/manage_user.html', user=user, form=form)


@admin.route('/user/<int:user_id>/change-account-type', methods=['GET', 'POST'])
@login_required
@admin_required
def change_account_type(user_id):
    """Route that allow admin to change a user role"""
    if current_user.id == user_id:
        flash('You cannot change the type of your own account.', 'bg-danger')
        return redirect(url_for('admin.user_info', user_id=user_id))

    user = User.query.get(user_id)
    if user is None:
        abort(404)
    form = ChangeAccountTypeForm()
    if form.validate_on_submit():
        user.role = form.role.data
        db.session.add(user)
        db.session.commit()
        flash('Role for user {} successfully changed to {}.'.format(user.full_name(), user.role.name), 'bg-primary')
    return render_template('admin/manage_user.html', user=user, form=form)


@admin.route('/user/<int:user_id>/delete')
@login_required
@admin_required
def delete_user_request(user_id):
    """Delete User"""
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    return render_template('admin/manage_user.html', user=user)


@admin.route('/user/<int:user_id>/_delete')
@login_required
@admin_required
def delete_user(user_id):
    """Delete User"""
    if current_user.id == user_id:
        flash('You cannot delete your own account.', 'bg-danger')
    else:
        user = User.query.filter_by(id=user_id).first()
        Password.query.filter_by(user_id=user_id).delete()
        files = File.query.filter_by(user_id=user_id)
        for file in files:
            file.hard_delete()
        db.session.delete(user)
        db.session.commit()
        flash('Successfully deleted user %s.' % user.full_name(), 'bg-primary')
    return redirect(url_for('admin.registered_users'))


@admin.route('/invite', methods=['GET', 'POST'])
@login_required
@admin_required
def invite_user():
    """Invite user"""

    form = InviteUserForm()
    if form.validate_on_submit():
        user = User(
            role=form.role.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        invite_link = url_for(
            'account.join_from_invite',
            user_id=user.id,
            token=token,
            _external=True)

        rq.get_queue("email").enqueue(
            send_email, 
            recipient=user.email,
            subject='You Are Invited To Join',
            template='email/invite',
            user=user,
            invite_link=invite_link,)
        flash(f'User {user.full_name()} successfully invited', 'bg-primary')
    else:
        render_errors(form.errors)
    
    return render_template('admin/invite_user.html', form=form)

# @admin.route('/_update_editor_contents', methods=['POST'])
# @login_required
# @admin_required
# def update_editor_contents():
#     """Update the contents of an editor."""

#     edit_data = request.form.get('edit_data')
#     editor_name = request.form.get('editor_name')

#     editor_contents = EditableHTML.query.filter_by(
#         editor_name=editor_name).first()
#     if editor_contents is None:
#         editor_contents = EditableHTML(editor_name=editor_name)
#     editor_contents.value = edit_data

#     db.session.add(editor_contents)
#     db.session.commit()

#     return 'OK', 200
