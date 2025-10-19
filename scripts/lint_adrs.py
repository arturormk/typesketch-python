#!/usr/bin/env python3
"""ADR Linter - validates ADR structure and required sections."""

import re
import sys
from pathlib import Path


def lint_adr(adr_file: Path) -> list[str]:
    """Lint a single ADR file and return list of errors."""
    errors = []

    try:
        content = adr_file.read_text()
    except Exception as e:
        return [f"Could not read file: {e}"]

    lines = content.split("\n")

    # Check title format
    if not lines or not re.match(r"^# ADR-\d{4}[–-] .+", lines[0]):
        errors.append("Title must be '# ADR-NNNN – Title' format")

    # Check required sections
    required_sections = ["## Context", "## Decision", "## Consequences"]
    for section in required_sections:
        if section not in content:
            errors.append(f"Missing required section: {section}")

    # Check status line
    status_pattern = r"\*\*Status\*\*:\s*(Proposed|Accepted|Superseded)"
    if not re.search(status_pattern, content):
        errors.append("Missing or invalid Status line")

    # Check date line
    date_pattern = r"\*\*Date\*\*:\s*\d{4}-\d{2}-\d{2}"
    if not re.search(date_pattern, content):
        errors.append("Missing or invalid Date line")

    return errors


def lint_all_adrs() -> int:
    """Lint all ADR files."""
    adr_dir = Path("docs/adr")
    if not adr_dir.exists():
        print("ADR directory docs/adr does not exist", file=sys.stderr)
        return 1

    adr_files = sorted([f for f in adr_dir.glob("ADR-*.md")])
    total_errors = 0

    for adr_file in adr_files:
        errors = lint_adr(adr_file)
        if errors:
            print(f"\n{adr_file.name}:", file=sys.stdout)
            for error in errors:
                print(f"  ✗ {error}", file=sys.stdout)
            total_errors += len(errors)
        else:
            print(f"✓ {adr_file.name}", file=sys.stdout)

    if total_errors > 0:
        print(f"\nFound {total_errors} errors in ADR files", file=sys.stderr)
        return 1

    print(f"\n✓ All {len(adr_files)} ADRs pass validation", file=sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(lint_all_adrs())
