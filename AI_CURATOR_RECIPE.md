# AI Curator Project Recipe

A comprehensive, project-agnostic playbook you can hand to an AI assistant to bootstrap and continuously maintain a **small, high-quality, AI‑assisted open source project** with a *Software Curator* posture (human accountability + transparent AI provenance).

This file defines: objectives, required artifacts, process constraints, quality gates, automation hooks, and escalation rules. Treat it as a contract between the human curator and the AI.

---
## 1. Objectives
- Produce a minimal, dependency-light codebase (prefer standard library first).
- Ship immediately usable CLI or library surface with versioning.
- Enforce architectural intent via ADRs (Architecture Decision Records).
- Maintain test-backed confidence (behavioral tests > line coverage obsession).
- Automate style, lint, and fast sanity tests locally (pre-commit) + full matrix in CI.
- Provide transparent AI involvement (curation policy, attribution, provenance signals).
- Keep contributor friction low but standards high.

## 2. Non-Goals
- Enterprise-scale monorepo features.
- Heavy framework scaffolding unless justified by ADR.
- Over-engineering premature abstractions.

## 3. Core Principles
1. **Human curator owns intent.** AI drafts; human approves direction.
2. **Docs as runway.** Add/update ADR or README section *before or with* behavior changes.
3. **Tests define truth.** Failing test first for new non-trivial behavior.
4. **Start simple; evolve deliberately.** Avoid speculative abstractions.
5. **Transparency > hype.** Always disclose AI assistance in attribution.
6. **Fast feedback loops.** Pre-commit is very fast; CI is comprehensive.

## 4. Mandatory Artifacts (Initial Milestones)
| Milestone | Artifact | Purpose |
|-----------|----------|---------|
| 1 | `README.md` | Value proposition, quick start, features, contribution outline |
| 1 | `LICENSE` (MIT/Apache-2.0) | Legal clarity |
| 1 | Primary module or package + CLI entry | Demonstrable functionality |
| 1 | `pyproject.toml` (PEP 621) | Build + metadata, dynamic version optional |
| 2 | `tests/` + helper utilities | Deterministic behavioral verification |
| 2 | `docs/adr/` + `README.md` index + `TEMPLATE.md` | Decision traceability |
| 2 | ADRs 0000–000x | Record seed decisions (language, packaging, tooling) |
| 3 | CI workflow (GitHub Actions or equivalent) | Lint, type, test, build, ADR lint |
| 3 | `requirements-dev.txt` | Stable dev bootstrap |
| 3 | Pre-commit config | Local guardrails |
| 4 | `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `AUTHORS` | Community + attribution |
| 4 | AI curation ADR + README attribution section | Provenance and policy |
| 5 | Optional: `CITATION.cff` | Scholarly citation & DOIs |
| 5 | `docs/incidents/` (Incident Log) | Curatorial knowledge base of reusable failure lessons |

## 5. ADR System
- Directory: `docs/adr/`
- Filenames: `NNNN-kebab-title.md` (4-digit incremental index)
- Required sections: `## Context`, `## Decision`, `## Consequences`
- Index file lists all ADRs; CI + pre-commit enforce inclusion.
- Status keywords: *Proposed*, *Accepted*, *Superseded* (min set).
- Reference ADR IDs in code comments/tests (e.g., `# See ADR-0004`).

### ADR Template (`docs/adr/TEMPLATE.md`)
```
# NNNN – Title
Status: Proposed
Date: YYYY-MM-DD
## Context
...
## Decision
...
## Consequences
Positive:
- ...
Negative / Trade-offs:
- ...
Follow-ups:
- ...
```

## 6. AI Curation Policy (Embed as ADR, e.g., ADR-0010)
Key points (enforce via documentation + hooks):
- AI output treated as draft; human remains legal author.
- Every meaningful behavior change must: (a) update/add ADR, (b) include tests, (c) pass pre-commit & CI.
- Summarize provenance in README Attribution & in `AUTHORS`.
- Optionally tag large AI batches with commit footer: `Curated-By: <Name>`.

