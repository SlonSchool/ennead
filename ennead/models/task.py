"""Module for Ennead task model and corresponding helper classes"""

from typing import TYPE_CHECKING, List

from peewee import BooleanField, CharField, TextField, IntegerField, ForeignKeyField

from ennead.utils import render_markdown
from ennead.models.base import BaseModel
if TYPE_CHECKING:
    # pylint: disable=R0401
    from ennead.models.thread import Thread  # noqa: F401


class TaskSet(BaseModel):
    """Set of tasks. Only one `TaskSet` can be used at one moment

    Attributes:
        name: human-readable name of `TaskSet`
        tasks: list of `Task` of this set
        active: is this `TaskSet` current
        threads: list of `Thread`s with this user as student
    """

    name: str = CharField()
    active: bool = BooleanField()

    tasks: List['Task']
    threads: List['Thread']


class Task(BaseModel):
    """One task for student

    Attributes:
        name: human-readable name of `Task`
        description: `Task` description in Markdown
        base_score: basic maximal score for `Task`
        task_set: set this `Task` belongs to
        threads: list of `Thread`s about this `Task`
    """

    name: str = CharField()
    description: str = TextField()
    base_score: int = IntegerField()
    task_set: TaskSet = ForeignKeyField(TaskSet, backref='tasks')

    threads: List['Thread']

    @property
    def html_description(self):
        """`Task` description in HTML"""

        return render_markdown(self.description)
