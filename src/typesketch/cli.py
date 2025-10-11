from __future__ import annotations
import sys, json, argparse
from typing import Any, Dict, List
from .infer import merge_objects
from .emit_yaml import emit_yaml

def main() -> None:
    ap = argparse.ArgumentParser(description="Emit a TypeSketch (type-oriented YAML) from JSON on stdin.")
    ap.add_argument('--root', help='Wrap output under this root key')
    ap.add_argument('--force-list', action='store_true', help='Treat single-object input as a one-item list')
    ap.add_argument('--array-samples', type=int, default=200, help='Max array items to sample')
    ap.add_argument('--indent', type=int, default=2, help='Spaces per indent')
    ap.add_argument('--stats', action='store_true', help='Emit key-frequency stats as YAML comments (TODO)')
    args = ap.parse_args()

    data = json.load(sys.stdin)

    # Shape inference
    if isinstance(data, list):
        if data and isinstance(data[0], dict):
            merged = merge_objects(data, sample_n=args.array_samples, max_array=args.array_samples)
            shape = [merged]
        else:
            # for scalar arrays, show union type only
            # promote to object with single key 'items' for readability
            from .infer import guess_type
            tset = set()
            for it in data[:args.array_samples]:
                tset |= guess_type(it)
            ts = [t for t in tset if isinstance(t, str)]
            shape = [{ 'items': f"array<{' | '.join(sorted(ts))}>" }]
    elif isinstance(data, dict):
        merged = merge_objects([data], sample_n=args.array_samples, max_array=args.array_samples)
        shape = merged if not args.force_list else [merged]
    else:
        shape = {'value': type(data).__name__.lower()}

    sys.stdout.write(emit_yaml(shape, root=args.root, indent=args.indent))

if __name__ == '__main__':
    main()
