"""Various common utils for Ennead"""

from typing import Any, Callable
from functools import wraps

from flask import g, redirect, url_for
from werkzeug.wrappers import Response


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
