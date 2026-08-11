"""AL-C1 + AL-C2 — i.i.d. denetim örneklemi kanalı (ölçüm temeli [0]).

Neden bu test var (2026-07-31):
    Worker'ın `audit_set_sampler` + `propagation_metrics` kodu **landed ama uykuda**; canlıya
    bağlanması `escalation_reason`'a additive bir değer (A) **ve** anti-anchoring denetim-modu
    (B) gerektiriyordu. Worker bunu tek taraflı ekleyemez (§2.1 platform-otoriter), bu yüzden
    karar-hazır devredilmişti:
    `tarlaanaliz-worker/denetim/birlesik_devir_spec_arsivi_2026.md` §9
    (2026-08-11'e kadar ayrı dosya: `audit_escalation_reason_devir_spec_2026_07_19`).

    Bilimsel çekirdek: denetim tile'ı **güvene/kümeye BAKILMAKSIZIN** seçilir. Bu yüzden
      * onu güven-temelli bir neden altında yollamak yansızlığı bozar → ayrı `AUDIT_SAMPLE`
      * uzman modelin tahminini görürse etiket modele **demirlenir (anchoring)** → sınıf
        etiketleri tel üzerinde hiç taşınmamalı
      * **güven-koşullu** `spot_check` ile aynı anda seçilmek i.i.d. bağımsızlığını bozar

    Bu dosya üçünü de sözleşme düzeyinde bağlar; hiçbiri Portal disiplinine bırakılmaz.
"""

import json
from pathlib import Path

import pytest

try:
    from jsonschema import Draft202012Validator  # type: ignore[import-untyped]
except ImportError:  # pragma: no cover
    pytest.skip("jsonschema yok", allow_module_level=True)

ROOT = Path(__file__).parent.parent
SCHEMA = ROOT / "schemas" / "worker" / "expert_review_queue.v1.schema.json"
CROP_ENUM = ROOT / "enums" / "crop_type.enum.v1.json"
PHENOLOGY_ENUM = ROOT / "enums" / "phenology_stage.enum.v1.json"

LEGACY_REASONS = [
    "LOW_CONFIDENCE",
    "LOW_AGREEMENT",
    "OOD_DETECTED",
    "HIGH_EPISTEMIC",
    "EXPERT_RE_TRIGGER",
    "QUARANTINE_CAUTION",
]


def _schema() -> dict:
    return json.loads(SCHEMA.read_text(encoding="utf-8"))


def _validator() -> "Draft202012Validator":
    return Draft202012Validator(_schema())


def _base(**overrides: object) -> dict:
    """Geçerli bir asgari eskalasyon paketi."""
    payload = {
        "job_id": "job_0f1e2d3c4b5a69788796a5b4",
        "mission_id": "mission_0f1e2d3c4b5a6978",
        "escalation_reason": "LOW_CONFIDENCE",
        "confidence_score": 0.42,
        "crop_type": "CORN",
        "analysis_type": "DISEASE",
    }
    payload.update(overrides)
    return payload


def _audit(**overrides: object) -> dict:
    """Geçerli bir DENETİM paketi.

    ⚠️ 2026-07-31 (KADEME 3 / D12-D15) ile genişledi: denetim satırı artık ölçüm
    bütünlüğü alanlarını da taşımak ZORUNDA — JOIN anahtarı (`tile_id`, M3), konsensüs
    dışlaması (`consensus_participation`, M2) ve seçim kanıtı (π_h + rotation + bucket,
    M1). Ayrıntılı davranış testleri `tests/test_audit_measurement_integrity.py`'de;
    burada yalnız AL-C1/AL-C2 eksenleri (bayrak↔neden, i.i.d. bağımsızlık) ölçülüyor.
    """
    payload = _base(
        escalation_reason="AUDIT_SAMPLE",
        confidence_score=0,  # Ç4/M7: denetim satırında güven kanalı kapalı (const: 0)
        audit_sample=True,
        audit_stratum={"crop_type": "CORN", "analysis_type": "DISEASE"},
        predicted_class=None,
        detection_type=None,
        sub_specialty=None,
        tile_id="tile_0f1e2d3c",
        consensus_participation="EXCLUDED",
        audit_selection_rate=0.05,
        audit_rotation_key="2026-W31",
        audit_bucket=42,
    )
    payload.update(overrides)
    return payload


