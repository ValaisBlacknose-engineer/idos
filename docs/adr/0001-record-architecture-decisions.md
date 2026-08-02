# 0001. Record architecture decisions

- Status: Accepted
- Date: 2026-08-02

## Context

IDOS is governed: architecture, security boundaries and approved business
logic may not change without a written decision record. Decisions and their
reasoning need to survive past the engineer who made them, be auditable, and
be citable from requirements and evidence documents.

## Decision

We record architecture-significant decisions as Architecture Decision
Records (ADRs) under `docs/adr/`, one file per decision, numbered
sequentially, using this template:

```
# NNNN. Title

- Status: Proposed | Accepted | Superseded by NNNN
- Date: YYYY-MM-DD

## Context
## Decision
## Consequences
```

A decision is "architecture-significant" if it constrains a module boundary,
a data contract, a technology choice, a security control, or the approved
sprint sequence. Anything narrower (a function's internal implementation, a
variable name) does not need an ADR.

`idos-validate-repo` enforces that at least one ADR exists and that every
file in `docs/adr/` matches the `NNNN-kebab-case-title.md` naming pattern
(see `repo_validation.yaml`).

## Consequences

- Every architecture-significant change is traceable to a written, dated
  rationale, satisfying the "traceability to approved requirements and
  decisions" delivery requirement.
- Proposing a technology or design change costs a small amount of writing
  up front, in exchange for not re-litigating it later.
- Superseding a decision must add a new ADR that references the old one
  rather than editing history in place.