## 7. Repository Layout (Example)
```
project/
  src/your_module.py  OR  src/your_pkg/__init__.py
  tests/
    test_*.py
    helpers.py
  docs/
    adr/
      0000-record-architecture-decisions.md
      0001-... (etc)
      README.md
      TEMPLATE.md
  scripts/
    lint_adrs.py
    check_adr_index.py
    fast_tests.sh
    check_prints.sh
  .github/
    workflows/ci.yml
    ISSUE_TEMPLATE/*.yml
    PULL_REQUEST_TEMPLATE/pull_request.md
  .pre-commit-config.yaml
  pyproject.toml
  requirements-dev.txt
  README.md
  LICENSE
  AUTHORS
  CODE_OF_CONDUCT.md
  CONTRIBUTING.md
  AI_CURATOR_RECIPE.md (this file)
```

## 8. Packaging (Python Example)
- Use `pyproject.toml` with:
  - `[build-system]` setuptools backend (or uv/poetry if justified by ADR)
  - `[project]` PEP 621 metadata
  - Dynamic version via module attribute or static version field (NOTE: for a single-module `py-modules` layout, prefer a static `version` field to avoid brittle dynamic resolution—see Incident Log if one exists)
  - Console script via `[project.scripts] toolname = "package_or_module:main"`
- Keep runtime deps minimal; dev-only items in `requirements-dev.txt`.

### Sample Minimal pyproject
```
[build-system]
requires = ["setuptools>=64", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "your-project"
description = "Short one-line value prop."
readme = "README.md"
requires-python = ">=3.9"
license = { file = "LICENSE" }
authors = [{ name = "Your Name" }]
keywords = ["keyword1", "keyword2"]
classifiers = ["Programming Language :: Python :: 3"]
dynamic = ["version"]

[project.scripts]
yourcli = "your_module:main"

[tool.setuptools]
py-modules = ["your_module"]
# or: packages = ["your_pkg"]

[tool.setuptools.dynamic]
version = { attr = "your_module:__version__" }  # Use only when package import path is stable; otherwise keep static.
```

## 9. Testing Strategy
- Focus: functional & behavioral tests; minimal mocks; small synthetic fixtures.
- Helpers: programmatically construct inputs (e.g., small binary/document artifacts) to avoid heavy fixtures.
- Distinguish categories: parser behavior, CLI contract, dialect/variant emission, integration round-trip.
- Avoid network or time sleeps; tests must be deterministic & fast (<5s total for core subset).

## 10. CI Pipeline (Example Matrix)
Stages per job:
1. Checkout
2. Set up language runtime (matrix over supported versions)
3. Install dev requirements
4. Lint (Ruff / flake8 / eslint etc.)
5. Type check (mypy/pyright) — optionally non-blocking early, then enforcing after maturity
6. Run test suite (fast, deterministic)
7. Build package (ensures packaging metadata sanity)
8. ADR lint (structural & required sections)

## 11. Pre-commit Hooks
Principles:
- Keep commit-time hooks under ~3s.
- Push-time hook may run a small representative test subset.

Suggested Hooks:
- trailing-whitespace, end-of-file-fixer, large-file guard
- Ruff (lint) + format
- Import smoke (`PYTHONPATH=src python -c "import your_module"`)
- ADR index checker (ensures new ADR added to index)
- Raw `print(` blocker (allow explicit `file=` usage for intentional streams)
- Fast test subset (pre-push): 1–3 sentinel tests covering critical paths
- (Optional) Incident guard hooks (e.g., verify `pyproject.toml` static version matches module `__version__` if dynamic disabled)
- Incident log linter (sequential IDs, required sections)

Escalation: full suite always in CI.

