"""Unit and self-check tests for idos.tooling.repo_validate."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
import yaml

from idos.tooling import repo_validate as rv


def _rules(tmp_path: Path) -> dict[str, Any]:
    return {
        "required_files": ["README.md", "LICENSE"],
        "required_dirs": ["docs/adr", "src/pkg"],
        "adr": {
            "directory": "docs/adr",
            "minimum_count": 1,
            "filename_pattern": r"^[0-9]{4}-[a-z0-9-]+\.md$",
        },
        "placeholder_markers": {
            "scan_paths": ["src"],
            "markers": ["TODO", "FIXME"],
        },
        "test_parity": {
            "source_root": "src/pkg",
            "test_root": "tests/unit",
            "exclude_names": ["__init__.py"],
        },
    }


def _make_valid_repo(tmp_path: Path) -> Path:
    (tmp_path / "README.md").write_text("# demo\n")
    (tmp_path / "LICENSE").write_text("MIT\n")
    adr_dir = tmp_path / "docs" / "adr"
    adr_dir.mkdir(parents=True)
    (adr_dir / "0001-record-architecture-decisions.md").write_text("# ADR 1\n")

    pkg_dir = tmp_path / "src" / "pkg"
    pkg_dir.mkdir(parents=True)
    (pkg_dir / "__init__.py").write_text("")
    (pkg_dir / "widget.py").write_text("def widget() -> int:\n    return 1\n")

    test_dir = tmp_path / "tests" / "unit"
    test_dir.mkdir(parents=True)
    (test_dir / "test_widget.py").write_text("def test_widget() -> None:\n    assert True\n")

    return tmp_path


# ---------------------------------------------------------------------------
# load_rules
# ---------------------------------------------------------------------------


def test_load_rules_missing_file_raises(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="rules file not found"):
        rv.load_rules(tmp_path / "does_not_exist.yaml")


def test_load_rules_rejects_non_mapping_top_level(tmp_path: Path) -> None:
    rules_path = tmp_path / "rules.yaml"
    rules_path.write_text("- just\n- a\n- list\n")
    with pytest.raises(ValueError, match="must contain a mapping"):
        rv.load_rules(rules_path)


def test_load_rules_parses_valid_yaml(tmp_path: Path) -> None:
    rules_path = tmp_path / "rules.yaml"
    rules_path.write_text(yaml.safe_dump({"required_files": ["a.txt"]}))
    assert rv.load_rules(rules_path) == {"required_files": ["a.txt"]}


# ---------------------------------------------------------------------------
# check_required_files / check_required_dirs
# ---------------------------------------------------------------------------


def test_check_required_files_passes_when_present(tmp_path: Path) -> None:
    repo = _make_valid_repo(tmp_path)
    assert rv.check_required_files(repo, _rules(tmp_path)) == []


def test_check_required_files_reports_missing(tmp_path: Path) -> None:
    repo = _make_valid_repo(tmp_path)
    (repo / "LICENSE").unlink()
    issues = rv.check_required_files(repo, _rules(tmp_path))
    assert len(issues) == 1
    assert issues[0].rule == "required_files"
    assert "LICENSE" in issues[0].message


def test_check_required_dirs_reports_missing(tmp_path: Path) -> None:
    repo = _make_valid_repo(tmp_path)
    issues = rv.check_required_dirs(repo, {"required_dirs": ["docs/adr", "docs/missing"]})
    assert len(issues) == 1
    assert "docs/missing" in issues[0].message


# ---------------------------------------------------------------------------
# check_adr_directory
# ---------------------------------------------------------------------------


def test_check_adr_directory_missing_dir_reports_issue(tmp_path: Path) -> None:
    rules = _rules(tmp_path)
    issues = rv.check_adr_directory(tmp_path, rules)
    assert len(issues) == 1
    assert "does not exist" in issues[0].message


def test_check_adr_directory_below_minimum_count(tmp_path: Path) -> None:
    repo = _make_valid_repo(tmp_path)
    rules = _rules(tmp_path)
    rules["adr"]["minimum_count"] = 2
    issues = rv.check_adr_directory(repo, rules)
    assert any("expected at least 2" in i.message for i in issues)


def test_check_adr_directory_rejects_bad_filename(tmp_path: Path) -> None:
    repo = _make_valid_repo(tmp_path)
    (repo / "docs" / "adr" / "not-a-valid-name.md").write_text("# oops\n")
    issues = rv.check_adr_directory(repo, _rules(tmp_path))
    assert any("does not match required pattern" in i.message for i in issues)


def test_check_adr_directory_passes_for_valid_repo(tmp_path: Path) -> None:
    repo = _make_valid_repo(tmp_path)
    assert rv.check_adr_directory(repo, _rules(tmp_path)) == []


def test_check_adr_directory_no_rules_returns_empty(tmp_path: Path) -> None:
    assert rv.check_adr_directory(tmp_path, {}) == []


# ---------------------------------------------------------------------------
# check_placeholder_markers
# ---------------------------------------------------------------------------


def test_check_placeholder_markers_detects_marker(tmp_path: Path) -> None:
    repo = _make_valid_repo(tmp_path)
    (repo / "src" / "pkg" / "widget.py").write_text("# TODO: finish this\ndef widget(): ...\n")
    issues = rv.check_placeholder_markers(repo, _rules(tmp_path))
    assert len(issues) == 1
    assert "TODO" in issues[0].message
    assert "widget.py:1" in issues[0].message


def test_check_placeholder_markers_clean_tree_passes(tmp_path: Path) -> None:
    repo = _make_valid_repo(tmp_path)
    assert rv.check_placeholder_markers(repo, _rules(tmp_path)) == []


def test_check_placeholder_markers_no_config_returns_empty(tmp_path: Path) -> None:
    assert rv.check_placeholder_markers(tmp_path, {}) == []


def test_check_placeholder_markers_skips_missing_scan_path(tmp_path: Path) -> None:
    rules = {"placeholder_markers": {"scan_paths": ["does/not/exist"], "markers": ["TODO"]}}
    assert rv.check_placeholder_markers(tmp_path, rules) == []


# ---------------------------------------------------------------------------
# check_test_parity
# ---------------------------------------------------------------------------


def test_check_test_parity_passes_when_test_exists(tmp_path: Path) -> None:
    repo = _make_valid_repo(tmp_path)
    assert rv.check_test_parity(repo, _rules(tmp_path)) == []


def test_check_test_parity_reports_missing_test(tmp_path: Path) -> None:
    repo = _make_valid_repo(tmp_path)
    (repo / "src" / "pkg" / "widget.py").unlink()
    (repo / "src" / "pkg" / "gadget.py").write_text("def gadget() -> int:\n    return 2\n")
    issues = rv.check_test_parity(repo, _rules(tmp_path))
    assert len(issues) == 1
    assert "gadget.py" in issues[0].message
    assert "test_gadget.py" in issues[0].message


def test_check_test_parity_excludes_configured_names(tmp_path: Path) -> None:
    repo = _make_valid_repo(tmp_path)
    # __init__.py has no matching test file, but is excluded by name.
    assert not any(
        "__init__" in issue.message for issue in rv.check_test_parity(repo, _rules(tmp_path))
    )


def test_check_test_parity_missing_source_root(tmp_path: Path) -> None:
    issues = rv.check_test_parity(tmp_path, _rules(tmp_path))
    assert len(issues) == 1
    assert "source_root does not exist" in issues[0].message


# ---------------------------------------------------------------------------
# validate_repo / main
# ---------------------------------------------------------------------------


def test_validate_repo_aggregates_all_checks(tmp_path: Path) -> None:
    repo = _make_valid_repo(tmp_path)
    assert rv.validate_repo(repo, _rules(tmp_path)) == []

    (repo / "LICENSE").unlink()
    (repo / "src" / "pkg" / "widget.py").write_text("# FIXME broken\n")
    issues = rv.validate_repo(repo, _rules(tmp_path))
    rules_hit = {issue.rule for issue in issues}
    assert "required_files" in rules_hit
    assert "placeholder_markers" in rules_hit


def test_main_returns_zero_for_valid_repo(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    repo = _make_valid_repo(tmp_path)
    rules_path = repo / "repo_validation.yaml"
    rules_path.write_text(yaml.safe_dump(_rules(tmp_path)))

    exit_code = rv.main(["--root", str(repo), "--rules", str(rules_path)])

    assert exit_code == 0
    assert "OK" in capsys.readouterr().out


def test_main_returns_one_for_invalid_repo(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    repo = _make_valid_repo(tmp_path)
    (repo / "LICENSE").unlink()
    rules_path = repo / "repo_validation.yaml"
    rules_path.write_text(yaml.safe_dump(_rules(tmp_path)))

    exit_code = rv.main(["--root", str(repo), "--rules", str(rules_path)])

    err = capsys.readouterr().err
    assert exit_code == 1
    assert "LICENSE" in err


def test_main_returns_two_for_missing_rules_file(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    exit_code = rv.main(["--root", str(tmp_path), "--rules", str(tmp_path / "missing.yaml")])
    assert exit_code == 2
    assert "error:" in capsys.readouterr().err


def test_main_defaults_rules_path_to_repo_root(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    repo = _make_valid_repo(tmp_path)
    (repo / "repo_validation.yaml").write_text(yaml.safe_dump(_rules(tmp_path)))

    exit_code = rv.main(["--root", str(repo)])

    assert exit_code == 0
    assert "OK" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# Self-check: the actual IDOS repository must pass its own rules.
# ---------------------------------------------------------------------------


def test_real_repository_passes_validation() -> None:
    repo_root = Path(__file__).resolve().parents[3]
    rules = rv.load_rules(repo_root / "repo_validation.yaml")
    issues = rv.validate_repo(repo_root, rules)
    assert issues == [], "\n".join(f"[{i.rule}] {i.message}" for i in issues)
