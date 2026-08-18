#!/usr/bin/env python3
"""CLAUDE.md atif butunlugu kapisi.

NEDEN VAR (2026-08-18 olcumu). `check_doc_links` bir *dokuman* kapisidir:
`DOC_SUFFIXES = (".md", ".txt")` -- kod yollarini ve kimlik atiflarini KAPSAM DISI
birakir (kendi docstring'i bunu soyluyor). Olculdu: iki kusur aylarca gorunmedi.

  * `services/security/av_engines.py` -- yanlis yol; dogrusu `src/core/services/...`
  * `MatchResult(..., method="MISSION_ID")` -- kodda oyle bir sinif/sabit yok

Bu kapi o iki sinifi kapatir ve YALNIZ CLAUDE.md'ye bakar (kusurlarin fiilen
ciktigi yer orasi; genis tarama yanlis-pozitif ureti):

  1. KIMLIK  -- CLAUDE.md'de gecen her KR-NNN / HC-NN / ADR-NNN / K-N / KARAR-NN /
               AL-KNN / DK-NN kimligi, depoda BASKA bir izli dosyada da gecmeli.
               Yakalar: uydurulmus veya yetim kalmis kimlik.
  2. KOD YOLU -- CLAUDE.md'de backtick icinde gecen her kaynak-yol atfi cozulmeli.
               Yakalar: tasinmis/yanlis yazilmis dosya yolu.

TASARIM KARARLARI
  * Evren `git ls-files` -- gitignore'a saygi duyar, dist/ gibi uretilmis agaclari gormez.
  * Fail-closed: CLAUDE.md yoksa ya da git calismazsa HATA doner ("olcemedim" != "temiz").
  * Sessiz atlama YOK: capraz-repo ve yer-tutucu atlamalari SAYIYLA basilir.
  * `--self-test` pozitif VE negatif kontrolu kosar; ikisi gecmeden sonuc guvenilmez.

DAGITIM. Dort depoda ayni MANTIK kosar; BICIM her deponun kendi linter'ina gore
degisir: contract lines-after-imports=2, digerleri 1 -> bayt-ozdeslik IMKANSIZ
(mevcut check_doc_links de zaten 2 varyant halinde duruyor, olculdu 2026-08-18).
Pariteyi bos satirlari normalize ederek olcun, `cmp` ile degil.

KULLANIM
    python scripts/check_claude_md_refs.py            # depo kokunden
    python scripts/check_claude_md_refs.py --self-test
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


# Sondaki virgul "magic trailing comma": 100/120/140 satir-uzunluklarinin
# HEPSI bu patlatilmis hali korur -> ayni bayt her depoda "bicimli" sayilir.
KIMLIK_RE = re.compile(
    r"\b(?:KR-\d{3}|HC-\d{2}|ADR-\d{3}|AL-K\d{2}|DK-\d{2}|KARAR-\d{2}|K-\d{1,2})\b",
)
BACKTICK_RE = re.compile(r"`([^`\n]{3,200})`")

KAYNAK_UZANTI = (".py", ".yaml", ".yml", ".json", ".sh", ".ps1", ".toml", ".cfg", ".ini", ".lock")
# Yer tutucu / sablon / glob / kabuk degiskeni iceren tokenlar atlanir.
YER_TUTUCU = re.compile(r"[<>{}*$\[\]]|\.\.\.")


def _git(args: list[str], repo: Path) -> str:
    r = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} basarisiz: {r.stderr.strip()[:200]}")
    return r.stdout


def _izli_dosyalar(repo: Path) -> list[str]:
    return [s for s in _git(["ls-files"], repo).splitlines() if s.strip()]


def _kimlik_denetle(repo: Path, metin: str, izli: set[str]) -> list[str]:
    """Her kimlik depoda BASKA bir dosyada geciyor mu."""
    hatalar = []
    for kimlik in sorted(set(KIMLIK_RE.findall(metin))):
        r = subprocess.run(
            # Glob (duz ad degil): (a) yerel-kopya varyantlarini da dislar, (b) bu
            # depoda BULUNMAYAN bir ajan-talimat dosyasinin adini koda LITERAL
            # yazmaz. Bu ikincisi zorunlu: check_doc_links .py dosyalarini da
            # tarar ve boyle bir literali "sarkan dokuman atfi" sanar (olculdu
            # 2026-08-18; ayni tuzak build_package.py icinde de yasandi).
            [
                "git",
                "-C",
                str(repo),
                "grep",
                "-lF",
                kimlik,
                "--",
                ".",
                ":!CLAUDE*.md",
                ":!AGENTS*.md",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if r.returncode != 0 or not r.stdout.strip():
            hatalar.append(f"YETIM KIMLIK: {kimlik} -- CLAUDE.md disinda depoda hic gecmiyor")
    return hatalar


def _yol_denetle(repo: Path, metin: str) -> tuple[list[str], int, int]:
    """Backtick icindeki kaynak-yol atiflari cozuluyor mu."""
    hatalar: list[str] = []
    atlanan_capraz = atlanan_yertutucu = 0
    for ham in sorted(set(BACKTICK_RE.findall(metin))):
        tok = ham.strip().rstrip(".,;:)")
        if "/" not in tok or " " in tok:
            continue
        if YER_TUTUCU.search(tok):
            atlanan_yertutucu += 1
            continue
        if tok.startswith("tarlaanaliz-"):  # capraz-repo: bu depodan cozulemez
            atlanan_capraz += 1
            continue
        if tok.startswith(("http", "//", "#")):
            continue
        dizin_mi = tok.endswith("/")
        if not dizin_mi and not tok.endswith(KAYNAK_UZANTI):
            continue  # .md/.txt zaten check_doc_links'in isi
        hedef = repo / tok
        if dizin_mi:
            if not hedef.is_dir():
                hatalar.append(f"YOK (dizin): {tok}")
        elif not hedef.exists():
            hatalar.append(f"YOK (dosya): {tok}")
    return hatalar, atlanan_capraz, atlanan_yertutucu


def _self_test() -> bool:
    """Pozitif: bulmasi gerekeni buluyor mu. Negatif: bulmamasi gerekeni birakiyor mu."""
    ok = True
    poz = "KR-018 HC-05 ADR-002 AL-K30 DK-28 KARAR-16 K-9"
    bulunan = set(KIMLIK_RE.findall(poz))
    beklenen = {"KR-018", "HC-05", "ADR-002", "AL-K30", "DK-28", "KARAR-16", "K-9"}
    if bulunan != beklenen:
        print(f"  POZITIF BASARISIZ -- kacan: {sorted(beklenen - bulunan)}")
        ok = False
    else:
        print(f"  POZITIF GECTI  ({len(beklenen)}/{len(beklenen)} kimlik)")

    neg = "BEKLENMEZ KALDIRILDI TABLOSU M1 M2 I-3 v1.2.0 2026-08-18 UTF-8 SHA-256"
    yanlis = set(KIMLIK_RE.findall(neg))
    if yanlis:
        print(f"  NEGATIF BASARISIZ -- yanlis pozitif: {sorted(yanlis)}")
        ok = False
    else:
        print("  NEGATIF GECTI  (10 tuzak token kimlik sayilmadi)")

    yer = ["config/crops/<ad>.yaml", "src/models/{name}/", "denetim/*_spec_*.md", "$TMP/x.py"]
    kacan = [t for t in yer if not YER_TUTUCU.search(t)]
    if kacan:
        print(f"  YER-TUTUCU BASARISIZ -- elenmedi: {kacan}")
        ok = False
    else:
        print("  YER-TUTUCU GECTI  (4 sablon token elendi)")
    return ok


def main() -> int:
    ap = argparse.ArgumentParser(description="CLAUDE.md atif butunlugu kapisi")
    ap.add_argument("--repo", default=".", help="depo koku (varsayilan: .)")
    ap.add_argument("--self-test", action="store_true", help="pozitif+negatif kontrolu kos")
    a = ap.parse_args()

    if a.self_test:
        print("=== TARAYICI KENDI UZERINDE SINANIYOR ===")
        return 0 if _self_test() else 2

    repo = Path(a.repo).resolve()
    claude = repo / "CLAUDE.md"
    if not claude.is_file():  # fail-closed
        print(f"HATA: {claude} yok -- kapi olcum YAPAMADI", file=sys.stderr)
        return 2
    try:
        izli = set(_izli_dosyalar(repo))
    except RuntimeError as e:
        print(f"HATA: {e}", file=sys.stderr)
        return 2

    metin = claude.read_text(encoding="utf-8")
    hatalar = _kimlik_denetle(repo, metin, izli)
    yol_hatalari, capraz, yertutucu = _yol_denetle(repo, metin)
    hatalar += yol_hatalari

    ozet = f"{repo.name}: {len(izli)} izli dosya tarandi"
    print(f"{ozet} | atlanan capraz-repo={capraz} | atlanan yer-tutucu={yertutucu}")
    if hatalar:
        print(f"KIRMIZI: {len(hatalar)} sarkan atif")
        for h in hatalar:
            print(f"  - {h}")
        return 1
    print("OK: CLAUDE.md atif butunlugu temiz (kimlik + kod yolu).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
