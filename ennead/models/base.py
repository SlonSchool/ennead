"""Base model for all Ennead models"""
# pylint: disable=missing-docstring,invalid-name

from peewee import DatabaseProxy, Model


database = DatabaseProxy()


class BaseModel(Model):
    class Meta:
        database = database
