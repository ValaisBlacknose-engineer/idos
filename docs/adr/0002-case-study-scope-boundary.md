# 0002. This repository is a portfolio case study scoped to Sprint 5A-R

- Status: Accepted
- Date: 2026-08-02

## Context

IDOS, as specified, is a multi-year, multi-module institutional investment
platform: market-data ingestion, an opportunity-intelligence system, a
governed decision resolver, portfolio construction and risk controls,
brokerage reconciliation, controlled-learning/reinforcement-learning
components, a full web UI, auth, observability, and disaster recovery --
delivered by a full engineering team against an approved sprint sequence
(5A-R through 5E-R).

This repository is **not** that engagement. It is an original, self-directed
case study built to demonstrate the engineering practices such a platform
would require: governed, incremental delivery; deterministic financial
primitives; ADR-driven decisions; repository-validation automation; and
test-first discipline. It is written for publication as a portfolio artifact
(Upwork, LinkedIn), not as deliverable work product for a paying client.

Building the full platform in one unsupervised pass would not demonstrate
those practices credibly -- it would produce exactly the "incomplete
scaffolding, hidden shortcuts and production placeholders" that a governed
delivery process exists to reject. A narrower, fully real slice is a more
honest demonstration than a wide, partially fake one.

## Decision

This repository implements **Sprint 5A-R (Repository, Tooling, Automation
and Continuous Integration) only**, completely and for real:

- Python 3.12 packaging (`pyproject.toml`, setuptools, src layout)
- pytest-based automated testing, including a self-check that the repository
  passes its own validation rules
- PyYAML-backed configuration for the repository-validation tool
- GitHub Actions CI (lint, type check, test with coverage, repository
  validation)
- Repository-validation tooling (`idos-validate-repo`)

Sprints 5B-R through 5E-R (Shared Kernel/SDK, Market Data Platform, Stock
Opportunity Intelligence System, and the reinforcement-learning
foundations), and every downstream module listed in the platform overview
(`docs/architecture/00-platform-overview.md`), are documented as an
architected roadmap in `docs/requirements/` but are **not implemented** in
this repository. No code in `src/idos` claims to implement them, and no
test suite claims to verify them.

Autonomous trade execution, public access, subscription services, real
brokerage connectivity, and uncontrolled model self-modification are out of
scope for the platform as specified, and are therefore also out of scope
here.

## Consequences

- Everything in this repository that is marked "done" is real, tested, and
  runnable -- there is no placeholder code presented as finished work.
- The requirements catalog and sprint plan describe a larger system than
  this repository implements; that gap is intentional and stated explicitly
  rather than implied away.
- A reader evaluating this repository as a hiring signal should read it as
  evidence of *how* the full engagement would be run, not as a partial
  implementation of the full engagement.
- Extending this repository into 5B-R work must follow ADR 0001: a new ADR
  before any Shared Kernel module boundary is fixed.
