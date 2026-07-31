"""C9 + C10 — ÖN RAPOR (report_phase) sözleşme testleri.

Neden bu test var (2026-07-31 denetimi):
    KG-0.b-R (Y-D) kararı "yeni faz/şema gerekmiyor, yalnız içerik kaynağı ekleniyor" diyordu.
    Faz kısmı doğruydu, **şema kısmı değildi**:

      1. İçerik: iki kanonik artefakt PRELIMINARY içeriğini "YALNIZ/ONLY" diyerek dört kaleme
         kapatıyordu; Y-D'nin göstereceği öncelik bölgesi (poligon + ndvi_value + ndvi_overlay)
         o listede yoktu.
      2. Zamanlama: `x-derived-from.mapping` yalnız analiz-ve-sonrası statüleri sayıyordu.
         Y-D raporu kalibrasyondan HEMEN SONRA (mission UPLOADED) gösterilir — mapping'de
         karşılığı yoktu. "Çalışıyor" görünmesinin tek sebebi platform kodundaki catch-all
         (`results_service_impl.py:227`: FULL if DONE else PRELIMINARY) idi; yani platform
         kanonik haritadan GENİŞ davranıyordu.
      3. Kanonik olmayan adlar: mapping `ANALYZING` ve `DONE` kullanıyordu; `mission_status.enum.v1`
         bunları TANIMAZ (kanonik karşılıkları `IN_ANALYSIS` ve `DELIVERED`). Dört girişin ikisi.

    Bu testler üçünü de kapıya bağlar; prose değil makine-okunur sözleşmeyi doğrular.
"""

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
REPORT_PHASE = ROOT / "enums" / "report_phase.enum.v1.json"
MISSION_STATUS = ROOT / "enums" / "mission_status.enum.v1.json"
PRELIM_EVENT = ROOT / "schemas" / "events" / "analysis_preliminary_ready.v1.schema.json"
KR_REGISTRY = ROOT / "ssot" / "kr_registry.md"

# Ön fazda ASLA görünmemesi gereken içerik (KR-019 / KR-025).
FORBIDDEN_IN_PRELIMINARY = {
    "findings",
    "detections",
    "expert_corrections",
    "prescription",
    "treatment_recommendation",
}


