#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"

# Choose command: prefer installed console script; otherwise use module with local src
if command -v typesketch >/dev/null 2>&1; then
	CMD=(typesketch)
else
	PY_BIN="python3"
	if ! command -v "$PY_BIN" >/dev/null 2>&1; then
		PY_BIN="python"
	fi
	export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
	CMD=("$PY_BIN" -m typesketch.cli)
fi

cat "$HERE/poi.json" | "${CMD[@]}" --root POIs
