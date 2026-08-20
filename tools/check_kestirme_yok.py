#!/usr/bin/env python3
# BOUND: TARLAANALIZ_SSOT_v1_2_0.txt - canonical rules are referenced, not duplicated.
"""KESTIRME YOK kuralinin olculebilir kismini kapiya baglar (iki yonlu mandal).

## Neden bu kapi var

Urun sahibi 2026-08-20'de kalici kural koydu: *"asla kestirme yollarla is yapma,
daima ispatli ve kalite odakli calis"*. Kuralin cogu (olcmeden soyleme, kapsami
sessizce daraltma, kendi ciktini curut) **insan davranisidir ve otomatik
olculemez**. Ama bir kismi olculebilir: **sessiz borc**.

## Ne olcer

`TODO` / `FIXME` / `HACK` / `XXX` isaretleri - ama **kelimeyi yasaklamaz**.
Olculdu 2026-08-20 (dort depo): kelimeyi yasaklayan bir kapi **%70 yanlis pozitif**
uretir. Ciplak `XXX` aramasi telefon maskesini (`05XX XXX XX XX`), odeme
referansini (`PAY-YYYYMMDD-XXXXXX`) ve DJI dosya adini (`result_<XXX>.tif`)
yakalar. `gecici` kelimesinin 50 gecisinin 26'si mekanik olarak mesrudur
("gecici hata", "gecici dosya", "gecici worktree").

**Ayirt edici olan kelime degil, yaninda IZLEME KIMLIGI olup olmadigidir.**
Bir kalemle baglanmis erteleme mesrudur; baglanmamis olan **sessiz borctur**.

Kabul edilen kimlikler: `KR-\\d+` - `DK-\\d+` - `AL-K\\d+` - `ADR-\\d+` - `I-\\d` -
`KARAR-\\d+` - `#\\d+` (PR/issue).

## Iki yonlu mandal

* Kimliksiz **yeni** isaret ve tabanda yok -> **KIRMIZI** (borc buyudu).
* Tabandaki bir kalem artik yok -> **KIRMIZI** (liste bayat; temizlik yapan
  kisi listeyi de guncellemeli, yoksa taban zamanla anlamini yitirir).

Taban **gerekcelidir**: her satir neden kabul edildigini yazar. Yeni bir kalem
tabana eklemek, bir insanin gerekce yazmasini zorunlu kilar - kural budur.

## Ayrica: kural blogunun kendisi

Kural metni dort `CLAUDE.md`'de **bayt-ozdes** durur ve bu betigi **adiyla
vaat eder**. Olculdu: `check_claude_md_refs.py` bu vaadi **yakalamiyor** (ciplak
ad, icinde `/` yok -> yol sayilmiyor, sessizce atlaniyor). Yani var olmayan bir
kapiyi vaat eden metin o kapidan yesil geciyordu. Bu betik o kor noktayi kapatir:
blogun varligini ve **bu dosyanin gercekten var oldugunu** dogrular.

Kullanim:  python scripts/check_kestirme_yok.py [--liste]
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


KOK = Path(__file__).resolve().parents[1]

_TARANAN_DIZINLER = ("src", "web/src", "scripts", "tools")
_UZANTILAR = {".py", ".ts", ".tsx", ".js", ".jsx", ".sh"}

# Kelime siniriyla: `TODOS`, `_TODO_` gibi tanimlayicilar yakalanmaz.
_ISARET = re.compile(r"(?<![A-Za-z0-9_])(TODO|FIXME|HACK|XXX)(?![A-Za-z0-9_])")
# Yorum baglami: kod icindeki bir dizgede gecen kelime borc degildir.
_YORUM = re.compile(r"(#|//|/\*|\*|<!--)")
_KIMLIK = re.compile(r"(KR-\d+|DK-\d+|AL-K\d+|ADR-\d+|KARAR-\d+|I-\d(?!\d)|#\d+)")

# ---------------------------------------------------------------------------
# TABAN - her satir GEREKCELIDIR. Olculdu 2026-08-20 (13 kalem).
#
# Buraya bir sey eklemek, o kalemin neden sessiz borc SAYILMADIGINI yazmayi
# zorunlu kilar. Gerekce yazamiyorsan kalem borctur: ya bitir ya kaleme yaz.
# ---------------------------------------------------------------------------
_TABAN: dict[str, str] = {
    # Olculdu 2026-08-20: bu depoda kimliksiz isaret YOK.
    # Taban BOS kalmali - buyurse kapi kirmizi verir.
}

_BLOK_BAS = "<!-- KESTIRME-YOK-BLOGU-BASLANGIC"
_BLOK_SON = "KESTIRME-YOK-BLOGU-BITIS -->"


def _izli_dosyalar() -> list[Path]:
    dizinler = [d for d in _TARANAN_DIZINLER if (KOK / d).is_dir()]
    if not dizinler:
        return []
    sonuc = subprocess.run(
        ["git", "-C", str(KOK), "ls-files", *dizinler],
        capture_output=True, text=True, encoding="utf-8", errors="replace", check=False,
    )
    return [
        KOK / yol
        for yol in sonuc.stdout.splitlines()
        if Path(yol).suffix in _UZANTILAR
    ]


def _bul() -> dict[str, str]:
    """`{"yol:satir": satir_metni}` - kimliksiz isaretler."""
    bulunan: dict[str, str] = {}
    for dosya in _izli_dosyalar():
        if dosya.name == Path(__file__).name:
            # Bu betik isaret kelimelerini TANIM olarak icerir; kendini saymaz.
            continue
        try:
            satirlar = dosya.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        for no, satir in enumerate(satirlar, 1):
            if not _ISARET.search(satir) or not _YORUM.search(satir):
                continue
            if _KIMLIK.search(satir):
                continue  # izleme kimligi var -> mesru erteleme
            anahtar = f"{dosya.relative_to(KOK).as_posix()}:{no}"
            bulunan[anahtar] = satir.strip()[:120]
    return bulunan


def _kural_blogu_kontrol() -> list[str]:
    """Kural blogu duruyor mu ve vaat ettigi kapi GERCEKTEN var mi."""
    hatalar: list[str] = []
    claude_md = KOK / "CLAUDE.md"
    if not claude_md.is_file():
        return ["CLAUDE.md bulunamadi"]
    metin = claude_md.read_text(encoding="utf-8")
    if _BLOK_BAS not in metin or _BLOK_SON not in metin:
        hatalar.append(
            "CLAUDE.md'de KESTIRME-YOK blogu YOK - kural dort depoda bayt-ozdes durmali"
        )
        return hatalar
    # [!] Kor noktanin kendisi: blok bu betigi ADIYLA vaat ediyor.
    # `check_claude_md_refs.py` ciplak adlari (icinde '/' olmayan) atliyor,
    # yani var olmayan bir kapiyi vaat eden metin oradan YESIL geciyordu.
    blok = metin[metin.index(_BLOK_BAS) : metin.index(_BLOK_SON)]
    vaat = re.findall(r"`(check_[a-z0-9_]+\.py)`", blok)
    for ad in vaat:
        if not any((KOK / d / ad).is_file() for d in ("scripts", "tools")):
            hatalar.append(
                f"kural blogu `{ad}` kapisini vaat ediyor ama o dosya YOK "
                f"(belgelenmis ama uygulanmayan kural bir dilektir)"
            )
    return hatalar


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    bulunan = _bul()

    if "--liste" in argv:
        for anahtar, satir in sorted(bulunan.items()):
            print(f"  {anahtar}  {satir}")
        print(f"\ntoplam kimliksiz isaret: {len(bulunan)}  -  taban: {len(_TABAN)}")
        return 0

    hatalar: list[str] = _kural_blogu_kontrol()

    yeni = sorted(set(bulunan) - set(_TABAN))
    if yeni:
        hatalar.append(f"{len(yeni)} YENI kimliksiz isaret (sessiz borc):")
        hatalar += [f"    {a}  {bulunan[a]}" for a in yeni]
        hatalar.append(
            "    Cozum: ya BITIR, ya yanina izleme kimligi yaz (KR-/DK-/AL-K/#123),"
        )
        hatalar.append("    ya da gerekcesiyle `_TABAN` listesine ekle.")

    kayip = sorted(set(_TABAN) - set(bulunan))
    if kayip:
        hatalar.append(f"{len(kayip)} taban kalemi ARTIK YOK - liste bayat:")
        hatalar += [f"    {a}  ({_TABAN[a]})" for a in kayip]
        hatalar.append("    Cozum: `_TABAN` listesinden SIL (mandal iki yonludur).")

    if hatalar:
        print("[KIRMIZI] KESTIRME YOK kapisi:")
        for h in hatalar:
            print(f"  {h}")
        return 1

    print(
        f"[OK] KESTIRME YOK kapisi temiz - kimliksiz isaret {len(bulunan)}, "
        f"taban {len(_TABAN)} (taban buyumedi, liste bayat degil)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
