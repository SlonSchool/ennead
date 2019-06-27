"""Views for dialogues"""

import datetime
from flask import g

from flask import session, current_app, render_template, request, redirect, url_for
from werkzeug.wrappers import Response

from ennead.utils import require_logged_in, require_teacher, require_student
from ennead.utils import render_markdown
from ennead.models.user import User, UserGroup
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
def thread_page(task_id: int, student_id: int) -> Response:
    """GET /thread/{task}/{student}: show student's thread for a specified task"""
    if not has_access_to_thread(student_id):
        return redirect(url_for('index'))
    thread = get_thread(task_id, student_id)
    posts = thread.ordered_posts(show_hidden=g.user.is_teacher)
    return render_template('dialogue.html', thread=thread, task=thread.task, student=thread.student, posts=posts)

@require_logged_in
def post_to_thread(task_id: int, student_id: int) -> Response:
    if not has_access_to_thread(student_id):
        return redirect(url_for('index'))
    thread = get_thread(task_id, student_id)

    text = request.form['text'].strip()
    hide_from_student = g.user.is_teacher and request.form.get('hide_from_student', False)

    if correct_message(text):
        if g.user.is_teacher:
            score = request.form.get('score')
            if thread.score != score:
                thread.update(score=score).execute()

        post = Post.create(text=text, date=datetime.datetime.now(),
                            author=g.user, thread=thread,
                            hide_from_student=hide_from_student)
    else:
        # TODO: redirect back to a dialogue, restoring a message draft not to lose it
        pass
    return redirect(url_for('thread', task_id=task_id, student_id=student_id))
