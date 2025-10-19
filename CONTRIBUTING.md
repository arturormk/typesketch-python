# Contributing to TypeSketch

Thanks for considering a contribution! This project is a small, dependency-light CLI with an AI-assisted, human-curated workflow.

## Development setup
- Python 3.9+
- Install dev deps: `pip install -r requirements-dev.txt`
- Install pre-commit hooks: `pre-commit install`

## Running
- Lint: `ruff check . && ruff format --check .`
- Tests: `pytest -q` (fast subset: `bash scripts/fast_tests.sh`)
- Build: `python -m build`

## Making changes
- Add or update an ADR under `docs/adr/` when changing behavior or architecture. Update the ADR index.
- Prefer tests-first for new behavior.
- Keep runtime dependencies at zero unless justified by an ADR.

## Commit style
- Use clear messages; `feat:`, `fix:`, `docs:` optional.
- Reference ADRs when applicable, e.g., `refs ADR-0003`.

## AI curation policy
- AI output is treated as draft; a human curator owns the final changes.
- Please keep the README attribution and `AUTHORS` provenance intact.

## Reporting issues
- Provide a minimal reproducible example, expected vs actual behavior, and environment details.