class TestAlC1AdditiveReason:
    def test_audit_sample_reason_exists(self) -> None:
        assert "AUDIT_SAMPLE" in _schema()["properties"]["escalation_reason"]["enum"]

    def test_legacy_reasons_are_untouched(self) -> None:
        """Additive olmalı: 6 pazarlık-dışı değerin hiçbiri kaybolmamalı/yeniden adlandırılmamalı."""
        enum = _schema()["properties"]["escalation_reason"]["enum"]
        assert enum[: len(LEGACY_REASONS)] == LEGACY_REASONS
        assert len(enum) == len(LEGACY_REASONS) + 1

    def test_legacy_package_still_validates(self) -> None:
        """Geriye uyumluluk: eski üretici audit alanlarını hiç bilmeden geçerli kalmalı."""
        _validator().validate(_base())


class TestAlC2AuditModeFields:
    def test_audit_sample_defaults_false_and_is_optional(self) -> None:
        doc = _schema()
        assert doc["properties"]["audit_sample"]["default"] is False
        assert "audit_sample" not in doc["required"], "zorunlu yapmak MAJOR breaking olurdu"

    def test_audit_stratum_is_structured_not_free_text(self) -> None:
        """§2.1: eksen karışımını imkânsız kıl — serbest dize kabul edilmemeli."""
        stratum = _schema()["properties"]["audit_stratum"]
        assert "object" in stratum["type"], "audit_stratum yapısal obje olmalı"
        assert stratum["additionalProperties"] is False
        assert set(stratum["required"]) == {"crop_type", "analysis_type"}

    def test_stratum_axes_mirror_canonical_enums(self) -> None:
        doc = _schema()
        stratum = doc["properties"]["audit_stratum"]["properties"]
        assert stratum["crop_type"]["enum"] == json.loads(
            CROP_ENUM.read_text(encoding="utf-8")
        )["enum"]
        assert stratum["analysis_type"]["enum"] == doc["properties"]["analysis_type"]["enum"]
        phen = [v for v in stratum["phenology_stage"]["enum"] if v is not None]
        assert phen == json.loads(PHENOLOGY_ENUM.read_text(encoding="utf-8"))["enum"]

    def test_phenology_is_optional_because_enum_covers_3_of_8_crops(self) -> None:
        """Kanonik fenoloji enum'u GRAPE/CORN/OLIVE kapsıyor; zorunlu olsa COTTON örneklenemezdi."""
        stratum = _schema()["properties"]["audit_stratum"]
        assert "phenology_stage" not in stratum["required"]
        covered = {v.split("_")[0] for v in json.loads(
            PHENOLOGY_ENUM.read_text(encoding="utf-8")
        )["enum"]}
        all_crops = set(json.loads(CROP_ENUM.read_text(encoding="utf-8"))["enum"])
        assert covered < all_crops, "enum artık tüm mahsulleri kapsıyorsa bu gerekçe güncellenmeli"

    def test_free_text_stratum_is_rejected(self) -> None:
        assert not _validator().is_valid(_audit(audit_stratum="CORN/DISEASE/w12"))

    def test_stratum_with_unknown_axis_is_rejected(self) -> None:
        assert not _validator().is_valid(
            _audit(audit_stratum={"crop_type": "CORN", "analysis_type": "DISEASE", "week": 12})
        )


