"""C2′ — `intake_manifest.v1` iki-form ayrımı ve `object_key` sahipliği.

Neden bu test var (2026-07-31):
    C2′, `PlatformForm`'a `priority_zones` ekledi. Bu şemanın kökü bir **`oneOf`**'tur ve
    `PlatformForm.required` ⊂ `EdgeForm.required` olduğu için ayrım `required` ile yapılmıyor.

    Ayrım ÖLÇÜLDÜ (2026-07-31) — **üç bağımsız katman** var, tek bir alana dayanmıyor:
      1. `unevaluatedProperties: false` — EdgeForm'un `schema_version` / `drone_make` /
         `correlation_id` alanları PlatformForm'da tanımlı değil
      2. **Kimlik biçimleri** — PlatformForm entity-önekli id ister
         (`^batch_[a-z0-9]{24}$`, `^field_…`, `^mission_…`); EdgeForm `BATCH_YYYYMMDD_…` + ham UUID
      3. **`files[]` şekli** — PlatformForm `sha256_hash` ister, EdgeForm `sha256` verir

    ⇒ Ayrım beklediğimden **sağlam**; yine de PlatformForm'a alan eklemek onu bulandırabileceği
    için bu dosya, iki örneğin hâlâ TAM OLARAK bir dala uyduğunu gerçek yüklerle doğrular.
    Ayrıca `object_key` sahipliği kuralını (KG-0.a-EK kural 1: anahtarı PLATFORM üretir)
    desen düzeyinde bağlar.

    `object_key` deseni bilinçli olarak tenant/dataset **biçimini dondurmaz**; yalnız
    güvenlik-anlamlı **yapıyı** zorlar: mutlak yol yok · `..` yok · `/patches/` öncesi en az
    iki segment (bu sonuncusu edge'in `patches/<id>/…` göreli yolunun anahtar olarak
    sızmasını engeller).
"""

import json
from pathlib import Path

import pytest

try:
    from jsonschema import Draft202012Validator  # type: ignore[import-untyped]
    from referencing import Registry, Resource  # type: ignore[import-untyped]
except ImportError:  # pragma: no cover
    pytest.skip("jsonschema or referencing not installed", allow_module_level=True)

ROOT = Path(__file__).parent.parent
SCHEMA_PATH = ROOT / "schemas" / "edge" / "intake_manifest.v1.schema.json"
EDGE_EXAMPLE = ROOT / "docs" / "examples" / "intake_manifest_edge.example.json"
PLATFORM_EXAMPLE = ROOT / "docs" / "examples" / "intake_manifest.example.json"

PATCH_ID = "a" * 32
DATASET_ID = "b" * 32
TENANT = "gap-diyarbakir"


