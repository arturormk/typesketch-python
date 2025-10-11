#!/usr/bin/env bash
set -euo pipefail
cat "$(dirname "$0")/poi.json" | typesketch --root POIs
