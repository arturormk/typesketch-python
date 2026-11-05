# typesketch v0.2.0

Correctness release: every value seen in the input now contributes to the
sketch, output is always valid YAML, and `--stats` works.

Highlights
- Every record is merged: arrays of objects are pooled across records, so
  fields seen only in earlier records are no longer lost (ADR-0004)
- Fields that are sometimes an object and sometimes something else keep
  their object shape and note the rest, e.g. `owner:  # also: null`
- Arrays mixing objects and scalars, and arrays of arrays, are sketched
  in full
- `--stats` marks optional fields: `coupon: null  # present in 1 of 2`
  (ADR-0006)
- Keys that YAML would reject or misread are quoted (ADR-0005)
- Invalid, empty, non-UTF-8 or too deeply nested input gives a one-line
  `typesketch: error: ...` message and exit status 1 (ADR-0005)

Breaking changes
- A top-level array of scalars prints `- string | int` instead of
  `items: array<string | int>`
- A top-level scalar uses the normal type names (`value: string`, not
  `value: str`)
- Empty objects print as `object`
- Keys such as `first name` or `123` are now quoted
- The internal helper `typesketch.infer.guess_type` was removed

Changelog
- Rewrite shape merging in `infer.py`; add `ObjectShape` and
  `Alternatives`
- Add `typesketch.cli.sketch()` to sketch parsed JSON in-process
- Add golden-fixture tests (`tests/golden/`), YAML round-trip checks and
  CLI error tests
- README: describe the new output, clarify installing from a clone, drop
  the non-existent depth option
- LICENSE: name the copyright holder

Thanks
- Maintainer: Arturo R. Montesinos (@arturormk)
