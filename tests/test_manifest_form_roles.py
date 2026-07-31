"""C0 — `calibrated_dataset_manifest.v1` iki-form ayrımının sözleşme testi.

Neden bu test var (2026-07-31 denetimi):
    `calibrated_dataset_manifest.v1.schema.json` **iki ayrı dosyadır** ve yalnız dizinle
    ayrılır (`schemas/edge/` vs `schemas/platform/`). İkisinin de description'ında
    karşılıklı prose atıf VARDI, ama bu bir plan turunun üç iş kalemini (C1/C2/C3)
    yanlış dosyaya yazmasını **engelleyemedi**: `patches[].object_key` alanı
    "calibrated_dataset_manifest'e eklensin" diye planlandı, oysa o alan hiçbir
    calibrated manifest formunda yok — `intake_manifest.v1` altında.

    Bu test prose'u değil, **makine-okunur `x-form-role` sözleşmesini** doğrular ve
    alanların yanlış forma sızmasını yakalar.
"""

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
EDGE_FORM = ROOT / "schemas" / "edge" / "calibrated_dataset_manifest.v1.schema.json"
PLATFORM_FORM = ROOT / "schemas" / "platform" / "calibrated_dataset_manifest.v1.schema.json"
INTAKE_MANIFEST = ROOT / "schemas" / "edge" / "intake_manifest.v1.schema.json"

REQUIRED_ROLE_KEYS = {
    "role",
    "emitter",
    "purpose",
    "counterpart",
    "owns",
    "not_owned_here",
    "field_placement_rule",
}


def _load(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


class TestCalibratedManifestFormRoles:
    """Her iki form kendi rolünü makine-okunur biçimde ilan eder."""

    @pytest.mark.parametrize("path", [EDGE_FORM, PLATFORM_FORM], ids=["edge", "platform"])
    def test_form_declares_x_form_role(self, path: Path) -> None:
        schema = _load(path)
        role = schema.get("x-form-role")
        assert role is not None, f"{path.name} ({path.parent.name}/) x-form-role bloğu taşımıyor"
        missing = REQUIRED_ROLE_KEYS - set(role)
        assert not missing, f"{path.parent.name}/{path.name} x-form-role eksik anahtar: {missing}"

    def test_roles_are_distinct(self) -> None:
        edge_role = _load(EDGE_FORM)["x-form-role"]["role"]
        platform_role = _load(PLATFORM_FORM)["x-form-role"]["role"]
        assert edge_role == "edge_proof_manifest"
        assert platform_role == "platform_package_aggregate"
        assert edge_role != platform_role, "İki form aynı rolü ilan edemez"

    def test_counterparts_point_at_each_other(self) -> None:
        """counterpart, karşı dosyanın $id'sine BİREBİR eşleşmeli (yeniden adlandırma kırar)."""
        edge, platform = _load(EDGE_FORM), _load(PLATFORM_FORM)
        assert edge["x-form-role"]["counterpart"] == platform["$id"]
        assert platform["x-form-role"]["counterpart"] == edge["$id"]

    def test_owned_fields_actually_exist_in_that_form(self) -> None:
        """`owns` listesi hayalî alan sayamaz — her biri o formun properties'inde olmalı."""
        for path in (EDGE_FORM, PLATFORM_FORM):
            schema = _load(path)
            props = set(schema.get("properties", {}))
            owned = set(schema["x-form-role"]["owns"])
            ghost = owned - props
            assert not ghost, f"{path.parent.name}/{path.name} owns[] var olmayan alan sayıyor: {ghost}"

    def test_owned_fields_do_not_overlap(self) -> None:
        """Bir alanın sahibi tektir; iki form aynı alanı sahiplenemez."""
        edge_owned = set(_load(EDGE_FORM)["x-form-role"]["owns"])
        platform_owned = set(_load(PLATFORM_FORM)["x-form-role"]["owns"])
        overlap = edge_owned & platform_owned
        assert not overlap, f"İki form aynı alanı sahipleniyor: {overlap}"


class TestPatchFieldsStayInIntakeManifest:
    """C2 regresyon kapısı: yama/öncelik-bölgesi alanları calibrated manifest'e SIZMAZ."""

    @pytest.mark.parametrize("path", [EDGE_FORM, PLATFORM_FORM], ids=["edge", "platform"])
    def test_no_patch_fields_in_calibrated_manifest(self, path: Path) -> None:
        props = set(_load(path).get("properties", {}))
        stray = props & {"patches", "priority_zones", "visualizations"}
        assert not stray, (
            f"{path.parent.name}/{path.name} içine {stray} eklenmiş. "
            "Bu alanlar intake_manifest.v1 → EdgeForm.priority_zones'a aittir; "
            "buraya eklemek 2026-07-31'de düzeltilen hatayı geri getirir."
        )

    def test_priority_zones_lives_in_intake_manifest_edge_form(self) -> None:
        """Alanın gerçek evi: yer değiştirirse bu test söyler."""
        defs = _load(INTAKE_MANIFEST)["$defs"]
        assert "priority_zones" in defs["EdgeForm"]["properties"], (
            "priority_zones EdgeForm'dan kayboldu — C2′ hedefi geçersizleşir"
        )

    def test_visualizations_carry_patch_paths(self) -> None:
        """`visualizations` bugün göreli yol taşıyor; C2′ buraya object_key ekleyecek."""
        viz = _load(INTAKE_MANIFEST)["$defs"]["EdgeForm"]["properties"]["priority_zones"]
        payload = json.dumps(viz, ensure_ascii=False)
        assert "ndvi_overlay" in payload, "priority_zones.visualizations.ndvi_overlay bulunamadı"


class TestAnalysisTypeNotProducibleMarkers:
    """C5 (KG-0.f): iki katman 'üretilemez' işaretli KALMALI — sessizce açılmasın."""

    def test_beneficial_and_thermal_stress_remain_not_producible(self) -> None:
        enum_doc = _load(ROOT / "enums" / "analysis_type.enum.v1.json")
        by_layer = enum_doc["metadata"]["bandRequirements"]["byLayer"]
        assert by_layer["BENEFICIAL"]["availability"] == "enum_valid_not_yet_emittable"
        assert by_layer["THERMAL_STRESS"]["availability"] == "requires_thermal_payload"

    def test_both_values_stay_in_enum(self) -> None:
        """'Üretilemez' işareti enum'dan SİLMEK demek değildir (parite korunur)."""
        enum_doc = _load(ROOT / "enums" / "analysis_type.enum.v1.json")
        assert "BENEFICIAL" in enum_doc["enum"]
        assert "THERMAL_STRESS" in enum_doc["enum"]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
