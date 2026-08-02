# Non-functional requirements

Cross-cutting qualities every module must satisfy, regardless of which
sprint introduces it. See [`00-index.md`](00-index.md) for the status
legend.

| ID | Requirement | Applies to | Status in this repo |
|---|---|---|---|
| NFR-01 | Determinism: identical inputs, code version, and config version produce identical outputs. No unseeded randomness or uncontrolled floating-point drift in anything that touches money or a governed decision. | Everything downstream of the Shared Kernel | N/A yet -- no financial calculations exist in 5A-R; the constraint is recorded here so FR-101 (`Money`, `Clock`) is designed against it |
| NFR-02 | Every module ships with unit tests; anything crossing a module or process boundary also gets integration/contract tests; anything with a failure mode gets a failure-path test. | All | Enforced for 5A-R by `idos-validate-repo`'s test-parity check plus CI |
| NFR-03 | No merged code is treated as complete if it contains scaffolding, TODO/FIXME markers, or placeholder logic standing in for real behavior. | All | Enforced by `idos-validate-repo`'s placeholder-marker check |
| NFR-04 | Architecture-significant decisions are recorded as ADRs before the decision is acted on, not after. | All | Enforced procedurally (ADR 0001); `idos-validate-repo` only checks that ADRs exist and are named correctly, not that every decision has one |
| NFR-05 | Every governed recommendation and every state-changing operation is traceable end-to-end: inputs, code version, config version, timestamp, and the human or rule that authorized it. | Decision Resolver, Portfolio Governor, and anything that changes portfolio state | Planned (FR-104, FR-105) |
| NFR-06 | Secrets and credentials are never committed to the repository; required secrets fail loudly and explicitly if absent, rather than falling back to an insecure default. | Configuration, market-data and brokerage integrations | Planned (FR-102); `.gitignore` excludes local env/secret files starting now |
| NFR-07 | CI enforces lint, static type checking, automated tests with a minimum coverage floor, and repository validation on every change before merge. | All | Done -- `.github/workflows/ci.yml` |
| NFR-08 | The system is observable: structured logs and metrics exist for operationally significant events, sufficient to diagnose an incident without reading source code. | All | Planned (FR-804) |
| NFR-09 | Any persistence layer has documented migration and rollback procedures. | Anything with a database | Planned -- blocked on ADR 0003's follow-up |
| NFR-10 | Backups and disaster-recovery procedures exist and are tested, not merely documented. | Production deployment | Planned (FR-901) |
| NFR-11 | Any learning/adaptive component is evaluated offline against a challenger process and requires explicit human gating before it can influence live output. | Controlled learning (5E-R) | Out of scope until 5E-R; uncontrolled self-modification is permanently out of scope (FR-953) |
