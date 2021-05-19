from flask import Blueprint, render_template, redirect, url_for

from OpenDrive.models import EditableHTML

from werkzeug.utils import secure_filename


main = Blueprint('main', __name__)


@main.route('/')
def index():
    # FIXME: main page?
    return redirect(url_for('drive.index'))
    # return render_template('main/index.html')


@main.route('/about')
def about():
    editable_html_obj = EditableHTML.get_editable_html('about')
    return render_template(
        'main/about.html', editable_html_obj=editable_html_obj)
