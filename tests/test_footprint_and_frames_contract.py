"""D7 (Ç7 tek hamle) — kare seçimi, izdüşüm ve CRS sözleşmesinin kapısı.

NEDEN (2026-07-31, 10-disiplin denetimi · Ç7 tartışma sonucu):
    `raw_frames[].footprint_wkt` dört disiplinin AYNI boşlukta buluştuğu alandı (Y2):

      * **E7 (edge):** 5.000 karelik izdüşüm listesi = tam uçuş rotası (HC-02/HC-08);
        `priority_zones.geom`'da bulunan "asla atomik GPS değil" uyarısı burada YOKTU.
      * **K7 (KVKK):** 35 m'de bir kare ~42×31 m; uçuş dönüşleri KOMŞU PARSELE taşar →
        üçüncü kişi verisi, hukuki sebep yok (KVKK md.5). Risk tartışmada ORTA→YÜKSEK.
      * **G2 (GIS):** izdüşümü doğrulamak için gereken GPS/irtifa/yaw/GSD şemada YOK →
        değer denetlenemez; "kanıt" değil "iddia".
      * **P3 (pentest):** sınırsız dize = DoS yüzeyi.

    Tartışmada G ve K, E'nin önerisini kabul etti: alan **kaldırıldı**, yerine tüketicinin
    gerçekten ihtiyaç duyduğu soru kondu — *"bu kare hangi işaretli yamayı görüyor?"*
    (`sees_patch_ids[]`). Alanın hiç üreticisi olmadığı için (E11 yazılmadı) kaldırma
    breaking değildir; pencere BU TURDA açıktı.

    Ayrıca G1 (KRİTİK): `observed_footprint_wkt` KR-065 **ödeme** girdisiydi ama CRS
    kanalı yoktu. CRS uyuşmazlığında kesişim ~0 → `coverage_ratio=0.0` → "TEKRAR UÇUŞ" →
    **pilot ödenmez**; ters yönde ise oran ≫1 → `min(...,1.0)` kırpması → "kusursuz
    kapsama" yalanı. Üstelik hata yolu sessizdi (`except → 0.0`).

Bu dosyanın sözleşmesi: her test, kaldırılan/eklenen kısıtlardan BİRİNİN geri gelmesini
ya da sessizce gevşemesini yakalar.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator


ROOT = Path(__file__).parent.parent
EDGE_MANIFEST = ROOT / "schemas" / "edge" / "calibrated_dataset_manifest.v1.schema.json"
INTAKE_MANIFEST = ROOT / "schemas" / "edge" / "intake_manifest.v1.schema.json"

#: Tek üreticinin (edge qc_report_writer.py:157-165) fiilen yazdığı bayraklar.
MEASURED_QC_FLAGS = {
    "blur_detected",
    "overexposure_detected",
    "crs_mismatch",
    "bands_incomplete",
    "low_coverage",
}


def _schema() -> dict:
    return json.loads(EDGE_MANIFEST.read_text(encoding="utf-8"))


def _frame_item() -> dict:
    return _schema()["properties"]["raw_frames"]["items"]


def _calibration_result() -> dict:
    return _schema()["properties"]["calibration_result"]


def _valid_manifest(**overrides: object) -> dict:
    """Şemaya uyan asgari bir manifest (davranış testleri için)."""
    doc = {
        "schema_version": "1.2",
        "dataset_id": "ds_0001",
        "raw_manifest_ref": "manifests/raw/ds_0001.json",
        "calibration_result": {
            "tool_name": "ODM",
            "tool_version": "3.5.4",
            "observed_footprint_wkt": (
                "POLYGON((32.0 37.0, 32.1 37.0, 32.1 37.1, 32.0 37.1, 32.0 37.0))"
            ),
            "calibration_type": "RELATIVE",
        },
        "qc_report": {"pass_warn_fail": "PASS", "coverage_ratio": 0.97, "flags": []},
        "calibrated_at": "2026-07-31T09:00:00Z",
        "tool_name": "ODM",
        "tool_version": "3.5.4",
        "correlation_id": "corr_0123456789abcdef",
    }
    doc.update(overrides)
    return doc


def _errors(doc: dict) -> list:
    return list(Draft202012Validator(_schema()).iter_errors(doc))


class TestFootprintWktIsGone:
    """Kaldırılan alan geri gelmemeli — dört disiplinin ortak kararıydı."""

    def test_raw_frames_has_no_footprint_wkt(self) -> None:
        assert "footprint_wkt" not in _frame_item()["properties"], (
            "raw_frames[].footprint_wkt GERİ GELDİ. Bu alan Ç7'de KALDIRILDI: kare izdüşümü "
            "pratikte atomik GPS'tir (E7/K7 — komşu parsel = üçüncü kişi verisi) ve şemada "
            "GPS/irtifa/yaw/GSD olmadığı için doğrulanamaz (G2). Yerine sees_patch_ids kullanın."
        )

    def test_no_frame_level_geometry_leaks_back_under_another_name(self) -> None:
        """Aynı bilgi başka adla dönmesin (wkt/geom/lat/lon/footprint...)."""
        forbidden = re.compile(r"wkt|geom|latitude|longitude|\blat\b|\blon\b|gps", re.I)
        leaked = [name for name in _frame_item()["properties"] if forbidden.search(name)]
        assert not leaked, (
            f"raw_frames[] içinde kare-düzeyi konum alanı belirdi: {leaked}. "
            "HC-02/HC-08: kare düzeyinde konum taşınmaz."
        )


class TestSeesPatchIds:
    def test_is_required_because_it_is_the_only_reason_to_list_a_frame(self) -> None:
        item = _frame_item()
        assert "sees_patch_ids" in item["required"], (
            "KG-0.c: bir kare listeye YALNIZ işaretli bir yamayı gördüğü için girer; "
            "gerekçesiz kare listelenemez."
        )

    def test_bounds_match_priority_zones(self) -> None:
        field = _frame_item()["properties"]["sees_patch_ids"]
        assert field["minItems"] == 1, "boş liste anlamsız (kare neden listede?)"
        assert field["maxItems"] == 500, (
            "üst sınır priority_zones ile aynı olmalı — bir kare, tarladaki yama "
            "sayısından fazlasını göremez"
        )

    def test_patch_id_vocabulary_matches_intake_manifest(self) -> None:
        """Çapraz-şema değişmez: aynı kimlik iki şemada aynı desenle tanımlanmalı."""
        mine = _frame_item()["properties"]["sees_patch_ids"]["items"]["pattern"]
        intake = json.loads(INTAKE_MANIFEST.read_text(encoding="utf-8"))
        theirs = (
            intake["$defs"]["PlatformForm"]["properties"]["priority_zones"]["items"]
            ["properties"]["patch_id"]["pattern"]
        )
        assert mine == theirs, (
            f"patch_id vocabulary'si ayrıştı: raw_frames {mine!r} vs priority_zones {theirs!r}. "
            "İkisi AYNI kimliği gösteriyor; desen tek olmalı."
        )

    @pytest.mark.parametrize(
        ("patch_id", "valid"),
        [
            ("0123456789abcdef0123456789abcdef", True),
            ("0123456789ABCDEF0123456789ABCDEF", False),  # büyük harf: UUID hex küçük harftir
            ("0123456789abcdef", False),  # kısa
            ("../../etc/passwd", False),  # traversal denemesi
        ],
    )
    def test_patch_id_pattern_behavior(self, patch_id: str, valid: bool) -> None:
        doc = _valid_manifest(raw_frames=[{
            "frame_id": "DJI_0001",
            "relative_path": "frames/DJI_0001.TIF",
            "sees_patch_ids": [patch_id],
        }])
        assert (not _errors(doc)) is valid


class TestObservedFootprintWkt:
    """G1 — KR-065 ödeme girdisi; CRS kanalı + derece ayırıcısı."""

    @pytest.mark.parametrize(
        ("wkt", "valid", "label"),
        [
            ("POLYGON((32.0 37.0, 32.1 37.0, 32.1 37.1, 32.0 37.1, 32.0 37.0))", True,
             "derece — edge fixture'ının birebir hâli"),
            ("POLYGON((32.123456 37.987654, 32.2 37.0, 32.2 37.2, 32.123456 37.987654))", True,
             "yüksek ondalık hassasiyet kısıtlanmaz"),
            ("MULTIPOLYGON(((32 37, 32.1 37, 32.1 37.1, 32 37)))", True, "multipolygon"),
            ("POLYGON((-32.5 -37.5, -32.4 -37.5, -32.4 -37.4, -32.5 -37.5))", True,
             "negatif derece"),
            ("POLYGON((500000.0 4000000.0, 500100.0 4000000.0, 500100.0 4000100.0, "
             "500000.0 4000000.0))", False, "UTM metre — G1 senaryosu"),
            ("SRID=4326;POLYGON((32.0 37.0, 32.1 37.0, 32.1 37.1, 32.0 37.0))", False,
             "EWKT — shapely.wkt.loads'u kırıyor (ölçüldü)"),
            ("POINT(32.0 37.0)", False, "nokta bir kapsama alanı değildir"),
            ("POLYGON((1000.0 37.0, 32.1 37.0, 32.1 37.1, 1000.0 37.0))", False,
             "|koordinat| > 180 ⇒ derece olamaz"),
        ],
    )
    def test_wkt_discriminator(self, wkt: str, valid: bool, label: str) -> None:
        doc = _valid_manifest()
        doc["calibration_result"]["observed_footprint_wkt"] = wkt
        assert (not _errors(doc)) is valid, label

    def test_max_length_bound_exists(self) -> None:
        field = _calibration_result()["properties"]["observed_footprint_wkt"]
        assert field.get("maxLength") == 4096, "P3/K7: sınırsız dize DoS yüzeyidir"

    def test_footprint_crs_channel_exists(self) -> None:
        field = _calibration_result()["properties"].get("footprint_crs")
        assert field is not None, "G1'in kök nedeni: CRS kanalı hiç yoktu"
        assert field.get("const") == "EPSG:4326"

    def test_footprint_crs_rejects_other_values(self) -> None:
        doc = _valid_manifest()
        doc["calibration_result"]["footprint_crs"] = "EPSG:32637"  # UTM 37N
        assert _errors(doc), "CRS beyanı EPSG:4326 dışında bir değeri kabul etmemeli"


class TestQcFlagVocabulary:
    """`crs_mismatch` artık makine-okunur (D7: 'bayrak bağlanır')."""

    def test_flags_are_a_closed_vocabulary(self) -> None:
        items = _schema()["properties"]["qc_report"]["properties"]["flags"]["items"]
        assert set(items["enum"]) == MEASURED_QC_FLAGS, (
            "Bayrak vocabulary'si üreticiden (edge qc_report_writer.py:157-165) ayrıştı. "
            "Üretici yeni bayrak yazıyorsa enum'a EKLEYİN (MINOR); listeyi serbest dizeye "
            "geri çevirmek crs_mismatch'i yeniden görünmez yapar."
        )

    def test_crs_mismatch_is_in_the_vocabulary(self) -> None:
        items = _schema()["properties"]["qc_report"]["properties"]["flags"]["items"]
        assert "crs_mismatch" in items["enum"]

    def test_unknown_flag_is_rejected(self) -> None:
        doc = _valid_manifest()
        doc["qc_report"]["flags"] = ["totally_new_flag"]
        assert _errors(doc), "kapalı vocabulary bilinmeyen bayrağı reddetmeli"


class TestAcceptedTighteningDeclarations:
    """`x-compat-accepted` bir BEYANDIR — boş kaşe olamaz.

    Dedektör bu beyanı gördüğünde daraltmayı NON_BREAKING'e indirir; bu yüzden beyanın
    kendisi denetlenebilir olmalı (ne değişti · ne zaman · neden · hangi karara dayanıyor).
    """

    REQUIRED_KEYS = ("change", "date", "rationale", "ref")

    def _declarations(self) -> list[tuple[str, dict]]:
        found: list[tuple[str, dict]] = []
        for path in list((ROOT / "schemas").rglob("*.json")) + list((ROOT / "enums").glob("*.json")):
            doc = json.loads(path.read_text(encoding="utf-8"))

            def walk(node: object, where: str) -> None:
                if isinstance(node, dict):
                    for key, value in node.items():
                        if key == "x-compat-accepted":
                            found.append((f"{path.name}:{where}", value))
                        walk(value, f"{where}.{key}")
                elif isinstance(node, list):
                    for index, item in enumerate(node):
                        walk(item, f"{where}[{index}]")

            walk(doc, "")
        return found

    def test_every_declaration_is_complete(self) -> None:
        for where, declaration in self._declarations():
            assert isinstance(declaration, dict), f"{where}: beyan nesne olmalı"
            missing = [k for k in self.REQUIRED_KEYS if not str(declaration.get(k, "")).strip()]
            assert not missing, f"{where}: beyanda eksik alan(lar): {missing}"

    def test_rationale_is_not_a_rubber_stamp(self) -> None:
        for where, declaration in self._declarations():
            rationale = str(declaration.get("rationale", ""))
            assert len(rationale) >= 80, (
                f"{where}: gerekçe çok kısa ({len(rationale)} karakter). Beyan, ÖLÇÜME "
                "dayanmalı (ör. 'üretici yok, kanıt: dosya:satır')."
            )

    def test_declarations_exist_where_we_tightened(self) -> None:
        """D7'nin üç daraltması beyanlı olmalı — sessiz daraltma kalmasın."""
        places = {where for where, _ in self._declarations()}
        assert any("observed_footprint_wkt" in p for p in places)
        assert any("flags" in p for p in places)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])


