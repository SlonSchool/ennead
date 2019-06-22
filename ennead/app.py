"""Main Ennead module for creating Flask app"""

from typing import Optional

from flask import Flask, g, session

from ennead.config import Config

from ennead.views.auth import register, register_page, login, login_page, logout
from ennead.views.tasks import index

from ennead.models.base import database
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
    if config_path:
        config = Config.from_filename(config_path)
    else:
        config = Config()
    app.config.from_object(config)

    database.initialize(config.DB_CLASS(config.DB_NAME, **config.DB_PARAMS))
    database.create_tables([User, Task, TaskSet, Thread, Post])

    app.before_request(inject_user)

    app.add_url_rule('/', 'index', index)

    app.add_url_rule('/register', 'register_page', register_page)
    app.add_url_rule('/register', 'register', register, methods=['POST'])
    app.add_url_rule('/login', 'login_page', login_page)
    app.add_url_rule('/login', 'login', login, methods=['POST'])
    app.add_url_rule('/logout', 'logout', logout)

    return app


if __name__ == '__main__':
    create_app('ennead.json').run()
