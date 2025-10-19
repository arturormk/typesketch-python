#!/usr/bin/env python3
"""Check for raw print() statements that don't specify file parameter."""

import re
import sys
from pathlib import Path


def check_prints_in_file(file_path: Path) -> list[str]:
    """Check a Python file for raw print() statements."""
    if file_path.suffix != ".py":
        return []

    try:
        content = file_path.read_text()
    except Exception:
        return []

    violations = []
    lines = content.split("\n")

    for i, line in enumerate(lines, 1):
        # Skip comments and strings
        if line.strip().startswith("#") or '"""' in line or "'''" in line:
            continue

        # Look for print( without file= parameter
        if re.search(r"\bprint\s*\(", line) and "file=" not in line:
            violations.append(f"Line {i}: {line.strip()}")

    return violations


def check_all_prints() -> int:
    """Check all Python files for print violations."""
    violations = []

    for py_file in Path(".").rglob("*.py"):
        # Skip __pycache__ and .venv directories
        if "__pycache__" in str(py_file) or ".venv" in str(py_file):
            continue

        file_violations = check_prints_in_file(py_file)
        if file_violations:
            violations.append((py_file, file_violations))

    if violations:
        print("Found print() statements without file= parameter:", file=sys.stderr)
        for file_path, file_violations in violations:
            print(f"\n{file_path}:", file=sys.stderr)
            for violation in file_violations:
                print(f"  {violation}", file=sys.stderr)
        print("\nUse print(..., file=sys.stdout) or print(..., file=sys.stderr)", file=sys.stderr)
        return 1

    print("✓ No raw print() statements found", file=sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(check_all_prints())
