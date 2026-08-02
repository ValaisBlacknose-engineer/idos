# IDOS platform overview

> Scope note: this document describes the full platform as specified, for
> architectural context. It is a roadmap, not a status report. For what is
> actually implemented in this repository, see
> [`docs/requirements/03-sprint-5-remediation-plan.md`](../requirements/03-sprint-5-remediation-plan.md)
> and [ADR 0002](../adr/0002-case-study-scope-boundary.md).

## What IDOS is

IDOS (Investment Decision Operating System) is a private, restricted-access
investment intelligence and decision-support platform. It is a
decision-support and reconciliation system, not an execution system:
Release 1 does not place trades. It supports two parallel investment
mandates -- general and Shariah-aligned -- across tactical, short-term and
medium-term decision horizons, within one governed platform.

## Module map

| Module | Responsibility | Sprint |
|---|---|---|
| Repository, Tooling, Automation, CI | Packaging, testing, linting, repository governance automation | 5A-R |
| Shared Kernel / SDK | Cross-cutting domain types, contracts, configuration, audit, evidence -- the vocabulary every other module is built on | 5B-R |
| Market Data Platform | Ingestion, validation, normalization and provenance of market data from external providers | 5C-R |
| Stock Opportunity Intelligence System (SOIS) | Identifies and scores candidate investment opportunities from market data and research inputs | 5D-R |
| Decision Resolver | Turns SOIS output and governed rules into a recommendation, with full lineage back to its inputs | 5D-R+ |
| SVIL module | Documented decision-support component (see requirements catalog); scope fixed at design time, not before | 5D-R+ |
| Portfolio Governor | Enforces mandate rules (general vs. Shariah-aligned), exposure limits, and approval gates over proposed portfolio changes | 5D-R+ |
| Portfolio construction & management | Builds and maintains target portfolios within Portfolio Governor constraints | 5D-R+ |
| Position sizing, exposure limits, risk controls | Deterministic sizing and risk-limit calculations | 5D-R+ |
| Actual-vs-target reconciliation | Compares live holdings against target portfolios | 5D-R+ |
| Brokerage reconciliation & transaction-cost logic | Reconciles broker-reported positions/fills and models transaction costs | 5D-R+ |
| Opportunity monitoring & revalidation | Re-checks standing opportunities against fresh data; flags invalidated theses | 5D-R+ |
| Controlled learning, replay, calibration, challenger evaluation | Reinforcement-learning and calibration foundations, evaluated offline against a "challenger" process before any influence on live output | 5E-R |
| Responsive UI & owner dashboard | Web front end for the platform owner | Post 5E-R |
| Auth, authorization, secure access | Identity and access control for the restricted-access platform | Cross-cutting, introduced with the API layer |
| Notifications, observability, operational monitoring | Structured logging, metrics, alerting | Cross-cutting |
| Decision lineage, evidence, audit trails, reproducibility | Every governed recommendation is traceable to its inputs, code version, and config version | Cross-cutting, rooted in the Shared Kernel's `audit` and `evidence` capabilities (5B-R) |
| Backup, disaster recovery, controlled production deployment | Operational resilience | Introduced once there is a persistence layer to protect |

## Explicit non-goals (Release 1)

- Autonomous trade execution.
- Public access or a subscription product.
- Uncontrolled model self-modification (any learning component is offline,
  challenger-evaluated, and human-gated before it can affect live output).
- Personalized investment advice as a standalone product -- IDOS supports a
  single governed owner's decision process; it is not a multi-tenant
  advisory service.

## Design principles carried through every module

1. **Determinism.** Financial calculations must be reproducible: same
   inputs, same code version, same config version -> same output. This
   rules out uncontrolled floating-point drift and unseeded randomness in
   anything that touches money or a governed decision.
2. **Governed change.** Architecture, security boundaries, and approved
   business logic change only through a written decision (ADR 0001).
   Downstream modules are not built ahead of the foundations and contracts
   they depend on.
3. **Auditability by construction.** Decision lineage is a first-class
   output of the system, not a log grepped after the fact.
4. **Small, independently reviewable increments.** No module is "complete"
   by having a lot of code; it is complete when it has tests, docs,
   evidence, and traceability to an approved requirement.

## Relationship to this repository

This repository currently implements the first row of the module map only
(Repository, Tooling, Automation, CI -- Sprint 5A-R), per
[ADR 0002](../adr/0002-case-study-scope-boundary.md). Everything else on
this page is design intent, useful for evaluating whether the foundation is
shaped correctly for what comes next -- it is not a claim that those
modules exist in code.