class TestFlagAndReasonMoveTogether:
    """A tek başına anchoring'i çözmez; B tek başına metriği kirletir → ikisi bağlandı."""

    def test_valid_audit_package(self) -> None:
        _validator().validate(_audit())

    def test_audit_flag_without_audit_reason_is_rejected(self) -> None:
        assert not _validator().is_valid(_audit(escalation_reason="LOW_CONFIDENCE"))

    def test_audit_reason_without_flag_is_rejected(self) -> None:
        payload = _audit()
        del payload["audit_sample"]
        assert not _validator().is_valid(payload)

    def test_audit_sample_requires_stratum(self) -> None:
        payload = _audit()
        del payload["audit_stratum"]
        assert not _validator().is_valid(payload), (
            "stratum'suz denetim örneklemi propagation_precision'ı stratifiye edemez"
        )


class TestIidIndependenceFromSpotCheck:
    """`spot_check` GÜVEN-KOŞULLUDUR (HIGH tile'ların ~%5'i); i.i.d. ile birlikte olamaz."""

    def test_both_flags_true_is_rejected(self) -> None:
        assert not _validator().is_valid(_audit(spot_check=True)), (
            "güven-koşullu spot_check ile i.i.d. audit_sample aynı anda seçilirse "
            "seçim güvene koşullanır ve bağımsızlık kaybolur"
        )

    def test_spot_check_alone_still_valid(self) -> None:
        """Mevcut spot_check yolu bozulmamalı."""
        _validator().validate(_base(spot_check=True))

    def test_audit_with_explicit_false_spot_check_is_valid(self) -> None:
        _validator().validate(_audit(spot_check=False))


class TestAntiAnchoringIsContractEnforced:
    """Sınıf etiketleri tel üzerinde HİÇ taşınmamalı — Portal disiplinine güvenilmez."""

    @pytest.mark.parametrize(
        ("field", "value"),
        [("predicted_class", "rust"), ("detection_type", "disease"), ("sub_specialty", "FUNGUS")],
    )
    def test_class_labels_are_forbidden_on_audit_rows(self, field: str, value: str) -> None:
        assert not _validator().is_valid(_audit(**{field: value})), (
            f"{field} denetim satırında taşınıyor — uzman etiketi modele DEMİRLENİR (anchoring) "
            "ve tüm ölçüm temeli geçersiz olur"
        )

    def test_class_labels_allowed_on_ordinary_escalation(self) -> None:
        """Kısıt YALNIZ denetim satırında; olağan eskalasyon tahmini taşımaya devam eder."""
        _validator().validate(
            _base(predicted_class="rust", detection_type="disease", sub_specialty="FUNGUS")
        )

    def test_residual_portal_obligation_is_documented(self) -> None:
        """confidence_score bu turda tel üzerinde kalıyor → yükümlülük YAZILI olmalı."""
        block = _schema().get("x-anti-anchoring")
        assert block, "x-anti-anchoring bloğu yok"
        assert "confidence_score" in block["residual_portal_obligation"]
        assert "AL-P1" in block["residual_portal_obligation"]

    def test_confidence_score_type_unchanged_this_round(self) -> None:
        """Nullable'a genişletmek MAJOR olurdu; bu tur MINOR — bilinçli olarak yapılmadı."""
        cs = _schema()["properties"]["confidence_score"]
        assert cs["type"] == "number", "tip değişti → tur MINOR olmaktan çıkar (AL-C3 kalemi)"


class TestKr071PiiInvariantHolds:
    """Denetim kanalı PII kapısını ATLAMAMALI (devir spesi §4)."""

    def test_no_field_id_property(self) -> None:
        assert "field_id" not in _schema()["properties"]

    def test_audit_stratum_carries_no_identifier(self) -> None:
        stratum = set(_schema()["properties"]["audit_stratum"]["properties"])
        forbidden = {"field_id", "owner_name", "ciftci_adi", "lat", "lon", "gps"}
        assert not (stratum & forbidden)

    def test_root_still_closed(self) -> None:
        assert _schema()["unevaluatedProperties"] is False


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
