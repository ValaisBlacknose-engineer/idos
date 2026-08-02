# Requirements index

- [`01-functional-requirements.md`](01-functional-requirements.md) -- what
  the full platform must do, organized by module, each with a stable ID and
  a status.
- [`02-nonfunctional-requirements.md`](02-nonfunctional-requirements.md) --
  the cross-cutting qualities (determinism, security, auditability, ...)
  every module must satisfy.
- [`03-sprint-5-remediation-plan.md`](03-sprint-5-remediation-plan.md) --
  the approved delivery sequence (5A-R through 5E-R) and this repository's
  position in it.

## Status legend

Used consistently across every requirements document in this directory.

| Status | Meaning |
|---|---|
| `Done` | Implemented, tested, and passing CI in this repository. |
| `Planned` | Specified here; no code in this repository implements it yet. |
| `Out of scope` | Explicitly excluded from the platform as approved (see `docs/architecture/00-platform-overview.md`, "Explicit non-goals"). |

Traceability convention: every non-trivial commit or ADR that implements or
changes a requirement should reference its ID (e.g. `FR-101`) in the commit
message or ADR text, per the "traceability to approved requirements and
decisions" delivery requirement.
