import datetime

from flask import Blueprint, session, current_app, render_template, request, redirect, url_for
from werkzeug.wrappers import Response

from ennead.models.user import User, UserGroup


auth = Blueprint('auth', __name__)


# GET /register
def register_page() -> Response:
    splash_text = {
        'fields': 'Not all required fields filled',
        'exists': 'User with this username already exists'
    }.get(str(request.args.get('splash')), '')

    return render_template('register.html', splash_text=splash_text)

# POST /register
def register() -> Response:
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
    return redirect('/')

# GET /login
def login_page() -> Response:
    splash_text = {
        'nouser': 'No such user',
        'password': 'Wrong password'
    }.get(str(request.args.get('splash')), '')

    return render_template('login.html', splash_text=splash_text)

# POST /login
def login() -> Response:
    for field in ('username', 'password'):
        if field not in request.form:
            return redirect(url_for('login_page', splash='fields'))

    try:
        user = User.get(User.username == request.form['username'])
    except User.DoesNotExist:
        return redirect(url_for('login_page', splash='nouser'))

    if user.check_password(request.form['password']):
        session['user_id'] = user.id
        return redirect('/')
    else:
        return redirect(url_for('login_page', splash='password'))

# GET /logout
def logout() -> Response:
    del session['user_id']
    return redirect('/')
