# TypeSketch — infer a type‑oriented YAML from JSON
> A tiny CLI that reads JSON from stdin and emits a concise, type‑oriented YAML **TypeSketch** — perfect for docs, quick API archeology, and codegen stubs.

![status-badge](https://img.shields.io/badge/status-experimental-blue) ![license](https://img.shields.io/badge/license-MIT-green)

## Why
When exploring unfamiliar APIs, we often need a *human‑readable* schema sketch rather than a full JSON Schema. TypeSketch summarizes field shapes, union types, and common formats (url, datetime, email, html-string) directly from example payloads.

## Features
- Infer scalar/union types and simple format hints
- Expand arrays of objects as proper YAML lists (no angle‑brackets)
- Merge multiple objects into a unified shape sorted by field popularity
- Configurable array sampling, depth, and indentation
- Zero-deps runtime (only Python stdlib)

## Quickstart
```bash
pipx install .   # or: pip install -e .
echo '{"id":1,"name":"X","tags":["a",2],"url":"https://x"}' | typesketch --root item
```

Output:
```yaml
item:
  id: int
  name: string
  tags:
    - string | int
  url: url
```

## CLI
```bash
# Read JSON from stdin
curl https://api.example.com/shops | typesketch

# Use a custom root key and show stats
cat data.json | typesketch --root Shops --stats

# Treat single object as a one-item list
cat item.json | typesketch --force-list
```

See `typesketch --help`.

## Software Curator Principles
- **Curation-first**: ADRs under `docs/adr/` document naming, heuristics, and trade-offs.
- **Reproducible**: Unit tests and golden fixtures in `tests/`.
- **Auditable**: Minimal, readable functions with explicit heuristics and TODOs for future refinement.
- **Extendable**: Clear seams for adding new detectors (currency, color-hex, uuid, etc.).

## Roadmap
- [ ] JSON Schema / OpenAPI emitters
- [ ] Presence/requiredness stats
- [ ] Friendly collapse rules for very deep objects
- [ ] YAML → Markdown renderer for docs sites
- [ ] Pluggable detector registry
- [ ] Streaming mode for very large inputs

## License
MIT — see `LICENSE`.
