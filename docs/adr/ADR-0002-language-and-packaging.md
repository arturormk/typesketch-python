# ADR-0002– Language & Packaging
**Status**: Accepted
**Date**: 2025-10-19

## Context
We want a zero-dependency CLI that is easy to install and runs fast.

## Decision
Use Python 3.9+ and package a zero‑deps CLI (`typesketch`) installable via pip/pipx.

## Consequences
**Positive:**
- Low contributor friction and fast startup.
- Wide availability across platforms.

**Negative / Trade-offs:**
- Avoids advanced frameworks unless justified later via ADR.
