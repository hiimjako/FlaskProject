from flask import Blueprint, render_template, redirect, url_for
from werkzeug.utils import secure_filename


main = Blueprint('main', __name__)


@main.route('/')
def index():
    # FIXME: main page?
    return redirect(url_for('drive.index'))
    # return render_template('main/index.html')
