import os
from OpenDrive.models import File
from flask import current_app


def getFilePath(file: File):
    path = None

    if os.path.isfile(file.path):
        path = file.path
    elif os.path.isfile(os.path.join(current_app.config['UPLOAD_PATH'], file.filename)):
        path = os.path.join(current_app.config['UPLOAD_PATH'], file.filename)

    return path
