#!/usr/bin/env python3
"""
Module for obfuscating log messages
"""

import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Obfuscates log messages.
    """
    pattern = '|'.join([f'{field}=[^{separator}]*' for field in fields])
    return re.sub(
        pattern, lambda m: f'{m.group().split("=")[0]}={redaction}', message)
