"""KADEME 3 (D12–D15) — denetim satırının ÖLÇÜM BÜTÜNLÜĞÜ kapısı.

NEDEN (2026-07-31, 10-disiplin denetimi · ML/DS bulguları M1–M4 + Ç1 + Ç4):
    AL-C1/AL-C2 denetim kanalını AÇTI (i.i.d. örneklem), ama kanal ölçüm aracı olarak
    KENDİ ÖLÇTÜĞÜ SİSTEMİ değiştiriyordu:

      * **M2** — denetim satırı KR-019 konsensüsüne *kardeş inceleme* olarak giriyordu:
        kör uzmanın etiketi yayın kapısını bloke edebilir (gözlemci etkisi) ve denetim
        etiketi, denetlediği kararın parçası olur (dairesellik).
      * **M3** — tile düzeyinde JOIN anahtarı yoktu. `analysis_result.detections` bir
        DİZİDİR; `job_id` ile JOIN bir işin TÜM tespitlerini getirir → hangi tile'ın
        denetlendiği bilinemez → `propagation_precision` HESAPLANAMAZ.
      * **M4** — denetim satırı bir tile GRUBUNA bağlanabiliyordu: toplu onay yayılımı
        denetim etiketini kendi ölçtüğü yayılıma besler ⇒ `propagation_precision`
        YAPISAL olarak 1'e gider (ölçüm kendini doğrular).
      * **M1/Y1** — tabaka etiketi taşınıyordu ama seçilme olasılığı π_h taşınmıyordu →
        Horvitz-Thompson yansız kestirimi imkânsız (örneklemden popülasyona geçilemez).
      * **Ç1** — denetim ile `spot_check` çakışmasının YÖNÜ yazılı değildi.
      * **Ç4/M7** — denetim satırında model güveni tel üzerinde bilgi taşıyordu
        (anti-anchoring ihlali); `const:0` bilgi kanalını kapatır.

Bu dosya, kapının her bir maddesini hem YAPI hem DAVRANIŞ düzeyinde ölçer.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

try:
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover
    pytest.skip("jsonschema not installed", allow_module_level=True)


ROOT = Path(__file__).parent.parent
SCHEMA = ROOT / "schemas" / "worker" / "expert_review_queue.v1.schema.json"


def _schema() -> dict:
    return json.loads(SCHEMA.read_text(encoding="utf-8"))


def _validator() -> "Draft202012Validator":
    return Draft202012Validator(_schema())


def _audit_row(**overrides: object) -> dict:
    """Sözleşmeye uyan asgari bir DENETİM satırı."""
    row = {
        "job_id": "job_0001",
        "mission_id": "mission_0001",
        "escalation_reason": "AUDIT_SAMPLE",
        "confidence_score": 0,
        "crop_type": "COTTON",
        "analysis_type": "DISEASE",
        "audit_sample": True,
        # AL-C2 kapısı: bayrak ve tabaka birlikte hareket eder (fenoloji ekseni bilerek yok —
        # A5/A6 kapanmadan doldurulamaz, bkz. TestStratumStaysUncemented).
        "audit_stratum": {"crop_type": "COTTON", "analysis_type": "DISEASE"},
        "tile_id": "tile_0001",
        "consensus_participation": "EXCLUDED",
        "audit_selection_rate": 0.05,
        "audit_rotation_key": "2026-W31",
        "audit_bucket": 42,
        "tile_group_id": None,
        "tile_group_size": 1,
        "required_reviewers": 1,
    }
    row.update(overrides)
    return row


def _ordinary_row(**overrides: object) -> dict:
    """Olağan (denetim olmayan) inceleme satırı — kapı buna KARIŞMAMALI."""
    row = {
        "job_id": "job_0002",
        "mission_id": "mission_0002",
        "escalation_reason": "LOW_CONFIDENCE",
        "confidence_score": 0.42,
        "crop_type": "CORN",
        "analysis_type": "PEST",
    }
    row.update(overrides)
    return row


def _errors(row: dict) -> list:
    return list(_validator().iter_errors(row))


class TestBaselineRowsValidate:
    def test_audit_row_is_valid(self) -> None:
        assert not _errors(_audit_row()), _errors(_audit_row())[:2]

    def test_ordinary_row_is_untouched(self) -> None:
        """Kapı yalnız denetim satırını bağlar; olağan inceleme eskisi gibi çalışır."""
        assert not _errors(_ordinary_row())

    def test_ordinary_row_may_still_use_groups_and_confidence(self) -> None:
        row = _ordinary_row(tile_group_id="grp_1", tile_group_size=12, required_reviewers=3)
        assert not _errors(row), "olağan satırın toplu-onay yolu kısıtlanmamalı"


class TestM2ConsensusExclusion:
    def test_audit_row_must_declare_exclusion(self) -> None:
        assert _errors(_audit_row(consensus_participation="PARTICIPATES")), (
            "denetim satırı konsensüse KATILIYOR olarak işaretlenebiliyor — ölçüm, ölçtüğü "
            "sistemi değiştirir (M2)"
        )

    def test_field_is_required_on_audit_rows(self) -> None:
        row = _audit_row()
        del row["consensus_participation"]
        assert _errors(row), "beyan zorunlu olmalı; varsayılan sessizce PARTICIPATES olamaz"

    def test_ordinary_row_may_participate(self) -> None:
        assert not _errors(_ordinary_row(consensus_participation="PARTICIPATES"))


class TestM3JoinKey:
    def test_tile_id_required_on_audit_rows(self) -> None:
        row = _audit_row()
        del row["tile_id"]
        assert _errors(row), "JOIN anahtarı olmadan propagation_precision hesaplanamaz (M3)"

    def test_tile_id_cannot_be_null_on_audit_rows(self) -> None:
        assert _errors(_audit_row(tile_id=None))

    def test_tile_id_optional_on_ordinary_rows(self) -> None:
        assert not _errors(_ordinary_row())


class TestM4NoGroupPropagation:
    def test_audit_row_cannot_join_a_group(self) -> None:
        assert _errors(_audit_row(tile_group_id="grp_1")), (
            "denetim satırı gruba bağlanabiliyor — toplu onay yayılımı ölçümü kendi "
            "sonucuna besler, propagation_precision yapısal olarak 1 olur (M4)"
        )

    def test_audit_row_group_size_is_one(self) -> None:
        assert _errors(_audit_row(tile_group_size=8))

    def test_required_reviewers_is_fixed(self) -> None:
        assert _errors(_audit_row(required_reviewers=3)), (
            "denetim satırında inceleyen sayısı değişebiliyor — tabakalar arası yük farkı "
            "ölçümü kirletir (Ç1/M2)"
        )


class TestM1SelectionEvidence:
    """π_h olmadan örneklemden POPÜLASYONA geçilemez."""

    @pytest.mark.parametrize(
        "missing", ["audit_selection_rate", "audit_rotation_key", "audit_bucket"]
    )
    def test_selection_evidence_is_required(self, missing: str) -> None:
        row = _audit_row()
        del row[missing]
        assert _errors(row), f"{missing} olmadan çekiliş denetlenebilir değil (M1/Y1)"

    @pytest.mark.parametrize("rate", [0, -0.1, 1.5])
    def test_rate_must_be_a_probability(self, rate: float) -> None:
        assert _errors(_audit_row(audit_selection_rate=rate)), (
            "π_h bir olasılıktır: 0 < π_h ≤ 1 (0 seçilemez olanı, >1 anlamsızı ifade eder)"
        )

    def test_rate_one_is_allowed(self) -> None:
        """π_h = 1 geçerlidir: tam sayım (census) yapılan tabaka."""
        assert not _errors(_audit_row(audit_selection_rate=1))


class TestC1PriorityRule:
    def test_suppression_flag_exists_and_is_boolean(self) -> None:
        field = _schema()["properties"]["spot_check_suppressed"]
        assert field["type"] == "boolean"
        assert field["default"] is False

    def test_priority_direction_is_written_normatively(self) -> None:
        """Kural metni SÖZLEŞMEDE olmalı — 'ekip biliyor' bir kural değildir."""
        text = json.dumps(_schema(), ensure_ascii=False)
        assert "audit_sample` kazanır" in text or "audit_sample kazanır" in text, (
            "çakışma yönü (denetim kazanır) sözleşmede yazılı değil (Ç1)"
        )

    def test_audit_row_can_record_suppression(self) -> None:
        assert not _errors(_audit_row(spot_check=False, spot_check_suppressed=True))

    def test_audit_and_spot_check_cannot_coexist(self) -> None:
        """Önceki turun i.i.d. kapısı korunuyor (AL-C2)."""
        assert _errors(_audit_row(spot_check=True))


class TestC4ConfidenceChannelClosed:
    def test_audit_row_confidence_is_zero(self) -> None:
        assert _errors(_audit_row(confidence_score=0.93)), (
            "denetim satırı model güvenini taşıyor — uzman 'bunu zaten biliyor' diye "
            "hizalanır (anti-anchoring ihlali, Ç4/M7)"
        )

    def test_ordinary_row_keeps_its_confidence(self) -> None:
        assert not _errors(_ordinary_row(confidence_score=0.93))

    def test_deprecation_window_is_declared(self) -> None:
        """Sabitleme bir GEÇİŞTİR; penceresi ve gerekçesi yazılı olmalı."""
        declaration = _schema()["x-deprecated-in-context"]["confidence_score"]
        for key in ("context", "since", "policy", "window", "why"):
            assert str(declaration.get(key, "")).strip(), f"beyanda eksik alan: {key}"
        assert "audit_sample" in declaration["context"]


class TestStratumStaysUncemented:
    """⚠️ D13'ün uyarısı: `audit_stratum` A6'nın BOZUK fenoloji eşlemesini çimentolamamalı.

    Plan metni *"opak dize kalsın"* diyordu; AL-C2 turunda alan YAPISAL yazılmıştı.
    Ölçüm: iki eksen (crop_type, analysis_type) kanonik enum'larla birebir eşleşiyor —
    onları opak dizeye geri çevirmek bilgi KAYBI olurdu. Tartışmalı olan tek eksen
    **fenoloji**: contract enum'u 8 ürünün 3'ünü kapsıyor ve edge'in
    `phenology_calendar.yaml`'ı ayrı bir sözlük (A5/A6) → alan bugün doldurulamaz.

    Bilinçli sapma: yapı KORUNUR, **fenoloji ekseni OPSİYONEL kalır** ve zorunlu hâle
    getirilmesi A5/A6 kapanmadan YASAKTIR. Bu test o kilidi tutar.
    """

    def test_phenology_axis_is_not_required(self) -> None:
        stratum = _schema()["properties"]["audit_stratum"]
        required = set(stratum.get("required", []) or [])
        assert "phenology_stage" not in required, (
            "fenoloji ekseni zorunlu yapılmış — contract enum'u ile edge takvimi arasında "
            "1:1 eşleme YOK (A5/A6); zorunlu alan üretici tarafından doldurulamaz ve "
            "bozuk eşleme tele çimentolanır"
        )

    def test_canonical_axes_stay_structured(self) -> None:
        stratum = _schema()["properties"]["audit_stratum"]
        assert "crop_type" in stratum["properties"]
        assert "analysis_type" in stratum["properties"]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
