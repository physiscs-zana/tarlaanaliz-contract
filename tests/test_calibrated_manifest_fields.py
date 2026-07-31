"""C1′ + C3′ — kalibre manifest alanları ve KELİME DAĞARCIĞI türetimi.

Neden bu test var (2026-07-31):
    Bu turun tekrar eden hata sınıfı **paralel vocabulary uydurmak**tı. Plan C1′ için
    `layer_type(ortho/ndvi/ndre/**ndwi**)` öneriyordu — oysa kanonik indeks kümesi
    `drone_capability_matrix.yaml → available_indices` altında yaşıyor ve **NDWI orada YOK**.
    Aynı şekilde plan `calibration_tier` diyordu; contract'ta öyle bir ad yok, kanonik ad
    `calibration_type` ve alt-kümeleri `calibration_type.enum.v1 → x-context-subsets`'te.

    Bu testler alanların **var olmasını** değil, **doğru kaynaktan türetilmiş olmasını** zorlar:
    yeni bir indeks/bant/kalibrasyon değeri ancak kanonik kaynakta varsa şemaya girebilir.
"""

import json
from pathlib import Path

import pytest

try:
    import yaml  # type: ignore[import-untyped]
except ImportError:  # pragma: no cover
    pytest.skip("pyyaml yok", allow_module_level=True)

ROOT = Path(__file__).parent.parent
PLATFORM_FORM = ROOT / "schemas" / "platform" / "calibrated_dataset_manifest.v1.schema.json"
EDGE_FORM = ROOT / "schemas" / "edge" / "calibrated_dataset_manifest.v1.schema.json"
INTAKE = ROOT / "schemas" / "edge" / "intake_manifest.v1.schema.json"
CAPABILITY_MATRIX = ROOT / "drone_capability_matrix.yaml"
CALIBRATION_ENUM = ROOT / "enums" / "calibration_type.enum.v1.json"

NON_INDEX_LAYERS = {"ORTHO", "DSM"}


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _matrix_indices() -> set[str]:
    """drone_capability_matrix.yaml'daki TÜM indeks adları (core+extended+thermal)."""
    doc = yaml.safe_load(CAPABILITY_MATRIX.read_text(encoding="utf-8"))
    found: set[str] = set()

    def walk(node: object) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if key == "available_indices" and isinstance(value, dict):
                    for group in value.values():
                        found.update(group or [])
                elif key == "thermal_indices":
                    found.update(value or [])
                else:
                    walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(doc)
    return found


def _canonical_bands() -> set[str]:
    """Kanonik bant kümesi: intake_manifest.available_bands."""
    intake = _load(INTAKE)
    return set(intake["$defs"]["EdgeForm"]["properties"]["available_bands"]["items"]["enum"])


class TestLayerTypeIsDerivedNotInvented:
    """C1′ — `layer_type` indeks değerleri kanonik matristen gelmeli."""

    def test_index_values_all_exist_in_capability_matrix(self) -> None:
        layer_types = set(
            _load(PLATFORM_FORM)["$defs"]["file_artifact"]["properties"]["layer_type"]["enum"]
        )
        invented = layer_types - NON_INDEX_LAYERS - _matrix_indices()
        assert not invented, (
            f"layer_type kanonik olmayan indeks taşıyor: {sorted(invented)}. "
            "İndeks vocabulary'si drone_capability_matrix.yaml → available_indices'tir; "
            "paralel bir liste uydurulamaz (planın önerdiği 'NDWI' bu yüzden ALINMADI)."
        )

    def test_ndwi_is_not_present(self) -> None:
        """Planın önerdiği ama kanonik olmayan değer regresyon kapısı."""
        layer_types = set(
            _load(PLATFORM_FORM)["$defs"]["file_artifact"]["properties"]["layer_type"]["enum"]
        )
        assert "NDWI" not in layer_types and "ndwi" not in layer_types

    def test_core_indices_are_covered(self) -> None:
        """M3M'in ürettiği çekirdek indeksler kapsanmalı, yoksa alan işe yaramaz."""
        layer_types = set(
            _load(PLATFORM_FORM)["$defs"]["file_artifact"]["properties"]["layer_type"]["enum"]
        )
        assert {"NDVI", "NDRE"} <= layer_types

    def test_layer_type_is_optional(self) -> None:
        artifact = _load(PLATFORM_FORM)["$defs"]["file_artifact"]
        assert "layer_type" not in artifact["required"], "MINOR kalmalı; zorunlu yapmak breaking"

    def test_registry_cross_reference_exists(self) -> None:
        """Türetim kaynağı şemada YAZILI olmalı (bir sonraki tur uydurma sanmasın)."""
        doc = _load(PLATFORM_FORM)
        sync = doc.get("x-registry-sync", {})
        assert "drone_capability_matrix" in json.dumps(sync)


