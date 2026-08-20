#!/usr/bin/env python3
# BOUND: TARLAANALIZ_SSOT_v1_2_0.txt – canonical rules are referenced, not duplicated.
"""KESTİRME YOK kuralının ölçülebilir kısmını kapıya bağlar (iki yönlü mandal).

## Neden bu kapı var

Ürün sahibi 2026-08-20'de kalıcı kural koydu: *"asla kestirme yollarla iş yapma,
daima ispatlı ve kalite odaklı çalış"*. Kuralın çoğu (ölçmeden söyleme, kapsamı
sessizce daraltma, kendi çıktını çürüt) **insan davranışıdır ve otomatik
ölçülemez**. Ama bir kısmı ölçülebilir: **sessiz borç**.

## Ne ölçer

`TODO` / `FIXME` / `HACK` / `XXX` işaretleri — ama **kelimeyi yasaklamaz**.
Ölçüldü 2026-08-20 (dört depo): kelimeyi yasaklayan bir kapı **%70 yanlış pozitif**
üretir. Çıplak `XXX` araması telefon maskesini (`05XX XXX XX XX`), ödeme
referansını (`PAY-YYYYMMDD-XXXXXX`) ve DJI dosya adını (`result_<XXX>.tif`)
yakalar. `geçici` kelimesinin 50 geçişinin 26'sı mekanik olarak meşrudur
("geçici hata", "geçici dosya", "geçici worktree").

**Ayırt edici olan kelime değil, yanında İZLEME KİMLİĞİ olup olmadığıdır.**
Bir kalemle bağlanmış erteleme meşrudur; bağlanmamış olan **sessiz borçtur**.

Kabul edilen kimlikler: `KR-\\d+` · `DK-\\d+` · `AL-K\\d+` · `ADR-\\d+` · `I-\\d` ·
`KARAR-\\d+` · `#\\d+` (PR/issue).

## İki yönlü mandal

* Kimliksiz **yeni** işaret ve tabanda yok → **KIRMIZI** (borç büyüdü).
* Tabandaki bir kalem artık yok → **KIRMIZI** (liste bayat; temizlik yapan
  kişi listeyi de güncellemeli, yoksa taban zamanla anlamını yitirir).

Taban **gerekçelidir**: her satır neden kabul edildiğini yazar. Yeni bir kalem
tabana eklemek, bir insanın gerekçe yazmasını zorunlu kılar — kural budur.

## Ayrıca: kural bloğunun kendisi

Kural metni dört `CLAUDE.md`'de **bayt-özdeş** durur ve bu betiği **adıyla
vaat eder**. Ölçüldü: `check_claude_md_refs.py` bu vaadi **yakalamıyor** (çıplak
ad, içinde `/` yok → yol sayılmıyor, sessizce atlanıyor). Yani var olmayan bir
kapıyı vaat eden metin o kapıdan yeşil geçiyordu. Bu betik o kör noktayı kapatır:
bloğun varlığını ve **bu dosyanın gerçekten var olduğunu** doğrular.

Kullanım:  python scripts/check_kestirme_yok.py [--liste]
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]

_TARANAN_DIZINLER = ("src", "web/src", "scripts", "tools")
_UZANTILAR = {".py", ".ts", ".tsx", ".js", ".jsx", ".sh"}

# Kelime sınırıyla: `TODOS`, `_TODO_` gibi tanımlayıcılar yakalanmaz.
_ISARET = re.compile(r"(?<![A-Za-z0-9_])(TODO|FIXME|HACK|XXX)(?![A-Za-z0-9_])")
# Yorum bağlamı: kod içindeki bir dizgede geçen kelime borç değildir.
_YORUM = re.compile(r"(#|//|/\*|\*|<!--)")
_KIMLIK = re.compile(r"(KR-\d+|DK-\d+|AL-K\d+|ADR-\d+|KARAR-\d+|I-\d(?!\d)|#\d+)")

# ---------------------------------------------------------------------------
# TABAN — her satır GEREKÇELİDİR. Ölçüldü 2026-08-20 (13 kalem).
#
# Buraya bir şey eklemek, o kalemin neden sessiz borç SAYILMADIĞINI yazmayı
# zorunlu kılar. Gerekçe yazamıyorsan kalem borçtur: ya bitir ya kaleme yaz.
# ---------------------------------------------------------------------------
_TABAN: dict[str, str] = {
    # Olculdu 2026-08-20: bu depoda kimliksiz isaret YOK.
    # Taban BOS kalmali — buyurse kapi kirmizi verir.
}

_BLOK_BAS = "<!-- KESTIRME-YOK-BLOGU-BASLANGIC"
_BLOK_SON = "KESTIRME-YOK-BLOGU-BITIS -->"


def _izli_dosyalar() -> list[Path]:
    dizinler = [d for d in _TARANAN_DIZINLER if (KOK / d).is_dir()]
    if not dizinler:
        return []
    sonuc = subprocess.run(  # noqa: S603
        ["git", "-C", str(KOK), "ls-files", *dizinler],  # noqa: S607
        capture_output=True, text=True, encoding="utf-8", errors="replace", check=False,
    )
    return [
        KOK / yol
        for yol in sonuc.stdout.splitlines()
        if Path(yol).suffix in _UZANTILAR
    ]


def _bul() -> dict[str, str]:
    """`{"yol:satir": satir_metni}` — kimliksiz işaretler."""
    bulunan: dict[str, str] = {}
    for dosya in _izli_dosyalar():
        if dosya.name == Path(__file__).name:
            # Bu betik işaret kelimelerini TANIM olarak içerir; kendini saymaz.
            continue
        try:
            satirlar = dosya.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        for no, satir in enumerate(satirlar, 1):
            if not _ISARET.search(satir) or not _YORUM.search(satir):
                continue
            if _KIMLIK.search(satir):
                continue  # izleme kimliği var → meşru erteleme
            anahtar = f"{dosya.relative_to(KOK).as_posix()}:{no}"
            bulunan[anahtar] = satir.strip()[:120]
    return bulunan


def _kural_blogu_kontrol() -> list[str]:
    """Kural bloğu duruyor mu ve vaat ettiği kapı GERÇEKTEN var mı."""
    hatalar: list[str] = []
    claude_md = KOK / "CLAUDE.md"
    if not claude_md.is_file():
        return ["CLAUDE.md bulunamadı"]
    metin = claude_md.read_text(encoding="utf-8")
    if _BLOK_BAS not in metin or _BLOK_SON not in metin:
        hatalar.append(
            "CLAUDE.md'de KESTIRME-YOK bloğu YOK — kural dört depoda bayt-özdeş durmalı"
        )
        return hatalar
    # 🔴 Kör noktanın kendisi: blok bu betiği ADIYLA vaat ediyor.
    # `check_claude_md_refs.py` çıplak adları (içinde '/' olmayan) atlıyor,
    # yani var olmayan bir kapıyı vaat eden metin oradan YEŞİL geçiyordu.
    blok = metin[metin.index(_BLOK_BAS) : metin.index(_BLOK_SON)]
    vaat = re.findall(r"`(check_[a-z0-9_]+\.py)`", blok)
    for ad in vaat:
        if not any((KOK / d / ad).is_file() for d in ("scripts", "tools")):
            hatalar.append(
                f"kural bloğu `{ad}` kapısını vaat ediyor ama o dosya YOK "
                f"(belgelenmiş ama uygulanmayan kural bir dilektir)"
            )
    return hatalar


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    bulunan = _bul()

    if "--liste" in argv:
        for anahtar, satir in sorted(bulunan.items()):
            print(f"  {anahtar}  {satir}")
        print(f"\ntoplam kimliksiz işaret: {len(bulunan)}  ·  taban: {len(_TABAN)}")
        return 0

    hatalar: list[str] = _kural_blogu_kontrol()

    yeni = sorted(set(bulunan) - set(_TABAN))
    if yeni:
        hatalar.append(f"{len(yeni)} YENİ kimliksiz işaret (sessiz borç):")
        hatalar += [f"    {a}  {bulunan[a]}" for a in yeni]
        hatalar.append(
            "    Çözüm: ya BİTİR, ya yanına izleme kimliği yaz (KR-/DK-/AL-K/#123),"
        )
        hatalar.append("    ya da gerekçesiyle `_TABAN` listesine ekle.")

    kayip = sorted(set(_TABAN) - set(bulunan))
    if kayip:
        hatalar.append(f"{len(kayip)} taban kalemi ARTIK YOK — liste bayat:")
        hatalar += [f"    {a}  ({_TABAN[a]})" for a in kayip]
        hatalar.append("    Çözüm: `_TABAN` listesinden SİL (mandal iki yönlüdür).")

    if hatalar:
        print("[KIRMIZI] KESTİRME YOK kapısı:")
        for h in hatalar:
            print(f"  {h}")
        return 1

    print(
        f"[OK] KESTİRME YOK kapısı temiz — kimliksiz işaret {len(bulunan)}, "
        f"taban {len(_TABAN)} (taban büyümedi, liste bayat değil)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
