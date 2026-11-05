from __future__ import annotations

import argparse
import json
import sys
from typing import Any, NoReturn

from . import __version__
from .emit_yaml import emit_yaml
from .infer import Shape, array_shape, merge_objects, scalar_type


def sketch(
    data: Any,
    root: str | None = None,
    force_list: bool = False,
    array_samples: int = 200,
    indent: int = 2,
    stats: bool = False,
) -> str:
    """Return the TypeSketch YAML for one parsed JSON document."""
    shape: Shape
    if isinstance(data, list):
        shape = array_shape([data], max_array=array_samples)
    elif isinstance(data, dict):
        merged = merge_objects([data], sample_n=array_samples, max_array=array_samples)
        shape = [merged] if force_list else merged
    else:
        shape = {"value": scalar_type(data)}
    return emit_yaml(shape, root=root, indent=indent, stats=stats)


def main() -> None:
    ap = argparse.ArgumentParser(
        description=("Emit a TypeSketch (type-oriented YAML) from JSON on stdin.")
    )
    ap.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    ap.add_argument("--root", help="Wrap output under this root key")
    ap.add_argument(
        "--force-list",
        action="store_true",
        help="Treat single-object input as a one-item list",
    )
    ap.add_argument("--array-samples", type=int, default=200, help="Max array items to sample")
    ap.add_argument("--indent", type=int, default=2, help="Spaces per indent")
    ap.add_argument(
        "--stats",
        action="store_true",
        help="Note fields missing from some records, as '# present in N of M' comments",
    )
    args = ap.parse_args()

    try:
        text = sys.stdin.buffer.read().decode("utf-8-sig")
        if not text.strip():
            _fail("no JSON on stdin")
        data = json.loads(text)
        out = sketch(
            data,
            root=args.root,
            force_list=args.force_list,
            array_samples=args.array_samples,
            indent=args.indent,
            stats=args.stats,
        )
    except UnicodeDecodeError as e:
        _fail(f"input is not valid UTF-8 ({e.reason} at byte {e.start})")
    except json.JSONDecodeError as e:
        _fail(f"invalid JSON on stdin: {e.msg} (line {e.lineno}, column {e.colno})")
    except RecursionError:
        _fail("input is nested too deeply")
    sys.stdout.write(out)


def _fail(message: str) -> NoReturn:
    sys.stderr.write(f"typesketch: error: {message}\n")
    sys.exit(1)


if __name__ == "__main__":
    main()
