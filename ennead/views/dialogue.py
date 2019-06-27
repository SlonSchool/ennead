"""Views for dialogues"""

import datetime
from flask import g

from flask import render_template, request, redirect, url_for
from werkzeug.wrappers import Response

from ennead.utils import require_logged_in
from ennead.models.user import User
from ennead.models.task import Task
from ennead.models.thread import Thread, Post


def has_access_to_thread(student_id):
    return g.user.is_teacher or (g.user.is_student and (g.user.id == student_id))


def get_thread(task_id, student_id):
    task = Task.get_by_id(task_id)
    student = User.get_by_id(student_id)
    thread, _ = Thread.get_or_create(task=task, student=student)
    return thread


def correct_message(text):
    return (len(text) != 0)


@require_logged_in
def change_thread_score(thread: Thread, score: float) -> None:
    """Change thread score (if necessary) and notify student in a dialog"""

    if thread.score != score:
        score_change_msg = f"Балл изменен. Текущий балл: {score}."
        Post.create(text=score_change_msg, date=datetime.datetime.now(),
                    author=g.user, thread=thread,
                    hide_from_student=False)
        thread.update(score=score).execute()


@require_logged_in
def thread_page(task_id: int, student_id: int) -> Response:
    """GET /thread/{task}/{student}: show specified thread"""

    if not has_access_to_thread(student_id):
        return redirect(url_for('index'))
    thread = get_thread(task_id, student_id)
    posts = thread.ordered_posts(show_hidden=g.user.is_teacher)
    return render_template('dialogue.html', thread=thread, task=thread.task,
                           student=thread.student, posts=posts)


@require_logged_in
def post_to_thread(task_id: int, student_id: int) -> Response:
    """POST /thread/{task}/{student}: send a message to a specified thread"""

    if not has_access_to_thread(student_id):
        return redirect(url_for('index'))
    thread = get_thread(task_id, student_id)

    text = request.form['text'].strip()
    hide_from_student = g.user.is_teacher and request.form.get('hide_from_student', False)

    if correct_message(text):
        Post.create(text=text, date=datetime.datetime.now(),
                    author=g.user, thread=thread,
                    hide_from_student=hide_from_student)
    else:
        # TODO: redirect back to a dialogue, restoring a message draft not to lose it
        pass

    if g.user.is_teacher:
        score = float(request.form.get('score'))
        change_thread_score(thread, score)

    return redirect(url_for('thread', task_id=task_id, student_id=student_id))
