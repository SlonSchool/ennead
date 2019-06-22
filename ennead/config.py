"""App configuration class for Ennead"""

import json
from typing import Dict
from dataclasses import dataclass, field

from peewee import Database, SqliteDatabase, PostgresqlDatabase


@dataclass
class Config:
    """App configuration

    db_type: database driver (currently `postgres` or `sqlite`)
    db_name: database name
    db_params: additional parameters for passing to peewee
    teacher_secret: code for new teacher registration
    """

    DB_TYPE: str = 'sqlite'
    DB_NAME: str = ':memory:'
    DB_PARAMS: Dict[str, str] = field(default_factory=dict)
    TEACHER_SECRET: str = 'muchsecret'
    SECRET_KEY: str = 'boomboomboom'  # For Flask
    UPLOAD_DIR: str = '/tmp/ennead'

    @classmethod
    def from_filename(cls, filename: str) -> 'Config':
        """Read Config params from JSON file"""

        result = cls()
        with open(filename, encoding='utf-8') as config_file:
            config_data = json.load(config_file)
            for key, value in config_data.items():
                setattr(result, key, value)
        return result

    @property
    def DB_CLASS(self) -> Database:  # pylint: disable=invalid-name
        """peewee class representing chosen database"""

        if self.DB_TYPE == 'sqlite':
            return SqliteDatabase
        if self.DB_TYPE in ('postgres', 'postgresql'):
            return PostgresqlDatabase
        raise ValueError("Don't know about database type `{}`".format(self.DB_TYPE))
