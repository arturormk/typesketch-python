# ADR-0003– Inference Heuristics
**Status**: Accepted
**Date**: 2025-10-19

## Context
We need deterministic, simple heuristics to infer types from JSON samples without dependencies.

## Decision
- Scalar types: int, number, boolean, null, string.
- Simple format hints: url, email, datetime, html-string.
- Arrays: merge shapes of item objects; scalar arrays use union (`string | int`).
- Key ordering: by frequency desc, then alpha as tiebreaker.
- Limits: arrays are sampled (default 200). No deep recursion guards yet.

## Consequences
**Positive:**
- Predictable results that are easy to explain.
- Works well for small to medium samples.

**Negative / Trade-offs:**
- Loses some nuance (e.g., requiredness/probabilities) until added in the future.
