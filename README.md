# TypeSketch — infer a type‑oriented YAML from JSON
> A tiny CLI that reads JSON from stdin and emits a concise, type‑oriented YAML **TypeSketch** — perfect for docs, quick API archeology, and codegen stubs.

[![CI](https://github.com/arturormk/typesketch-python/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/arturormk/typesketch-python/actions/workflows/ci.yml) ![license](https://img.shields.io/badge/license-MIT-green)

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

Example output (the live API's data changes, so yours may differ slightly):

```yaml
docs:
  -
    author_key:
      - string
    author_name:
      - string
    cover_i: int
    ebook_access: string
    edition_count: int
    first_publish_year: int
    has_fulltext: boolean
    ia:
      - string
    key: string
    language:
      - string
    public_scan_b: boolean
    title: string
    cover_edition_key: string
    ia_collection:
      - string
    lending_edition_s: string
    lending_identifier_s: string
    subtitle: string
    cover_height: int
    cover_width: int
documentation_url: url
numFound: int
numFoundExact: boolean
num_found: int
offset: null
q: string
start: int
```

That’s a concise “type sketch” of the response — handy for docs, quick API archaeology, or bootstrapping code. Add `--stats` to see which fields are optional, e.g. `subtitle: string  # present in 2 of 5`.

## Features
- Infer scalar/union types and simple format hints (url, email, datetime, html-string)
- Merge every record into one shape, with fields sorted by how often they appear
- Expand arrays of objects as proper YAML lists, including nested arrays and arrays that mix objects and scalars
- Show fields that are sometimes an object and sometimes something else (often `null`) as `# also: null`
- Optional presence stats (`--stats`) for fields missing from some records
- Valid YAML output: keys that need it are quoted
- Clear one-line errors for invalid or empty input
- Configurable array sampling and indentation
- Zero-deps runtime (only Python stdlib)

## Quickstart
TypeSketch isn't on PyPI yet; install it from a clone:

```bash
git clone https://github.com/arturormk/typesketch-python
cd typesketch-python
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

## Reading the output
Records are merged into one shape. Fields present in every record come first; a field that changes type between records gets a union, and a field that is an object in some records and something else in others keeps its object shape with the other types in a comment. With `--stats`, optional fields say how many of the merged objects had them:

```bash
echo '[{"id":1,"owner":{"name":"Ana"}},{"id":2,"owner":null,"note":"x"}]' \
  | typesketch --stats
```

```yaml
-
  id: int
  owner:  # also: null
    name: string
  note: string  # present in 1 of 2
```

Comments are ignored by YAML parsers, so a tool that loads the sketch sees only the shapes. The rules are documented in [ADR-0004](docs/adr/ADR-0004-shape-merging.md), [ADR-0005](docs/adr/ADR-0005-key-quoting-and-input-errors.md) and [ADR-0006](docs/adr/ADR-0006-presence-stats.md).

## CLI
```bash
# Read JSON from stdin
curl https://api.example.com/shops | typesketch

# Use a custom root key and show which fields are optional
cat data.json | typesketch --root Shops --stats

# Treat single object as a one-item list
cat item.json | typesketch --force-list

# Sample up to 50 items per array, indent with 4 spaces
cat big.json | typesketch --array-samples 50 --indent 4
```

Invalid input prints a one-line `typesketch: error: ...` message on stderr and exits with status 1. See `typesketch --help`.

## Software Curator Principles
- **Curation-first**: ADRs under `docs/adr/` document naming, heuristics, and trade-offs.
- **Reproducible**: Unit tests and golden fixtures in `tests/`.
- **Auditable**: Minimal, readable functions with explicit heuristics and TODOs for future refinement.
- **Extendable**: Clear seams for adding new detectors (currency, color-hex, uuid, etc.).

## Roadmap
- [ ] JSON Schema / OpenAPI emitters
- [x] Presence stats (`--stats`)
- [ ] Requiredness in JSON Schema / OpenAPI output
- [ ] Friendly collapse rules for very deep objects
- [ ] YAML → Markdown renderer for docs sites
- [ ] Pluggable detector registry
- [ ] Streaming mode for very large inputs

## License
MIT — see `LICENSE`.

## Attribution & Curation
This project is AI-assisted and human-curated. Significant changes are documented via ADRs and validated by tests. See [ADR-0010](docs/adr/ADR-0010-ai-curation-policy.md) for the AI curation policy. Maintainers are listed in `AUTHORS`.
