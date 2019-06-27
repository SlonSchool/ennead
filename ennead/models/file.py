"""Module for Ennead file model"""

import os
import secrets
import datetime

from peewee import CharField, DateTimeField, FixedCharField, ForeignKeyField

from ennead.models.base import BaseModel
from ennead.models.user import User


class FileCreationError(Exception):
    """Error occured while creating file"""


class File(BaseModel):
    """One file, uploaded to server

    Attributes:
        user: user who uploaded file
        name: filename as specified on upload
        token: short token for path
    """

    user: User = ForeignKeyField(User, backref='+')
    name: str = CharField()
    token: str = FixedCharField(8)
    uploaded_at: datetime.datetime = DateTimeField()

    @property
    def path(self) -> str:
        """path of file relative to upload dir"""

        return f'{self.token}/{self.name}'

    @classmethod
    def from_data(cls, directory: str, name: str, data: bytes, user: User) -> 'File':
        """Save file to directory and create DB entry for it"""

        file_entry = cls()
        file_entry.user = user
        file_entry.name = name
        file_entry.token = secrets.token_urlsafe(6)  # token_urlsafe(6) produces 8 characters
        file_entry.uploaded_at = datetime.datetime.now()
        file_entry.save()

        dir_path = os.path.join(os.path.realpath(directory), file_entry.token)
        os.makedirs(dir_path)
        full_path = os.path.normpath(os.path.join(dir_path, name))
        if not full_path.startswith(dir_path + os.sep):
            raise FileCreationError(f"{name} doesn't seems like correct file name")

        with open(full_path, 'wb') as file:
            file.write(data)

        return file_entry
