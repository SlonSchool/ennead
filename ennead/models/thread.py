"""Model for Ennead thread and post models"""

import datetime
from typing import List

from peewee import DateTimeField, IntegerField, DecimalField, TextField, ForeignKeyField

from ennead.models.user import User
from ennead.models.task import Task
from ennead.models.base import BaseModel


class Thread(BaseModel):
    """Student-with-teachers chat about `Task`

    Attributes:
        task: `Task` this thread belongs to
        score: how much points student got for this `Thread`
        student: `User` this thread belongs to
        post: list of `Post`s in this `Thread`
    """

    task: Task = ForeignKeyField(Task, backref='threads')
    score: float = DecimalField(default=0)
    student: User = ForeignKeyField(User, backref='threads')

    posts: List['Post']

    def ordered_posts(self, show_hidden=False):
        posts = self.posts
        if show_hidden:
            posts = filter(lambda post: not post.hidden, posts)
        posts = sorted(posts, key=lambda post: post.date)
        return posts
    


class Post(BaseModel):
    """One post in `Thread` with `User` about `Task`

    Attributes:
        text: `Post` text in Markdown
        date: date this `Post` was posted
        author: `User` who wrote this post
        thread: `Thread` this task belongs to
    """

    text: str = TextField()
    date: datetime.datetime = DateTimeField()
    author: User = ForeignKeyField(User, backref='+')  # '+' means 'no backref'
    thread: Thread = ForeignKeyField(Thread, backref='posts')
