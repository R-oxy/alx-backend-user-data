#!/usr/bin/env python3
""" password encryption """

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt.

    Args:
        password: The password string to hash.

    Returns:
        bytes: The salted, hashed password as a byte string.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates if provided password matches hashed password using bcrypt.

    Args:
        hashed_password: The hashed password as a byte string.
        password: The plain text password string to validate.

    Returns:
        bool: True if password matches hashed password, False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
