"""Unit tests for tools/pin_version.VersionPinner.

Covers the integrity-critical hashing surface that changed in 4.1.2:
- CRLF->LF normalization (cross-OS reproducible file hashes)
- enums/ coverage + posix-style relative paths in the aggregate
- order-independent aggregate checksum
- changelog accumulation (_extract_existing_changelog) with skip-version
- File Checksums table completeness: NO file in the aggregate may be silently
  dropped from the human-readable table (Datasets category + Other fallback).
"""

from __future__ import annotations

import hashlib
import importlib.util
import re
from pathlib import Path

import pytest

from release_state import REPIN_PENDING

_TOOL = Path(__file__).resolve().parents[1] / "tools" / "pin_version.py"

# --- Tur içi "beklenen kırmızı" beyanı (KADEME 0 / D5 · Ç6) --------------------
# Bir contract turu boyunca şema ağacı değişir ama agrega checksum BİLEREK yeniden
# pinlenmez (ara re-pin, yayımlanmış etiketin checksum anlamını bozar; tek re-pin
# noktası C8 release törenidir). Bu, `test_real_repo_checksum_verifies`'i tur boyunca
# kırmızı yapar. Eskiden bu kırmızı "beklenen" diye AĞIZDAN söyleniyordu; artık
# CONTRACTS_VERSION.md'deki `**Checksum State:** PENDING_REPIN` satırı ile BEYAN
# ediliyor (tek kaynak: tests/release_state.py) ve aynı satırı CI'daki verify-checksums
# işi de okuyor.
#
# `strict=True` neden önemli: C8'de re-pin yapılınca test GEÇMEYE başlar; strict xfail
# bunu XPASS = HATA sayar → beyan satırının kaldırılması zorunlu hâle gelir. Yani
# beyan kendi kendini temizler, bayat "beklenen kırmızı" mazereti yaşayamaz.

_spec = importlib.util.spec_from_file_location("pin_version", _TOOL)
assert _spec and _spec.loader
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
VersionPinner = _mod.VersionPinner


def _scaffold(base: Path) -> None:
    """Create the schemas/, enums/, api/ trees VersionPinner scans."""
    (base / "schemas" / "core").mkdir(parents=True)
    (base / "enums").mkdir()
    (base / "api").mkdir()


def test_compute_file_hash_normalizes_crlf(tmp_path: Path) -> None:
    p = VersionPinner(tmp_path)
    lf = tmp_path / "a.txt"
    lf.write_bytes(b"line1\nline2\n")
    crlf = tmp_path / "b.txt"
    crlf.write_bytes(b"line1\r\nline2\r\n")
    assert p.compute_file_hash(lf) == p.compute_file_hash(crlf)
    assert p.compute_file_hash(lf) == hashlib.sha256(b"line1\nline2\n").hexdigest()


def test_collect_includes_enums_and_uses_posix_paths(tmp_path: Path) -> None:
    _scaffold(tmp_path)
    (tmp_path / "schemas" / "core" / "x.json").write_text("{}", encoding="utf-8")
    (tmp_path / "enums" / "crop_type.enum.v1.json").write_text("{}", encoding="utf-8")
    (tmp_path / "api" / "spec.v1.yaml").write_text("openapi: 3.1.0", encoding="utf-8")
    p = VersionPinner(tmp_path)
    hashes = p.collect_file_hashes()
    assert "enums/crop_type.enum.v1.json" in hashes
    assert "schemas/core/x.json" in hashes
    assert "api/spec.v1.yaml" in hashes
    assert all("\\" not in key for key in hashes), "paths must be posix-style"


def test_contracts_checksum_is_order_independent(tmp_path: Path) -> None:
    p = VersionPinner(tmp_path)
    ordered = {"a/x.json": "11", "b/y.json": "22"}
    shuffled = {"b/y.json": "22", "a/x.json": "11"}
    assert p.compute_contracts_checksum(ordered) == p.compute_contracts_checksum(shuffled)


