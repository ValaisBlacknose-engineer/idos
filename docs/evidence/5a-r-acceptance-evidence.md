# Sprint 5A-R acceptance evidence

Captured 2026-08-02, on macOS (Darwin 27.0.0), Python 3.12.13, from a clean
`pip install -e ".[dev]"` in a fresh virtual environment. Every block below
is real, unedited command output, not a transcription -- re-running the
commands in [`CLAUDE.md`](../../CLAUDE.md#working-in-this-repo) against
this commit should reproduce it.

## FR-001 -- installable package

```
$ pip install -e ".[dev]"
...
Successfully installed idos-0.1.0 ...
```

## FR-005 / NFR-07 -- lint gate

```
$ ruff check .
All checks passed!
```

## FR-005 / NFR-07 -- type-check gate (strict mypy)

```
$ mypy src tests
Success: no issues found in 5 source files
```

## FR-002 / FR-005 / NFR-02 / NFR-07 -- test suite with coverage

```
$ pytest --cov --cov-report=term-missing
============================= test session starts ==============================
platform darwin -- Python 3.12.13, pytest-9.1.1, pluggy-1.6.0
rootdir: ...
configfile: pyproject.toml
testpaths: tests
plugins: cov-7.1.0
collected 26 items

tests/unit/test_package.py .                                             [  3%]
tests/unit/tooling/test_repo_validate.py .........................       [100%]

================================ tests coverage ================================
______________ coverage: platform darwin, python 3.12.13-final-0 _______________

Name                                Stmts   Miss Branch BrPart  Cover   Missing
-------------------------------------------------------------------------------
src/idos/__init__.py                    1      0      0      0   100%
src/idos/tooling/__init__.py            0      0      0      0   100%
src/idos/tooling/repo_validate.py     121      3     52      3    97%   113, 137, 231
-------------------------------------------------------------------------------
TOTAL                                 122      3     52      3    97%
Required test coverage of 90.0% reached. Total coverage: 96.55%
============================== 26 passed in 0.20s ==============================
```

26/26 tests pass. Coverage floor is `fail_under = 90` (`pyproject.toml`);
actual coverage is 96.55%, comfortably above it. The three uncovered
branches (lines 113, 137, 231) are non-matching-ADR-filename and
missing-scan-path edge cases not exercised by the current test list --
tracked as acceptable for 5A-R, not hidden.

## FR-003 / FR-004 / NFR-03 -- repository validation

```
$ idos-validate-repo
idos-validate-repo: OK (.../Senior Python Engineering Team for Investment Decision Platform)
```

Includes `test_real_repository_passes_validation`
(`tests/unit/tooling/test_repo_validate.py`), which runs the same check as
part of the pytest suite above -- the repository validates itself on every
test run, not just when someone remembers to run the CLI manually.

## FR-006 -- this document

This file is itself FR-006's deliverable: reproducible acceptance evidence,
captured at sprint completion, cited from the sprint plan
([`docs/requirements/03-sprint-5-remediation-plan.md`](../requirements/03-sprint-5-remediation-plan.md)).

## Not covered by this evidence

CI (`.github/workflows/ci.yml`) has not run on GitHub Actions as of this
commit -- there is no remote for it to run against yet (this is a local
case study, not a hosted repository). The workflow runs the identical
commands shown above, so this local evidence is the CI outcome by
construction, but it is not a substitute for an actual green Actions run
once this repository has a remote.
