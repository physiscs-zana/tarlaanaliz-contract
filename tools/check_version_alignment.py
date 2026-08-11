#!/usr/bin/env python3
"""I-1 (sürüm hizası) kapısı — AL-K30.

NEDEN VAR (2026-08-11 ölçümü):
    Üç deponun `CLAUDE.md`'sinde *"I-1: `CONTRACTS_VERSION.md` sürümü üç depoda aynı"*
    yazıyor. Bu kuralı doğrulayan **tek bir komut yoktu** — dört depo tarandı: contract'ta
    2 isabet düzyazı, platform'daki 8 isabet **başka bir numaralandırma** (Dockerfile
    değişmezi, çapraz-repo sürümüyle ilgisiz), worker ve edge'de **0**.

    Kuralın sessizce kırıldığı da ölçüldü: edge `7.6.1`'i **hiç pinlemedi**
    (pin geçmişi 7.5.0 → 7.6.0 → 7.7.0). Kimse fark etmedi, çünkü bakan yoktu.
    Belgelenmiş ama uygulanmayan kural bir dilektir.

NEREDE KOŞAR (D4-b):
    Kapı **burada yazılır, kardeş depolarda koşar** — `tests/test_vendored_parity.py`
    ile aynı model. Bu depo PUBLIC, kardeşlerin üçü de PRIVATE; contract CI'ına kardeş
    anahtarı koymak sır yüzeyini yanlış yöne açar. Ters yön bedava: kardeş CI bu public
    depoyu ek sır olmadan checkout eder.

    ⚠️ **Kardeşin KENDİ checkout'uyla karşılaştırmak TOTOLOJİDİR.** Kardeş CI sözleşmeyi
    `ref: v${pin}` ile çeker; çektiği ağacın sürümü elbette pinine eşittir. Anlamlı
    karşılaştırma **yayımlanmış en yüksek etiketle** yapılır — bu yüzden `--latest`
    ya da `--latest-from-git` zorunludur ve bulunamazsa kapı **fail-closed** kapanır.

İKİ KİP (aynı kural değil — karıştırmak yanlış alarm üretir):
    * `consumer`  — kardeş depo: pin **en yeni yayımlanmış sürüme EŞİT** olmalı.
                    Geçici gerilik yalnız I-5 gereği **tarihli + gerekçeli** muafiyetle.
    * `canonical` — contract'ın kendisi: sürüm en yeni etiketin **GERİSİNDE olamaz**.
                    İleride olabilir (sürüm yükseltildi, etiket henüz basılmadı — release
                    PR'ının normal hâli). Geride olmak sürüm gerilemesidir, hatadır.

KULLANIM:
    python3 tools/check_version_alignment.py --mode canonical --pinned-file CONTRACTS_VERSION.md \
        --label '## Version:' --latest-from-git
    python3 tools/check_version_alignment.py --mode consumer --pinned-file CONTRACTS_VERSION.md \
        --label 'Upstream Contract Set' --latest 7.7.2
    python3 tools/check_version_alignment.py --mode consumer --pinned-file CONTRACTS_VERSION.md --latest 7.7.2 \\
        --allow-lag-until 2026-08-20 --reason "worker re-pin PR #226 bekliyor"
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import date
from pathlib import Path


#: Sürüm dizesi — `v` öneki isteğe bağlı (worker `v7.7.2`, edge ve contract `7.7.2` yazar).
_VERSION = re.compile(r"\bv?(\d+)\.(\d+)\.(\d+)\b")

#: Etiket adı — yalnız `vX.Y.Z` biçimi kanoniktir (I-2).
_TAG = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")


def parse_version(text: str) -> tuple[int, int, int] | None:
    """Metindeki İLK sürüm dizesini ayrıştırır (tek satırlık girdi için)."""
    match = _VERSION.search(text)
    if not match:
        return None
    return (int(match.group(1)), int(match.group(2)), int(match.group(3)))


def extract_pinned(
    text: str, label: str | None = None
) -> tuple[tuple[int, int, int] | None, str]:
    """(sürüm, gerekçe) — ETİKETLİ SATIRDAN okur; belirsizlikte TAHMİN ETMEZ.

    🔴 İlk yazımda kural *"dosyadaki ilk eşleşme"*ydi. Gerçek veriye karşı koşturunca
    **yanlış sayıyı sessizce okudu** (2026-08-11 ölçümü):

        edge/CONTRACTS_VERSION.md
          satır  3 : CONTRACTS_VERSION=1.7.0        ← edge'in KENDİ SemVer'i
          satır  5 : **Version:** 1.7.0
          satır 11 : | **Upstream Contract Set (SSOT)** | `7.7.2` …   ← ASIL PIN

    Kapı `1.7.0` okuyup *"pin 1.7.0, en yeni 7.7.2 → I-1 KIRIK"* dedi. Doğru cevabı
    yanlış gerekçeyle verdi — bu, sessiz yanlış-negatiften bile beter bir durumdur,
    çünkü sürüm dizeleri bir gün örtüşürse **yanlış YEŞİL** verirdi.

    Ölçüm: üç sürüm dosyasında sırasıyla **30 · 22 · 27** farklı sürüm dizesi geçiyor
    (değişiklik geçmişi aynı dosyada tutuluyor). Yani "ilk eşleşme" tahmindir.

    Kural: `label` verilirse **yalnız o metni içeren satırlar** taranır. Verilmezse ve
    dosyada birden çok farklı sürüm varsa kapı **fail-closed** kapanır ve etiket ister —
    hangi sayının okunacağını asla tahmin etmez.
    """
    satirlar = text.splitlines()
    if label:
        secili = [ln for ln in satirlar if label in ln]
        if not secili:
            return None, f"`{label}` metnini içeren satır yok"
        found = parse_version(secili[0])
        if found is None:
            return None, f"`{label}` satırında sürüm dizesi yok: {secili[0].strip()[:80]!r}"
        return found, "ok"

    hepsi = [
        (int(m.group(1)), int(m.group(2)), int(m.group(3)))
        for m in _VERSION.finditer(text)
    ]
    farkli = sorted(set(hepsi))
    if not farkli:
        return None, "sürüm dizesi bulunamadı"
    if len(farkli) > 1:
        ornek = ", ".join(format_version(v) for v in farkli[:5])
        return None, (
            f"dosyada {len(farkli)} FARKLI sürüm dizesi var ({ornek}…) — hangisinin pin "
            "olduğu TAHMİN EDİLEMEZ. `--label <metin>` ile pin satırını gösterin. "
            "(Ölçüldü 2026-08-11: bu araç etiket olmadan edge dosyasında `1.7.0` okudu; "
            "doğru pin 11. satırdaki `7.7.2` idi.)"
        )
    return farkli[0], "ok"


def format_version(version: tuple[int, int, int]) -> str:
    return "{}.{}.{}".format(*version)


def newest_tag(tags: list[str]) -> tuple[int, int, int] | None:
    """`vX.Y.Z` biçimindeki etiketlerin en yükseği. Diğer biçimler YOK SAYILIR."""
    parsed = [
        (int(m.group(1)), int(m.group(2)), int(m.group(3)))
        for m in (_TAG.match(tag.strip()) for tag in tags)
        if m
    ]
    return max(parsed) if parsed else None


def git_tags(repo: Path) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(repo), "tag", "--list", "v*"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if result.returncode != 0:
        return []
    return result.stdout.splitlines()


def evaluate(
    mode: str,
    pinned: tuple[int, int, int],
    latest: tuple[int, int, int],
    today: date,
    allow_lag_until: date | None = None,
    reason: str | None = None,
) -> tuple[int, str]:
    """(çıkış kodu, mesaj) — saf fonksiyon, sentetik olarak sınanabilir."""
    p, l = format_version(pinned), format_version(latest)

    if mode == "canonical":
        if pinned < latest:
            return 1, (
                f"I-1 KIRIK (kanonik): sürüm {p}, en yeni etiket ise v{l}. Kanonik sürüm "
                "etiketin GERİSİNDE olamaz — bu bir sürüm gerilemesidir."
            )
        if pinned > latest:
            return 0, (
                f"OK (kanonik): sürüm {p}, en yeni etiket v{l} — release uçuşta "
                "(sürüm yükseltildi, etiket henüz basılmadı). I-2 gereği merge sonrası "
                f"`v{p}` annotated etiketi basılmalı."
            )
        return 0, f"OK (kanonik): sürüm {p} = en yeni etiket v{l}."

    # consumer
    if pinned == latest:
        return 0, f"OK (tüketici): pin {p} = en yeni yayımlanmış sürüm {l}."

    if pinned > latest:
        return 1, (
            f"I-1 KIRIK (tüketici): pin {p}, yayımlanmış en yeni sürüm ise {l}. Tüketici "
            "yayımlanmamış bir sürüme pinlenemez — etiket yoksa checkout da edilemez."
        )

    # pinned < latest → gerilik
    if allow_lag_until is None:
        return 1, (
            f"I-1 KIRIK (tüketici): pin {p}, yayımlanmış en yeni sürüm {l}. Sessiz gerilik "
            "YASAK (I-5: sapma yalnız GEÇİCİ). 2026-08-11 ölçümü: edge 7.6.1'i hiç "
            "pinlemedi ve kimse fark etmedi — bu kapı tam o durumu yakalar. Geçici olarak "
            "geride kalınacaksa `--allow-lag-until <tarih> --reason <gerekçe>` verin."
        )
    if not reason or not reason.strip():
        return 1, (
            f"I-1 muafiyeti GEREKÇESİZ: pin {p} < {l}. Tarihli muafiyet bir gerekçe "
            "olmadan kabul edilmez — gerekçesiz muafiyet, kuralın sessizce kapatılmasıdır."
        )
    if today > allow_lag_until:
        return 1, (
            f"I-1 muafiyeti SÜRESİ DOLDU: pin {p} < {l}; muafiyet {allow_lag_until} "
            f"tarihine kadardı, bugün {today}. Gerekçe: {reason.strip()}"
        )
    return 0, (
        f"OK (tüketici, GEÇİCİ SAPMA): pin {p} < {l}, muafiyet {allow_lag_until} "
        f"tarihine kadar geçerli. Gerekçe: {reason.strip()}"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="I-1 sürüm hizası kapısı (AL-K30)")
    parser.add_argument("--mode", choices=("consumer", "canonical"), required=True)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--pinned-file", help="Pinlenen sürümü taşıyan dosya")
    source.add_argument("--pinned", help="Pinlenen sürüm (doğrudan)")
    latest = parser.add_mutually_exclusive_group(required=True)
    latest.add_argument("--latest", help="Yayımlanmış en yeni sürüm")
    latest.add_argument(
        "--latest-from-git", metavar="REPO", nargs="?", const=".",
        help="En yeni sürümü bu depodaki vX.Y.Z etiketlerinden oku",
    )
    parser.add_argument(
        "--label",
        help="Pin satırını seçen metin (örn. 'Upstream Contract Set'). Dosyada birden çok "
             "sürüm dizesi varsa ZORUNLU — araç hangisinin pin olduğunu tahmin etmez.",
    )
    parser.add_argument("--allow-lag-until", help="I-5 geçici muafiyet bitiş tarihi (YYYY-AA-GG)")
    parser.add_argument("--reason", help="Muafiyetin gerekçesi (zorunlu)")
    parser.add_argument("--today", help="Test kancası — bugünün tarihi (YYYY-AA-GG)")
    args = parser.parse_args(argv)

    if args.pinned_file:
        path = Path(args.pinned_file)
        if not path.exists():
            print(f"HATA: pin dosyası yok: {path} — kapı fail-closed kapanır.")
            return 1
        pinned, gerekce = extract_pinned(
            path.read_text(encoding="utf-8", errors="replace"), args.label
        )
        kaynak = str(path) + (f"  [--label {args.label!r}]" if args.label else "")
    else:
        pinned, gerekce = parse_version(args.pinned), "ok"
        if pinned is None:
            gerekce = "sürüm dizesi bulunamadı"
        kaynak = "--pinned"
    if pinned is None:
        print(f"HATA: pin okunamadı ({kaynak}): {gerekce} — fail-closed.")
        return 1

    if args.latest:
        newest = parse_version(args.latest)
        latest_kaynak = "--latest"
    else:
        newest = newest_tag(git_tags(Path(args.latest_from_git)))
        latest_kaynak = f"git etiketleri ({args.latest_from_git})"
    if newest is None:
        print(
            f"HATA: en yeni sürüm belirlenemedi ({latest_kaynak}). Kapı fail-closed "
            "kapanır — 'ölçemedim' asla 'hizalı' sayılmaz."
        )
        return 1

    # Hangi değeri okuduğumuzu DAİMA bas: sessizce yanlış satırı okumak en sinsi hatadır.
    print(f"okunan pin      : {format_version(pinned)}   ({kaynak})")
    print(f"okunan en yeni  : {format_version(newest)}   ({latest_kaynak})")

    try:
        allow_until = date.fromisoformat(args.allow_lag_until) if args.allow_lag_until else None
        today = date.fromisoformat(args.today) if args.today else date.today()
    except ValueError as exc:
        print(f"HATA: tarih ayrıştırılamadı ({exc}) — fail-closed.")
        return 1

    code, message = evaluate(args.mode, pinned, newest, today, allow_until, args.reason)
    print(message)
    return code


if __name__ == "__main__":
    sys.exit(main())
