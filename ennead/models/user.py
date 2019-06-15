"""Module for Ennead user model and corresponding helper classes"""

import hashlib
import secrets
import datetime
from enum import IntEnum

from peewee import CharField, DateField, IntegerField, FixedCharField

from ennead.models.base import BaseModel


class UserGroup(IntEnum):
    """Enum of possible user groups

    Attributes:
        teacher: has admin privileges, can create and modify tasks
        student: can only submit tasks
    """

    teacher = 0
    student = 1


class User(BaseModel):
    """System user, either teacher or student

    Attributes:
        username: used to log in
        email: email address used for notifications
        group: is user teacher or student
        password_sha512: salted sha512 of user password
        password_salt: salt, used for password hashing
    """

    username: str = CharField(32, unique=True)
    email: str = CharField(null=True)
    registered_at: datetime.datetime = DateField()
    first_name: str = CharField()
    surname: str = CharField()
    patronym: str = CharField(null=True)
    group: UserGroup = IntegerField()
    password_sha512: str = FixedCharField(128)
    password_salt: str = FixedCharField(32)

    def _hash_password(self, password: str) -> str:
        """Hash password using stored salt"""

        hashed_password = hashlib.sha512()
        hashed_password.update(password.encode('utf-8'))
        hashed_password.update(self.password_salt.encode('utf-8'))
        return hashed_password.hexdigest()

    def set_password(self, new_password: str) -> None:
        """Generate salt and set new password for `User`"""

        self.password_salt = secrets.token_urlsafe(32)
        self.password_sha512 = self._hash_password(new_password)

    def check_password(self, password: str) -> bool:
        """Safely check password for correctness"""

        return secrets.compare_digest(
            self._hash_password(password),
            self.password_sha512
        )

    @property
    def is_teacher(self) -> bool:
        """Check is user a teacher"""

        return self.group == UserGroup.teacher
