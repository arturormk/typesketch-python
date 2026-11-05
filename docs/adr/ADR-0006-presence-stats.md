# ADR-0006– Presence Stats

**Status**: Proposed
**Date**: 2026-11-05

## Context

v0.1.0 accepted a `--stats` flag ("key-frequency stats as YAML comments")
that did nothing. When records are merged into one shape (ADR-0004), the
sketch shows every field but not which ones are optional, which is often
the first thing you need to know about an unfamiliar API. The roadmap lists
"Presence/requiredness stats".

## Decision

With `--stats`, every field that is missing from some of the objects merged
into its shape gets a comment on its key line:

```yaml
coupon: null  # present in 1 of 2
```

- Counts are per merged object shape: `N` is how many of the merged objects
  had the key, `M` how many objects were merged (after `--array-samples`
  sampling). For an array of objects pooled across records, `M` counts the
  pooled items, not the records.
- A key that is present with value `null` counts as present; `null` shows
  up in the type instead.
- Fields present in every object get no comment, to keep the output short.
- When a key already has an `also:` comment, both notes share one comment,
  separated by `; `, e.g. `owner:  # also: null; present in 2 of 3`.
- Without `--stats`, output is unchanged.

Merged objects carry their counts as an `ObjectShape` (a `dict` subclass),
so existing code that treats shapes as plain dicts keeps working.

## Consequences

**Positive:**
- Optional fields are visible at a glance.
- The flag now does what its name suggests, and the output stays valid
  YAML.

**Negative / Trade-offs:**
- Counts live in comments, so YAML parsers don't see them.
- Counts reflect only the sampled data, not what the API guarantees.

**Follow-ups:**
- Use the counts for `required` lists when JSON Schema / OpenAPI emitters
  are added.
