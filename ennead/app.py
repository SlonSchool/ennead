"""Main Ennead module for creating Flask app"""

from typing import Optional

from flask import Flask, g, session

from ennead.config import Config

from ennead.views.file import upload_file, uploaded_file, files_page
from ennead.views.auth import register, register_page, login, login_page, logout
from ennead.views.tasks import index
from ennead.views.system import render_markdown_endpoint
from ennead.views.admin import (adm_task_list_page, add_task_set, choose_task_set,
                                task_edit_page, task_edit, task_delete)

from ennead.models.base import database
from ennead.models.file import File
from ennead.models.user import User
from ennead.models.task import TaskSet, Task
from ennead.models.thread import Thread, Post


def inject_user() -> None:
    """Before-request hook injecting user into `flask.g`"""

    g.user = None
    if 'user_id' in session:
        try:
            user = User.get(User.id == session['user_id'])
        except User.DoesNotExist:
            return
        g.user = user


def create_app(config_path: Optional[str] = None) -> Flask:
    """Create Flask app from JSON config (or with defaults)"""

    app = Flask(__name__)
    config = None
    if config_path:
        try:
            config = Config.from_filename(config_path)
        except FileNotFoundError:
            pass
    if config is None:
        config = Config.from_env()
    app.config.from_object(config)

    database.initialize(config.DB_CLASS(config.DB_NAME, **config.DB_PARAMS))
    database.create_tables([User, Task, TaskSet, Thread, Post, File])

    app.before_request(inject_user)

    app.add_url_rule('/', 'index', index)
    app.add_url_rule('/md', 'render_markdown_endpoint', render_markdown_endpoint, methods=['POST'])

    app.add_url_rule('/upload/<path:filename>', 'uploaded_file', uploaded_file)
    app.add_url_rule('/upload', 'upload_file', upload_file, methods=['POST'])
    app.add_url_rule('/adm/files', 'files_page', files_page)

    app.add_url_rule('/register', 'register_page', register_page)
    app.add_url_rule('/register', 'register', register, methods=['POST'])
    app.add_url_rule('/login', 'login_page', login_page)
    app.add_url_rule('/login', 'login', login, methods=['POST'])
    app.add_url_rule('/logout', 'logout', logout)

    app.add_url_rule('/adm/task_set', 'add_task_set', add_task_set, methods=['POST'])
    app.add_url_rule('/adm/task_set/choose', 'choose_task_set', choose_task_set, methods=['POST'])

    app.add_url_rule('/adm/tasks', 'adm_task_list_page', adm_task_list_page)
    app.add_url_rule('/adm/tasks/<int:task_id>', 'task_edit_page', task_edit_page)
    app.add_url_rule('/adm/tasks', 'task_edit', task_edit, methods=['POST'])
    app.add_url_rule(
        '/adm/tasks/<int:task_id>/delete',
        'task_delete',
        task_delete,
        methods=['POST']
    )

    return app


if __name__ == '__main__':
    create_app('ennead.json').run()