def _load(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


class TestDerivationMapUsesCanonicalStatuses:
    """C10 — harita anahtarları kanonik mission_status üyeleri olmalı."""

    def test_every_mapping_key_is_a_canonical_mission_status(self) -> None:
        mapping = _load(REPORT_PHASE)["x-derived-from"]["mapping"]
        canonical = set(_load(MISSION_STATUS)["enum"])
        unknown = set(mapping) - canonical
        assert not unknown, (
            f"report_phase mapping kanonik olmayan statü kullanıyor: {sorted(unknown)}. "
            "Platform-içi adlar (ANALYZING/DONE/ACKED/FLOWN) kanonik enum'da YOKTUR; "
            "çeviri x-derived-from.platform_internal_aliases altında belgelenir."
        )

    def test_platform_internal_aliases_are_documented_and_not_canonical(self) -> None:
        """Alias bloğu, kanonik olmayan adların nereye çevrildiğini söylemeli."""
        derived = _load(REPORT_PHASE)["x-derived-from"]
        aliases = derived.get("platform_internal_aliases")
        assert aliases, "platform_internal_aliases bloğu yok — çeviri belgesiz kalır"
        canonical = set(_load(MISSION_STATUS)["enum"])
        for internal, canon in aliases.items():
            if internal == "description":
                continue
            assert internal not in canonical, f"{internal} kanonik enum'da var; alias sayılmamalı"
            assert canon in canonical, f"alias hedefi {canon} kanonik enum'da yok"

    def test_mapping_values_are_valid_phases_or_withdrawn(self) -> None:
        doc = _load(REPORT_PHASE)
        phases = set(doc["enum"])
        for status, phase in doc["x-derived-from"]["mapping"].items():
            assert phase in phases or phase.startswith("WITHDRAWN"), (
                f"{status} → {phase!r} geçerli bir faz değil"
            )


class TestPreliminaryTimingCoversPostCalibration:
    """C10 — Y-D anı (kalibrasyon sonrası, worker öncesi) haritada olmalı."""

    def test_uploaded_maps_to_preliminary(self) -> None:
        mapping = _load(REPORT_PHASE)["x-derived-from"]["mapping"]
        assert mapping.get("UPLOADED") == "PRELIMINARY", (
            "mission UPLOADED (kalibrasyon bitti, worker sonucu yok) PRELIMINARY'ye eşlenmeli; "
            "aksi hâlde Y-D ÖN RAPOR'u kanonik haritanın DIŞINDA sunulur."
        )

    def test_analysis_and_review_stages_still_preliminary(self) -> None:
        mapping = _load(REPORT_PHASE)["x-derived-from"]["mapping"]
        assert mapping["IN_ANALYSIS"] == "PRELIMINARY"
        assert mapping["PENDING_REVIEW"] == "PRELIMINARY"

    def test_full_requires_expert_approved_terminal_status(self) -> None:
        mapping = _load(REPORT_PHASE)["x-derived-from"]["mapping"]
        full_statuses = {s for s, p in mapping.items() if p == "FULL"}
        assert full_statuses == {"DELIVERED"}, (
            f"FULL yalnız uzman onaylı terminal statüden türer; bulunan: {full_statuses}"
        )

    def test_expert_rejected_is_withdrawn_not_a_phase(self) -> None:
        mapping = _load(REPORT_PHASE)["x-derived-from"]["mapping"]
        assert mapping["EXPERT_REJECTED"].startswith("WITHDRAWN")

    def test_unlisted_status_behavior_is_fail_closed(self) -> None:
        """'Listelenmeyen = PRELIMINARY' varsayımı açıkça yasaklanmalı."""
        derived = _load(REPORT_PHASE)["x-derived-from"]
        rule = derived.get("unlisted_status_behavior", "")
        assert rule, "unlisted_status_behavior kuralı yok — catch-all davranışı belirsiz kalır"
        assert "FAIL-CLOSED" in rule.upper()

    def test_pre_flight_statuses_are_not_mapped(self) -> None:
        """Uçuş öncesi statüler ön rapor üretemez."""
        mapping = _load(REPORT_PHASE)["x-derived-from"]["mapping"]
        for status in ("DRAFT", "PLANNED", "ASSIGNED", "ACCEPTED"):
            assert status not in mapping, f"{status} uçuş öncesidir; faz üretmemeli"


class TestPreliminaryContentIsAClosedList:
    """C9 — sunulabilir içerik kapalı liste; tespit hiçbir aşamada yok."""

    def test_x_preliminary_content_exists_with_both_stages(self) -> None:
        content = _load(REPORT_PHASE).get("x-preliminary-content")
        assert content, "x-preliminary-content yok — içerik kuralı test edilemez"
        assert "stage_a_post_calibration" in content
        assert "stage_b_post_analysis" in content
        assert "never" in content

    def test_stage_a_carries_priority_zone_fields(self) -> None:
        """Y-D'nin göstereceği alanlar listede olmalı (yoksa P6/P12 kanonik dışı kalır)."""
        stage_a = _load(REPORT_PHASE)["x-preliminary-content"]["stage_a_post_calibration"]
        fields = set(stage_a["fields"])
        assert {"geom", "ndvi_value", "ndvi_overlay"} <= fields, (
            f"Aşama A öncelik bölgesi alanlarını taşımalı; bulunan: {sorted(fields)}"
        )

    def test_stage_b_keeps_original_kr093_layers(self) -> None:
        """KR-093'ün özgün tanımı daraltılmamalı."""
        stage_b = _load(REPORT_PHASE)["x-preliminary-content"]["stage_b_post_analysis"]
        fields = set(stage_b["fields"])
        assert {"HEALTH", "NITROGEN_STRESS", "WATER_STRESS", "overall_health_index"} <= fields

    @pytest.mark.parametrize("stage", ["stage_a_post_calibration", "stage_b_post_analysis"])
    def test_no_detection_content_in_any_stage(self, stage: str) -> None:
        """KR-019 kapısı: tespit ön faza sızamaz."""
        fields = set(_load(REPORT_PHASE)["x-preliminary-content"][stage]["fields"])
        leak = fields & FORBIDDEN_IN_PRELIMINARY
        assert not leak, f"{stage} tespit içeriği taşıyor: {leak} — KR-019 ihlali"

    def test_never_list_names_the_forbidden_content(self) -> None:
        never = set(_load(REPORT_PHASE)["x-preliminary-content"]["never"])
        assert FORBIDDEN_IN_PRELIMINARY <= never, (
            f"never[] eksik: {sorted(FORBIDDEN_IN_PRELIMINARY - never)}"
        )


class TestEventDescriptionDoesNotClaimPhaseWideRule:
    """C9 — olay açıklaması faz-düzeyi 'ONLY' iddiasında bulunmamalı."""

    def test_event_defers_to_report_phase_for_the_phase_rule(self) -> None:
        desc = _load(PRELIM_EVENT)["description"]
        assert "report_phase.enum.v1.json" in desc, (
            "Olay açıklaması, faz içeriğinin kanonik kaynağına (report_phase :: "
            "x-preliminary-content) işaret etmeli; aksi hâlde olay payload'ı faz kuralı sanılır."
        )

    def test_event_still_excludes_detections(self) -> None:
        desc = _load(PRELIM_EVENT)["description"]
        assert "NO expert-dependent detections" in desc, "KR-019 ifadesi korunmalı"


class TestKr093IsDefinedInCanonicalRegistry:
    """C9 ön koşulu — normatif atıf yapılan KR kanonik registry'de TANIMLI olmalı."""

    def test_kr093_section_exists(self) -> None:
        text = KR_REGISTRY.read_text(encoding="utf-8")
        assert "## KR-093" in text, (
            "ssot/kr_registry.md KR-093'ü tanımlamıyor, ama report_phase.enum.v1 ve "
            "analysis_preliminary_ready.v1 ona normatif atıf yapıyor → sarkan kanonik atıf."
        )

    def test_every_kr_referenced_by_report_phase_is_defined(self) -> None:
        """x-kr-ref'teki her KR registry'de tanımlı olmalı (genel sarkan-atıf kapısı)."""
        text = KR_REGISTRY.read_text(encoding="utf-8")
        for kr in _load(REPORT_PHASE)["x-kr-ref"]:
            assert f"## {kr}" in text, f"{kr} ssot/kr_registry.md'de tanımlı değil"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
