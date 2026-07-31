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
           "Worker KR-018/KR-070/KR-072 uygular; korpusu 2026-07-31'e dek HİÇ taşımıyordu."),
)

#: 🔄 1b (2026-07-31) — `kr_registry.md` KOPYA HEDEFİ OLMAKTAN ÇIKARILDI.
#:
#: İlk tasarımda kardeş depoların `kr_registry.md` dosyaları "bayat kopya" sayılıyordu.
#: `--apply` gerçek depolarda koşturulunca ölçüldü: DEĞİLLER. Ayrışan içerik incelendiğinde
#: görüldü ki bu dosyalar aynı KR'leri **farklı BİÇİMDE** anlatan YEREL RENDER'lardır:
#:   platform → `**Başlık:** / **Gerekçe:** / **Applies to:**` biçimi, 23 KR'de yerel metin
#:   worker   → `**Normatif özet:**` biçimi, 35 KR'de yerel özet + sürüm/senkron notları
#: contract'ın registry'si ise 8 bölümlü şablon kullanır. Yani üçü aynı dosyanın kopyaları
#: değil, üç ayrı DOKÜMAN.
#:
#: Birleştirme (1b) bu yüzden "kopyala" değil "SINIFLANDIR" oldu:
#:   * Kanonik KR metni = `docs/TARLAANALIZ_SSOT_v1_2_0.txt` (ikisine de senkronlandı ✅)
#:   * Kardeş `kr_registry.md` = YEREL RENDER; başına kanonik kaynağa işaretçi konur ve
#:     çelişkide kanonik metin kazanır. İçerik KORUNUR (kimse veri kaybetmez).
#: Aşağıdaki kontrol, o işaretçinin varlığını ölçer (kopya eşitliği DEĞİL).
POINTER_TARGETS: tuple[tuple[str, str], ...] = (
    ("tarlaanaliz-platform", "docs/kr/kr_registry.md"),
    ("tarlaanaliz-worker", "docs/reference/kr_registry.md"),
)
POINTER_MARK = "KANONİK KR METNİ BURADA DEĞİL"


def _normalized_hash(path: Path) -> str:
    """CRLF→LF normalize edilmiş SHA-256 (Windows/Linux farkı sapma sayılmasın)."""
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def _meaningful_lines(path: Path) -> set:
    """İçerik taşıyan satırlar (tablo/çizgi/kod-çiti gürültüsü hariç)."""
    return {
        line.strip()
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines()
        if len(line.strip()) > 25 and not line.strip().startswith(("|", "---", "```"))
    }


def content_only_in_destination(source: Path, destination: Path) -> set:
    """Hedefte olup KAYNAKTA OLMAYAN içerik — üzerine yazılırsa KAYBOLUR.

    ⚠️ Bu fonksiyon 2026-07-31'de, aracın kendisi kullanıcı direktifiyle ilk kez
    `--apply` ile koşturulduğunda EKLENDİ. Ölçüm: `--apply` kardeş depoların
    `kr_registry.md` kopyalarını ezecekti ve **platformda 143, worker'da 313 anlamlı
    satır** yok olacaktı (ör. worker'ın "Admin Export Endpoint", bulut örtüsü çift eşik
    semantiği; platformun "Risk & Business Continuity" bölümü).

    Yani o kopyalar **bayat kopya değil, AYRIŞMIŞ ÇATAL**: kendi içerikleri var. Kör
    kopyalama bir senkron değil, veri kaybıdır. Araç artık bunu önce ölçer.
    """
    if not destination.exists():
        return set()
    return _meaningful_lines(destination) - _meaningful_lines(source)


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
            lost = content_only_in_destination(source, destination)
            row["state"] = "DIVERGENT" if lost else "STALE"
            row["would_lose"] = len(lost)
            row["sample_loss"] = sorted(lost)[:3]
        else:
            row["state"] = "IN_SYNC"
        rows.append(row)

    for repo, destination in POINTER_TARGETS:
        path = WORKSPACE / repo / destination
        if not (WORKSPACE / repo).exists():
            state = "REPO_ABSENT"
        elif not path.exists():
            state = "MISSING"
        elif POINTER_MARK in path.read_text(encoding="utf-8", errors="replace"):
            state = "POINTER_OK"
        else:
            state = "POINTER_MISSING"
        rows.append({
            "source": "(işaretçi kontrolü — kopya DEĞİL)",
            "repo": repo,
            "destination": destination,
            "reason": "Yerel render; kanonik metne işaretçi taşımalı (1b).",
            "state": state,
        })
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
        loss = f"  ⚠️ {row['would_lose']} satır kaybolurdu" if row.get("would_lose") else ""
        print(f"  {row['state']:<14} {where:<{width}}  ← {row['source']}{loss}")

    absent = [r for r in rows if r["state"] == "REPO_ABSENT"]
    copyable = [r for r in rows if r["state"] in ("MISSING", "STALE")]
    pointerless = [r for r in rows if r["state"] == "POINTER_MISSING"]
    divergent = [r for r in rows if r["state"] == "DIVERGENT"]

    if args.apply:
        for row in copyable:
            source = ROOT / str(row["source"])
            destination = WORKSPACE / str(row["repo"]) / str(row["destination"])
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
            print(f"  ✍  yazıldı: {destination}")
        if divergent:
            print("\n🛑 AYRIŞMIŞ hedeflere YAZILMADI — kör kopyalama senkron değil, VERİ KAYBIDIR:")
            for row in divergent:
                print(f"   - {row['repo']}/{row['destination']}: hedefte olup kaynakta "
                      f"OLMAYAN {row['would_lose']} anlamlı satır")
                for line in row.get("sample_loss", []):  # type: ignore[union-attr]
                    print(f"       · {line[:96]}")
            print("   → Bunlar bayat kopya DEĞİL, ayrışmış ÇATALdır: elle BİRLEŞTİRİLMELİ")
            print("     (contract'ta tek gövde + kardeş depoda işaretçi — D16-b deseni).")
        print(f"\n✅ {len(copyable)} dosya kopyalandı · 🛑 {len(divergent)} hedef KORUNDU.")
        print("⚠️ Her kardeş depoda AYRI commit + PR gerekir.")
        return 1 if divergent else 0

    if absent:
        print(f"\nℹ️  {len(absent)} hedef ölçülemedi (kardeş depo bu makinede yok).")
    if divergent:
        print(f"\n🛑 {len(divergent)} hedef AYRIŞMIŞ (çatal) — kopyalanamaz, BİRLEŞTİRME ister.")
        for row in divergent:
            print(f"   - {row['repo']}/{row['destination']}: {row['would_lose']} satır "
                  "yalnız hedefte var")
    if copyable:
        print(f"\n❌ {len(copyable)} hedef bayat (güvenle kopyalanabilir).")
        print("   Düzeltme (bu depoda): python tools/sync_kr_corpus.py --apply")
        print("   Sonra her kardeş depoda commit + PR (SDLC_GATES §3C).")
    if pointerless:
        print(f"\n❌ {len(pointerless)} yerel render kanonik metne İŞARETÇİ taşımıyor.")
        for row in pointerless:
            print(f"   - {row['repo']}/{row['destination']}")
    if divergent or copyable or pointerless:
        return 1
    print("\n✅ KR korpusu tüm ölçülebilir hedeflerde güncel.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
