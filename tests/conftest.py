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
    1. **Beyan edilmemiş atlama = HATA.** Bir test atlanacaksa hem gerekçesi hem
       **DOSYASI** aşağıdaki ALLOWED_SKIP_REASONS listesinde YAZILI olmalı. Yeni bir
       atlama gerekçesi (ör. "pyyaml yok") ya beyanlı bir gerekçeyi yeni bir dosyada
       kullanmak sessizce yeşile dönüşemez; oturumu düşürür.
    2. **`release_gate` deselect edilemez.** Tur içi "beklenen kırmızı"yı
       `-m "not release_gate"` ile gizlemek, kırmızıyı çözmek değil saklamaktır.
"""

from __future__ import annotations

from typing import Any

import pytest


# Atlanmasına İZİN VERİLEN gerekçeler. Her giriş bir taahhüttür: "bu atlama biliniyor,
# gerekçesi şu, HANGİ DOSYADA olduğu yazılı ve nerede koştuğu belli".
#
# ⚠️ 2026-08-01 öz-denetiminde ölçülen kusur (Ö2/Ö3): eşleşme yalnız GEREKÇE dizesine
# bakıyordu, dosyaya bakmıyordu. Sonuç: `test_c11_sorties_absorption.py` aynı gerekçeyle
# atlamaya başladı ve **hiç adı geçmeden** bu beyanın altına sığındı. Beyan yalnız parite
# süitini anlatıyordu; kapsam sessizce genişledi. Beyan artık dosyayı da kapsar — kapsam
# dışı bir dosya aynı gerekçeyi kullanırsa oturum DÜŞER.
ALLOWED_SKIP_REASONS: tuple[tuple[str, tuple[str, ...], str], ...] = (
    (
        "kardeş depo yok",
        (
            "tests/test_vendored_parity.py",
            "tests/test_c11_sorties_absorption.py",
            # 2026-08-11 · KAPSAM GENİŞLETME KARARI: `test_vendored_policy_parity.py`
            # aynı D4-b desenindedir — kanonik ile vendored kopyanın ALAN SIZMASI
            # POLİTİKASINI karşılaştırır ve kardeş depo checkout'u ister. Neden ayrı bir
            # dosya: mevcut parite süiti ortak `$defs` ALANLARINI karşılaştırıyor,
            # `$.properties.*` altındaki iç içe düğümlerin politika anahtarına bakmıyor —
            # ölçüldü, 5 sapma iki kapının da (propagate --check dahil) kör noktasındaydı.
            "tests/test_vendored_policy_parity.py",
        ),
        "Bu iki süit kardeş depoları okur; bu deponun Actions'ında yalnız kendisi checkout "
        "edilir → CI'da atlanırlar. D4-b KARARI: kapı bu depoda değil KARŞI TARAFTA koşar — "
        "bu depo PUBLIC, kardeşlerin üçü de PRIVATE, dolayısıyla kardeş CI'ı burayı sırsız "
        "çekebilir ama tersi private anahtarı public Actions'a koyardı. Kardeş depo bu "
        "dosyaları olduğu gibi koşar (E17/W10 — **ikisini birden**, bkz. aşağıdaki ölçüm). "
        "Ayrıca C8 release töreninde YEREL koşum zorunludur (SDLC_GATES §3C).",
    ),
)

#: 2026-08-01 CI ÖLÇÜMÜ (run 30710485267, commit 20e541f) — sayı değil **oran** beyanıdır:
#: `1093 passed, 134 skipped, 2 xfailed`; yerelde (kardeş depolar diskte) `1227 passed,
#: 0 skipped`. Yani 1227'nin **134'ü (%11) bu deponun CI'ında görünmez**. Dağılım:
#: `test_vendored_parity.py` 132 · `test_c11_sorties_absorption.py` 2.
#: 🔴 Öz-denetim bulgusu Ö1: ee4aed7 YERELDE kırmızıydı ama CI'ı YEŞİL geçti — kırılan test
#: tam bu 2'nin içindeydi. Bu depoda CI, kardeş-bağımlı kapılar için otoriter DEĞİLDİR.
SIBLING_DEPENDENT_FILES: tuple[str, ...] = ALLOWED_SKIP_REASONS[0][1]


def _reason_of(report: Any) -> str:
    longrepr = getattr(report, "longrepr", None)
    if isinstance(longrepr, tuple) and len(longrepr) == 3:
        return str(longrepr[2])
    return str(longrepr) if longrepr is not None else "<gerekçesiz>"


def _file_of(report: Any) -> str:
    return str(getattr(report, "nodeid", "") or "").split("::")[0].replace("\\", "/")


def _is_declared(reason: str, file: str) -> bool:
    return any(
        pattern in reason and any(file.endswith(allowed) for allowed in files)
        for pattern, files, _note in ALLOWED_SKIP_REASONS
    )


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

    counts: dict[tuple[str, str], int] = {}
    for report in skipped:
        key = (_file_of(report), _reason_of(report))
        counts[key] = counts.get(key, 0) + 1

    undeclared = {key: n for key, n in counts.items() if not _is_declared(key[1], key[0])}

    reporter.write_line("")
    reporter.write_line(f"SKIP BÜTÇESİ: {len(skipped)} test atlandı")
    for (file, reason), number in sorted(counts.items(), key=lambda kv: -kv[1]):
        state = "BEYAN EDİLMEMİŞ" if (file, reason) in undeclared else "beyanlı"
        reporter.write_line(f"  [{state}] {number}x {file} — {reason}")

    if undeclared:
        reporter.write_line(
            "ATLAMA KAPISI DÜŞTÜ — yukarıdaki (dosya, gerekçe) çiftleri tests/conftest.py "
            "ALLOWED_SKIP_REASONS listesinde yok. Sessiz atlama yeşil sayılmaz: ya eksik "
            "bağımlılığı kurun, ya atlamayı gerekçesiyle beyan edin, ya da beyanın DOSYA "
            "kapsamını genişletin (kapsam genişletmek bir karardır — E17/W10 gibi bir "
            "kardeş-CI kalemi doğurur).",
            red=True,
        )
        session.exitstatus = 1
