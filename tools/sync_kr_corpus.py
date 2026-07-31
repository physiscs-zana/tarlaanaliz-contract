#!/usr/bin/env python3
"""KR korpusunun tüketici depolarına dağıtımı + sapma dedektörü (AK-10 / C-SSOT-2).

SORUN (2026-07-31'de ÖLÇÜLDÜ):
    KR korpusu iki dosyada yaşıyor ve **hiçbir senkron aracının kapsamında değil** —
    `tools/sync_to_repos.sh` yalnız `schemas/` + `enums/` + `CONTRACTS_VERSION.md` taşır.
    Sonuç, kâğıt üzerinde dağıtım / içerikte çürüme:

        kr_registry.md   contract 1267 · platform/docs/kr 1211 · platform/contracts/ssot 1242
                         · worker/docs/reference 936   → ÜÇÜNDE DE `KR-093` başlığı YOK
        SSOT metni       contract 1906 · platform 1895 · worker YOK (hiç taşımıyor)

    Yani KR-093 (çiftçi ön raporu — demo kritik yolunun kanonik tanımı) tüketicilerin
    HİÇBİRİNDE yok; onu uygulayacak platform, kuralın metnini görmüyor.

TASARIM — neden kopyalama değil, ÖNCE tespit:
    Kardeş depolar ayrı git depolarıdır; oraya yazmak ayrı bir PR'dır. Bu araç bu yüzden
    iki kipe ayrıldı:
      * `--check`  : sapmayı ÖLÇER ve raporlar (kimseye yazmaz) — kapı budur.
      * `--apply`  : dosyaları kopyalar; **yalnız operatör** çalıştırır ve sonucu kardeş
                     depoda kendi PR'ıyla commit eder.
    Sessiz kopyalama, C8 töreninin görünmez bir yan etkisi olurdu; `--check` ise sapmayı
    release checklist'inde KIRMIZI yapar.

KULLANIM (bu depoda, geliştirme makinesinde — kardeş depolar yanında olmalı):
    python tools/sync_kr_corpus.py --check
    python tools/sync_kr_corpus.py --apply          # sonra her kardeş depoda commit+PR
"""

from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
from pathlib import Path
from typing import Dict, List, NamedTuple


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent


class Target(NamedTuple):
    """Bir kaynak dosyanın bir tüketici depoda bulunması gereken yeri."""
    source: str          # contract deposuna göre
    repo: str            # kardeş depo dizini
    destination: str     # kardeş depo içindeki yol
    reason: str


#: Kim neyi taşımalı — gerekçesiyle. Yol yoksa "eksik" sayılır (sessiz atlanmaz).
TARGETS: tuple[Target, ...] = (
    Target("docs/TARLAANALIZ_SSOT_v1_2_0.txt", "tarlaanaliz-platform",
           "docs/TARLAANALIZ_SSOT_v1_2_0.txt",
           "Platform KR-093/KR-019/KR-033'ü UYGULAR; normatif metni görmek zorundadır."),
    Target("docs/TARLAANALIZ_SSOT_v1_2_0.txt", "tarlaanaliz-worker",
           "docs/TARLAANALIZ_SSOT_v1_2_0.txt",
           "Worker KR-018/KR-070/KR-072 uygular; bugün korpusu HİÇ taşımıyor (ölçüldü)."),
    Target("ssot/kr_registry.md", "tarlaanaliz-platform", "docs/kr/kr_registry.md",
           "Platform'un mevcut kopyası bayat (KR-093 yok)."),
    Target("ssot/kr_registry.md", "tarlaanaliz-worker", "docs/reference/kr_registry.md",
           "Worker'ın mevcut kopyası bayat (936 satır, KR-093 yok)."),
)


def _normalized_hash(path: Path) -> str:
    """CRLF→LF normalize edilmiş SHA-256 (Windows/Linux farkı sapma sayılmasın)."""
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def survey() -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for target in TARGETS:
        source = ROOT / target.source
        destination = WORKSPACE / target.repo / target.destination
        row: Dict[str, object] = {
            "source": target.source,
            "repo": target.repo,
            "destination": target.destination,
            "reason": target.reason,
        }
        if not source.exists():
            row["state"] = "SOURCE_MISSING"
        elif not (WORKSPACE / target.repo).exists():
            row["state"] = "REPO_ABSENT"      # kardeş depo yok — bu makinede ölçülemez
        elif not destination.exists():
            row["state"] = "MISSING"
        elif _normalized_hash(source) != _normalized_hash(destination):
            row["state"] = "STALE"
        else:
            row["state"] = "IN_SYNC"
        rows.append(row)
    return rows


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="KR korpusu dağıtımı / sapma dedektörü")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true", help="sapmayı ölç (yazmaz)")
    group.add_argument("--apply", action="store_true", help="kardeş depolara KOPYALA")
    args = parser.parse_args()

    rows = survey()
    width = max(len(f"{r['repo']}/{r['destination']}") for r in rows)
    for row in rows:
        where = f"{row['repo']}/{row['destination']}"
        print(f"  {row['state']:<14} {where:<{width}}  ← {row['source']}")

    absent = [r for r in rows if r["state"] == "REPO_ABSENT"]
    drift = [r for r in rows if r["state"] in ("MISSING", "STALE")]

    if args.apply:
        for row in drift:
            source = ROOT / str(row["source"])
            destination = WORKSPACE / str(row["repo"]) / str(row["destination"])
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
            print(f"  ✍  yazıldı: {destination}")
        print(f"\n✅ {len(drift)} dosya kopyalandı. ⚠️ Her kardeş depoda AYRI commit + PR gerekir.")
        return 0

    if absent:
        print(f"\nℹ️  {len(absent)} hedef ölçülemedi (kardeş depo bu makinede yok).")
    if drift:
        print(f"\n❌ KR korpusu SAPMIŞ — {len(drift)} hedef güncel değil.")
        print("   Düzeltme (bu depoda): python tools/sync_kr_corpus.py --apply")
        print("   Sonra her kardeş depoda commit + PR (C8 töreninin parçası, SDLC_GATES §3C).")
        return 1
    print("\n✅ KR korpusu tüm ölçülebilir hedeflerde güncel.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
