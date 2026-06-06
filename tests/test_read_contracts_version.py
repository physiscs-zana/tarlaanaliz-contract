"""Tests for tools/read_contracts_version.read_version.

Regression: the tool previously searched for `semver: vX.Y.Z`, but pin_version.py
writes `## Version: X.Y.Z`, so it always raised SystemExit('semver not found') and
broke sync_to_repos.py. These tests lock in parsing of the canonical format.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


_TOOL = Path(__file__).resolve().parents[1] / "tools" / "read_contracts_version.py"
_spec = importlib.util.spec_from_file_location("read_contracts_version", _TOOL)
assert _spec and _spec.loader
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
read_version = _mod.read_version


def test_canonical_format_parsed() -> None:
    """Canonical format emitted by pin_version.py."""
    text = "# TarlaAnaliz Contracts Version Lock\n\n## Version: 3.2.0\n\n**Breaking Change:** NO\n"
    assert read_version(text) == "v3.2.0"


def test_canonical_with_v_prefix() -> None:
    assert read_version("## Version: v1.0.0\n") == "v1.0.0"


def test_legacy_semver_fallback() -> None:
    """The old 'semver: vX.Y.Z' form is still supported for resilience."""
    assert read_version("semver: v9.8.7\n") == "v9.8.7"


def test_missing_version_raises() -> None:
    with pytest.raises(SystemExit):
        read_version("# no version here\n")


def test_real_contracts_version_file_parses() -> None:
    """The repo's actual CONTRACTS_VERSION.md is parseable (live regression)."""
    real = (_TOOL.parents[1] / "CONTRACTS_VERSION.md").read_text(encoding="utf-8")
    out = read_version(real)
    assert out.startswith("v") and out.count(".") == 2
