# 0003. Application framework and database selection: deferred

- Status: Proposed
- Date: 2026-08-02

## Context

The platform will eventually need a production API layer and a persistence
layer. FastAPI and PostgreSQL are reasonable, widely-used candidates for a
Python 3.12, deterministic, auditable financial system:

- FastAPI: async-capable, Pydantic-based request/response validation, OpenAPI
  schema generation for free (useful for the "API and schema documentation"
  delivery requirement), strong typing story.
- PostgreSQL: mature transactional guarantees, `NUMERIC`/`DECIMAL` types
  suited to deterministic financial arithmetic, row-level constraints,
  mature migration tooling, strong operational track record for
  audit-heavy systems.

Neither choice is exercised by anything in this repository yet: there is no
API layer and no persistence layer in Sprint 5A-R (see ADR 0002). Fixing the
choice now, before the Shared Kernel contracts (5B-R) and the Market Data
Platform's ingestion and storage requirements (5C-R) are known in detail,
would lock in an irrevocable decision on assumptions rather than evidence --
which is exactly what the platform's own governance rules (decisions must be
"supported by technical reasoning and approved through an Architecture
Decision Record") are designed to prevent.

## Decision

Do not fix the application framework or database yet. FastAPI + PostgreSQL
are recorded here as the leading candidates and the default assumption for
capacity planning, but this ADR's status stays `Proposed` until a follow-up
ADR (`0004-...` or later) is written at the start of Sprint 5C-R, once the
Market Data Platform's actual throughput, schema, and query-pattern
requirements are known, and can:

- confirm FastAPI + PostgreSQL, with reasoning tied to those requirements, or
- pick an alternative, with reasoning for why the default doesn't fit.

Until that ADR exists, no code in this repository may depend on FastAPI,
PostgreSQL, or any other web framework or database.

## Consequences

- 5A-R and 5B-R work stays framework-agnostic, which is correct: the Shared
  Kernel (domain types, contracts, audit, evidence) should not depend on the
  transport or storage layer.
- The follow-up ADR has a concrete trigger (start of 5C-R) instead of being
  indefinitely postponed.
- Anyone resuming this project must write that ADR before introducing a web
  framework or ORM dependency -- `idos-validate-repo`'s placeholder-marker
  and ADR checks make an undocumented dependency addition visible in review,
  though they cannot enforce this specific rule mechanically.
