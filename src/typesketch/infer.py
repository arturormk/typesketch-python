from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any, Dict, Iterable, List, Tuple, Union, cast

from .detectors import detect_string_format

# e.g., "int" or ("object", {...}) or ("array<object>", {...}) or
# ("array<scalar>", "int | string")
TypeMarker = Union[str, Tuple[str, Dict[str, Any]], Tuple[str, str]]


def _type_sort_key(t: str) -> Tuple[int, str]:
    order = [
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
    ]
    try:
        idx = order.index(t)
    except ValueError:
        idx = len(order)
    return (idx, t)


def _union_str(types: Iterable[str]) -> str:
    ts = sorted(set(types), key=_type_sort_key)
    return " | ".join(ts) if len(ts) > 1 else (ts[0] if ts else "unknown")


def guess_type(value: Any, max_array: int = 200) -> List[TypeMarker]:
    if value is None:
        return ["null"]
    if isinstance(value, bool):
        return ["boolean"]
    if isinstance(value, int):
        return ["int"]
    if isinstance(value, float):
        return ["number"]
    if isinstance(value, str):
        return [detect_string_format(value)]
    if isinstance(value, list):
        items = value[:max_array]
        if not items:
            return [("array<scalar>", "unknown")]
        tlist: List[TypeMarker] = []
        obj_items = []
        for it in items:
            it_types = guess_type(it, max_array=max_array)
            tlist.extend(it_types)
            if isinstance(it, dict):
                obj_items.append(it)
        if obj_items:
            merged = merge_objects(obj_items, max_array=max_array)
            return [("array<object>", merged)]
        else:
            # collapse scalar unions inside array
            leaf_types = [t for t in tlist if isinstance(t, str)]
            return [("array<scalar>", _union_str(leaf_types))]
    if isinstance(value, dict):
        return [("object", value)]
    return ["unknown"]


def merge_objects(
    objs: List[Dict[str, Any]],
    sample_n: int = 200,
    max_array: int = 200,
) -> Dict[str, Any]:
    key_counts: Counter[str] = Counter()
    field_vals: defaultdict[str, List[Any]] = defaultdict(list)

    for o in objs[:sample_n]:
        if not isinstance(o, dict):
            continue
        for k, v in o.items():
            key_counts[k] += 1
            field_vals[k].append(v)

    keys = sorted(field_vals.keys(), key=lambda k: (-key_counts[k], k))
    merged: Dict[str, Any] = {}
    for k in keys:
        vals = field_vals[k]
        local_types: set[str] = set()
        object_shapes: List[Dict[str, Any]] = []
        array_object_shape: Dict[str, Any] | None = None
        scalar_array_inner_types: set[str] = set()
        for v in vals:
            tset = guess_type(v, max_array=max_array)
            for t in tset:
                if isinstance(t, tuple) and t[0] == "object":
                    object_shapes.append(cast(Dict[str, Any], t[1]))
                elif isinstance(t, tuple) and t[0] == "array<object>":
                    array_object_shape = cast(Dict[str, Any], t[1])
                elif isinstance(t, tuple) and t[0] == "array<scalar>":
                    # t[1] is a union string like "int | string"
                    for inner in map(str.strip, cast(str, t[1]).split("|")):
                        if inner:
                            scalar_array_inner_types.add(inner)
                elif isinstance(t, str):
                    local_types.add(t)
        if object_shapes:
            merged[k] = merge_objects(object_shapes, sample_n=sample_n, max_array=max_array)
        elif array_object_shape is not None:
            merged[k] = [array_object_shape]  # list with merged item shape
        elif scalar_array_inner_types:
            merged[k] = [" | ".join(sorted(scalar_array_inner_types, key=_type_sort_key))]
        else:
            merged[k] = _union_str(local_types) if local_types else "unknown"
    return merged
