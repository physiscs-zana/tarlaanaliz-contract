#!/usr/bin/env python3
"""Sarkan (dangling) dokuman atifi muhafizi — ratchet.

NEDEN VAR (AL-K20, 2026-08-11 olculdu)
--------------------------------------
Kok `CLAUDE.md` *"diff olmadan is yapmak"* diyor: bir dosya silinince ona isaret
eden satirlar duzeltilmeli. Kural dort depoda da YAZILI ama hicbir yerde
KOSTURULMUYORDU. Sonuc ampirik: 2026-08-11 sadelestirme turu 83 dokuman sildi ve
**12 sarkan atif** hayatta kaldi — 9'u tek bir canli mimari belgede
(`docs/architecture/end_to_end_workflow.md`), biri ACIK bir DEFER kaleminin
hedefiydi. Elle tarama uc turda uc kez kacirdi. Sorun dikkat degil **kapi
yoklugu**; bu betik o kapidir.

NE DENETLER
-----------
Izli metin dosyalarindan `.md` / `.txt` ile biten **dokuman atiflarini** cikarir ve
her birinin bir izli dosyaya cozulup cozulmedigine bakar. Cozum sirasi:
  1. depo-koku goreli tam yol          docs/architecture/foo.md
  2. atif yapan dosyaya goreli yol     ../adr/ADR-007.md
  3. CIPLAK ad (basename) esleme       `foo.md`   <- 12 bulgunun 9'unu bu yakalar

NE DENETLEMEZ (bilincli kapsam)
-------------------------------
* Kod yolu atiflari (`settings.py:214`) — bu bir *dokuman* kapisidir; kod yollari
  icin ayri bir arac gerekir ve yanlis-pozitif profili tumuyle farklidir.
* Joker iceren desenler (`config/crops/*.yaml`) ve URL'ler.
* KISALTILMIS ad (`DENETIM_2026-05-31` — tam kok `..._pentest_ve_kurulum`).
  OLCULDU (2026-08-11): onek tabanli tarama dort depoda **933 yanlis pozitif**
  uretiyor, cunku veri seti kimlikleri onek paylasiyor
  (`zenodo_olive_taal_raw_ms` vs `zenodo_olive_verticillium_2023`). Kapiya
  konulamaz. Bu bosluk BILINIR ve elle taramayla kapatilir.

CAPRAZ-REPO ATIFLARI (`tarlaanaliz-worker/denetim/x.md`)
--------------------------------------------------------
Kardes depo yan yana checkout edilmisse ORADA cozulur; degilse cozulemez ve
**baseline'a bakilmaksizin ATLANIR** — ama atlanan sayi ekrana basilir. Boylece
kapi sessizce fail-open olmaz: cikti "N capraz-repo atifi atlandi" der.
AL-K13'un tarif ettigi tuzak budur; CI'da baglayici kilmak icin karsi deponun
checkout adimi gerekir (E17 deseni).

RATCHET (mandal) — bolge kapisiyla ayni semantik
------------------------------------------------
  * baseline'da OLMAYAN yeni cozulmemis atif  -> FAIL (yeni sarkma)
  * baseline'da olup artik cozulmemis OLMAYAN -> FAIL (duzeldi, satiri sil)

Kullanim:
  python -m scripts.check_doc_links                   # CI kapisi
  python -m scripts.check_doc_links --write-baseline  # baseline'i yeniden uret
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Bu dosya DORT DEPODA DA BAYT-OZDES tutulur; bu yuzden hicbir yol elle
# yazilmaz, hepsi kendi konumundan TURETILIR. (Depolarin betik dizini farkli:
# platform/worker/edge `scripts/` + `config/`, contract `tools/`.)
# Ikinci kopya elle duzenlenirse sessizce ayrisir — dogrulama: dort dosyayi
# `cmp` ile karsilastir.
SELF_REL = Path(__file__).resolve().relative_to(REPO_ROOT).as_posix()
_BASELINE_DIR = "config" if (REPO_ROOT / "config").is_dir() else SELF_REL.split("/")[0]
BASELINE_REL = f"{_BASELINE_DIR}/doc_link_baseline.yaml"
BASELINE = REPO_ROOT / _BASELINE_DIR / "doc_link_baseline.yaml"

# Icinde atif ARANACAK dosya turleri.
SCANNED_SUFFIXES = {".md", ".txt", ".py", ".yaml", ".yml"}

# Dokuman uzantilari — yalniz bunlarla biten atiflar aday sayilir.
DOC_SUFFIXES = (".md", ".txt")

# Kardes depo onekleri (capraz-repo atiflari).
SIBLING_PREFIXES = (
    "tarlaanaliz-contract/",
    "tarlaanaliz-platform/",
    "tarlaanaliz-worker/",
    "tarlaanaliz-edge/",
)

# 1) Backtick icindeki spanlar — bosluklu adlari da yakalar (`docs/Gorev Haritasi.txt`).
BACKTICK_RE = re.compile(r"`([^`\n]{3,200})`")
# 2) Ciplak token — backtick'siz yazilmis yollar.
# `$` lookbehind'da: kabuk degiskenli yollar (`$RUNNER_TEMP/reminder-body.md`)
# `$`siz kismiyla eslesip sahte aday uretiyordu (olculdu 2026-08-11).
BARE_RE = re.compile(r"(?<![`\w/.$-])([\w./§-]+\.(?:md|txt))(?![\w])", re.UNICODE)

# Aday temizligi: sondaki satir/bolum/noktalama ekleri.
TRAILING_RE = re.compile(r"(?::\d+(?:-\d+)?|#[\w-]+|\s*§[\w.\d]+)+\s*$")


def tracked_files() -> list[str]:
    out = subprocess.run(  # noqa: S603
        ["git", "-C", str(REPO_ROOT), "ls-files", "-z"],  # noqa: S607
        capture_output=True, check=True,
    ).stdout.decode("utf-8")
    return [p for p in out.split("\0") if p]


def submodule_files() -> list[str]:
    """Submodule (alt-depo) icerigi `git ls-files`'da TEK satirdir (gitlink).

    Platformun `contracts/` submodule'u boyle gorunur; icindeki 60+ dokumana
    yapilan mesru atiflar bu yuzden 'cozulemedi' sanilir. OLCULDU (2026-08-11):
    bu duzeltme olmadan platformda 158 isabetin cogunlugu bu tek nedenden.
    """
    out = subprocess.run(  # noqa: S603
        ["git", "-C", str(REPO_ROOT), "ls-files", "-s", "-z"],  # noqa: S607
        capture_output=True, check=True,
    ).stdout.decode("utf-8")
    extra: list[str] = []
    for entry in out.split("\0"):
        if not entry.startswith("160000"):
            continue
        rel = entry.split("\t", 1)[-1]
        sub = REPO_ROOT / rel
        # `.git` VARLIGINA bak, `is_dir()`a DEGIL: doldurulmamis submodule bos ama
        # MEVCUT bir klasordur ve `git -C <bos klasor> ls-files` UST depoya duser,
        # exit 0 + bos cikti verir. Yani "returncode == 0" burada kanit DEGILDIR
        # (olculdu 2026-08-11 — ilk yazimda tam bu yuzden fail-closed tetiklenmedi).
        populated = (sub / ".git").exists()
        sub_out = subprocess.run(  # noqa: S603
            ["git", "-C", str(sub), "ls-files", "-z"],  # noqa: S607
            capture_output=True,
        ) if populated else None
        if sub_out is None or sub_out.returncode != 0:
            # FAIL-CLOSED: submodule doldurulmamis bir agacta bu kapi YANLIS cevap
            # verir (submodule icindeki 60+ dokumana yapilan mesru atiflari
            # 'sarkan' sanir) ve o yanlis sayiyla uretilen baseline CI'da patlar.
            # Sessizce eksik olcmek yerine kosmayi REDDEDER.
            raise SystemExit(
                f"HATA: `{rel}` submodule'u doldurulmamis — bu kapi eksik agacta "
                f"yanlis olcer.\n"
                f"Cozum: git submodule update --init --recursive"
            )
        for p in sub_out.stdout.decode("utf-8").split("\0"):
            if p:
                extra.append(f"{rel}/{p}")
    return extra


def _clean(token: str) -> str | None:
    """Ham adayi normalize et; aday degilse None."""
    tok = token.strip().strip("*_\"'()[]<>,;")
    tok = TRAILING_RE.sub("", tok).strip()
    tok = tok.rstrip(".,;:")
    if tok.startswith("./"):
        tok = tok[2:]
    if not tok.endswith(DOC_SUFFIXES):
        return None
    if "://" in tok or "*" in tok or "?" in tok:
        return None
    # Sablon/degisken/yer-tutucu iceren metinler yol degildir:
    #   $RUNNER_TEMP/reminder-body.md · <submodule-pin>:CONTRACTS_VERSION.md · {name}.md
    if any(ch in tok for ch in "$<>{}|"):
        return None
    # "bir .md dosyasi" gibi cumle parcalari
    if len(tok) < 5 or tok in DOC_SUFFIXES:
        return None
    return tok


def _is_doc_shaped(cand: str) -> bool:
    """KOD dosyalarinda (.py/.yaml) aday olmak icin BELGE bicimli olmali.

    Neden: test dosyalari sahte dosya adlarini VERI olarak tasir
    (`secret.txt` · `notes.txt` · `/tmp/data.txt` · `file.txt`) — bunlar atif
    degildir ve kapiyi gurultuye bogar (olculdu: platformda 110 isabetin 8'i).
    Belge bicimli sayilanlar: `docs/` ya da `denetim/` iceren yollar, ya da `.md`.
    Bu turda bulunan GERCEK kusurlarin hepsi bu susgecten gecer:
      worker  tests/contract/... -> `platform docs/governance/....md`   (docs/)
      contract tests/...          -> `tarlaanaliz-worker/denetim/...md` (denetim/ + .md)
    """
    return cand.endswith(".md") or "docs/" in cand or "denetim/" in cand


def candidates(text: str, code_file: bool = False) -> set[str]:
    found: set[str] = set()
    for span in BACKTICK_RE.findall(text):
        # ONCE span'in TAMAMINI dene — dosya adinda BOSLUK olabilir
        # (`docs/Görev Haritası.txt`). Bosluktan bolmek onu "Haritası.txt"ye
        # kirpar ve sahte sarkma uretir (olculdu 2026-08-11).
        whole = _clean(span)
        if whole:
            found.add(whole)
            continue
        for piece in re.split(r"[,;·]+", span):
            cand = _clean(piece)
            if cand:
                found.add(cand)
    for tok in BARE_RE.findall(text):
        cand = _clean(tok)
        if cand:
            found.add(cand)
    if code_file:
        found = {c for c in found if _is_doc_shaped(c)}
    return found


def _sibling_resolves(cand: str) -> bool | None:
    """Capraz-repo adayi: True/False = cozuldu/cozulmedi, None = kardes depo yok."""
    for prefix in SIBLING_PREFIXES:
        if cand.startswith(prefix):
            sibling = REPO_ROOT.parent / prefix.rstrip("/")
            if not (sibling / ".git").exists():
                return None
            rel = cand[len(prefix):]
            if (sibling / rel).is_file():
                return True
            # ciplak ad eslemesi kardes depoda da gecerli
            base = rel.rsplit("/", 1)[-1]
            return any(p.name == base for p in sibling.rglob(base))
    return False


def scan() -> tuple[set[str], int]:
    files = tracked_files()
    # Cozum kumesi submodule iceriklerini DE kapsar (yalniz cozumde; taranan
    # dosyalar hala bu deponun kendi izli dosyalaridir).
    resolvable = files + submodule_files()
    tracked_set = set(resolvable)
    by_basename: dict[str, list[str]] = {}
    for rel in resolvable:
        by_basename.setdefault(rel.rsplit("/", 1)[-1], []).append(rel)

    unresolved: set[str] = set()
    skipped_cross_repo = 0

    for rel in files:
        if rel in (SELF_REL, BASELINE_REL):
            continue
        path = REPO_ROOT / rel
        if not path.is_file() or path.suffix.lower() not in SCANNED_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        here = rel.rsplit("/", 1)[0] if "/" in rel else ""
        code_file = path.suffix.lower() in {".py", ".yaml", ".yml"}
        for cand in candidates(text, code_file=code_file):
            if cand.startswith(SIBLING_PREFIXES):
                verdict = _sibling_resolves(cand)
                if verdict is None:
                    skipped_cross_repo += 1
                    continue
                if verdict:
                    continue
                unresolved.add(f"{rel}|{cand}")
                continue
            # 1) depo-koku goreli
            if cand in tracked_set:
                continue
            # 2) atif yapan dosyaya goreli
            if here:
                joined = str(Path(here) / cand).replace("\\", "/")
                # ".." bilesenlerini duzlestir
                parts: list[str] = []
                for part in joined.split("/"):
                    if part == "..":
                        if parts:
                            parts.pop()
                    elif part not in ("", "."):
                        parts.append(part)
                if "/".join(parts) in tracked_set:
                    continue
            # 3) ciplak ad
            if cand.rsplit("/", 1)[-1] in by_basename:
                continue
            unresolved.add(f"{rel}|{cand}")

    return unresolved, skipped_cross_repo


def load_baseline() -> set[str]:
    if not BASELINE.exists():
        return set()
    entries: set[str] = set()
    for line in BASELINE.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s.startswith("- "):
            entries.add(s[2:].strip())
    return entries


def write_baseline(hits: set[str]) -> None:
    header = (
        f"# Sarkan dokuman atifi baseline'i (ratchet) — {SELF_REL}\n"
        "# `--write-baseline` ile uretilir; ELLE DUZENLENMEZ.\n"
        "#\n"
        "# Her satir `atif_yapan_dosya|cozulemeyen_hedef` biciminde KABUL EDILMIS bir\n"
        "# sarkmadir. Kapi cift yonludur: yeni sarkma FAIL, duzelmis girdi de FAIL.\n"
        "#\n"
        "# Bir girdiyi buraya EKLEMEDEN once sor: hedef gercekten yok mu, yoksa\n"
        "# yalnizca adi mi degisti? Ad degistiyse ATFI duzelt, baseline'i degil.\n"
        "# Mesru kalabilecek tek sinif: bilincli TARIHSEL atif (silinmis bir dosyayi\n"
        "# `git show <sha>:<yol>` ile anan kayitlar) ve kardes depoya isaret eden,\n"
        "# bu depodan cozulemeyen yollar.\n"
        "accepted:\n"
    )
    body = "".join(f"- {h}\n" for h in sorted(hits))
    BASELINE.parent.mkdir(parents=True, exist_ok=True)
    BASELINE.write_text(header + body, encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Sarkan dokuman atifi kapisi")
    parser.add_argument("--write-baseline", action="store_true",
                        help="Baseline'i canli duruma gore yeniden uret")
    args = parser.parse_args()

    live, skipped = scan()

    if args.write_baseline:
        write_baseline(live)
        print(f"Baseline yazildi: {BASELINE_REL} ({len(live)} kayit)")
        if skipped:
            print(f"NOT: {skipped} capraz-repo atifi atlandi (kardes depo checkout degil).")
        return 0

    base = load_baseline()
    new = sorted(live - base)
    resolved = sorted(base - live)

    if new:
        print("HATA: YENI sarkan dokuman atifi (baseline'da yok):")
        for h in new:
            citing, target = h.split("|", 1)
            print(f"  + {citing}  ->  {target}")
    if resolved:
        print("HATA: baseline'da olup ARTIK sarkmayan kayit (duzeldi -> satiri sil):")
        for h in resolved:
            print(f"  - {h}")

    if new or resolved:
        print(
            "\nDuzeltme: hedef yeniden adlandirildiysa/birlestirildiyse ATFI duzelt "
            "(yeni dosya + bolum numarasi). Hedef gercekten kalicI olarak yoksa "
            "`--write-baseline` ile baseline'i guncelle ve DIFF'i gozden gecir."
        )
        return 1

    msg = f"OK: sarkan dokuman atifi kapisi temiz ({len(live)} kabul edilmis kayit izleniyor)."
    if skipped:
        msg += f" {skipped} capraz-repo atifi atlandi (kardes depo checkout degil)."
    print(msg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