def test_table_lists_every_hashed_file(tmp_path: Path) -> None:
    """M1 regression: a file present in the aggregate must appear in the table.

    Includes a schemas/datasets/ file (named category) and a schemas/<unknown>/
    file (must land in the Other fallback) so neither is silently dropped.
    """
    _scaffold(tmp_path)
    (tmp_path / "schemas" / "datasets").mkdir()
    (tmp_path / "schemas" / "novel").mkdir()
    (tmp_path / "schemas" / "datasets" / "d.json").write_text("{}", encoding="utf-8")
    (tmp_path / "schemas" / "novel" / "w.json").write_text("{}", encoding="utf-8")
    (tmp_path / "enums" / "e.json").write_text("{}", encoding="utf-8")
    p = VersionPinner(tmp_path)
    content = p.generate_version_file((4, 1, 2), is_breaking=False, changelog_entry="t")
    for path in p.collect_file_hashes():
        assert path in content, f"{path} missing from File Checksums table"
    assert "### Datasets" in content
    assert "schemas/novel/w.json" in content  # caught by Other fallback


def test_extract_changelog_accumulates_and_skips_target(tmp_path: Path) -> None:
    p = VersionPinner(tmp_path)
    p.contracts_file.write_text(
        "header\n\n## Changelog\n\n"
        "### v2.0.0 (2026-01-01)\n\n**Breaking:** NO\n\nnew stuff\n\n"
        "### v1.0.0 (2025-01-01)\n\n**Breaking:** NO\n\nold stuff\n\n"
        "---\n\n## Verification\n\nblah\n",
        encoding="utf-8",
    )
    kept = p._extract_existing_changelog(skip_version="2.0.0")
    assert "v1.0.0" in kept and "old stuff" in kept
    assert "v2.0.0" not in kept
    both = p._extract_existing_changelog()
    assert "v1.0.0" in both and "v2.0.0" in both


def test_extract_changelog_empty_when_no_file(tmp_path: Path) -> None:
    p = VersionPinner(tmp_path)
    assert p._extract_existing_changelog() == ""


def test_get_and_increment_version(tmp_path: Path) -> None:
    p = VersionPinner(tmp_path)
    p.contracts_file.write_text("## Version: 4.1.2\n", encoding="utf-8")
    assert p.get_current_version() == (4, 1, 2)
    assert p.increment_version("patch") == (4, 1, 3)
    assert p.increment_version("minor") == (4, 2, 0)
    assert p.increment_version("major") == (5, 0, 0)


def test_pin_version_writes_and_round_trips(tmp_path: Path) -> None:
    """End-to-end: pin writes a lock file whose checksum self-verifies."""
    _scaffold(tmp_path)
    (tmp_path / "schemas" / "core" / "x.json").write_text("{}", encoding="utf-8")
    (tmp_path / "enums" / "e.json").write_text("{}", encoding="utf-8")
    p = VersionPinner(tmp_path)
    assert p.pin_version(version=(1, 0, 0), changelog="init") is True
    assert p.contracts_file.exists()
    assert p.get_current_version() == (1, 0, 0)
    assert p.verify_checksums() is True


def test_verify_false_when_no_file(tmp_path: Path) -> None:
    assert VersionPinner(tmp_path).verify_checksums() is False


def test_verify_detects_mismatch(tmp_path: Path) -> None:
    _scaffold(tmp_path)
    (tmp_path / "enums" / "e.json").write_text("{}", encoding="utf-8")
    p = VersionPinner(tmp_path)
    p.contracts_file.write_text(
        "**Contracts Checksum (SHA-256):** `" + "0" * 64 + "`\n", encoding="utf-8"
    )
    assert p.verify_checksums() is False


