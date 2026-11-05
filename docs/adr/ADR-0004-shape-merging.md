# ADR-0004– Shape Merging Across Records

**Status**: Proposed
**Date**: 2026-11-05

## Context

ADR-0003 says shapes from many records are merged, but v0.1.0 lost
information in several cases:

- When an array of objects appeared in several records, only the last
  record's array was kept, so fields seen only in earlier records vanished.
- A field that was an object in some records and a scalar (often `null`) in
  others showed only the object; the scalar types were dropped.
- Arrays mixing objects and scalars dropped the scalars; arrays of arrays
  became `unknown`.
- A top-level array was classified by its first element only, and a
  top-level array of scalars was printed as `items: array<...>`, unlike
  arrays everywhere else.

## Decision

Every value a field takes, in every sampled record, contributes to its
shape:

- **Objects** seen for a field are merged into one object shape, recursively.
- **Arrays** seen for a field are pooled (up to `--array-samples` items from
  each) and their items merged as one array.
- **Array items** produce one list entry per kind seen, in this order: the
  merged object shape, the merged nested-array shape, then the union of
  scalar types. Example: `[{"x": 1}, 5]` becomes `- {x: int}` and `- int`.
- **Mixed fields**: if a field is an object (or array) in some records and
  something else in others, the object (else the array) is shown, and the
  other types are given in a YAML comment on the key line, e.g.
  `owner:  # also: null`. An array alongside an object is reported as
  `array` in that comment, without its shape.
- **Top level**: a JSON array is treated exactly like an array field, so
  `[1, "a"]` gives `- string | int`. A top-level scalar gives
  `value: <type>`, using the same type names as everywhere else.
- **Empty objects** are shown as `object` rather than an empty key.

Exact expected outputs are kept as golden fixtures in `tests/golden/`.

## Consequences

**Positive:**
- No field or type seen in the sample is silently dropped.
- Output stays valid YAML: alternatives live in comments, not in the
  structure.
- Golden fixtures make output changes visible in review.

**Negative / Trade-offs:**
- Changes output for top-level scalar arrays (`items: array<...>` is gone)
  and for top-level scalars (`value: str` becomes `value: string`).
- Information in comments is lost by YAML parsers; tools that consume the
  sketch see only the object or array shape.
- When a field is both an object and an array, the array's shape is not
  shown.

**Follow-ups:**
- Consider a structured representation for alternatives when JSON Schema /
  OpenAPI emitters are added.
