# ADR-0003: Inference Heuristics
**Status**: Accepted

- Scalar types: int, number, boolean, null, string.
- Simple format hints: url, email, datetime, html-string.
- Arrays: merge shapes of item objects; scalar arrays use union (`string | int`).
- Key ordering: by frequency desc, then alpha as tiebreaker.
- Limits: arrays are sampled (default 200). No deep recursion guards yet.
