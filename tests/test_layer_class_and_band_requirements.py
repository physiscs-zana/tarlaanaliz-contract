"""D9 (Ç5 zinciri) — `layer_type` sınıflandırması + bant gereksinimi kapısı.

NEDEN (2026-07-31, 10-disiplin denetimi · yakınsama Y4 = A8/A10 + S10/S11):
    `layer_type` düz bir enum'du ve içinde ÜÇ FARKLI türden şey vardı: fotogrametri
    ürünü (ORTHO/DSM), spektral indeks (NDVI…), görselleştirme kompoziti (CIR) ve
    termal türetilmiş büyüklük (CWSI…). "Bu katman bu drone ile üretilebilir mi?"
    sorusunun makine-okunur cevabı YOKTU → 4 bantlı bir drone için `CWSI` (LWIR ister)
    ya da `EVI` (BLUE ister) iddia eden bir manifest hiçbir kapıya takılmazdı.

    Ayrıca `IRRIGATION_EFFICIENCY` ölçülemeyen bir şeyi adlandırıyordu: termal kamera
    sulama VERİMLİLİĞİNİ ölçemez (uygulanan su + bitki su tüketimi bilinmeden
    hesaplanamaz, ikisi de sistemde yok). LWIR'den türetilebilen büyüklük kanopi
    sıcaklığının tekdüzeliğidir → `CANOPY_TEMP_UNIFORMITY`.

Bu dosyanın kapıları:
    ① her `layer_type` değerinin bir SINIFI var
    ② matris ile şema aynı vocabulary'yi konuşuyor (drift yok)
    ③ bir drone'un LİSTELEDİĞİ her indeks, o drone'un bantlarıyla ÜRETİLEBİLİR
    ④ eski ad geri gelmiyor
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

yaml = pytest.importorskip("yaml", reason="pyyaml yok")


ROOT = Path(__file__).parent.parent
PLATFORM_FORM = ROOT / "schemas" / "platform" / "calibrated_dataset_manifest.v1.schema.json"
MATRIX = ROOT / "drone_capability_matrix.yaml"

#: Sınıfına göre bant gereksinimi ARANACAK olanlar.
BAND_GATED_CLASSES = {"index", "composite"}


def _schema() -> dict:
    return json.loads(PLATFORM_FORM.read_text(encoding="utf-8"))


def _matrix() -> dict:
    return yaml.safe_load(MATRIX.read_text(encoding="utf-8"))


def _layer_types() -> list[str]:
    return _schema()["$defs"]["file_artifact"]["properties"]["layer_type"]["enum"]


def _classes() -> dict[str, str]:
    return _schema()["x-layer-classes"]["map"]


def _effective_bands(entry: dict) -> set[str]:
    """Drone'un gerçekten sahip olduğu bantlar (termal payload dahil)."""
    bands = set(entry.get("supported_bands", []))
    variant = entry.get("thermal_variant") or {}
    bands |= set(variant.get("thermal_bands", []) or [])
    return bands


def _listed_indices(entry: dict) -> set[str]:
    available = entry.get("available_indices", {}) or {}
    listed = set()
    for group in ("core", "extended", "thermal"):
        listed |= set(available.get(group) or [])
    variant = entry.get("thermal_variant") or {}
    listed |= set(variant.get("thermal_indices") or [])
    return listed


class TestLayerClassification:
    def test_every_layer_type_has_a_class(self) -> None:
        classes = _classes()
        missing = [value for value in _layer_types() if value not in classes]
        assert not missing, (
            f"sınıfsız layer_type değeri: {missing}. Sınıf, üretilebilirlik kapısının "
            "hangi kurala göre işleyeceğini belirler (Y4)."
        )

    def test_class_map_has_no_phantom_values(self) -> None:
        extra = [value for value in _classes() if value not in _layer_types()]
        assert not extra, f"enum'da olmayan değere sınıf atanmış: {extra}"

    def test_classes_are_from_the_declared_vocabulary(self) -> None:
        declared = set(_schema()["x-layer-classes"]["classes"])
        used = set(_classes().values())
        assert used <= declared, f"tanımsız sınıf kullanılmış: {sorted(used - declared)}"

    def test_raster_products_carry_no_band_requirement(self) -> None:
        """ORTHO/DSM bant gerektirmez — onlara gereksinim yazmak sahte kapı üretir."""
        requirements = _matrix()["index_requirements"]
        raster = [v for v, c in _classes().items() if c == "raster_product"]
        offenders = [v for v in raster if v in requirements]
        assert not offenders, (
            f"raster ürününe bant gereksinimi yazılmış: {offenders} — `index_requirements` "
            "yalnız index/composite içindir (D9③)."
        )