def _schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def _registry() -> "Registry":
    """Yerel `$id` → kaynak kaydı (şema göreli `$ref`'ler kullanıyor)."""
    registry = Registry()
    for search_dir in (ROOT / "schemas", ROOT / "enums"):
        for json_file in search_dir.rglob("*.json"):
            try:
                contents = json.loads(json_file.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            if isinstance(contents, dict) and contents.get("$id"):
                registry = registry.with_resource(
                    contents["$id"], Resource.from_contents(contents)
                )
    return registry


def _validator() -> "Draft202012Validator":
    return Draft202012Validator(_schema(), registry=_registry())


def _branch_matches(payload: dict) -> list[str]:
    """Yükün `oneOf` dallarından hangilerine uyduğunu döndür.

    Dal şeması, kökün `$id`'siyle AYNI DİZİN altında sahte bir `$id` alır — böylece
    göreli `$ref`'ler (`../../enums/...`) kökle birebir aynı biçimde çözülür.
    (İlk yazımda `$id` düşürülmüştü ve tüm testler çözümleme hatasıyla düşmüştü.)
    """
    schema = _schema()
    base = schema["$id"].rsplit("/", 1)[0]
    registry = _registry()
    matched = []
    for name in ("PlatformForm", "EdgeForm"):
        sub = {
            "$schema": schema["$schema"],
            "$id": f"{base}/_branch_{name}.json",
            "$ref": f"#/$defs/{name}",
            "$defs": schema["$defs"],
        }
        if Draft202012Validator(sub, registry=registry).is_valid(payload):
            matched.append(name)
    return matched


def _zone(visualizations: dict | None) -> dict:
    zone = {
        "patch_id": PATCH_ID,
        "geom": {
            "type": "Polygon",
            "coordinates": [[[40.0, 37.0], [40.1, 37.0], [40.1, 37.1], [40.0, 37.0]]],
        },
        "priority_level": "EXPRESS",
        "ndvi_value": 0.21,
        "sampling_reason": "NDVI_THRESHOLD",
    }
    if visualizations is not None:
        zone["visualizations"] = visualizations
    return zone


def _edge_viz() -> dict:
    return {
        "true_color": f"patches/{PATCH_ID}/true_color.jpg",
        "false_color": f"patches/{PATCH_ID}/false_color.jpg",
        "ndvi_overlay": f"patches/{PATCH_ID}/ndvi_overlay.png",
    }


def _platform_viz(prefix: str | None = None) -> dict:
    base = prefix or f"{TENANT}/{DATASET_ID}/patches/{PATCH_ID}"
    return {
        "true_color": f"{base}/true_color.jpg",
        "false_color": f"{base}/false_color.jpg",
        "ndvi_overlay": f"{base}/ndvi_overlay.png",
    }


class TestOneOfDiscriminationSurvivesC2Prime:
    """C2′ regresyon kapısı: iki form hâlâ TAM OLARAK bir dala uymalı."""

    def test_edge_example_matches_exactly_edge_form(self) -> None:
        payload = json.loads(EDGE_EXAMPLE.read_text(encoding="utf-8"))
        assert _branch_matches(payload) == ["EdgeForm"]
        _validator().validate(payload)

    def test_platform_example_matches_exactly_platform_form(self) -> None:
        payload = json.loads(PLATFORM_EXAMPLE.read_text(encoding="utf-8"))
        assert _branch_matches(payload) == ["PlatformForm"]
        _validator().validate(payload)

    def test_edge_payload_with_priority_zones_still_only_edge(self) -> None:
        """C2′'nin ana riski: PlatformForm'a priority_zones eklenince ayrım bulanabilirdi."""
        payload = json.loads(EDGE_EXAMPLE.read_text(encoding="utf-8"))
        payload["priority_zones"] = [_zone(_edge_viz())]
        assert _branch_matches(payload) == ["EdgeForm"], (
            "EdgeForm yükü artık PlatformForm'a da uyuyor — oneOf ayrımı bozuldu"
        )
        _validator().validate(payload)

    def test_platform_payload_with_object_keys_only_platform(self) -> None:
        payload = json.loads(PLATFORM_EXAMPLE.read_text(encoding="utf-8"))
        payload["priority_zones"] = [_zone(_platform_viz())]
        assert _branch_matches(payload) == ["PlatformForm"]
        _validator().validate(payload)


class TestObjectKeyOwnership:
    """KG-0.a-EK kural 1: anahtarı PLATFORM üretir; edge'in yolu anahtar olamaz."""

    def test_edge_relative_path_is_rejected_as_object_key(self) -> None:
        """Edge'in göreli yolu PlatformForm'a anahtar olarak SIZAMAZ."""
        payload = json.loads(PLATFORM_EXAMPLE.read_text(encoding="utf-8"))
        payload["priority_zones"] = [_zone(_edge_viz())]  # goreli yol
        assert not _validator().is_valid(payload), (
            "Edge göreli yolu object_key olarak kabul edildi — KG-0.a-EK kural 1 ihlali "
            "(çapraz-dataset okuma yüzeyi geri açılır)"
        )

    @pytest.mark.parametrize(
        "bad_prefix",
        [
            f"../{TENANT}/{DATASET_ID}/patches/{PATCH_ID}",  # traversal
            f"/{TENANT}/{DATASET_ID}/patches/{PATCH_ID}",  # mutlak yol
            f"{TENANT}/{DATASET_ID}/raw/{PATCH_ID}",  # yanlis kapsam (raw)
            f"{DATASET_ID}/patches/{PATCH_ID}",  # tek segment: tenant yok
            f"t/../{DATASET_ID}/patches/{PATCH_ID}",  # ic traversal
        ],
        ids=["traversal", "absolute", "wrong-scope", "no-tenant", "inner-traversal"],
    )
    def test_malformed_keys_are_rejected(self, bad_prefix: str) -> None:
        payload = json.loads(PLATFORM_EXAMPLE.read_text(encoding="utf-8"))
        payload["priority_zones"] = [_zone(_platform_viz(bad_prefix))]
        assert not _validator().is_valid(payload), f"kabul edilmemeliydi: {bad_prefix}"

    def test_wellformed_key_is_accepted(self) -> None:
        payload = json.loads(PLATFORM_EXAMPLE.read_text(encoding="utf-8"))
        payload["priority_zones"] = [_zone(_platform_viz())]
        _validator().validate(payload)


class TestEdgeFormRemainsBackwardCompatible:
    """C2′ non-breaking olmalı: edge bugünkü yükünü göndermeye devam edebilmeli."""

    def test_edge_relative_paths_still_valid_in_edge_form(self) -> None:
        payload = json.loads(EDGE_EXAMPLE.read_text(encoding="utf-8"))
        payload["priority_zones"] = [_zone(_edge_viz())]
        _validator().validate(payload)

    def test_priority_zones_stays_optional_in_both_forms(self) -> None:
        schema = _schema()
        for name in ("EdgeForm", "PlatformForm"):
            assert "priority_zones" not in schema["$defs"][name]["required"], (
                f"{name}: priority_zones zorunlu yapılamaz — MAJOR breaking olurdu"
            )

    def test_edge_form_visualizations_documents_it_is_not_a_key(self) -> None:
        """Göreli yolun 'anahtar değildir' uyarısı korunmalı (yanlış kullanım geri gelmesin)."""
        schema = _schema()
        viz = schema["$defs"]["EdgeForm"]["properties"]["priority_zones"]["items"][
            "properties"
        ]["visualizations"]
        assert "anahtar" in viz["description"].lower()
        assert "KG-0.a-EK" in viz["description"]


class TestBothFormsCarryTheSameZoneData:
    """İki form aynı bölgeyi anlatmalı; yalnız görsel referansı farklı olmalı."""

    def test_zone_fields_match_except_visualizations(self) -> None:
        schema = _schema()
        e = schema["$defs"]["EdgeForm"]["properties"]["priority_zones"]["items"]
        p = schema["$defs"]["PlatformForm"]["properties"]["priority_zones"]["items"]
        assert set(e["properties"]) == set(p["properties"])
        assert e["required"] == p["required"]

    def test_platform_visualizations_are_object_keys_not_paths(self) -> None:
        schema = _schema()
        p = schema["$defs"]["PlatformForm"]["properties"]["priority_zones"]["items"][
            "properties"
        ]["visualizations"]["properties"]
        for name in ("true_color", "false_color", "ndvi_overlay"):
            pattern = p[name]["pattern"]
            assert "/patches/" in pattern, f"{name}: desen patches kapsamını zorlamalı"
            assert not pattern.startswith("^patches/"), (
                f"{name}: edge göreli yol deseni platform formuna kopyalanmış"
            )
            # '.' segmentlerde yasak olmalı — aksi hâlde '..' traversal geçer
            assert "[A-Za-z0-9_-]" in pattern, (
                f"{name}: segment sınıfı '.' içeriyor olabilir → '..' traversal riski"
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
