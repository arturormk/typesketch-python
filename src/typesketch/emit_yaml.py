from __future__ import annotations

from typing import Any, List


def _to_yaml(obj: Any, indent: int = 0, step: int = 2) -> List[str]:
    sp = " " * (indent * step)
    lines: List[str] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, dict):
                lines.append(f"{sp}{k}:")
                lines.extend(_to_yaml(v, indent + 1, step))
            elif isinstance(v, list):
                lines.append(f"{sp}{k}:")
                for item in v:
                    if isinstance(item, dict):
                        lines.append(f"{sp}{' ' * step}-")
                        lines.extend(_to_yaml(item, indent + 2, step))
                    else:
                        lines.append(f"{sp}{' ' * step}- {item}")
            else:
                lines.append(f"{sp}{k}: {v}")
        return lines
    elif isinstance(obj, list):
        for item in obj:
            if isinstance(item, dict):
                lines.append(f"{sp}-")
                lines.extend(_to_yaml(item, indent + 1, step))
            else:
                lines.append(f"{sp}- {item}")
        return lines
    else:
        lines.append(f"{sp}{obj}")
        return lines


def emit_yaml(shape: Any, root: str | None = None, indent: int = 2) -> str:
    lines: List[str] = []
    if root:
        lines.append(f"{root}:")
        lines.extend(_to_yaml(shape, 1, indent))
    else:
        lines.extend(_to_yaml(shape, 0, indent))
    return "\n".join(lines) + "\n"
