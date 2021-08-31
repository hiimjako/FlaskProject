from flask import render_template

from OpenDrive.main.views import main


@main.app_errorhandler(403)
def forbidden(_):
    return render_template('errors/generic.html', code=403, text='Forbidden'), 403


@main.app_errorhandler(404)
def page_not_found(_):
    return render_template('errors/generic.html', code=404, text='Page not found'), 404


@main.app_errorhandler(500)
def internal_server_error(_):
    return render_template('errors/generic.html', code=500, text='Internal Server Error'), 500
