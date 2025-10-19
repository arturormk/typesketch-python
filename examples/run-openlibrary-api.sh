#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"

# Fetch a free open API sample with real data (Open Library)
# Search for books about "python" and limit to 20 results
# Docs: https://openlibrary.org/developers/api
curl -s 'https://openlibrary.org/search.json?q=python&limit=20' \
  | "$HERE/typesketch"
