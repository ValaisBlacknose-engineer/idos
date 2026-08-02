# Sprint 5 remediation plan

The approved implementation order. Downstream modules are not started
before their supporting foundations and contracts are complete -- each
sprint below is a hard prerequisite for the next.

| Sprint | Scope | Status | Implemented in this repo |
|---|---|---|---|
| **5A-R** | Repository, Tooling, Automation and Continuous Integration | **Complete** | Yes -- see FR-0xx in [`01-functional-requirements.md`](01-functional-requirements.md) |
| **5B-R** | Shared Kernel, Software Development Kit and Domain Foundation | Not started | No -- see FR-1xx |
| **5C-R** | Market Data Platform | Not started | No -- see FR-2xx |
| **5D-R** | Stock Opportunity Intelligence System (and downstream: Decision Resolver, SVIL, Portfolio Governor, portfolio construction, sizing, risk, reconciliation) | Not started | No -- see FR-3xx through FR-6xx |
| **5E-R** | Reinforcement Learning Model and associated foundations | Not started | No -- see FR-7xx |

## Why this repository stops after 5A-R

This is a portfolio case study, not a resourced multi-sprint engagement --
see [ADR 0002](../adr/0002-case-study-scope-boundary.md). Sprint 5A-R is a
complete, self-contained unit of governed delivery: it has its own
requirements (FR-0xx), its own non-functional bar (the NFRs in
`02-nonfunctional-requirements.md`), its own CI gate, and its own
acceptance evidence
([`docs/evidence/5a-r-acceptance-evidence.md`](../evidence/5a-r-acceptance-evidence.md)).
Stopping here, with everything above the line real and everything below the
line explicitly marked `Not started`, is the honest version of this
project.

## Entry criteria for 5B-R, if this repository is ever extended

1. An ADR fixing the Shared Kernel's module boundaries (`config`,
   `contracts`, `domain`, `audit`, `evidence`) before any of them are coded.
2. FR-101 through FR-105 broken into PR-sized increments, each with its own
   test plan.
3. NFR-01 (determinism) made concrete for each module: what "same inputs"
   means for `Money` arithmetic, ID generation, and time-dependent logic.
4. `repo_validation.yaml`'s `test_parity` rule extended to cover the new
   `src/idos/sdk/` tree once it exists.
