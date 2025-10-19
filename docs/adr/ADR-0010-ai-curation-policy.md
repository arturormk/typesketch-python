# ADR-0010– AI Curation Policy

**Status**: Accepted  
**Date**: 2025-10-19

## Context

This project leverages AI assistance to accelerate development while maintaining human accountability and transparent provenance.

## Decision

Adopt an AI curation policy:
- AI output is treated as draft; a human Software Curator owns intent and merges changes.
- Any meaningful behavior change must include: (a) ADR update/addition, (b) tests, (c) passing pre-commit & CI.
- Attribution: README includes a "Attribution & Curation" section; `AUTHORS` lists human maintainers and provenance note.
- Large AI-assisted batches may include commit footer: `Curated-By: <Name>`.

## Consequences

**Positive:**
- Fast iteration with explicit guardrails and traceability.
- Clear provenance for contributors and users.

**Negative / Trade-offs:**
- Requires discipline to maintain documentation and tests.

**Follow-ups:**
- Ensure CI includes ADR lint and fast tests.
- Periodically audit README attribution section for accuracy.