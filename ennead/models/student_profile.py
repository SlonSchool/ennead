"""Module for Ennead task model and corresponding helper classes"""

from typing import TYPE_CHECKING, List

from peewee import BooleanField, CharField, TextField, IntegerField, ForeignKeyField, DateField

from datetime import date
from ennead.models.user import User
from flask import Request


from ennead.models.base import BaseModel
if TYPE_CHECKING:
    # pylint: disable=R0401
    from ennead.models.thread import Thread  # noqa: F401


class StudentProfile(BaseModel):
    """Student questionnaire

    Attributes:
        grade: year of education
        city:  city of living
        birth_date: date of birth
        sex: sex (True if male)
        allergy: human-readable list of allergies 
        communication: preferred communication type (vk/telegram profile)
        telephone: student's telephone number
        parent_information: human-readable name and contacts of one 
    """

    grade: int = IntegerField()
    city: str = CharField(32)
    birth_date: date = DateField()
    sex: bool = BooleanField()
    allergy: str = TextField()
    communication: str = TextField()
    telephone: str = CharField(20)
    parent_information: str = TextField()

    user: User = ForeignKeyField(User, backref='student_profiles')

