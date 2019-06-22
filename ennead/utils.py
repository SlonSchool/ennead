"""Various common utils for Ennead"""

from typing import Any, Callable
from functools import wraps

from flask import g, abort, redirect, url_for
from werkzeug.wrappers import Response

from markdown import Markdown


MARKDOWN_ENGINE = Markdown(extensions=['mdx_math'])


def require_logged_in(func: Callable) -> Callable:
    """Make endpoint require logged in user"""

    @wraps(func)
    def wrapped(*args: Any, **kwargs: Any) -> Response:
        if not g.user:
            return redirect(url_for('login_page'))
        return func(*args, **kwargs)

    return wrapped


def require_not_logged_in(func: Callable) -> Callable:
    """Make endpoint require NOT logged in user"""

    @wraps(func)
    def wrapped(*args: Any, **kwargs: Any) -> Response:
        if g.user:
            return redirect(url_for('index'))
        return func(*args, **kwargs)

    return wrapped


def require_teacher(func: Callable) -> Callable:
    """Make endpoint require logged in teacher"""

    # pylint: disable=inconsistent-return-statements
    @wraps(func)
    def wrapped(*args: Any, **kwargs: Any) -> Response:
        if g.user and g.user.is_teacher:
            return func(*args, **kwargs)
        abort(403)

    return wrapped


def render_markdown(markdown: str) -> str:
    """Convert Markdown to HTML"""

    return MARKDOWN_ENGINE.convert(markdown)
