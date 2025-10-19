#!/usr/bin/env bash
"""Fast test subset for pre-commit/pre-push."""

set -euo pipefail

echo "Running fast test subset..."

# Run a subset of critical tests only
python -m pytest tests/test_cli_smoke.py::test_scalar_and_array_unions -v

echo "✓ Fast tests passed"