"""Serving user-uploaded files"""

from flask import g, abort, current_app, render_template, request, send_from_directory
from werkzeug.wrappers import Response

from ennead.utils import require_logged_in, require_teacher
from ennead.models.file import File


def uploaded_file(filename: str) -> Response:
    """GET /upload/<token>/<filename>: serve user-uploaded file"""

    return send_from_directory(current_app.config['UPLOAD_DIR'], filename)


@require_logged_in
def upload_file() -> Response:
    """POST /upload: upload a file to server and return it's URL"""

    if 'file' not in request.files:
        abort(400)

    filename = request.files['file'].filename
    filedata = request.files['file'].read()
    file_model = File.from_data(
        current_app.config['UPLOAD_DIR'], filename, filedata, g.user
    )

    return Response(f'/upload/{file_model.path}')


@require_teacher
def files_page() -> Response:
    """GET /adm/files: list stored files"""

    # While it's possible to explain mypy that File.uploaded_at has .desc(),
    # it's easier to just type: ignore it
    return render_template(
        'files.html', files=File.select().order_by(File.uploaded_at.desc())  # type: ignore
    )
