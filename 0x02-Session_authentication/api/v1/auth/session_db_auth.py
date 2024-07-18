#!/usr/bin/env python3
""" Module of Session DB Auth
"""

from datetime import datetime, timedelta
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ Session DB Auth class
    """
    def create_session(self, user_id: str = None) -> str:
        """ Create a Session ID for a user_id
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        kwargs = {'user_id': user_id, 'session_id': session_id}
        session = UserSession(**kwargs)
        session.save()
        UserSession.save_to_file()
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Return a User ID based on a Session ID
        """
        if session_id is None:
            return None
        UserSession.load_from_file()
        session = UserSession.search({"session_id": session_id})
        if not session:
            return None
        session = session[0]
        expired_time = session.created_at + timedelta(
            seconds=self.session_duration)
        if expired_time < datetime.now():
            return None
        return session.user_id

    def destroy_session(self, request=None) -> bool:
        """ Destroy a Session ID
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        session = UserSession.search({"session_id": session_id})
        if not session:
            return False
        session = session[0]
        try:
            session.remove()
            UserSession.save_to_file()
        except Exception:
            return False
        return True
