"""Repository validation for IDOS.

Reads a YAML rules file (default: ``repo_validation.yaml`` at the repository
root) and checks the repository tree against it: required files/directories,
Architecture Decision Record (ADR) presence, placeholder markers left in
source code, and unit-test parity between ``src/idos`` and ``tests/unit``.

This is the "repository-validation tooling" and "GitHub Actions repository
validation" capability for Sprint 5A-R. It intentionally does not know
anything about the application domain -- it only enforces repository
hygiene rules that are themselves declared in the YAML rules file.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    """A single repository-validation failure."""

    rule: str
    message: str


def load_rules(rules_path: Path) -> dict[str, Any]:
    """Load and minimally shape-check the YAML rules file."""
    try:
        raw = rules_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ValueError(f"rules file not found: {rules_path}") from exc

    data = yaml.safe_load(raw)
    if not isinstance(data, dict):
        raise ValueError(f"rules file {rules_path} must contain a mapping at the top level")
    return data


def check_required_files(root: Path, rules: dict[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for rel_path in rules.get("required_files", []):
        if not (root / rel_path).is_file():
            issues.append(
                ValidationIssue("required_files", f"missing required file: {rel_path}")
            )
    return issues


def check_required_dirs(root: Path, rules: dict[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for rel_path in rules.get("required_dirs", []):
        if not (root / rel_path).is_dir():
            issues.append(
                ValidationIssue("required_dirs", f"missing required directory: {rel_path}")
            )
    return issues


def check_adr_directory(root: Path, rules: dict[str, Any]) -> list[ValidationIssue]:
    adr_rules = rules.get("adr")
    if not adr_rules:
        return []

    issues: list[ValidationIssue] = []
    adr_dir = root / adr_rules["directory"]
    minimum_count = int(adr_rules.get("minimum_count", 1))
    pattern = re.compile(adr_rules["filename_pattern"])

    if not adr_dir.is_dir():
        return [ValidationIssue("adr", f"ADR directory does not exist: {adr_rules['directory']}")]

    matching = [p for p in adr_dir.iterdir() if p.is_file() and pattern.fullmatch(p.name)]
    if len(matching) < minimum_count:
        issues.append(
            ValidationIssue(
                "adr",
                f"expected at least {minimum_count} ADR file(s) matching "
                f"{adr_rules['filename_pattern']!r} in {adr_rules['directory']}, "
                f"found {len(matching)}",
            )
        )

    non_matching = [
        p.name for p in adr_dir.iterdir() if p.is_file() and not pattern.fullmatch(p.name)
    ]
    for name in non_matching:
        issues.append(
            ValidationIssue(
                "adr",
                f"ADR filename does not match required pattern "
                f"{adr_rules['filename_pattern']!r}: {name}",
            )
        )
    return issues


def check_placeholder_markers(root: Path, rules: dict[str, Any]) -> list[ValidationIssue]:
    marker_rules = rules.get("placeholder_markers")
    if not marker_rules:
        return []

    issues: list[ValidationIssue] = []
    markers: list[str] = list(marker_rules.get("markers", []))
    if not markers:
        return []

    for scan_path in marker_rules.get("scan_paths", []):
        scan_root = root / scan_path
        if not scan_root.exists():
            continue
        for py_file in sorted(scan_root.rglob("*.py")):
            text = py_file.read_text(encoding="utf-8")
            for lineno, line in enumerate(text.splitlines(), start=1):
                for marker in markers:
                    if marker in line:
                        rel = py_file.relative_to(root)
                        issues.append(
                            ValidationIssue(
                                "placeholder_markers",
                                f"placeholder marker {marker!r} found at {rel}:{lineno}",
                            )
                        )
    return issues


def check_test_parity(root: Path, rules: dict[str, Any]) -> list[ValidationIssue]:
    parity_rules = rules.get("test_parity")
    if not parity_rules:
        return []

    source_root = root / parity_rules["source_root"]
    test_root = root / parity_rules["test_root"]
    exclude_names = set(parity_rules.get("exclude_names", []))

    if not source_root.is_dir():
        return [
            ValidationIssue(
                "test_parity", f"source_root does not exist: {parity_rules['source_root']}"
            )
        ]

    issues: list[ValidationIssue] = []
    for source_file in sorted(source_root.rglob("*.py")):
        if source_file.name in exclude_names:
            continue
        relative_dir = source_file.parent.relative_to(source_root)
        expected_test = test_root / relative_dir / f"test_{source_file.name}"
        if not expected_test.is_file():
            rel_source = source_file.relative_to(root)
            rel_expected = expected_test.relative_to(root)
            issues.append(
                ValidationIssue(
                    "test_parity",
                    f"no test file for {rel_source} (expected {rel_expected})",
                )
            )
    return issues


CHECKS = (
    check_required_files,
    check_required_dirs,
    check_adr_directory,
    check_placeholder_markers,
    check_test_parity,
)


def validate_repo(root: Path, rules: dict[str, Any]) -> list[ValidationIssue]:
    """Run every check against ``root`` and return all issues found."""
    issues: list[ValidationIssue] = []
    for check in CHECKS:
        issues.extend(check(root, rules))
    return issues


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="idos-validate-repo",
        description="Validate the IDOS repository against repo_validation.yaml rules.",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("."),
        help="Repository root to validate (default: current directory).",
    )
    parser.add_argument(
        "--rules",
        type=Path,
        default=None,
        help="Path to the YAML rules file (default: <root>/repo_validation.yaml).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_arg_parser()
    args = parser.parse_args(argv)

    root: Path = args.root.resolve()
    rules_path: Path = (args.rules or (root / "repo_validation.yaml")).resolve()

    try:
        rules = load_rules(rules_path)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    issues = validate_repo(root, rules)

    if not issues:
        print(f"idos-validate-repo: OK ({root})")
        return 0

    print(f"idos-validate-repo: {len(issues)} issue(s) found in {root}\n", file=sys.stderr)
    for issue in issues:
        print(f"  [{issue.rule}] {issue.message}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
