"""Views for task pages"""
from flask import render_template
from werkzeug.wrappers import Response


def index() -> Response:
    return render_template('index.html')
