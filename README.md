# IDOS -- Investment Decision Operating System

**This repository proves four things about how it was built: every
requirement has a stable ID and a real status (a functional and
non-functional requirements catalogue), every architecture-significant
decision is written down before it's acted on (ADR discipline), every
shipped module has a matching test enforced mechanically (1:1
source-to-test parity), and all of it is gated in CI by
`idos-validate-repo` rather than asserted in a README. It's a portfolio
case study in governed Python engineering, built against a realistic
institutional investment-platform brief.**

> **This is not a real product, client engagement, or investment service.**
> There is no live market data, no brokerage connectivity, no trade
> execution, and no investment advice anywhere in this repository. It was
> built independently as a demonstration of engineering practice, using a
> representative institutional-platform specification as the brief. See
> [`docs/adr/0002-case-study-scope-boundary.md`](docs/adr/0002-case-study-scope-boundary.md)
> for the full, explicit scope statement.

## Why this repository exists

Institutional financial software has to be governed: architecture decisions
are written down, nothing merges as "done" unless it's actually done, every
recommendation is traceable to its inputs, and delivery happens in small,
reviewable increments rather than one large drop. Those constraints are
easy to state and easy to fake. This repository is a demonstration of
actually running that process, on a real (if intentionally narrow) slice of
work, rather than describing it in a cover letter.

The brief behind this project specifies a multi-module institutional
platform delivered across an approved five-sprint sequence (`5A-R` through
`5E-R`) -- market-data ingestion, an opportunity-intelligence system, a
governed decision resolver, portfolio construction and risk controls,
brokerage reconciliation, and a controlled-learning/reinforcement-learning
component, among others. That's realistically a multi-year, multi-engineer
engagement. Rather than fake a shallow version of all of it, this
repository implements the **first sprint only, completely and for real**,
and documents the rest as an honestly-labeled, unimplemented roadmap.

## What's actually implemented: Sprint 5A-R

*Repository, Tooling, Automation and Continuous Integration.*

- Python 3.12 package (`setuptools`, `src/` layout)
- `idos-validate-repo`: a repository-governance CLI that checks required
  files/directories exist, that Architecture Decision Records are present
  and correctly named, that no placeholder markers (`TODO`/`FIXME`/`XXX`)
  are left in shipped source, and that every source module has a matching
  test module -- configured entirely from
  [`repo_validation.yaml`](repo_validation.yaml), not hardcoded
- A pytest suite, including a self-check that this repository passes its
  own validation rules
- GitHub Actions CI: lint (`ruff`), strict type checking (`mypy`), tests
  with coverage, and repository validation, on every push and PR

See [`docs/evidence/5a-r-acceptance-evidence.md`](docs/evidence/5a-r-acceptance-evidence.md)
for real, captured command output proving all of the above actually run
and pass -- not a claim, a log.

## What's documented but not built

Everything past Sprint 5A-R -- the Shared Kernel/SDK, market-data
ingestion, the opportunity-intelligence system, the decision resolver,
portfolio construction and risk controls, brokerage reconciliation, and the
controlled-learning foundations -- is specified as a requirements catalog
and architecture overview, explicitly marked `Planned`, with nothing in
`src/` claiming to implement it:

- [`docs/architecture/00-platform-overview.md`](docs/architecture/00-platform-overview.md)
  -- full module map and design principles
- [`docs/requirements/`](docs/requirements/) -- functional and
  non-functional requirements, each with a stable ID and status
- [`docs/adr/`](docs/adr/) -- architecture decisions, including one
  (`0003`) that deliberately defers picking a web framework and database
  until there's enough evidence to justify the choice, rather than
  guessing up front

## Quickstart

```bash
git clone <this-repo>
cd idos
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

ruff check .                                   # lint
mypy src tests                                 # strict type check
pytest --cov --cov-report=term-missing         # tests, with coverage
idos-validate-repo                             # repository governance check
```

## Practices demonstrated here

- **ADR-driven architecture** ([`docs/adr/`](docs/adr/)) -- decisions are
  written down with context and consequences before they're acted on, and
  superseded rather than silently changed.
- **Determinism as a design constraint**, stated explicitly in the
  non-functional requirements before there's any financial logic to test it
  against, so it shapes the Shared Kernel design (Sprint 5B-R, not yet
  built) rather than getting bolted on afterward.
- **Machine-enforced repository governance** -- `idos-validate-repo` turns
  "no incomplete scaffolding, no hidden shortcuts" from a review guideline
  into a CI gate.
- **Honest scope statements** -- ADR 0002 exists specifically so this
  README can't quietly overclaim what's in the repository.

## License

MIT -- see [`LICENSE`](LICENSE). This is original demonstration work; it
is not derived from, and does not contain, any real client's codebase or
proprietary material.
