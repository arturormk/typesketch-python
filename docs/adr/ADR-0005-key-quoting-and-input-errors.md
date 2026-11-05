# ADR-0005– Key Quoting and Input Errors

**Status**: Proposed
**Date**: 2026-11-05

## Context

TypeSketch output is meant to be valid YAML, but v0.1.0 wrote every JSON
key as-is. Keys such as `"a: b"`, `"- x"`, `""`, `"#tag"` or `"true"`
produced output that YAML parsers reject or misread.

Bad input (invalid JSON, empty stdin, non-UTF-8 bytes, very deep nesting)
ended in a Python traceback rather than a message a CLI user can act on.

## Decision

**Keys.** A key is written plain only when it starts with a letter or
underscore and continues with letters, digits, `_`, `.` or `-` (Unicode
letters included), and is not a word YAML reads as a boolean or null
(`true`, `false`, `yes`, `no`, `on`, `off`, `y`, `n`, `null`, in any case).
Every other key, including numeric ones like `"123"`, is written as a
double-quoted string using JSON escaping, which is also valid YAML. The same
rule applies to the `--root` name.

**Input errors.** Input is read as UTF-8 (a leading BOM is accepted). On
empty input, invalid UTF-8, invalid JSON or nesting too deep to process, the
CLI writes one line, `typesketch: error: <reason>`, to stderr, writes
nothing to stdout and exits with status 1. JSON errors include the line and
column.

## Consequences

**Positive:**
- Output parses as YAML and the keys come back exactly as in the JSON;
  golden tests check this with PyYAML when it is installed.
- Errors are short, clear and scriptable.

**Negative / Trade-offs:**
- Keys that were plain before, e.g. `first name` or `123`, are now quoted.
- The quoting rule is conservative, so some keys that YAML would accept
  plain are quoted anyway.
- Nesting depth is still bounded by Python's recursion limit; deep input is
  refused rather than processed.

**Follow-ups:**
- Revisit the depth limit if real-world data needs more than a few hundred
  levels.
