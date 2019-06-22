"""Views for dialogues"""

import datetime
from flask import g

from flask import session, current_app, render_template, request, redirect, url_for
from werkzeug.wrappers import Response

from ennead.utils import require_logged_in, require_logged_in_as_teacher, require_logged_in_as_student
from ennead.models.user import User, UserGroup
from ennead.models.task import Task
from ennead.models.thread import Thread, Post


@require_logged_in_as_student
def student_thread_page(task_id: int) -> Response:
    """GET /student_thread_page/{task}: show student's thread for a specified task"""
    task = Task.get_by_id(task_id)
    thread, _ = Thread.get_or_create(task=task_id, student=g.user)
    return render_template('dialogue.html', task=task, thread=thread)

@require_logged_in_as_teacher
def teacher_thread_page(task_id: int, student_id: int) -> Response:
    """GET /teacher_thread_page/{task}: show student's thread for a specified task"""
    task = Task.get_by_id(task_id)
    student = User.get_by_id(student_id)
    thread, _ = Thread.get_or_create(task=task_id, student=student)
    return render_template('dialogue.html', task=task, thread=thread)


@require_logged_in
def send_post_to_thread(thread_id: int) -> Response:
    thread = Thread.get_by_id(thread_id)
    text = request.form['text'].strip()
    if len(text) != 0 and (g.user.is_teacher or (g.user.is_student and thread.student == g.user)):
        hide_from_student = False
        if g.user.is_teacher:
            hide_from_student = request.form.get('hide_from_student', False)
        post = Post.create(text=text, date=datetime.datetime.now(), author=g.user, thread=thread, hide_from_student=hide_from_student)
    if g.user.is_student:
        return redirect(url_for('student_thread_page', task_id=thread.task.id))
    if g.user.is_teacher:
        return redirect(url_for('teacher_thread_page', task_id=thread.task.id, student_id=thread.student.id))

@require_logged_in_as_teacher
def update_score(thread_id: int) -> Response:
    thread = Thread.get_by_id(thread_id)
    thread.score = request.form.get('score', thread.score)
    thread.save()
    return redirect(url_for('teacher_thread_page', task_id=thread.task.id, student_id=thread.student.id))
