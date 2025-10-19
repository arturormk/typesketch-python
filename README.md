# TypeSketch — infer a type‑oriented YAML from JSON
> A tiny CLI that reads JSON from stdin and emits a concise, type‑oriented YAML **TypeSketch** — perfect for docs, quick API archeology, and codegen stubs.

![status-badge](https://img.shields.io/badge/status-experimental-blue) ![license](https://img.shields.io/badge/license-MIT-green)

## Why
When exploring unfamiliar APIs, we often need a *human‑readable* schema sketch rather than a full JSON Schema. TypeSketch summarizes field shapes, union types, and common formats (url, datetime, email, html-string) directly from example payloads.

## TL;DR
Quick taste using a free, real API (no install needed, run the module directly):

```bash
git clone https://github.com/arturormk/typesketch-python
cd typesketch-python/src

# Pipe Open Library search results directly into the CLI module
curl -s 'https://openlibrary.org/search.json?q=python&limit=5' | python3 -m typesketch.cli
```

Example output:

```yaml
docs:
  -
    author_key:
      - string
    author_name:
      - string
    cover_edition_key: string
    cover_i: int
    ebook_access: string
    edition_count: int
    first_publish_year: int
    has_fulltext: boolean
    key: string
    language:
      - string
    public_scan_b: boolean
    title: string
    ia:
      - string
    ia_collection_s: string
    lending_edition_s: string
    lending_identifier_s: string
    subtitle: string
documentation_url: url
numFound: int
numFoundExact: boolean
num_found: int
offset: null
q: string
start: int
```

That’s a concise “type sketch” of the response — handy for docs, quick API archaeology, or bootstrapping code.

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

## Attribution & Curation
This project is AI-assisted and human-curated. Significant changes are documented via ADRs and validated by tests. See [ADR-0010](docs/adr/ADR-0010-ai-curation-policy.md) for the AI curation policy. Maintainers are listed in `AUTHORS`.
