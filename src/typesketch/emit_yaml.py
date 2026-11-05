"""Render an inferred shape (see ``infer``) as type-oriented YAML."""

from __future__ import annotations

import json
import re
from typing import Any, List, Mapping, Sequence

from .infer import Alternatives

# Keys that are safe as plain YAML scalars: a letter or underscore, then
# letters, digits, "_", "." or "-". Anything else is double-quoted.
_PLAIN_KEY = re.compile(r"[^\W\d][\w.-]*")
# Plain words YAML 1.1 or 1.2 would read as booleans or null.
_RESERVED = {"true", "false", "yes", "no", "on", "off", "y", "n", "null"}


def _key(name: str) -> str:
    """Render a mapping key, quoting it when YAML would misread it."""
    if _PLAIN_KEY.fullmatch(name) and name.lower() not in _RESERVED:
        return name
    # A JSON string literal is also a valid YAML double-quoted scalar.
    return json.dumps(name, ensure_ascii=False)


def _scalar(value: Any) -> str:
    # An empty object has no fields to list; call it what it is.
    return "object" if isinstance(value, dict) else str(value)


def _mapping(obj: Mapping[str, Any], level: int, step: int) -> List[str]:
    sp = " " * (level * step)
    if not obj:
        return [f"{sp}object"]
    lines: List[str] = []
    for name, v in obj.items():
        k = _key(name)
        comment = ""
        if isinstance(v, Alternatives):
            # The other types go in a comment: a YAML key can't hold both
            # a block and a scalar. See ADR-0004.
            comment = f"  # also: {v.also}"
            v = v.shape
        if isinstance(v, dict) and v:
            lines.append(f"{sp}{k}:{comment}")
            lines.extend(_mapping(v, level + 1, step))
        elif isinstance(v, list):
            lines.append(f"{sp}{k}:{comment}")
            lines.extend(_sequence(v, level + 1, step))
        else:
            lines.append(f"{sp}{k}: {_scalar(v)}{comment}")
    return lines


def _sequence(items: Sequence[Any], level: int, step: int) -> List[str]:
    sp = " " * (level * step)
    lines: List[str] = []
    for item in items:
        if isinstance(item, dict) and item:
            lines.append(f"{sp}-")
            lines.extend(_mapping(item, level + 1, step))
        elif isinstance(item, list):
            lines.append(f"{sp}-")
            lines.extend(_sequence(item, level + 1, step))
        else:
            lines.append(f"{sp}- {_scalar(item)}")
    return lines


def _to_yaml(obj: Any, level: int, step: int) -> List[str]:
    if isinstance(obj, dict):
        return _mapping(obj, level, step)
    if isinstance(obj, list):
        return _sequence(obj, level, step)
    return [f"{' ' * (level * step)}{obj}"]


def emit_yaml(shape: Any, root: str | None = None, indent: int = 2) -> str:
    lines: List[str] = []
    if root:
        lines.append(f"{_key(root)}:")
        lines.extend(_to_yaml(shape, 1, indent))
    else:
        lines.extend(_to_yaml(shape, 0, indent))
    return "\n".join(lines) + "\n"