class TestGeoJsonCoordinateBounds:
    """G3/G4 (KADEME 5) — `geom` artık DERECE dışını reddediyor.

    Ölçüldü (2026-07-31): sınırsız `{"type":"number"}` hâli şunların HEPSİNİ kabul ediyordu —
    UTM METRE koordinatı (`[500000, 4000000]`), enlem 91, boylam −181. Yanlış CRS'teki bir
    poligon sözleşmeden sessizce geçiyor, ardından `ST_SetSRID(..., 4326)` onu **yanlış CRS
    ile damgalıyordu** (G4). Bu, D7'de `observed_footprint_wkt` için konan derece
    ayırıcısının GeoJSON karşılığıdır — aynı kural, aynı gerekçe, iki farklı gösterim.

    ⚠️ Şemanın ZORLAYAMADIKLARI ayrıca test ediliyor (aşağıda): kapanış, kendini kesme ve
    halka yönü JSON Schema ile ifade EDİLEMEZ; kapı bunları gördüğünü iddia etmemelidir.
    """

    @staticmethod
    def _geom_validator(form: str) -> "Draft202012Validator":
        schema = json.loads(
            (ROOT / "schemas" / "edge" / "intake_manifest.v1.schema.json").read_text(
                encoding="utf-8"
            )
        )
        geom = schema["$defs"][form]["properties"]["priority_zones"]["items"]["properties"]["geom"]
        return Draft202012Validator(geom)

    @pytest.mark.parametrize("form", ["EdgeForm", "PlatformForm"])
    @pytest.mark.parametrize(
        ("label", "ring", "valid"),
        [
            ("WGS84 derece", [[32.0, 37.0], [32.1, 37.0], [32.1, 37.1], [32.0, 37.0]], True),
            ("yükseklikli üçlü", [[32.0, 37.0, 850], [32.1, 37.0, 850], [32.1, 37.1, 850],
                                  [32.0, 37.0, 850]], True),
            ("UTM metre", [[500000, 4000000], [500100, 4000000], [500100, 4000100],
                           [500000, 4000000]], False),
            ("enlem 91", [[32.0, 91.0], [32.1, 91.0], [32.1, 91.1], [32.0, 91.0]], False),
            ("boylam -181", [[-181.0, 37.0], [32.1, 37.0], [32.1, 37.1], [-181.0, 37.0]], False),
        ],
    )
    def test_coordinate_bounds(self, form: str, label: str, ring: list, valid: bool) -> None:
        document = {"type": "Polygon", "coordinates": [ring]}
        errors = list(self._geom_validator(form).iter_errors(document))
        assert (not errors) is valid, f"{form} / {label}"

    @pytest.mark.parametrize("form", ["EdgeForm", "PlatformForm"])
    def test_lon_lat_order_is_documented(self, form: str) -> None:
        """RFC 7946 sırası [boylam, enlem] — ters yazım sessiz hata kaynağıdır."""
        schema = json.loads(
            (ROOT / "schemas" / "edge" / "intake_manifest.v1.schema.json").read_text(
                encoding="utf-8"
            )
        )
        coord = (schema["$defs"][form]["properties"]["priority_zones"]["items"]
                 ["properties"]["geom"]["properties"]["coordinates"]["items"]["items"])
        assert coord["prefixItems"][0]["maximum"] == 180, "ilk eleman BOYLAM olmalı (±180)"
        assert coord["prefixItems"][1]["maximum"] == 90, "ikinci eleman ENLEM olmalı (±90)"

    def test_schema_does_not_claim_to_validate_topology(self) -> None:
        """Kapının GÖRMEDİĞİ şeyler AÇIKÇA yazılı olmalı (aşırı iddia etmesin).

        Kapanmamış halka ve papyon (bowtie) JSON Schema ile ifade edilemez; bu belge
        şemada yazılı değilse tüketici kapının bunları gördüğünü sanır.
        """
        schema = json.loads(
            (ROOT / "schemas" / "edge" / "intake_manifest.v1.schema.json").read_text(
                encoding="utf-8"
            )
        )
        coord = (schema["$defs"]["PlatformForm"]["properties"]["priority_zones"]["items"]
                 ["properties"]["geom"]["properties"]["coordinates"]["items"]["items"])
        text = coord["description"]
        for needle in ("KAPANIŞ", "KESEN", "ST_IsValid"):
            assert needle in text, f"şemanın sınırı yazılı değil: {needle}"

    def test_unclosed_and_bowtie_still_pass_by_design(self) -> None:
        """Bilinen sınırın REGRESYON kaydı: bunlar şemadan geçer, tüketici yakalamalı."""
        validator = self._geom_validator("PlatformForm")
        unclosed = {"type": "Polygon",
                    "coordinates": [[[32.0, 37.0], [32.1, 37.0], [32.1, 37.1], [32.05, 37.05]]]}
        bowtie = {"type": "Polygon",
                  "coordinates": [[[0, 0], [1, 1], [1, 0], [0, 1], [0, 0]]]}
        assert not list(validator.iter_errors(unclosed)), (
            "kapanmamış halka artık şemadan geçmiyor — güzel; bu testi ve şemadaki "
            "'zorlayamadıklarım' notunu güncelleyin"
        )
        assert not list(validator.iter_errors(bowtie)), (
            "papyon artık şemadan geçmiyor — bu testi ve notu güncelleyin"
        )
