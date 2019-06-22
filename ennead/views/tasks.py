"""Views for task pages"""
from flask import render_template
from werkzeug.wrappers import Response
from ennead.models.task import TaskSet, Task


def index() -> Response:
    try:
        active_set = TaskSet.get(TaskSet.active == 1)
    except TaskSet.DoesNotExist:
        return render_template('index.html', tasks=None)
    tasks = Task.select().where(Task.task_set == active_set.active)
    return render_template('index.html', tasks=tasks)
