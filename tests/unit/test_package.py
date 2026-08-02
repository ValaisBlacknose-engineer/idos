"""Smoke test: the idos package imports and exposes version metadata."""

from __future__ import annotations

import re

import idos


def test_version_is_a_semver_string() -> None:
    assert re.fullmatch(r"\d+\.\d+\.\d+", idos.__version__)
