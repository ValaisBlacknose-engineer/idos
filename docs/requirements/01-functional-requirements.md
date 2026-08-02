# Functional requirements

See [`00-index.md`](00-index.md) for the status legend and traceability
convention. IDs are stable once assigned; do not renumber.

## FR-0xx -- Repository, Tooling, Automation, CI (Sprint 5A-R)

| ID | Requirement | Status |
|---|---|---|
| FR-001 | Installable Python 3.12 package, setuptools src layout | Done |
| FR-002 | Automated test suite (pytest) covering every shipped module | Done |
| FR-003 | Repository-validation tool: required files/dirs, ADR presence, placeholder-marker absence, source/test parity | Done |
| FR-004 | Validation rules are external YAML config, not hardcoded in the tool | Done |
| FR-005 | CI pipeline runs lint, type check, test-with-coverage, and repository validation on every push/PR | Done |
| FR-006 | Reproducible acceptance evidence captured at sprint completion | Done |

## FR-1xx -- Shared Kernel / SDK (Sprint 5B-R)

| ID | Requirement | Status |
|---|---|---|
| FR-101 | Domain value objects: currency-safe `Money`, strongly-typed identifiers, injectable `Clock` for deterministic time | Planned |
| FR-102 | Configuration module: hierarchical YAML config, environment overlay, schema validation, explicit failure (not silent default) on a missing required secret | Planned |
| FR-103 | Contracts module: stable Command/Query/Event/Result vocabulary for module boundaries | Planned |
| FR-104 | Audit module: structured, append-only, tamper-evident audit event log | Planned |
| FR-105 | Evidence module: reproducibility bundles linking a decision's inputs, code version, config version, and outputs | Planned |

## FR-2xx -- Market Data Platform (Sprint 5C-R)

| ID | Requirement | Status |
|---|---|---|
| FR-201 | Provider-agnostic ingestion interface | Planned |
| FR-202 | Validation and normalization of ingested market data | Planned |
| FR-203 | Point-in-time data provenance | Planned |
| FR-204 | Provider selection evaluated on coverage, licensing, reliability, cost, replacement risk; recorded via ADR | Planned |

## FR-3xx -- Stock Opportunity Intelligence System (Sprint 5D-R)

| ID | Requirement | Status |
|---|---|---|
| FR-301 | Opportunity scoring from market data and research inputs | Planned |
| FR-302 | Parallel evaluation under general and Shariah-aligned mandates | Planned |

## FR-4xx -- Decision Resolver, SVIL, Portfolio Governor (Sprint 5D-R+)

| ID | Requirement | Status |
|---|---|---|
| FR-401 | Decision Resolver produces governed recommendations with full lineage to SOIS output and applied rules | Planned |
| FR-402 | SVIL module (scope fixed via ADR before implementation begins) | Planned |
| FR-403 | Portfolio Governor enforces mandate rules and exposure limits as an approval gate | Planned |

## FR-5xx -- Portfolio construction, sizing, risk, reconciliation (Sprint 5D-R+)

| ID | Requirement | Status |
|---|---|---|
| FR-501 | Portfolio construction and management within Portfolio Governor constraints | Planned |
| FR-502 | Deterministic position sizing and exposure-limit calculation | Planned |
| FR-503 | Actual-vs-target portfolio reconciliation | Planned |
| FR-504 | Brokerage reconciliation and transaction-cost modeling | Planned |

## FR-6xx -- Opportunity monitoring (Sprint 5D-R+)

| ID | Requirement | Status |
|---|---|---|
| FR-601 | Opportunity monitoring and revalidation against fresh data | Planned |

## FR-7xx -- Controlled learning (Sprint 5E-R)

| ID | Requirement | Status |
|---|---|---|
| FR-701 | Offline replay and calibration harness | Planned |
| FR-702 | Challenger evaluation gate before any learned change affects live output | Planned |

## FR-8xx -- UI, auth, notifications, observability (cross-cutting / post 5E-R)

| ID | Requirement | Status |
|---|---|---|
| FR-801 | Responsive web UI and owner dashboard | Planned |
| FR-802 | Authentication and authorization for restricted access | Planned |
| FR-803 | Notifications | Planned |
| FR-804 | Structured logging, metrics, operational monitoring | Planned |

## FR-9xx -- Backup, disaster recovery, deployment

| ID | Requirement | Status |
|---|---|---|
| FR-901 | Backup and disaster recovery procedures | Planned |
| FR-902 | Controlled production deployment process | Planned |

## FR-95x -- Explicit non-goals

| ID | Requirement | Status |
|---|---|---|
| FR-951 | Autonomous trade execution | Out of scope |
| FR-952 | Public access / subscription product | Out of scope |
| FR-953 | Uncontrolled model self-modification | Out of scope |
