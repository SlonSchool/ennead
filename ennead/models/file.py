"""Module for Ennead file model"""

import os
import uuid

from peewee import CharField, FixedCharField

from ennead.models.base import BaseModel


class FileCreationError(Exception):
    """Error occured while creating file"""


class File(BaseModel):
    """One file, uploaded to server

    Attributes:
        path: real path to file on server
        uuid: file UUID as string
        name: filename as specified on upload
    """

    path: str = CharField()
    uuid: str = FixedCharField(36)
    name: str = CharField()

    @classmethod
    def from_data(cls, directory: str, name: str, data: bytes) -> 'File':
        """Save file to directory and create DB entry for it"""

        file_uuid = str(uuid.uuid4())
        dir_path = os.path.join(os.path.realpath(directory), file_uuid)
        os.mkdir(dir_path)
        full_path = os.path.normpath(os.path.join(dir_path, name))
        if not full_path.startswith(dir_path):
            raise FileCreationError(f"{name} doesn't seems like correct file name")

        with open(full_path, 'wb') as file:
            file.write(data)

        file_entry = cls()
        file_entry.name = name
        file_entry.path = full_path
        file_entry.uuid = file_uuid
        file_entry.save()

        return file_entry
