#!/usr/bin/env python3
"""Harici `$ref`'leri çözerek KENDİ KENDİNE YETEN yayın biçimi üretir (E3 / §14.2.1).

KARAR (koordinatör onaylı, 2026-07-31 — eylem planı §14.2.1, seçenek A):
    Kanonik şemalar `enums/` altına **göreli harici `$ref`** veriyor. Ölçüldü: **38 harici
    referans, 23 dosyada, 13 enum'a** (E3 bunu 3 sanıyordu — yalnız `intake_manifest`e
    bakmıştı). Vendored kopyalarda bu referanslar **YOK**: değerler satır içi. Yani sözleşme
    iki biçimde yaşıyor ve hava-boşluklu M1 kanonik biçimi **çözemiyor** (`Unresolvable`).

    Karar: **kaynak DRY kalır** (`$ref` korunur — enum tek yerde tanımlıdır), **yayın biçimi
    satır içidir**. Bu araç ikisi arasındaki köprüdür.

ŞARTLAR (kararla birlikte onaylandı):
    ① Satır içi üretim ARAÇLA yapılır — elle kopyala-yapıştır YASAK.
    ② Üretilen her düğüm `x-inlined-from` izi taşır (nereden geldiği ölçülebilir).
    ③ Bir test satır içi değerlerin kanonik enum'la BİREBİR olduğunu zorlar (C-PARİTE deseni).
    ④ Enum değişince yeniden üretim release checklist'ine girer (SDLC_GATES §3G).

NE SATIR İÇİ ALINIR (bilerek DAR):
    Yalnız **doğrulama anlamı olan** anahtarlar: `type`, `enum`, `pattern`, `format`,
    `minimum`, `maximum`, `minLength`, `maxLength`, `const`.
    Enum dosyasının `$id`/`$schema`/`metadata`/`notes` alanları **taşınmaz** — `$id`
    kopyalamak aynı kimliği iki yerde tanımlar (çözücüyü bozar), `metadata` ise
    doğrulamaya girmez ve dosyayı şişirir.

YERELDE KULLANIM (bu depoda, geliştirme makinesinde):
    python tools/inline_refs.py --check    # dist/ güncel mi? (CI/koşum kapısı)
    python tools/inline_refs.py --write    # dist/ yeniden üretilir (C8 töreni adımı)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
DIST = ROOT / "dist" / "schemas"

#: Satır içi alınan doğrulama anahtarları (bilerek dar — bkz. modül docstring'i).
VALIDATION_KEYS = (
    "type", "enum", "const", "pattern", "format",
    "minimum", "maximum", "exclusiveMinimum", "exclusiveMaximum",
    "minLength", "maxLength", "minItems", "maxItems",
)


def _resolve(source: Path, ref: str) -> Path:
    return (source.parent / ref).resolve()


def inline_node(node: Dict[str, Any], source: Path) -> Tuple[Dict[str, Any], List[str]]:
    """Bir `$ref` düğümünü satır içi hâline çevir. (yeni düğüm, uyarılar) döndürür."""
    ref = node["$ref"]
    target = _resolve(source, ref)
    if not target.exists():
        return node, [f"{source.relative_to(ROOT).as_posix()}: ÇÖZÜLEMEYEN $ref -> {ref}"]

    enum_doc = json.loads(target.read_text(encoding="utf-8"))
    inlined: Dict[str, Any] = {k: enum_doc[k] for k in VALIDATION_KEYS if k in enum_doc}
    if not inlined:
        return node, [f"{source.relative_to(ROOT).as_posix()}: {ref} doğrulama anahtarı taşımıyor"]

    # Yerel kardeş anahtarlar KORUNUR ve satır içi değerleri EZMEZ değil — tam tersi:
    # yerel `description` gibi alanlar üstte kalır (Draft 2020-12 $ref-sibling semantiği).
    for key, value in node.items():
        if key != "$ref":
            inlined[key] = value

    inlined["x-inlined-from"] = {
        "ref": ref,
        "source_id": enum_doc.get("$id"),
        "keys": sorted(k for k in VALIDATION_KEYS if k in enum_doc),
        "note": (
            "OTOMATİK ÜRETİLDİ — elle düzenlemeyin. Kaynak: yukarıdaki `ref`. "
            "Yeniden üretim: python tools/inline_refs.py --write (SDLC_GATES §3G)."
        ),
    }
    return inlined, []


def inline_document(doc: Any, source: Path) -> Tuple[Any, List[str]]:
    warnings: List[str] = []
    if isinstance(doc, dict):
        if isinstance(doc.get("$ref"), str) and not doc["$ref"].startswith("#"):
            return inline_node(doc, source)
        out = {}
        for key, value in doc.items():
            out[key], warn = inline_document(value, source)
            warnings.extend(warn)
        return out, warnings
    if isinstance(doc, list):
        items = []
        for value in doc:
            new, warn = inline_document(value, source)
            items.append(new)
            warnings.extend(warn)
        return items, warnings
    return doc, warnings


def build() -> Tuple[Dict[str, str], List[str]]:
    """Tüm şemaların satır içi hâlini üret. {göreli yol: içerik} + uyarılar."""
    produced: Dict[str, str] = {}
    warnings: List[str] = []
    for path in sorted(SCHEMAS.rglob("*.json")):
        doc = json.loads(path.read_text(encoding="utf-8"))
        inlined, warn = inline_document(doc, path)
        warnings.extend(warn)
        relative = path.relative_to(SCHEMAS).as_posix()
        produced[relative] = json.dumps(inlined, indent=2, ensure_ascii=False) + "\n"
    return produced, warnings


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Harici $ref'leri satır içi alarak dist/ üretir")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true", help="dist/ ağacını yeniden üret")
    group.add_argument("--check", action="store_true", help="dist/ güncel mi (üretmeden)")
    args = parser.parse_args()

    produced, warnings = build()
    for warning in warnings:
        print(f"⚠️  {warning}", file=sys.stderr)
    if warnings:
        print("❌ Çözülemeyen referans var — yayın biçimi üretilemez.", file=sys.stderr)
        return 2

    if args.write:
        for relative, content in produced.items():
            out = DIST / relative
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(content, encoding="utf-8")
        print(f"✅ dist/schemas/ yeniden üretildi: {len(produced)} dosya")
        return 0

    stale: List[str] = []
    for relative, content in produced.items():
        out = DIST / relative
        if not out.exists() or out.read_text(encoding="utf-8") != content:
            stale.append(relative)
    if stale:
        print(f"❌ dist/ BAYAT ({len(stale)} dosya) — `python tools/inline_refs.py --write` koşun:",
              file=sys.stderr)
        for relative in stale[:10]:
            print(f"   - {relative}", file=sys.stderr)
        return 1
    print(f"✅ dist/ güncel: {len(produced)} dosya")
    return 0


if __name__ == "__main__":
    sys.exit(main())
