#!/usr/bin/env python3
"""C8-a — vendored yayılımı elle yapmayı bırak.

NEDEN (üç turun ölçülmüş bedeli):
    C8 töreninin 2. adımı ("`PENDING_PROPAGATION`'ı boşalt") üç kez **elle** yapıldı.
    İlk denemede kanonik prose vendored kopyaya taşındı ve worker'da **45 test**
    cp1254'te kırıldı; ikinci turda `analysis_job` gözden kaçtı ve `scale` tel üstünde
    ölü kaldı (ÖD-2); üçüncü turda (v7.4.0) dört ayrı JSON düzenlemesi yapıldı.
    Aynı işi elle yapmak, her turda aynı üç hatayı yeniden yapma şansı demektir.

BU ARAÇ NEYİ OTOMATİKLEŞTİRİR — ve NEYİ BİLEREK ETMEZ:

    ✅ GENİŞLETME (mekanik, güvenli): kanonikte olup vendored'da olmayan
       * enum DEĞERLERİ (aynı pointer'da)
       * opsiyonel ALANLAR
       Bunlar additive'dir: vendored kopyanın bugün kabul ettiği her belge sonrasında
       da geçer. Yayılım kopyalama DEĞİL alan taşımadır — vendored idiom korunur
       (`unevaluatedProperties` → `additionalProperties`) ve prose KIRPILIR (I-4;
       prose tavanı kapısı `test_vendored_prose_does_not_exceed_canonical`).

    🔴 DARALTMA (asla otomatik): kanonik bir alanı KISITLADIYSA (ör. serbest dize →
       5 değerlik enum, `qc_report.flags` — v7.4.0) araç bunu **uygulamaz, RAPOR EDER**.
       Sebep ölçümle biliniyor: daraltma, o alana bugün yazan bir üreticiyi
       REDDEDEBİLİR. v7.4.0'da bu güvenli çıktı ama güvenli olduğu VARSAYILMADI —
       `qc_report_writer.py:154-165` okunup tam olarak o beş bayrağı yazdığı
       görüldü. O ölçümü bir araç yapamaz; insan yapar. Araç yalnız "burada bir
       daraltma var, ÜRETİCİYİ ÖLÇ" der.

    🔴 SİLME: hiçbir koşulda. Vendored'da olup kanonikte olmayan şey ya beyanlı
       eksen farkıdır (W14) ya da borçtur (`KNOWN_VENDORED_AHEAD`); ikisi de karar
       ister.

KULLANIM:
    python tools/propagate_vendored.py            # --check (varsayılan): raporla, değiştirme
    python tools/propagate_vendored.py --apply    # genişletmeleri UYGULA
    python tools/propagate_vendored.py --pair calibration_metadata.v1.schema.json

ÇIKIŞ KODU (--check): bekleyen genişletme ya da raporlanmış daraltma varsa 1.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent

# Çift listesi TEK KAYNAKTAN gelir: parite kapısının kendisi. İkinci bir liste
# tutmak, D16'nın kapattığı "ikili gövde" hatasının araç hâli olurdu — listeler
# ayrışınca araç kapının görmediği dosyaya yazar ya da tersi.
sys.path.insert(0, str(ROOT / "tests"))


def _pairs() -> list[tuple[str, str, str]]:
    """(kip, kanonik_yol, vendored_yol) — parite kapısından okunur."""
    import test_vendored_parity as parity  # type: ignore[import-not-found]

    return [("MIRROR", c, v) for c, v in parity.MIRROR_PAIRS] + [
        ("SUBSET", c, v) for c, v in parity.SUBSET_PAIRS
    ]


def _enums_by_pointer(doc: Any) -> dict[str, list]:
    found: dict[str, list] = {}

    def rec(node: Any, ptr: str) -> None:
        if isinstance(node, dict):
            if isinstance(node.get("enum"), list):
                found[ptr] = list(node["enum"])
            for key, value in node.items():
                rec(value, f"{ptr}/{key}")
        elif isinstance(node, list):
            for index, value in enumerate(node):
                rec(value, f"{ptr}/{index}")

    rec(doc, "")
    return found


def _at_pointer(doc: Any, ptr: str) -> Any:
    node = doc
    for part in [p for p in ptr.split("/") if p]:
        if isinstance(node, list):
            node = node[int(part)]
        else:
            node = node[part]
    return node


def _crop_prose(node: Any) -> Any:
    """Kanonik alt ağacı vendored biçime indir: prose kırpılır, idiom çevrilir.

    I-4: vendored kopya kanoniğin DAR RUNTIME ALT KÜMESİDİR. Kanonik `description`
    alanları uzun Türkçe gerekçeler taşır; onları taşımak (a) I-4'ü ihlal eder,
    (b) prose tavanı kapısını kırar, (c) C8'de worker'da 45 testi cp1254'te kırdı.
    Yerine kanoniğe İŞARET EDEN tek satır bırakılır.
    """
    if isinstance(node, dict):
        out: dict[str, Any] = {}
        for key, value in node.items():
            if key == "description":
                out[key] = "-> kanonik tanim: contracts (bkz. ayni pointer)"
            elif key == "unevaluatedProperties":
                # Vendored idiom: kapalilik `additionalProperties` ile ifade edilir.
                out["additionalProperties"] = value
            else:
                out[key] = _crop_prose(value)
        return out
    if isinstance(node, list):
        return [_crop_prose(v) for v in node]
    return node


class Finding:
    __slots__ = ("kind", "pair", "pointer", "detail")

    def __init__(self, kind: str, pair: str, pointer: str, detail: str) -> None:
        self.kind, self.pair, self.pointer, self.detail = kind, pair, pointer, detail

    def __str__(self) -> str:
        mark = {"ENUM": "+", "FIELD": "+", "NARROWING": "!"}[self.kind]
        return f"  {mark} [{self.kind}] {self.pair}{self.pointer} -> {self.detail}"


def analyse(canonical: dict, vendored: dict, pair: str) -> list[Finding]:
    findings: list[Finding] = []
    ce, ve = _enums_by_pointer(canonical), _enums_by_pointer(vendored)

    for ptr, cvals in ce.items():
        if ptr in ve:
            missing = [v for v in cvals if v not in ve[ptr]]
            if missing:
                findings.append(Finding("ENUM", pair, ptr, f"eksik deger {missing}"))
        else:
            # Kanonikte enum var, vendored'da YOK. Iki ayri durum:
            #   (a) vendored'da o dugum HIC yok  -> alan zaten yok, enum sorunu degil
            #       (asagidaki alan karsilastirmasi yakalar)
            #   (b) dugum VAR ama enum'suz      -> alan KISITSIZ, kanonik kisitladi
            #       => DARALTMA. v7.4.0'daki `qc_report.flags` (serbest dize -> 5
            #          degerlik sozluk) tam olarak buydu.
            try:
                node = _at_pointer(vendored, ptr)
            except (KeyError, IndexError, ValueError):
                continue
            if not isinstance(node, dict) or "enum" in node:
                continue
            findings.append(
                Finding(
                    "NARROWING",
                    pair,
                    ptr,
                    f"kanonik {len(cvals)} degerlik enum getirdi, vendored KISITSIZ "
                    "-- URETICIYI OLC, otomatik uygulanmaz",
                )
            )

    cprops = canonical.get("properties", {})
    vprops = vendored.get("properties", {})
    creq = set(canonical.get("required", []))
    if isinstance(cprops, dict) and isinstance(vprops, dict):
        for name in sorted(set(cprops) - set(vprops)):
            if name in creq:
                findings.append(
                    Finding(
                        "NARROWING",
                        pair,
                        f"/properties/{name}",
                        "kanonikte ZORUNLU yeni alan -- additive degil, elle karar",
                    )
                )
            else:
                findings.append(Finding("FIELD", pair, f"/properties/{name}", "opsiyonel alan"))
    return findings


def apply_widenings(canonical: dict, vendored: dict, findings: list[Finding]) -> int:
    """Yalniz GENISLETMELERI yazar; yazilan oge sayisini dondurur.

    🔴 Ilk surumde burada sessiz bir hata vardi ve YALNIZ MUTASYONLA gorundu:
    `_enums_by_pointer` pointer'i enum'u ICEREN dugume verir (`.../calibration_type`),
    enum LISTESINE degil. Kod `_at_pointer(...)` sonucunu liste sanip uzerinde
    donuyordu -> sozlugun ANAHTARLARINI ("type", "enum", ...) geziyor, hepsi zaten
    "var" cikiyor ve hicbir sey yazilmiyordu. `--check` kusursuz gorunurken `--apply`
    "0 genisletme yazildi" deyip EXIT 0 donuyordu; yani arac basariyla HICBIR SEY
    yapmiyordu. Bu yuzden asagida once `enum` anahtari acikca alinir.
    """
    applied = 0
    for f in findings:
        if f.kind == "ENUM":
            target_node = _at_pointer(vendored, f.pointer)
            source_node = _at_pointer(canonical, f.pointer)
            target = target_node["enum"]
            for value in source_node["enum"]:
                if value not in target:
                    target.append(value)
                    applied += 1
        elif f.kind == "FIELD":
            name = f.pointer.rsplit("/", 1)[1]
            vendored.setdefault("properties", {})[name] = _crop_prose(canonical["properties"][name])
            applied += 1
    return applied


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument(
        "--apply", action="store_true", help="genisletmeleri UYGULA (varsayilan: yalniz raporla)"
    )
    ap.add_argument("--pair", help="yalniz bu vendored dosya adi")
    args = ap.parse_args()

    total_w = total_n = 0
    for mode, canonical_rel, vendored_rel in _pairs():
        name = Path(vendored_rel).name
        if args.pair and args.pair != name:
            continue
        if mode != "MIRROR":
            # SUBSET ciftlerinde vendored kopya kanonigin DAR ALT KUMESIDIR (I-4):
            # alan/enum EKSIKLIGI normaldir, "bekleyen yayilim" DEGILDIR. Ilk surumde
            # bu ayrim yoktu ve arac `analysis_job`/`analysis_result` icin 28 sahte
            # yayilim onerdi -- uygulansaydi worker'in KASITLI dar runtime formunu
            # kanonik superset'e sisirecekti (I-4 ihlali). Parite kapisinin SUBSET
            # kurallari (paylasilan `$defs` birebir · vendored enum degeri uydurulamaz
            # · vendored-only ust duzey alan = AK-4) bu ciftleri zaten kolluyor.
            continue
        vpath = WORKSPACE / vendored_rel
        if not vpath.exists():
            continue  # kardes depo yok -- parite kapisiyla ayni davranis
        canonical = json.loads((ROOT / canonical_rel).read_text(encoding="utf-8"))
        raw = vpath.read_text(encoding="utf-8")
        vendored = json.loads(raw)

        findings = analyse(canonical, vendored, name)
        if not findings:
            continue
        print(f"\n{name}  [{mode}]")
        for f in findings:
            print(f)
        widenings = [f for f in findings if f.kind in ("ENUM", "FIELD")]
        total_w += len(widenings)
        total_n += len(findings) - len(widenings)

        if args.apply and widenings:
            applied = apply_widenings(canonical, vendored, widenings)
            newline = "\r\n" if "\r\n" in raw else "\n"
            vpath.write_text(
                json.dumps(vendored, indent=2, ensure_ascii=False).replace("\n", newline) + newline,
                encoding="utf-8",
            )
            print(f"  -> UYGULANDI: {applied} genisletme yazildi ({vendored_rel})")

    print("\n" + "=" * 70)
    print(f"Genisletme (mekanik): {total_w}   |   Daraltma/karar (ELLE): {total_n}")
    if total_n:
        print("!! Daraltma kalemleri OTOMATIK UYGULANMAZ. Her biri icin URETICIYI OLC:")
        print("   o alana bugun yazan kod var mi, yazdigi degerler yeni kisiti geciyor mu?")
        print("   (v7.4.0'da qc_report.flags tam boyleydi ve guvenli oldugu OLCULEREK gosterildi.)")
    if args.apply:
        print("Sonraki adim: kardes depoda hash/pin yenile, testleri kostur, PR ac.")
        return 0
    if total_w or total_n:
        print("(--check kipi: hicbir dosya degistirilmedi. Uygulamak icin --apply.)")
        return 1
    print("Bekleyen yayilim YOK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
