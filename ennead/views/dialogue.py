"""Views for dialogues"""

import datetime
from flask import g

from flask import session, current_app, render_template, request, redirect, url_for
from werkzeug.wrappers import Response

from ennead.utils import require_logged_in
from ennead.models.user import User, UserGroup
from ennead.models.task import Task
from ennead.models.thread import Thread, Post


@require_logged_in
def student_thread_page(task_id: int) -> Response:
    """GET /thread/{task}: show student's thread for a specified task"""
    task = Task.get_by_id(task_id)
    thread, _ = Thread.get_or_create(task=task_id, student=g.user)
    return render_template('dialogue.html', task=task, thread=thread)
