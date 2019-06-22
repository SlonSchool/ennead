"""Views, used for task creation and editing"""

from flask import abort, redirect, render_template, request, url_for
from werkzeug.wrappers import Response

from ennead.utils import require_teacher
from ennead.models.task import Task, TaskSet


@require_teacher
def adm_task_list_page() -> Response:
    """GET /adm/tasks: list of tasks & creation of new"""

    return render_template('adm_task_list.html', task_set=TaskSet.get(active=True))


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
            task = Task.get(Task.id == int(request.form['id']))
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