## 12. Attribution & Transparency
- README section: Attribution & Curation (policy summary, link to AI curation ADR)
- `AUTHORS`: list human maintainers + provenance note (AI-assisted, human curated)
- Optional: `CITATION.cff` for academic citation & DOIs

### Example CITATION.cff Skeleton
```
cff-version: 1.2.0
message: "If you use this software, please cite it."
title: "your-project"
version: 0.1.0
authors:
  - given-names: Your
    family-names: Name
repository-code: https://github.com/your/repo
license: MIT
abstract: "One-sentence summary."
preferred-citation:
  type: software
  title: "your-project"
  version: 0.1.0
  notes: "AI-assisted code; curated and validated by a human Software Curator."
```

## 13. Code Style & Conventions
- Lint config centralized (e.g., Ruff section in `pyproject.toml`).
- Use single quotes or consistent quote style (enforced by formatter).
- Keep line length reasonable (e.g., 100–120) while permitting explicit exemptions for long SQL.
- Avoid wildcard imports & deep relative imports.
- Prefer pure functions for transformations; isolate I/O in boundary functions.

## 14. Logging / Output Policy
- CLI tools: primary output → stdout; diagnostics → stderr.
- Pre-commit hook allows `print(..., file=stderr)` and `print(..., file=out)` only.
- Avoid hidden global state; pass file handles explicitly if needed.

## 15. Versioning & Releases
- Semantic versioning (MAJOR.MINOR.PATCH).
- `__version__` constant single-sourced. Prefer static `version` in `pyproject.toml` for single-file modules; only enable dynamic attribute resolution once migrated to a package dir and guarded by an import verification step.
- Release checklist:
  1. Update CHANGELOG (optional) or summarize in GitHub Release notes.
  2. Ensure CI green.
  3. Tag `vX.Y.Z` and push tag.
  4. (Optional) Publish to package index.
  5. Archive artifact / mint DOI (Zenodo) if needed.

## 16. Commit Conventions
- Conventional style (optional): `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`.
- Include ADR references when modifying a decided area: `refs ADR-0006`.
- Large AI-assisted batches include footer: `Curated-By: <Name>`.

## 17. Quality Gates Definition of Done (Per Change)
| Gate | Requirement |
|------|-------------|
| Lint | No new lint errors (auto-fix allowed) |
| Types | No new type errors OR documented defer rationale |
| Tests | Added/updated tests for new or changed behavior; all pass |
| Docs | README or ADR updated if user-visible or structural decision changed |
| Provenance | Attribution maintained (no removal of curation policy) |
| Packaging | Build step succeeds (wheel/sdist) |
| ADR Integrity | Index updated, required sections present |
| Incidents (if applicable) | New reusable failure documented in `docs/incidents/` with guardrail noted |

## 18. Threats / Anti-Patterns to Avoid
- Silent behavior changes without tests/ADRs.
- Introducing heavy dependencies for trivial tasks without ADR justification.
- Skipping human review under time pressure.
- Overloading pre-commit with long-running tasks (causes bypassing).
- Copy/pasting external code without license vetting.
- Allowing the same class of failure to recur without capturing a distilled lesson (missing incident log entry & guardrail).

## 19. AI Assistant Operating Procedure (Hand This to the AI)
1. Read repository tree (list + targeted reads) before acting.
2. Enumerate explicit user request into checklist (no omissions).
3. Gather missing context via file reads; avoid blind assumptions.
4. Propose minimal diff; implement directly using appropriate edit tool.
5. After edits: run linters/tests/build locally; iterate until green.
6. Summarize deltas & map each requirement → Done/Deferred.
7. Suggest adjacent low-risk improvements (docs/tests) if safe.
8. Never claim authorship; always attribute human curator.

### AI Must Not:
- Add dependencies casually.
- Remove attribution or license lines.
- Force push or rewrite history unless explicitly requested.
- Ship failing CI state without explicit deferral note.

