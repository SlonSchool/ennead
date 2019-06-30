"""Views, used for task creation and editing"""

from typing import Any, Dict

from flask import abort, redirect, render_template, request, url_for
from werkzeug.wrappers import Response

from peewee import PeeweeException

from ennead.utils import require_teacher
from ennead.models.base import database
from ennead.models.task import Task, TaskSet


@require_teacher
def adm_task_list_page() -> Response:
    """GET /adm/tasks: list of tasks & creation of new"""

    task_set = None
    task_set_criterion: Dict[str, Any] = {'active': True}
    task_set_id = request.args.get('task_set')
    if isinstance(task_set_id, (str, int)):
        try:
            task_set_criterion = {'id': int(task_set_id)}
        except (TypeError, ValueError):
            abort(400)
    try:
        task_set = TaskSet.get(**task_set_criterion)
    except TaskSet.DoesNotExist:
        pass

    return render_template('adm_task_list.html', task_set=task_set, task_set_list=TaskSet.select())


@require_teacher
def task_edit_page(task_id: int) -> Response:
    """GET /adm/tasks/<task_id>: task edit page"""

    try:
        task = Task.get(Task.id == task_id)
    except Task.DoesNotExist:
        abort(404)

    return render_template('task_edit.html', task=task)


@require_teacher
def task_edit() -> Response:
    """POST /adm/tasks: create or update task"""

    if request.form['id']:
        try:
            task = Task.get_by_id(int(request.form['id']))
        except Task.DoesNotExist:
            abort(404)
        except ValueError:
            abort(400)
    else:
        task = Task()

    try:
        task.task_set
    except TaskSet.DoesNotExist:
        # pylint: disable=singleton-comparison
        task.task_set = TaskSet.get(TaskSet.active == True)  # noqa: E712
    task.name = request.form.get('name', task.name)
    task.description = request.form.get('description', task.description)
    try:
        task.base_score = int(request.form.get('base_score', task.base_score) or 0)
    except ValueError:
        abort(400)

    task.save()
    return redirect(url_for('adm_task_list_page'))


@require_teacher
def task_delete(task_id: int) -> Response:
    """DELETE /adm/tasks/<task_id>: delete a task"""

    Task.delete().where(Task.id == task_id).execute()
    return redirect(url_for('adm_task_list_page'))


@require_teacher
def add_task_set() -> Response:
    """POST /adm/task_set: add a new task set"""

    if 'name' not in request.form:
        abort(400)

    task_set = TaskSet()
    task_set.name = request.form['name']
    task_set.active = True

    with database.atomic() as transaction:
        try:
            TaskSet.update({TaskSet.active: False}).execute(database)
            task_set.save()
        except PeeweeException:
            transaction.rollback()
            abort(500)

    return redirect(url_for('adm_task_list_page'))


@require_teacher
def choose_task_set() -> Response:
    """"POST /adm/task_set/choose: select active task set"""

    if 'task_set' not in request.form:
        abort(400)

    try:
        task_set = TaskSet.get_by_id(int(request.form['task_set']))
    except (ValueError, TypeError, TaskSet.DoesNotExist):
        abort(400)

    task_set.active = True
    with database.atomic() as transaction:
        try:
            TaskSet.update({TaskSet.active: False}).execute(database)
            task_set.save()
        except PeeweeException:
            transaction.rollback()
            abort(500)

    return redirect(url_for('adm_task_list_page'))