class TestVocabularyStaysInSync:
    def test_matrix_indices_are_all_known_layer_types(self) -> None:
        known = set(_layer_types())
        for name, entry in _matrix()["capabilities"].items():
            unknown = _listed_indices(entry) - known
            assert not unknown, (
                f"{name}: matriste layer_type enum'unda olmayan indeks var: {sorted(unknown)}. "
                "İki vocabulary birlikte değişmeli (biri yeniden adlandırılırsa diğeri de)."
            )

    def test_band_gated_layer_types_have_a_requirement_entry(self) -> None:
        requirements = _matrix()["index_requirements"]
        gated = [v for v, c in _classes().items() if c in BAND_GATED_CLASSES]
        missing = [v for v in gated if v not in requirements]
        assert not missing, (
            f"bant-kapılı katmanın gereksinim kaydı yok: {missing}. Kayıt YOKSA kapı, "
            "iddiayı doğrulayamaz."
        )

    def test_undeclared_requirements_are_explicit_open_items(self) -> None:
        """`null` = 'henüz beyan edilmedi'; sessiz eksiklik değil, AÇIK KALEM."""
        requirements = _matrix()["index_requirements"]
        undeclared = [k for k, v in requirements.items() if v is None]
        assert undeclared == ["CHLOROPHYLL_A"], (
            f"beyan edilmemiş gereksinim kümesi değişti: {undeclared}. Yeni bir `null` "
            "eklendiyse eylem planına açık kalem olarak işleyin; kaldırıldıysa bu testi "
            "güncelleyin."
        )
        open_item = _schema()["x-layer-classes"].get("x-open-item", "")
        assert "CHLOROPHYLL_A" in open_item, "açık kalem şemada da yazılı olmalı"


class TestProducibility:
    """③ Bir drone'un LİSTELEDİĞİ indeks, bantlarıyla ÜRETİLEBİLİR olmalı."""

    def test_listed_indices_are_producible(self) -> None:
        requirements = _matrix()["index_requirements"]
        classes = _classes()
        violations: list[str] = []
        for name, entry in _matrix()["capabilities"].items():
            bands = _effective_bands(entry)
            for index in sorted(_listed_indices(entry)):
                needed = requirements.get(index)
                if needed is None:  # beyan edilmemiş (açık kalem) veya termal metrik
                    if classes.get(index) in BAND_GATED_CLASSES and index not in requirements:
                        violations.append(f"{name}: {index} için gereksinim kaydı yok")
                    continue
                missing = set(needed) - bands
                if missing:
                    violations.append(
                        f"{name}: {index} listelenmiş ama {sorted(missing)} bandı yok "
                        f"(mevcut: {sorted(bands)})"
                    )
        assert not violations, "İMKÂNSIZ indeks iddiası:\n  " + "\n  ".join(violations)

    def test_thermal_metrics_require_lwir(self) -> None:
        """Termal türetilmiş büyüklükler yalnız LWIR taşıyan (veya payload'lı) drone'da."""
        classes = _classes()
        violations = []
        for name, entry in _matrix()["capabilities"].items():
            bands = _effective_bands(entry)
            thermal_listed = {i for i in _listed_indices(entry)
                              if classes.get(i) == "derived_metric"}
            if thermal_listed and "LWIR" not in bands:
                violations.append(f"{name}: {sorted(thermal_listed)} var ama LWIR yok")
        assert not violations, "LWIR'siz termal metrik iddiası:\n  " + "\n  ".join(violations)

    def test_savi_is_producible_on_four_band_drones(self) -> None:
        """Ölçümün somut sonucu: SAVI Blue GEREKTİRMEZ (worker formülü).

        Bu testin işi SAVI'yi `core`'a taşımak DEĞİL (o bir ürün kararıdır) — mekanizmanın
        gerçeği söylediğini sabitlemektir: 4 bantlı bir drone SAVI üretebilir.
        """
        requirements = _matrix()["index_requirements"]
        assert set(requirements["SAVI"]) == {"RED", "NIR"}
        basic = _matrix()["capabilities"]["DJI_MAVIC_3M"]
        assert set(requirements["SAVI"]) <= _effective_bands(basic)

    def test_evi_needs_blue(self) -> None:
        """Karşı örnek: EVI Blue ister; 4 bantlı drone üretemez (kod: B yoksa sıfırlanır)."""
        requirements = _matrix()["index_requirements"]
        assert "BLUE" in requirements["EVI"]
        basic = _matrix()["capabilities"]["DJI_MAVIC_3M"]
        assert not set(requirements["EVI"]) <= _effective_bands(basic)


