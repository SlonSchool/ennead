"""Serving user-uploaded files"""

from flask import abort, current_app, request, send_from_directory
from werkzeug.wrappers import Response

from ennead.models.file import File


def uploaded_file(filename: str) -> Response:
    """Serve user-uploaded file"""

    return send_from_directory(current_app.config['UPLOAD_DIR'], filename)


def upload_file() -> Response:
    """Upload file to server and return it's URL"""

    if 'file' not in request.files:
        abort(400)

    filename = request.files['file'].filename
    filedata = request.files['file'].read()
    file_model = File.from_data(current_app.config['UPLOAD_DIR'], filename, filedata)

    return Response(f'{request.host_url}upload/{file_model.uuid}/{file_model.name}')
