from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from . import __version__
from .emit_yaml import emit_yaml
from .infer import merge_objects


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
        help="Emit key-frequency stats as YAML comments (TODO)",
    )
    args = ap.parse_args()

    data = json.load(sys.stdin)

    # Shape inference
    shape: Any
    if isinstance(data, list):
        if data and isinstance(data[0], dict):
            merged = merge_objects(data, sample_n=args.array_samples, max_array=args.array_samples)
            shape = [merged]
        else:
            # for scalar arrays, show union type only
            # promote to object with single key 'items' for readability
            from .infer import guess_type

            types_set: set[str] = set()
            for it in data[: args.array_samples]:
                for t in guess_type(it):
                    if isinstance(t, str):
                        types_set.add(t)
            ts = sorted(types_set)
            shape = [{"items": f"array<{' | '.join(ts)}>"}]
    elif isinstance(data, dict):
        merged = merge_objects([data], sample_n=args.array_samples, max_array=args.array_samples)
        shape = merged if not args.force_list else [merged]
    else:
        shape = {"value": type(data).__name__.lower()}

    sys.stdout.write(emit_yaml(shape, root=args.root, indent=args.indent))


if __name__ == "__main__":
    main()