## 20. Extensibility Hooks (Future ADR Candidates)
- Property-based testing for parser/transform core.
- Cross-platform smoke (Linux/Windows/macOS) matrix.
- Security scanning (bandit, pip-audit) once dependencies exist.
- Performance regression micro-benchmarks.
- Coverage thresholds (after baseline confidence established).

## 21. Onboarding Checklist (New Repository)
1. Initialize VCS + base `README.md`, `LICENSE`, `.gitignore`.
2. Add core module + trivial `main()` returning a constant.
3. Add pyproject with dynamic or static version.
4. Add first test verifying CLI exit code & output.
5. Introduce ADR system (0000 + at least 2 more core decisions).
6. Add CI workflow (lint, tests, build, ADR lint).
7. Add pre-commit minimal hooks; install locally.
8. Add attribution & AI curation ADR.
9. Harden tests (edge cases) & indexing of ADR references.
10. Introduce `docs/incidents/` scaffold (README + TEMPLATE) early or upon first qualifying incident.
11. Tag `v0.1.0` once stable.

## 22. Maintenance Cycle (Per Sprint / Iteration)
- Review open ADR proposals; accept or supersede.
- Prune stale branches/issues.
- Run `pre-commit run --all-files` to flush drift.
- Audit README for accuracy vs features.
- Verify `pyproject.toml` authors & metadata still correct.
- Review Incident Log: close resolved ones, consolidate patterns, ensure added guardrails are still active.
  - Run incident linter (automated in CI + pre-commit) to ensure structural integrity.

## 23. Human Curator Quick Reference
| Task | Command Examples |
|------|------------------|
| Install dev deps | `pip install -r requirements-dev.txt` |
| Run full tests | `pytest -q` |
| Run fast tests | `bash scripts/fast_tests.sh` |
| Lint fix | `ruff check . --fix && ruff format .` |
| Type check | `mypy --strict src tests scripts` |
| Pre-commit all | `pre-commit run --all-files` |
| Build dist | `python -m build` |

## 24. License & Authorship Guidance
- License should remain permissive unless strong reason documented in ADR.
- AI *cannot* hold copyright; repository retains human author(s) in LICENSE / headers.

## 25. Optional Enhancements (When Stable)
- Add CHANGELOG.md using Keep a Changelog format.
- Add badges: coverage, PyPI version, license.
- Provide Docker dev container or devcontainer.json (ADR documenting rationale).
- Add `Makefile` or task runner (only if it reduces friction; otherwise keep docs simple).
- Automated incident linter (sequential IDs, required sections) in CI.

## 26. Curatorial Incident Log
Purpose: capture non-trivial events (CI/build failures, packaging pitfalls, subtle contract risks) that generate reusable prevention value.

Location: `docs/incidents/`

Include (TEMPLATE fields): ID (`INC-XXXX`), Date, Status, Context/Trigger, Symptom, Root Cause, Resolution, Prevention/Guardrail, References (commit, ADR, CI log), Tags.

Inclusion Criteria:
- Failure class could plausibly recur or teach a general safeguard.
- Led to a policy, hook, test, or documentation change.

Exclusions:
- Trivial typos, purely cosmetic formatting, obvious one-off mistakes.

Process:
1. Upon resolving qualifying incident, create file `INC-XXXX-<kebab>.md`.
2. Link relevant ADR(s); if a decision changes materially, update ADR and reference the incident.
3. Add/verify guardrail (test, hook, CI step) before closing incident.
4. Periodic consolidation: extract recurring patterns into higher-level guidance; prune obsolete entries.

Goal: strengthen institutional memory for AI-assisted curation while keeping user-facing docs (README/CHANGELOG) succinct.

---
## Final Notes
This recipe aims for *just enough rigor* to sustain a trustworthy, small open source project while embracing AI acceleration transparently. Adapt cautiously: remove sections only with a deliberate decision (record via ADR) to avoid silent erosion of quality gates.

> When in doubt: write (or update) an ADR first, then code.
