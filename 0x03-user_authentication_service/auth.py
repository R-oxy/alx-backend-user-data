#!/usr/bin/env python3
"""hash user password"""

from typing import Union
import uuid
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User


class Auth:
    """Authentication class to interact with the auth database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers and returns the user."""
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            pwd = _hash_password(password)
            return self._db.add_user(email, pwd)

    def valid_login(self, email: str, password: str) -> bool:
        """Validates user password."""
        try:
            usr = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  usr.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Creates a session ID."""
        try:
            usr = self._db.find_user_by(email=email)
            self._db.update_user(usr.id, session_id=_generate_uuid())
            return usr.session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Returns the User or None for the given session ID."""
        if session_id is None:
            return None
        try:
            usr = self._db.find_user_by(session_id=session_id)
            return usr
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroys a user's session."""
        self._db.update_user(user_id=user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """Generates and returns a reset token."""
        try:
            usr = self._db.find_user_by(email=email)
            rest_tok = _generate_uuid()
            self._db.update_user(usr.id, reset_token=rest_tok)
            return rest_tok
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates the user's password."""
        try:
            usr = self._db.find_user_by(reset_token=reset_token)
            new_p = _hash_password(password)
            self._db.update_user(usr.id, hashed_password=new_p)
            self._db.update_user(usr.id, reset_token=None)
        except NoResultFound:
            raise ValueError


def _hash_password(password: str) -> bytes:
    """Hashes a password."""
    hash_p = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
    return hash_p


def _generate_uuid() -> str:
    """Generates and returns a UUID string."""
    return str(uuid.uuid4())
