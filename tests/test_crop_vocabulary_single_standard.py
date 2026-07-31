"""Ürün (crop) vocabulary'si TEK standarttır — contract/edge/worker/platform aynı sözlük.

NEDEN (2026-07-31, AK-7 · kullanıcı direktifi):
    Contract içinde İKİ ürün sözlüğü yaşıyordu:
      * kanonik `enums/crop_type.enum.v1.json` — **BÜYÜK harf, 8 değer**
      * edge'in vendored kopyası — **küçük harf, 5 değer**

    Kök neden ölçüldü: kanonik şemalarda **beş** ürün alanı `{"type": "string"}` idi,
    yani serbest metin. Dördünün açıklaması *"reference: enums/crop_type.enum.v1.json"*
    diyordu ama şema hiçbir şeyi ZORLAMIYORDU (C0'ın manifest formlarında kapattığı
    "prose var, zorlanabilirlik yok" sınıfının aynısı); beşincisi
    (`edge/worker_result.v1.crop_type`) enum'a atıf bile yapmadan
    *"e.g. cotton, wheat"* diyordu — edge küçük harfi oradan almıştı.

    Yani sapma edge'in keyfi tercihi değil, **kanonik boşluğun sonucuydu.**

Bu dosyanın kuralı: bir alan ürünü ADLANDIRIYORSA, kanonik sözlüğü kullanmak
ZORUNDADIR. Yeni bir şema serbest metin ürün alanı eklerse burası kırmızıya döner.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest


ROOT = Path(__file__).parent.parent
CROP_ENUM = ROOT / "enums" / "crop_type.enum.v1.json"

#: Ürün ADLANDIRAN alan adları. `crops` (dizi kabı) ve `calendar_risk_by_crop`
#: (mahsul GRUBU ekseni: cereals/fruit_trees) bilerek dışarıda — farklı eksenler.
CROP_VALUE_FIELDS = {"crop_type", "crop"}


def _canonical() -> list[str]:
    return json.loads(CROP_ENUM.read_text(encoding="utf-8"))["enum"]


def _crop_fields() -> list[tuple[str, str, dict]]:
    """Kanonik şemalardaki tüm ürün-değeri alanlarını topla."""
    found: list[tuple[str, str, dict]] = []
    for path in sorted((ROOT / "schemas").rglob("*.json")):
        doc = json.loads(path.read_text(encoding="utf-8"))
        where = str(path.relative_to(ROOT)).replace("\\", "/")

        def walk(node: object, trail: str) -> None:
            if isinstance(node, dict):
                for key, value in node.items():
                    if key in CROP_VALUE_FIELDS and isinstance(value, dict):
                        found.append((where, f"{trail}.{key}".lstrip("."), value))
                    walk(value, f"{trail}.{key}")
            elif isinstance(node, list):
                for index, item in enumerate(node):
                    walk(item, f"{trail}[{index}]")

        walk(doc, "")
    return found


class TestNoFreeTextCropField:
    def test_collector_finds_something(self) -> None:
        assert _crop_fields(), "toplayıcı bozuk — hiç ürün alanı bulunamadı"

    def test_every_crop_field_is_bound_to_the_canonical_vocabulary(self) -> None:
        canonical = _canonical()
        offenders: list[str] = []
        for where, trail, field in _crop_fields():
            if "$ref" in field:
                if not str(field["$ref"]).endswith("crop_type.enum.v1.json"):
                    offenders.append(f"{where}:{trail} → yabancı $ref {field['$ref']}")
                continue
            values = field.get("enum")
            if values is None:
                offenders.append(f"{where}:{trail} → SERBEST METİN (enum yok)")
            elif list(values) != canonical:
                offenders.append(f"{where}:{trail} → farklı sözlük {values}")
        assert not offenders, (
            "Ürün alanları kanonik sözlüğe bağlı değil:\n  " + "\n  ".join(offenders)
            + "\n\nKural: bir alan ürünü adlandırıyorsa ya kanonik enum'a `$ref` verir ya "
            "aynı değerleri satır içi taşır (air-gap şemalarında satır içi tercih edilir). "
            "Açıklamada 'reference: crop_type.enum.v1' yazmak ZORLAMAZ — C0 dersi."
        )

    def test_no_lowercase_crop_vocabulary_anywhere(self) -> None:
        """Küçük harf sözlük kanoniğe SIZAMAZ (edge'in sapması absorbe edilmesin)."""
        offenders = []
        for where, trail, field in _crop_fields():
            for value in field.get("enum", []) or []:
                if isinstance(value, str) and value != value.upper():
                    offenders.append(f"{where}:{trail} → {value!r}")
        assert not offenders, f"küçük harf ürün değeri: {offenders}"


class TestCanonicalEnumIsTheSingleSource:
    def test_inline_copies_match_the_enum_exactly(self) -> None:
        """Satır içi kopyalar bayatlamasın: enum'a değer eklenirse hepsi güncellenmeli."""
        canonical = _canonical()
        inline = [
            (where, trail)
            for where, trail, field in _crop_fields()
            if "enum" in field and list(field["enum"]) != canonical
        ]
        assert not inline, f"satır içi kopya kanonikten ayrışmış: {inline}"

    def test_enum_has_the_expected_gap_set(self) -> None:
        """GAP-8 kümesi (KR-030) — beklenmedik daralma/genişleme fark edilsin."""
        assert set(_canonical()) == {
            "COTTON", "PISTACHIO", "CORN", "WHEAT", "SUNFLOWER", "GRAPE", "OLIVE", "RICE",
        }


class TestTighteningIsDeclared:
    """Serbest metni daraltmak biçimsel breaking'dir → beyanı olmalı."""

    @pytest.mark.parametrize(
        "relative",
        [
            "schemas/edge/worker_result.v1.schema.json",
            "schemas/events/analysis_completed.v1.schema.json",
            "schemas/events/analysis_review_requested.v1.schema.json",
            "schemas/events/field_created.v1.schema.json",
            "schemas/events/field_health_changed.v1.schema.json",
        ],
    )
    def test_declaration_exists(self, relative: str) -> None:
        text = (ROOT / relative).read_text(encoding="utf-8")
        assert "x-compat-accepted" in text, (
            f"{relative}: serbest metin daraltıldı ama beyan yok — dedektör bunu BREAKING "
            "sayar ve haklıdır."
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
