#!/usr/bin/env python3
"""Authentication module for handling user authorization."""

from typing import List, TypeVar

class Auth():
    """Handles authentication and authorization."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if authentication is required for a given path.

        Args:
            path (str): The path to check for authentication requirement.
            excluded_paths (List[str]): List of paths excluded from authentication.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is None or excluded_paths is None or not len(excluded_paths):
            return True
        if path[-1] != '/':
            path += '/'
        for item in excluded_paths:
            if item.endswith('*'):
                if path.startswith(item[:-1]):
                    return False
        if path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """Extracts the authorization header from a given request.

        Args:
            request (request object, optional): The request object containing headers.

        Returns:
            str: The authorization header value, or None if not found.
        """
        if request is None or not request.headers.get("Authorization"):
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns the current user based on the request.

        Args:
            request (request object, optional): The request object.

        Returns:
            TypeVar('User'): The current user object or None if not authenticated.
        """
        return None
