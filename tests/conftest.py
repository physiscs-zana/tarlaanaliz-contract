"""Test oturumu kapıları — "sessiz atlama yeşil sayılmaz" (KADEME 0 / D4 · D5).

NEDEN (2026-07-31, 10-disiplin denetimi):
    Yeni yazılan 156 testin **%40'ı CI'da hiç koşmuyordu** ve bu HİÇBİR YERDE
    görünmüyordu:
      * Q2 — `test_calibrated_manifest_fields` 18/18 test `pyyaml` kurulu olmadığı için
        modül düzeyinde atlanıyordu (CI `pip install jsonschema pytest pytest-cov`
        diyordu; `pyyaml` yalnız `pyproject.toml`'daydı).
      * Q3/AR4/SD6 — vendored parite süiti 45 test kardeş depo bulunmadığı için
        atlanıyordu; CI çıktısında yalnız nokta görünüyordu.
    Sonuç: kapı **yeşil** görünüyordu ama koruduğunu iddia ettiği şeyi hiç ölçmemişti.

Bu dosyanın iki kuralı:
    1. **Beyan edilmemiş atlama = HATA.** Bir test atlanacaksa gerekçesi aşağıdaki
       ALLOWED_SKIP_REASONS listesinde YAZILI olmalı. Yeni bir atlama gerekçesi
       (ör. "pyyaml yok") sessizce yeşile dönüşemez; oturumu düşürür.
    2. **`release_gate` deselect edilemez.** Tur içi "beklenen kırmızı"yı
       `-m "not release_gate"` ile gizlemek, kırmızıyı çözmek değil saklamaktır.
"""

from __future__ import annotations

from typing import Any

import pytest


# Atlanmasına İZİN VERİLEN gerekçeler (alt dize eşleşmesi). Her giriş bir taahhüttür:
# "bu atlama biliniyor, gerekçesi şu ve nerede koştuğu belli".
ALLOWED_SKIP_REASONS: tuple[tuple[str, str], ...] = (
    (
        "kardeş depo yok",
        "Vendored parite süiti (tests/test_vendored_parity.py) kardeş depoları okur; "
        "GitHub Actions'ta yalnız bu depo checkout edilir. Bu kapı C8 release töreninde "
        "YEREL olarak koşar ve SDLC_GATES §3C'de zorunludur.",
    ),
)

_ALLOWED_PATTERNS: tuple[str, ...] = tuple(pattern for pattern, _note in ALLOWED_SKIP_REASONS)


def _reason_of(report: Any) -> str:
    longrepr = getattr(report, "longrepr", None)
    if isinstance(longrepr, tuple) and len(longrepr) == 3:
        return str(longrepr[2])
    return str(longrepr) if longrepr is not None else "<gerekçesiz>"


def _is_declared(reason: str) -> bool:
    return any(pattern in reason for pattern in _ALLOWED_PATTERNS)


def pytest_configure(config: Any) -> None:
    """`release_gate` testlerini deselect etmeyi reddet (D5 · SD4)."""
    markexpr = str(getattr(config.option, "markexpr", "") or "")
    if "release_gate" in markexpr and "not" in markexpr:
        raise pytest.UsageError(
            f"release_gate testleri deselect EDİLEMEZ (-m '{markexpr}').\n"
            "Tur içi beklenen kırmızı, CONTRACTS_VERSION.md'deki "
            "'**Checksum State:** PENDING_REPIN' beyanıyla yönetilir; beyan xfail(strict) "
            "üretir ve C8 re-pin'inde kendini temizler.\n"
            "Bkz. docs/checklists/SDLC_GATES.md §3A."
        )


def pytest_sessionfinish(session: Any, exitstatus: int) -> None:
    """Atlanan testleri GÖRÜNÜR kıl; beyan edilmemiş atlamada oturumu düşür."""
    reporter = session.config.pluginmanager.get_plugin("terminalreporter")
    if reporter is None:  # -p no:terminal ile koşulursa sessiz kalma hakkı yok ama
        return  # raporlayacak yüzey de yok.

    skipped = reporter.stats.get("skipped", [])
    if not skipped:
        reporter.write_line("SKIP BÜTÇESİ: 0 atlanan test.", green=True)
        return

    counts: dict[str, int] = {}
    for report in skipped:
        reason = _reason_of(report)
        counts[reason] = counts.get(reason, 0) + 1

    undeclared = {reason: n for reason, n in counts.items() if not _is_declared(reason)}

    reporter.write_line("")
    reporter.write_line(f"SKIP BÜTÇESİ: {len(skipped)} test atlandı")
    for reason, number in sorted(counts.items(), key=lambda kv: -kv[1]):
        state = "BEYAN EDİLMEMİŞ" if reason in undeclared else "beyanlı"
        reporter.write_line(f"  [{state}] {number}x {reason}")

    if undeclared:
        reporter.write_line(
            "ATLAMA KAPISI DÜŞTÜ — yukarıdaki gerekçeler tests/conftest.py "
            "ALLOWED_SKIP_REASONS listesinde yok. Sessiz atlama yeşil sayılmaz: ya eksik "
            "bağımlılığı kurun ya atlamayı gerekçesiyle beyan edin.",
            red=True,
        )
        session.exitstatus = 1
