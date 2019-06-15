"""Views, used for registration and logging in"""

import datetime

from flask import session, current_app, render_template, request, redirect, url_for
from werkzeug.wrappers import Response

from ennead.utils import require_not_logged_in
from ennead.models.user import User, UserGroup


@require_not_logged_in
def register_page() -> Response:
    """GET /register: show registration page"""

    splash_text = {
        'fields': 'Not all required fields filled',
        'exists': 'User with this username already exists'
    }.get(str(request.args.get('splash')), '')

    return render_template('register.html', splash_text=splash_text)


@require_not_logged_in
def register() -> Response:
    """POST /register: process registration form"""

    user = User()

    for field in ('username', 'first_name', 'surname'):
        if field not in request.form:
            return redirect(url_for('register_page', splash='fields'))
        setattr(user, field, request.form[field])

    if user.username.endswith(':' + current_app.config['TEACHER_SECRET']):
        user.username = user.username[:-(len(current_app.config['TEACHER_SECRET']) + 1)]
        user.group = UserGroup.teacher
    else:
        user.group = UserGroup.student

    if list(User.select().where(User.username == user.username)):
        return redirect(url_for('register_page', splash='exists'))

    for field in ('email', 'patronym'):
        setattr(user, field, request.form.get(field))

    if 'password' not in request.form:
        return redirect(url_for('register_page', splash='fields'))

    user.set_password(request.form['password'])
    user.registered_at = datetime.datetime.now()
    user.save()

    session['user_id'] = user.id
    return redirect(url_for('index'))


@require_not_logged_in
def login_page() -> Response:
    """GET /login: show login page"""

    splash_text = {
        'nouser': 'No such user',
        'password': 'Wrong password'
    }.get(str(request.args.get('splash')), '')

    return render_template('login.html', splash_text=splash_text)


@require_not_logged_in
def login() -> Response:
    """POST /login: process registration form"""

    for field in ('username', 'password'):
        if field not in request.form:
            return redirect(url_for('login_page', splash='fields'))

    try:
        user = User.get(User.username == request.form['username'])
    except User.DoesNotExist:
        return redirect(url_for('login_page', splash='nouser'))

    if user.check_password(request.form['password']):
        session['user_id'] = user.id
        return redirect(url_for('index'))
    return redirect(url_for('login_page', splash='password'))


def logout() -> Response:
    """GET /logout: end user session"""

    del session['user_id']
    return redirect(url_for('index'))