class TestRenameIsComplete:
    """④ Ölçülemeyen ad geri gelmesin."""

    OLD = "IRRIGATION_EFFICIENCY"
    NEW = "CANOPY_TEMP_UNIFORMITY"

    def test_new_name_is_canonical(self) -> None:
        assert self.NEW in _layer_types()
        assert self.OLD not in _layer_types()

    def test_old_name_is_gone_from_every_value_position(self) -> None:
        """Eski ad hiçbir DEĞER konumunda kalmamalı.

        ⚠️ Kapı METİN değil DEĞER tarar. Açıklamalardaki *"şu addan yeniden
        adlandırıldı"* notu kalmalıdır — değişikliğin gerekçesini silmek, bir sonraki
        oturumun aynı adı "eksik" sanıp geri koymasına davetiyedir. Yasak olan, adın
        yeniden bir `enum`/`const`/matris listesine GİRMESİDİR.
        """
        offenders: list[str] = []

        for path in list((ROOT / "schemas").rglob("*.json")) + list((ROOT / "enums").glob("*.json")):
            doc = json.loads(path.read_text(encoding="utf-8"))
            where = str(path.relative_to(ROOT)).replace("\\", "/")

            def walk(node: object, trail: str) -> None:
                if isinstance(node, dict):
                    for key, value in node.items():
                        if key in ("enum", "const"):
                            values = value if isinstance(value, list) else [value]
                            if self.OLD in [v for v in values if isinstance(v, str)]:
                                offenders.append(f"{where}:{trail}.{key}")
                        if key == "map" and isinstance(value, dict) and self.OLD in value:
                            offenders.append(f"{where}:{trail}.map")
                        walk(value, f"{trail}.{key}")
                elif isinstance(node, list):
                    for index, item in enumerate(node):
                        walk(item, f"{trail}[{index}]")

            walk(doc, "")

        matrix = _matrix()
        for name, entry in matrix["capabilities"].items():
            if self.OLD in _listed_indices(entry):
                offenders.append(f"drone_capability_matrix.yaml:capabilities.{name}")
        if self.OLD in matrix.get("index_requirements", {}):
            offenders.append("drone_capability_matrix.yaml:index_requirements")

        assert not offenders, (
            f"{self.OLD} bir DEĞER olarak geri gelmiş: {offenders}. Termal kamera sulama "
            "VERİMLİLİĞİNİ ölçemez (uygulanan su + bitki su tüketimi gerekir, ikisi de yok); "
            f"ölçülebilen büyüklük {self.NEW}'dir."
        )

    def test_rename_rationale_stays_documented(self) -> None:
        """Gerekçe metni SİLİNMEMELİ — 'neden' kaybolursa ad geri gelir."""
        text = PLATFORM_FORM.read_text(encoding="utf-8")
        assert self.OLD in text and self.NEW in text, (
            "yeniden adlandırmanın gerekçesi açıklamadan silinmiş; tarihsel not kalmalı"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
