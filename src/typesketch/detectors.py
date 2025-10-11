from __future__ import annotations
import re

RE_URL = re.compile(r'^https?://', re.I)
RE_EMAIL = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')
RE_ISO_DT = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}')

def detect_string_format(s: str) -> str:
    if RE_URL.match(s):
        return "url"
    if RE_EMAIL.match(s):
        return "email"
    if RE_ISO_DT.match(s):
        return "datetime"
    if "<" in s and ">" in s and "/" in s:
        return "html-string"
    return "string"
