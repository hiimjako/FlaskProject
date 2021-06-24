import os

from flask import render_template
from flask_mail import Message
import OpenDrive


def send_email(recipient, subject, template, **kwargs):
    """Wrapper for email"""
    app = OpenDrive.create_app(os.environ.get("FLASK_ENV", default="development"))
    with app.app_context():
        msg = Message(
            'OpenDrive: ' + subject,
            sender=app.config['MAIL_USERNAME'],
            recipients=[recipient])
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)
        OpenDrive.mail.send(msg)
