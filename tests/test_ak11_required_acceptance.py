"""AK-11: `x-compat-accepted` beyanı `FIELD_MADE_REQUIRED` yolunda da tanınmalı.

ÖLÇÜLEN TUTARSIZLIK (2026-08-01, S7 turunda bulundu):
    Dedektör beyanı kısıt daraltmalarında (pattern / maxLength / enum / oneOf)
    tanıyordu ama alanı ZORUNLU kılma yolunda **hiç kontrol etmiyordu** — o dal
    `_record()` yerine doğrudan `self.changes.append()` çağırıyordu. Sonuç: *"üretici
    yok, ÖLÇÜLDÜ"* gerekçesi bu değişiklik tipinde beyanla geçirilemiyordu ve S7-b
    gibi kalemler MEKANİK olarak MAJOR'a itiliyordu. Yani beyan mekanizmasının kendisi
    tutarsızdı: aynı kanıt bir tipte kabul ediliyor, diğerinde görülmüyordu.

BU DOSYA NEYİ KORUR:
    ① Beyan + açık opt-in varsa `FIELD_MADE_REQUIRED` NON_BREAKING'e iner.
    ② Beyan YOKSA hâlâ BREAKING kalır (indirme sessiz bir arka kapı değildir).
    ③ Opt-in YOKSA iner DEĞİL — çünkü tek damga, aynı düğümdeki DAHA GÜÇLÜ iddiayı
      sessizce kapsamamalı (bir alanın hem pattern'ı daralıp hem required olması).
    ④ `properties`de tanımsız bir required alan için taşıyıcı düğüm yok → indirme yok.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

_TOOL = Path(__file__).resolve().parents[1] / "tools" / "breaking_change_detector.py"


def _detector_module():
    spec = importlib.util.spec_from_file_location("bcd", _TOOL)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write(base: Path, name: str, doc: dict) -> None:
    (base / "schemas").mkdir(parents=True, exist_ok=True)
    (base / "schemas" / name).write_text(json.dumps(doc), encoding="utf-8")


_DECL = {
    "change": "band alani zorunlu kilindi",
    "date": "2026-08-02",
    "rationale": "olculdu: bu alani yazan uretici yok (E11 kare secici henuz yazilmadi)",
    "ref": "S7-b",
}


def _old() -> dict:
    return {
        "type": "object",
        "required": [],
        "properties": {"band": {"type": "string"}},
    }


def _run(tmp_path: Path, new_doc: dict):
    old_dir, new_dir = tmp_path / "old", tmp_path / "new"
    _write(old_dir, "t.v1.schema.json", _old())
    _write(new_dir, "t.v1.schema.json", new_doc)
    mod = _detector_module()
    det = mod.BreakingChangeDetector(old_dir, new_dir)
    det.scan_tree(old_dir, new_dir)
    return [c for c in det.changes if c["type"] == "FIELD_MADE_REQUIRED"]


class TestDeclarationIsHonouredOnTheRequiredPath:
    def test_declared_with_opt_in_is_downgraded(self, tmp_path: Path) -> None:
        doc = _old()
        doc["required"] = ["band"]
        doc["properties"]["band"]["x-compat-accepted"] = {
            **_DECL,
            "accepts": ["FIELD_MADE_REQUIRED"],
        }
        found = _run(tmp_path, doc)
        assert len(found) == 1
        assert (
            found[0]["severity"] == "NON_BREAKING"
        ), "beyan + opt-in varken hala BREAKING -- AK-11 regresyonu"
        assert "ACCEPTED TIGHTENING" in found[0]["message"]
        assert "olculdu" in found[0]["message"], "gerekce rapora yazilmali (sessiz indirme yok)"

    def test_undeclared_stays_breaking(self, tmp_path: Path) -> None:
        doc = _old()
        doc["required"] = ["band"]
        found = _run(tmp_path, doc)
        assert len(found) == 1
        assert (
            found[0]["severity"] == "BREAKING"
        ), "beyansiz zorunlu-kilma indirildi -- indirme bir ARKA KAPI olmus"

    def test_declaration_without_opt_in_does_not_downgrade(self, tmp_path: Path) -> None:
        """Tek damga, aynı düğümdeki DAHA GÜÇLÜ iddiayı kapsamamalı.

        Bir alanın hem `pattern`'ı daraltılıp hem `required` yapıldığını düşünün:
        pattern için yazılmış bir gerekçe, "zorunlu kıldım"ı da sessizce indirirdi.
        Mevcut beyanlar `change`'i SERBEST METİN yazıyor, dolayısıyla tip eşleşmesi
        metinden çıkarılamaz -> açık `accepts` listesi gerekir.
        """
        doc = _old()
        doc["required"] = ["band"]
        doc["properties"]["band"]["x-compat-accepted"] = dict(_DECL)  # accepts YOK
        found = _run(tmp_path, doc)
        assert found[0]["severity"] == "BREAKING"

    def test_opt_in_for_a_different_type_does_not_leak(self, tmp_path: Path) -> None:
        doc = _old()
        doc["required"] = ["band"]
        doc["properties"]["band"]["x-compat-accepted"] = {
            **_DECL,
            "accepts": ["PATTERN_TIGHTENED"],
        }
        assert _run(tmp_path, doc)[0]["severity"] == "BREAKING"

    def test_required_field_without_a_property_node_cannot_be_declared(
        self, tmp_path: Path
    ) -> None:
        """Taşıyıcı düğüm yoksa indirme de yok — olmayan bir yere beyan yapıştırılamaz."""
        doc = {
            "type": "object",
            "required": ["hayalet"],
            "properties": {"band": {"type": "string"}},
        }
        found = _run(tmp_path, doc)
        assert [c for c in found if c["field"].endswith("hayalet")][0]["severity"] == "BREAKING"


class TestExistingTighteningPathIsUnchanged:
    """Geriye uyum: eski beyanlar (opt-in'siz) daraltmalarda AYNEN çalışmalı."""

    def test_pattern_tightening_still_downgrades_without_opt_in(self, tmp_path: Path) -> None:
        old_dir, new_dir = tmp_path / "old", tmp_path / "new"
        _write(
            old_dir, "p.v1.schema.json", {"type": "object", "properties": {"a": {"type": "string"}}}
        )
        _write(
            new_dir,
            "p.v1.schema.json",
            {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "string",
                        "pattern": "^x",
                        "x-compat-accepted": dict(_DECL),  # accepts YOK -- olmamali da
                    }
                },
            },
        )
        mod = _detector_module()
        det = mod.BreakingChangeDetector(old_dir, new_dir)
        det.scan_tree(old_dir, new_dir)
        tightenings = [c for c in det.changes if c["type"] == "PATTERN_TIGHTENED"]
        assert tightenings, "onkosul: pattern daraltmasi bulunmali"
        assert all(
            c["severity"] == "NON_BREAKING" for c in tightenings
        ), "eski beyanlar bozuldu -- AK-11 geriye uyumu kirmis"


class TestTheTypeIsActuallyWiredIn:
    def test_field_made_required_is_in_acceptable_types(self) -> None:
        mod = _detector_module()
        assert "FIELD_MADE_REQUIRED" in mod.ACCEPTABLE_TYPES

    def test_field_made_required_requires_explicit_opt_in(self) -> None:
        mod = _detector_module()
        assert "FIELD_MADE_REQUIRED" in mod.EXPLICIT_OPT_IN_TYPES


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
