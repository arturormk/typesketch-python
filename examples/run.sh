#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
echo "[DEPRECATED] examples/run.sh has been renamed to examples/run-poi_json.sh" 1>&2
exec "$HERE/run-poi_json.sh"
