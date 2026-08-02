# CLAUDE.md

Guidance for Claude Code (or any agent/developer) working in this
repository.

## What this project is

IDOS (Investment Decision Operating System) is a **portfolio case study**,
built to demonstrate governed, test-first Python engineering practice
against a realistic institutional-investment-platform brief. It is:

- Not a client engagement -- there is no client, no contract, no NDA.
- Not a production or trading system -- Release-1-as-specified is
  decision-support and reconciliation only, and this repository doesn't
  even reach that; it currently implements the repository/tooling
  foundation (Sprint 5A-R) only.
- Not connected to any real market-data provider or brokerage, and never
  contains real credentials, tokens, or client data.

Read [`docs/adr/0002-case-study-scope-boundary.md`](docs/adr/0002-case-study-scope-boundary.md)
before doing anything else in this repo -- it is the definitive statement
of what's real here and what's roadmap.

## Source of truth

- [`docs/architecture/00-platform-overview.md`](docs/architecture/00-platform-overview.md)
  -- the full platform's module map and design principles (roadmap, not
  status).
- [`docs/requirements/`](docs/requirements/) -- functional requirements
  (`FR-*`), non-functional requirements (`NFR-*`), and the sprint plan.
  Every requirement has a `Status` of `Done`, `Planned`, or `Out of scope`.
  Trust this over any prose summary, including this file.
- [`docs/adr/`](docs/adr/) -- architecture decisions, numbered
  sequentially, never edited after acceptance (superseded, not rewritten).
- [`docs/evidence/`](docs/evidence/) -- captured, real command output
  proving a sprint's acceptance criteria were met.

## Engineering rules for this repository

These are not aspirational; `idos-validate-repo` and CI enforce what can be
enforced mechanically, and reviewers should reject anything that violates
the rest.

1. **Nothing merges as "done" that isn't real.** No TODO/FIXME markers, no
   stub functions standing in for real logic, no tests that assert `True`.
   `idos-validate-repo` scans `src/` for placeholder markers and fails the
   build if it finds one.
2. **Every source module has a test module.** `src/idos/<path>/<name>.py`
   requires `tests/unit/<path>/test_<name>.py` to exist (see
   `repo_validation.yaml`, `test_parity`). `__init__.py` files are exempt.
3. **Determinism in anything financial.** No unseeded randomness, no `float`
   for money, no unmocked wall-clock reads inside logic that's supposed to
   be reproducible. This isn't exercised yet (5A-R has no financial logic)
   but is a hard constraint on everything built after it -- see NFR-01.
4. **ADR before architecture.** A new module boundary, a new external
   dependency (a web framework, a database, a market-data SDK), or a change
   to an existing contract needs an ADR *before* the code, not as a
   retroactive explanation. See ADR 0001 for what counts as
   architecture-significant, and ADR 0003 for a live example of a decision
   deliberately left open until its trigger condition is met.
5. **Small, reviewable increments.** Prefer several small, focused commits
   over one large one, each buildable and tested on its own. There's no
   remote/PR workflow wired up in this local case study, but write commits
   as if there were a reviewer on the other end.
6. **Traceability.** Reference the requirement ID (`FR-NNN`) a change
   implements in its commit message where one exists.

## Working in this repo

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

ruff check .                                   # lint
mypy src tests                                 # type check (strict)
pytest --cov --cov-report=term-missing         # test, with coverage
idos-validate-repo                             # repository governance check
```

All four are what CI runs (`.github/workflows/ci.yml`); run them locally
before considering anything finished.

## Repository map

```
src/idos/                  the idos package
  tooling/repo_validate.py the repository-validation CLI (idos-validate-repo)
repo_validation.yaml       rules the validator enforces (edit this, not the
                            validator's source, to add/change a check's
                            parameters)
tests/unit/                mirrors src/idos/ 1:1 (see rule 2 above)
docs/adr/                  architecture decisions
docs/architecture/         platform-wide design docs (roadmap)
docs/requirements/         functional/non-functional requirements + sprint plan
docs/evidence/             captured proof that a sprint's acceptance criteria
                            were actually met
```

## If asked to extend scope beyond 5A-R

Sprint 5B-R (Shared Kernel/SDK: config, contracts, domain, audit, evidence)
is the approved next step per the sprint sequence. Before writing any of
it: read `docs/requirements/03-sprint-5-remediation-plan.md`'s "Entry
criteria for 5B-R" section, and write the ADR it calls for first. Do not
start 5C-R or later work before 5B-R is complete and evidenced -- that
ordering constraint is itself a requirement (NFR / sprint plan), not a
suggestion.
