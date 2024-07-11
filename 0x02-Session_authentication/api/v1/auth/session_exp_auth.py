#!/usr/bin/env python3
""" Module of Session Exp Auth
"""

from datetime import datetime, timedelta
from os import getenv

from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """ Session Exp Auth class
    """
    def __init__(self):
        """ Constructor
        """
        self.session_duration = 0

        try:
            self.session_duration = int(getenv("SESSION_DURATION"))
        except Exception:
            pass

    def create_session(self, user_id: str = None) -> str:
        """ Create a Session ID for a user_id
        """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Return a User ID based on a Session ID
        """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        session_dictionary = self.user_id_by_session_id.get(session_id)
        if session_dictionary is None:
            return None
        if "created_at" not in session_dictionary:
            return None
        created_at = session_dictionary.get("created_at")
        if not isinstance(created_at, datetime):
            return None
        if self.session_duration <= 0:
            return session_dictionary.get("user_id")
        if created_at + timedelta(seconds=self.session_duration) < datetime.now():
            return None
        return session_dictionary.get("user_id")