@pytest.mark.release_gate
@pytest.mark.xfail(
    REPIN_PENDING,
    strict=True,
    reason=(
        "CONTRACTS_VERSION.md 'Checksum State: PENDING_REPIN' beyan ediyor — tur içi "
        "beklenen kırmızı; C8 re-pin'inde beyan kalkar ve bu test normal GEÇER "
        "(strict: geçerse XPASS = hata → beyanı silmeyi zorlar)"
    ),
)
def test_real_repo_checksum_verifies() -> None:
    """Live regression: the committed CONTRACTS_VERSION.md self-verifies.

    Recomputes directly (rather than calling verify_checksums, which prints
    non-ASCII status glyphs) so the assertion is portable under capture.

    ⚠️ `release_gate` işaretlidir: C8 öncesi bu test **deselect EDİLEMEZ**
    (`-m "not release_gate"` çalıştırmak tests/conftest.py tarafından reddedilir).
    """
    repo = _TOOL.parents[1]
    p = VersionPinner(repo)
    content = p.contracts_file.read_text(encoding="utf-8")
    match = re.search(r"Contracts Checksum \(SHA-256\):\*\* `([a-f0-9]{64})`", content)
    assert match, "pinned checksum not found in CONTRACTS_VERSION.md"
    actual = p.compute_contracts_checksum(p.collect_file_hashes())
    assert actual == match.group(1)


# --- ÖD-0 (sürüm-riski lensi, 2026-08-02) -------------------------------------
# BULGU: yayımlanan sürümün CHANGELOG bölümü olduğunu **hiçbir kapı ölçmüyordu.**
# `pin_version.py` yalnız CONTRACTS_VERSION.md'yi yazar; CHANGELOG.md'deki
# `## [Unreleased]` başlığını `## [X.Y.Z]`'ye çevirmek ELLE yapılan bir adımdır ve
# unutulursa **her kapı yeşil kalır** — sürüm, notları hâlâ "Unreleased" etiketli
# olarak yayımlanır. Asimetri ölçüldü: worker deposunun CI'ında CHANGELOG kapısı VAR,
# SSOT deposunda YOKTU.
#
# Kapı tur içinde de anlamlıdır: CONTRACTS_VERSION.md bir önceki yayımlanmış sürümü
# gösterdiği sürece o sürümün bölümü aranır. C8'de `--minor` 7.4.0 yazınca kapı
# KIRMIZIYA döner ve `[Unreleased]` başlığını çevirmeyi ZORLAR.


def _released_version() -> str:
    """Yayımlanan sürüm — kanonik okuyucudan (yeni regex yazılmaz, D16 dersi)."""
    import sys

    sys.path.insert(0, str(_TOOL.parent))
    from read_contracts_version import read_version  # type: ignore[import-not-found]

    repo = _TOOL.parents[1]
    return read_version((repo / "CONTRACTS_VERSION.md").read_text(encoding="utf-8")).lstrip("v")


@pytest.mark.release_gate
def test_changelog_has_a_section_for_the_pinned_version() -> None:
    version = _released_version()
    changelog = (_TOOL.parents[1] / "CHANGELOG.md").read_text(encoding="utf-8")
    headings = re.findall(r"^##\s*\[([^\]]+)\]", changelog, re.MULTILINE)
    assert version in headings, (
        f"CONTRACTS_VERSION.md `{version}` diyor ama CHANGELOG.md'de `## [{version}]` "
        f"bölümü YOK (bulunan başlıklar: {headings[:6]}). C8 töreninde `pin_version.py` "
        "sürümü yazar ama CHANGELOG başlığını ÇEVİRMEZ — `## [Unreleased]` satırını "
        f"`## [{version}] - <tarih>` yapın, yoksa sürüm notları 'Unreleased' etiketiyle "
        "yayımlanır."
    )


@pytest.mark.release_gate
def test_pinned_version_section_is_not_empty() -> None:
    """Başlık ATMAK yetmez: bölümün gövdesi olmalı (ÖD-12'nin dersi, başlık ≠ gövde)."""
    version = _released_version()
    changelog = (_TOOL.parents[1] / "CHANGELOG.md").read_text(encoding="utf-8")
    match = re.search(
        rf"^##\s*\[{re.escape(version)}\][^\n]*\n(.*?)(?=^##\s*\[|\Z)",
        changelog,
        re.MULTILINE | re.DOTALL,
    )
    assert match, f"`## [{version}]` bölümü bulunamadı"
    body = match.group(1).strip()
    assert len(body) >= 200, (
        f"`## [{version}]` bölümünün gövdesi {len(body)} karakter — boş başlık kapıyı "
        "geçemez. Sürüm ne taşıyorsa adıyla yazılmalı (yayımlanmış içerik ↔ CHANGELOG "
        "örtüşmesi, ÖD-0)."
    )
