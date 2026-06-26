"""Unit tests for the rebrand guard (tools/check_no_<legacy-brand>.py).

The legacy brand is assembled from parts (BRAND) so this test's own source
never contains the contiguous brand string — otherwise the guard, which scans
the whole repo including tests/, would flag this file. The guard's own source
uses the same trick.

Covers M3: the allowlist is LINE-LEVEL, so only a specific cross-reference line
is exempted while any other legacy-brand line in the same file is still caught.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

BRAND = "ege" + "analiz"
_CONTEXT = "ayrı dağıtım"  # the substring that exempts a CHANGELOG line

_TOOL = Path(__file__).resolve().parents[1] / "tools" / f"check_no_{BRAND}.py"
_spec = importlib.util.spec_from_file_location("brand_guard", _TOOL)
assert _spec and _spec.loader
_g = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_g)


def test_brand_regex_matches_legacy_only() -> None:
    assert _g.BRAND_RE.search(f"see {BRAND} repo")
    assert not _g.BRAND_RE.search("tarlaanaliz only")


def test_line_allowlist_exempts_only_context_line(tmp_path, monkeypatch, capsys) -> None:
    monkeypatch.setattr(_g, "REPO_ROOT", tmp_path)
    (tmp_path / "clean.md").write_text("tarlaanaliz content\n", encoding="utf-8")
    (tmp_path / "leak.md").write_text(f"migrate {BRAND} schemas\n", encoding="utf-8")
    (tmp_path / "CHANGELOG.md").write_text(
        f"Ege yok ({BRAND} {_CONTEXT})\n", encoding="utf-8"
    )
    rc = _g.main()
    out = capsys.readouterr().out
    assert rc == 1, "an un-exempt leak must fail the guard"
    assert "leak.md" in out
    assert "CHANGELOG.md" not in out, "the context line must stay exempt"


def test_changelog_leak_outside_context_is_caught(tmp_path, monkeypatch, capsys) -> None:
    """A NEW legacy-brand line in CHANGELOG (no context) must NOT hide."""
    monkeypatch.setattr(_g, "REPO_ROOT", tmp_path)
    (tmp_path / "CHANGELOG.md").write_text(
        f"({BRAND} {_CONTEXT})\nTODO: drop {BRAND} leftovers\n", encoding="utf-8"
    )
    rc = _g.main()
    out = capsys.readouterr().out
    assert rc == 1
    assert "CHANGELOG.md:2" in out


def test_clean_tree_with_exempt_line_passes(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(_g, "REPO_ROOT", tmp_path)
    (tmp_path / "a.md").write_text("tarlaanaliz\n", encoding="utf-8")
    (tmp_path / "CHANGELOG.md").write_text(f"({BRAND} {_CONTEXT})\n", encoding="utf-8")
    assert _g.main() == 0


def test_filename_with_brand_is_flagged(tmp_path, monkeypatch, capsys) -> None:
    monkeypatch.setattr(_g, "REPO_ROOT", tmp_path)
    (tmp_path / f"{BRAND}_notes.md").write_text("nothing here\n", encoding="utf-8")
    assert _g.main() == 1
    assert "_notes.md" in capsys.readouterr().out


def test_real_repo_is_clean() -> None:
    """Live regression: the actual repository has no legacy-brand leak."""
    assert _g.main() == 0
