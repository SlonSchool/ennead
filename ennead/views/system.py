from flask import request
from werkzeug.wrappers import Response

from ennead.utils import render_markdown


def render_markdown_endpoint() -> Response:
    markdown = request.get_data().decode('utf-8')
    return Response(render_markdown(markdown))
