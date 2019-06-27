"""App configuration class for Ennead"""

import os
import json
from typing import Dict, Union
from dataclasses import dataclass, field, fields
from urllib.parse import urlparse

from peewee import Database, SqliteDatabase, PostgresqlDatabase


@dataclass
class Config:  # pylint: disable=invalid-name
    """App configuration

    db_type: database driver (currently `postgres` or `sqlite`)
    db_name: database name
    db_params: additional parameters for passing to peewee
    teacher_secret: code for new teacher registration
    """

    DB_TYPE: str = 'sqlite'
    DB_NAME: str = ':memory:'
    DB_PARAMS: Dict[str, Union[str, int, None]] = field(default_factory=dict)
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

    @classmethod
    def from_env(cls) -> 'Config':
        """Read Config params from system environment"""

        result = cls()
        for config_field in fields(result):
            # TODO: handling non-str fields
            if config_field.type == str:
                setattr(
                    result,
                    config_field.name,
                    os.environ.get(config_field.name, getattr(cls, config_field.name))
                )
        if os.environ.get('DATABASE_URL'):
            parsed_url = urlparse(os.environ['DATABASE_URL'])
            result.DB_TYPE = parsed_url.scheme
            result.DB_NAME = parsed_url.path[1:]  # Stripping leading slash
            result.DB_PARAMS = {
                'user': parsed_url.username,
                'password': parsed_url.password,
                'host': parsed_url.hostname,
                'port': (int(parsed_url.port) if parsed_url.port else None)
            }
        return result

    @property
    def DB_CLASS(self) -> Database:
        """peewee class representing chosen database"""

        if self.DB_TYPE == 'sqlite':
            return SqliteDatabase
        if self.DB_TYPE in ('postgres', 'postgresql'):
            return PostgresqlDatabase
        raise ValueError("Don't know about database type `{}`".format(self.DB_TYPE))
