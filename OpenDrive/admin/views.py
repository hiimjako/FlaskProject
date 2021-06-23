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

from OpenDrive import db
from OpenDrive.admin.forms import (
    ChangeAccountTypeForm,
    ChangeUserEmailForm,
    NewUserForm,
)
from OpenDrive.decorators import admin_required
from OpenDrive.models import Role, User, File, Password
from sqlalchemy import func, distinct

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
    users = User.query.order_by(User.role_id.desc(), User.last_name).all()
    roles = Role.query.all()
    return render_template(
        'admin/registered_users.html', users=users, roles=roles)


@admin.route('/user/<int:user_id>')
@admin.route('/user/<int:user_id>/info')
@login_required
@admin_required
def user_info(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    return render_template('admin/manage_user.html', user=user)


@admin.route('/system-manager')
@login_required
@admin_required
def hardware_usage():
    users = []
    # , isouter=True)\
    users = db.session.query(User.last_name, User.first_name, User.email, func.count(distinct(File.id)).label("nFiles"), func.count(distinct(Password.id)).label("nPassword"))\
        .join(File)\
        .join(Password)\
        .filter(File.id is not None)\
        .filter(Password.id is not None)\
        .group_by(User.id).all()
    return render_template('admin/system_manager.html', users=users)


@admin.route('/user/<int:user_id>/change-email', methods=['GET', 'POST'])
@login_required
@admin_required
def change_user_email(user_id):
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
        for error in form.errors:
            flash(form.errors[error][0], 'bg-danger')

    return render_template('admin/manage_user.html', user=user, form=form)


@ admin.route('/user/<int:user_id>/change-account-type', methods=['GET', 'POST'])
@ login_required
@ admin_required
def change_account_type(user_id):
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
        flash('Role for user {} successfully changed to {}.'.format(
            user.full_name(), user.role.name), 'bg-primary')
    return render_template('admin/manage_user.html', user=user, form=form)


@ admin.route('/user/<int:user_id>/delete')
@ login_required
@ admin_required
def delete_user_request(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    return render_template('admin/manage_user.html', user=user)


@ admin.route('/user/<int:user_id>/_delete')
@ login_required
@ admin_required
def delete_user(user_id):
    if current_user.id == user_id:
        flash('You cannot delete your own account.', 'bg-danger')
    else:
        user = User.query.filter_by(id=user_id).first()
        db.session.delete(user)
        db.session.commit()
        flash('Successfully deleted user %s.' % user.full_name(), 'success')
    return redirect(url_for('admin.registered_users'))


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
