#!/usr/bin/env python3
"""
Module for obfuscating log messages and custom log formatter
"""

import logging
import re
from typing import List
import os
import mysql.connector

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Obfuscates log messages.
    """
    pattern = '|'.join([f'{field}=[^{separator}]*' for field in fields])
    return re.sub(
        pattern, lambda m: f'{m.group().split("=")[0]}={redaction}', message)


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats log records to filter PII fields.
        """
        original = super().format(record)
        return filter_datum(self.fields, self.REDACTION, original,
                            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    Creates a logging.Logger instance named "user_data".
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ returns a connector to the database """
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    dbname = os.getenv('PERSONAL_DATA_DB_NAME')

    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=dbname
    )
