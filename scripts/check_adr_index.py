#!/usr/bin/env python3
"""ADR Index Checker - ensures all ADRs are included in the index."""

import sys
from pathlib import Path


def check_adr_index() -> int:
    """Check that all ADR files are listed in the index."""
    adr_dir = Path("docs/adr")
    if not adr_dir.exists():
        print("ADR directory docs/adr does not exist", file=sys.stderr)
        return 1

    index_file = adr_dir / "README.md"
    if not index_file.exists():
        print("ADR index file docs/adr/README.md does not exist", file=sys.stderr)
        return 1

    # Find all ADR files
    adr_files = sorted([f for f in adr_dir.glob("ADR-*.md")])

    # Read index content
    index_content = index_file.read_text()

    # Check each ADR is referenced in index
    missing = []
    for adr_file in adr_files:
        if adr_file.name not in index_content:
            missing.append(adr_file.name)

    if missing:
        print(f"ADRs missing from index: {', '.join(missing)}", file=sys.stderr)
        return 1
    
    print(f"✓ All {len(adr_files)} ADRs are indexed", file=sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(check_adr_index())