class TestBandVocabularyIsShared:
    """`band` alanı kendi listesini uydurmamalı."""

    def test_platform_artifact_band_matches_canonical(self) -> None:
        bands = set(_load(PLATFORM_FORM)["$defs"]["file_artifact"]["properties"]["band"]["enum"])
        assert bands == _canonical_bands()

    def test_raw_frame_band_matches_canonical(self) -> None:
        frames = _load(EDGE_FORM)["properties"]["raw_frames"]["items"]
        assert set(frames["properties"]["band"]["enum"]) == _canonical_bands()


class TestCalibrationTypeUsesCanonicalName:
    """C1′ — `calibration_tier` diye bir alan YOKTUR."""

    def test_field_is_named_calibration_type(self) -> None:
        props = _load(PLATFORM_FORM)["properties"]
        assert "calibration_type" in props
        assert "calibration_tier" not in props

    def test_no_schema_defines_calibration_tier(self) -> None:
        offenders = [
            str(p.relative_to(ROOT)).replace("\\", "/")
            for p in (ROOT / "schemas").rglob("*.json")
            if '"calibration_tier"' in p.read_text(encoding="utf-8")
        ]
        assert not offenders, f"`calibration_tier` alanı tanımlanmış: {offenders}"

    def test_values_are_a_subset_of_canonical_enum(self) -> None:
        canonical = set(_load(CALIBRATION_ENUM)["enum"])
        used = set(_load(PLATFORM_FORM)["properties"]["calibration_type"]["enum"])
        assert used <= canonical, f"kanonik enum dışı değer: {sorted(used - canonical)}"

    def test_context_subset_is_registered_and_matches(self) -> None:
        """Alt-küme enum'da KAYITLI olmalı — C6'da bunun eksikliği 'iş yok' yanılgısı yaratmıştı."""
        subsets = _load(CALIBRATION_ENUM)["x-context-subsets"]
        key = "platform/calibrated_dataset_manifest"
        assert key in subsets, f"{key} alt-kümesi enum'a kaydedilmemiş"
        assert set(subsets[key]) == set(
            _load(PLATFORM_FORM)["properties"]["calibration_type"]["enum"]
        ), "şemadaki enum ile kayıtlı alt-küme ayrışmış"

    def test_none_is_excluded(self) -> None:
        """NONE = KR-018 hard reject; kalibre paket manifesti onu ilan edemez."""
        used = set(_load(PLATFORM_FORM)["properties"]["calibration_type"]["enum"])
        assert "NONE" not in used


class TestRawFramesOwnership:
    """C3′ — ham kareler edge formunda ve object_key TAŞIMAZ."""

    def test_raw_frames_live_in_edge_form_only(self) -> None:
        assert "raw_frames" in _load(EDGE_FORM)["properties"]
        assert "raw_frames" not in _load(PLATFORM_FORM)["properties"]

    def test_raw_frames_carry_no_object_key(self) -> None:
        """KG-0.a-EK kural 1: anahtarı platform üretir; kiosk-emitted form anahtar bildiremez."""
        item = _load(EDGE_FORM)["properties"]["raw_frames"]["items"]
        assert "object_key" not in item["properties"], (
            "raw_frames[].object_key eklenmiş — edge anahtarı ÜRETEMEZ (KG-0.a-EK kural 1); "
            "C2′'de patches için verilen kararla çelişir"
        )

    def test_relative_path_blocks_traversal_and_absolute(self) -> None:
        import re

        pattern = _load(EDGE_FORM)["properties"]["raw_frames"]["items"]["properties"][
            "relative_path"
        ]["pattern"]
        rx = re.compile(pattern)
        assert rx.match("frames/DJI_0001_MS_G.tif")
        assert rx.match("a/b/c/x.tif")
        assert not rx.match("/frames/x.tif"), "mutlak yol kabul edildi"
        assert not rx.match("../frames/x.tif"), "traversal kabul edildi"
        assert not rx.match("a/../b/x.tif"), "iç traversal kabul edildi"

    def test_raw_frames_optional_and_bounded(self) -> None:
        doc = _load(EDGE_FORM)
        assert "raw_frames" not in doc["required"], "zorunlu yapmak MAJOR breaking olurdu"
        assert doc["properties"]["raw_frames"]["maxItems"] > 0, "DoS sınırı yok"

    def test_minimum_provenance_is_required(self) -> None:
        item = _load(EDGE_FORM)["properties"]["raw_frames"]["items"]
        assert set(item["required"]) == {"frame_id", "relative_path"}

    def test_form_role_owns_raw_frames(self) -> None:
        assert "raw_frames" in _load(EDGE_FORM)["x-form-role"]["owns"]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
