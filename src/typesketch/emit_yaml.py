"""Render an inferred shape (see ``infer``) as type-oriented YAML."""

from __future__ import annotations

from typing import Any, List, Mapping, Sequence

from .infer import Alternatives


def _scalar(value: Any) -> str:
    # An empty object has no fields to list; call it what it is.
    return "object" if isinstance(value, dict) else str(value)


def _mapping(obj: Mapping[str, Any], level: int, step: int) -> List[str]:
    sp = " " * (level * step)
    if not obj:
        return [f"{sp}object"]
    lines: List[str] = []
    for k, v in obj.items():
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
        lines.append(f"{root}:")
        lines.extend(_to_yaml(shape, 1, indent))
    else:
        lines.extend(_to_yaml(shape, 0, indent))
    return "\n".join(lines) + "\n"
