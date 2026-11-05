"""Infer a type shape from example JSON values.

A shape is one of:

- ``str``: a scalar type or union, e.g. ``"int"`` or ``"string | null"``
- ``dict``: an object, mapping each field name to its shape; merged
  objects are ``ObjectShape`` instances, which also record how many of the
  merged objects had each field
- ``list``: an array, holding one shape per kind of item seen (object,
  array, scalars), in that order
- ``Alternatives``: an object or array shape that is sometimes replaced by
  other types, e.g. an object that is sometimes ``null``

Every value a field takes, in every record, contributes to its shape. See
ADR-0003 (heuristics) and ADR-0004 (merge rules).
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Sequence, Tuple, Union

from .detectors import detect_string_format

DEFAULT_SAMPLES = 200


class ObjectShape(Dict[str, "Shape"]):
    """Merged object shape that also records how often each field appeared.

    ``presence[field]`` is the number of merged objects that had the field,
    out of ``total`` objects merged. See ADR-0006.
    """

    def __init__(self, fields: Dict[str, Shape], presence: Dict[str, int], total: int) -> None:
        super().__init__(fields)
        self.presence = presence
        self.total = total


@dataclass(frozen=True)
class Alternatives:
    """An object or array shape plus the other types the value sometimes has."""

    shape: Union[Dict[str, Shape], List[Shape]]
    also: str


Shape = Union[str, Dict[str, "Shape"], List["Shape"], Alternatives]

_TYPE_ORDER = [
    "string",
    "int",
    "number",
    "boolean",
    "null",
    "url",
    "email",
    "datetime",
    "html-string",
    "unknown",
    "array",
]


def _type_sort_key(t: str) -> Tuple[int, str]:
    try:
        idx = _TYPE_ORDER.index(t)
    except ValueError:
        idx = len(_TYPE_ORDER)
    return (idx, t)


def _union_str(types: Iterable[str]) -> str:
    ts = sorted(set(types), key=_type_sort_key)
    return " | ".join(ts) if ts else "unknown"


def scalar_type(value: Any) -> str:
    """Type name of a JSON scalar (anything that isn't an object or array)."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "int"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return detect_string_format(value)
    return "unknown"


def _partition(
    values: Iterable[Any],
) -> Tuple[List[Dict[str, Any]], List[List[Any]], List[str]]:
    """Split values into objects, arrays and scalar type names."""
    objs: List[Dict[str, Any]] = []
    arrays: List[List[Any]] = []
    scalars: List[str] = []
    for v in values:
        if isinstance(v, dict):
            objs.append(v)
        elif isinstance(v, list):
            arrays.append(v)
        else:
            scalars.append(scalar_type(v))
    return objs, arrays, scalars


def array_shape(arrays: Sequence[List[Any]], max_array: int = DEFAULT_SAMPLES) -> List[Shape]:
    """Merged shape of several arrays that hold the same kind of items.

    Up to ``max_array`` items are sampled from each array. The result has one
    entry per kind of item seen: the merged object shape, the merged nested
    array shape, then the union of scalar types.
    """
    items = [it for arr in arrays for it in arr[:max_array]]
    if not items:
        return ["unknown"]
    objs, nested, scalars = _partition(items)
    out: List[Shape] = []
    if objs:
        out.append(merge_objects(objs, sample_n=len(objs), max_array=max_array))
    if nested:
        out.append(array_shape(nested, max_array=max_array))
    if scalars:
        out.append(_union_str(scalars))
    return out


def infer_values(values: Sequence[Any], max_array: int = DEFAULT_SAMPLES) -> Shape:
    """Shape of a field that took each of ``values`` across records."""
    objs, arrays, scalars = _partition(values)
    primary: Union[Dict[str, Shape], List[Shape]]
    if objs:
        primary = merge_objects(objs, sample_n=len(objs), max_array=max_array)
        others = (["array"] if arrays else []) + scalars
    elif arrays:
        primary = array_shape(arrays, max_array=max_array)
        others = scalars
    else:
        return _union_str(scalars)
    return Alternatives(primary, _union_str(others)) if others else primary


def merge_objects(
    objs: Sequence[Dict[str, Any]],
    sample_n: int = DEFAULT_SAMPLES,
    max_array: int = DEFAULT_SAMPLES,
) -> ObjectShape:
    """Merge the first ``sample_n`` objects into one shape.

    Fields are ordered by how many objects have them, then alphabetically.
    """
    key_counts: Counter[str] = Counter()
    field_vals: defaultdict[str, List[Any]] = defaultdict(list)
    sampled = objs[:sample_n]
    for o in sampled:
        for k, v in o.items():
            key_counts[k] += 1
            field_vals[k].append(v)

    keys = sorted(field_vals, key=lambda k: (-key_counts[k], k))
    fields = {k: infer_values(field_vals[k], max_array=max_array) for k in keys}
    return ObjectShape(fields, dict(key_counts), len(sampled))
