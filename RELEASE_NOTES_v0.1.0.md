# typesketch v0.1.0

This is the first curated release of typesketch.

Highlights
- ADR system with documented decisions and curation policy (ADR-0010)
- Pre-commit hooks (ruff, mypy --strict, ADR checks, fast tests) and CI pipeline
- Zero-runtime-deps CLI to infer types from JSON and emit YAML
- Examples: pipe Open Library API and local POIs
- Dynamic versioning sourced from package __version__

Breaking changes
- N/A (initial release)

Changelog
- Add ADR scaffold and linter scripts
- Implement inference fixes and deterministic unions
- Add CLI --version and improve help
- Add examples and docs; improve README TL;DR
- Packaging with PEP 621 + setuptools, src layout

Thanks
- Maintainer: Arturo R. Montesinos (@arturormk)
- Contributors: you! (see AUTHORS)
