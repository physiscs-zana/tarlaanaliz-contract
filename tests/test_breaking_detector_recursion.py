"""`breaking_change_detector` özyineleme kapısı — D3 regresyon testi.

NEDEN (2026-07-31, 10-disiplin denetimi · SD1/SD2/Y5):
    Denetimde **mutasyonla** ölçüldü: `schemas/worker/expert_review_queue.v1.schema.json`
    içindeki `properties.escalation_reason.enum`'dan `QUARANTINE_CAUTION` silindiğinde
    (= MAJOR breaking) araç **"Breaking Changes: 0"** dedi. Eski sürüm yalnız KÖK
    düzeydeki `enum` ve `properties` sözlüğünü okuyordu → `$defs`, `items`,
    `oneOf/allOf/if-then` altındaki her şey görünmezdi.

    Aynı turda ikinci bir yalan daha ölçüldü (bu oturumda): araç ilerleme metnini
    **stdout**'a basıyordu; CI `--json > breaking_changes.json` yönlendirmesi yüzünden
    dosya geçersiz JSON oluyor, `json.load` patlıyor ve CI'ın `if` bloğu else dalına
    düşerek **has_breaking=false** yazıyordu. Yani kapı, `continue-on-error` hiç
    olmasaydı bile DAİMA "breaking yok" derdi.

Bu dosyanın sözleşmesi:
    Her test, kapının GÖRMESİ gereken bir değişiklik sınıfını temsil eder. Bir test
    düşerse kapı o sınıfa kör demektir — düzeltme dedektördedir, testte değil.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest


ROOT = Path(__file__).parent.parent
TOOL = ROOT / "tools" / "breaking_change_detector.py"

sys.path.insert(0, str(ROOT / "tools"))
from breaking_change_detector import BreakingChangeDetector  # noqa: E402


def _run(tmp_path: Path, old: dict, new: dict) -> dict:
    """İki şemayı ayrı ağaçlara yazıp dedektörü koştur, kategorize sonucu döndür."""
    old_dir = tmp_path / "old" / "schemas"
    new_dir = tmp_path / "new" / "schemas"
    old_dir.mkdir(parents=True)
    new_dir.mkdir(parents=True)
    (old_dir / "t.json").write_text(json.dumps(old), encoding="utf-8")
    (new_dir / "t.json").write_text(json.dumps(new), encoding="utf-8")
    detector = BreakingChangeDetector(old_dir, new_dir)
    return detector.detect_changes()


def _breaking_fields(result: dict) -> set[str]:
    return {str(c.get("field")) for c in result["breaking"]}


def _wrap(node: dict) -> dict:
    """Bir alt şemayı kök şema kabuğuna sar."""
    base: dict[str, Any] = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "unevaluatedProperties": False,
    }
    base.update(node)
    return base


class TestNestedEnumBlindness:
    """SD1 — turun tetikleyici bulgusu: iç içe enum değeri silme."""

    def test_enum_value_removed_under_properties_is_breaking(self, tmp_path: Path) -> None:
        old = _wrap({"properties": {"escalation_reason": {
            "type": "string", "enum": ["LOW_CONFIDENCE", "QUARANTINE_CAUTION"]}}})
        new = _wrap({"properties": {"escalation_reason": {
            "type": "string", "enum": ["LOW_CONFIDENCE"]}}})
        result = _run(tmp_path, old, new)
        assert result["has_breaking"], (
            "properties.<alan>.enum'dan değer silmek MAJOR'dır — dedektör kör kaldı "
            "(2026-07-31'de tam olarak bu ölçülmüştü)"
        )
        assert "properties.escalation_reason" in _breaking_fields(result)

    def test_enum_value_added_under_properties_is_not_breaking(self, tmp_path: Path) -> None:
        old = _wrap({"properties": {"r": {"enum": ["A"]}}})
        new = _wrap({"properties": {"r": {"enum": ["A", "B"]}}})
        result = _run(tmp_path, old, new)
        assert not result["has_breaking"]
        assert any(c["type"] == "ENUM_VALUE_ADDED" for c in result["non_breaking"])

    def test_enum_removed_under_defs_is_breaking(self, tmp_path: Path) -> None:
        old = _wrap({"$defs": {"Form": {"properties": {"k": {"enum": ["A", "B"]}}}}})
        new = _wrap({"$defs": {"Form": {"properties": {"k": {"enum": ["A"]}}}}})
        assert _run(tmp_path, old, new)["has_breaking"], "$defs altı enum görünmüyor (SD2)"

    def test_enum_removed_under_items_is_breaking(self, tmp_path: Path) -> None:
        old = _wrap({"properties": {"zones": {"type": "array",
                                              "items": {"properties": {"lvl": {"enum": ["HI", "LO"]}}}}}})
        new = _wrap({"properties": {"zones": {"type": "array",
                                              "items": {"properties": {"lvl": {"enum": ["HI"]}}}}}})
        assert _run(tmp_path, old, new)["has_breaking"], "items altı enum görünmüyor"

    def test_enum_removed_under_oneof_branch_is_breaking(self, tmp_path: Path) -> None:
        old = _wrap({"oneOf": [{"properties": {"k": {"enum": ["A", "B"]}}}, {"type": "object"}]})
        new = _wrap({"oneOf": [{"properties": {"k": {"enum": ["A"]}}}, {"type": "object"}]})
        assert _run(tmp_path, old, new)["has_breaking"], "oneOf dalı altı enum görünmüyor"

    def test_enum_removed_under_if_then_is_breaking(self, tmp_path: Path) -> None:
        old = _wrap({"if": {"properties": {"m": {"const": "X"}}},
                     "then": {"properties": {"k": {"enum": ["A", "B"]}}}})
        new = _wrap({"if": {"properties": {"m": {"const": "X"}}},
                     "then": {"properties": {"k": {"enum": ["A"]}}}})
        assert _run(tmp_path, old, new)["has_breaking"], "if/then altı enum görünmüyor"


class TestNestedStructuralChanges:
    def test_required_added_under_defs_is_breaking(self, tmp_path: Path) -> None:
        old = _wrap({"$defs": {"F": {"properties": {"a": {}, "b": {}}, "required": ["a"]}}})
        new = _wrap({"$defs": {"F": {"properties": {"a": {}, "b": {}}, "required": ["a", "b"]}}})
        assert _run(tmp_path, old, new)["has_breaking"], "$defs altı required genişlemesi görünmüyor"

    def test_field_removed_under_defs_is_breaking(self, tmp_path: Path) -> None:
        old = _wrap({"$defs": {"F": {"properties": {"a": {}, "b": {}}}}})
        new = _wrap({"$defs": {"F": {"properties": {"a": {}}}}})
        assert _run(tmp_path, old, new)["has_breaking"], "$defs altı alan silme görünmüyor"

    def test_maxitems_tightened_under_defs_is_breaking(self, tmp_path: Path) -> None:
        old = _wrap({"$defs": {"F": {"properties": {"z": {"type": "array", "maxItems": 500}}}}})
        new = _wrap({"$defs": {"F": {"properties": {"z": {"type": "array", "maxItems": 100}}}}})
        assert _run(tmp_path, old, new)["has_breaking"]

    def test_constraint_newly_added_is_breaking(self, tmp_path: Path) -> None:
        """Var olan bir alana SONRADAN `maxLength` koymak eski veriyi reddeder."""
        old = _wrap({"properties": {"wkt": {"type": "string"}}})
        new = _wrap({"properties": {"wkt": {"type": "string", "maxLength": 4096}}})
        assert _run(tmp_path, old, new)["has_breaking"]

    def test_pattern_newly_added_is_breaking(self, tmp_path: Path) -> None:
        old = _wrap({"properties": {"key": {"type": "string"}}})
        new = _wrap({"properties": {"key": {"type": "string", "pattern": "^[a-z]+$"}}})
        assert _run(tmp_path, old, new)["has_breaking"]

    def test_oneof_branch_removed_is_breaking(self, tmp_path: Path) -> None:
        old = _wrap({"oneOf": [{"type": "object"}, {"type": "object"}]})
        new = _wrap({"oneOf": [{"type": "object"}]})
        assert _run(tmp_path, old, new)["has_breaking"], "oneOf dalı silmek seçenek siler"

    def test_allof_branch_added_is_breaking(self, tmp_path: Path) -> None:
        old = _wrap({"allOf": [{"type": "object"}]})
        new = _wrap({"allOf": [{"type": "object"}, {"required": ["x"]}]})
        assert _run(tmp_path, old, new)["has_breaking"], "allOf dalı eklemek kısıt ekler"

    @pytest.mark.parametrize("key", ["allOf", "oneOf", "anyOf", "prefixItems"])
    def test_first_composition_constraint_is_breaking(self, tmp_path: Path, key: str) -> None:
        """HİÇ YOKKEN bileşim eklemek de daraltmadır — eski sürüm bunu HİÇ görmüyordu.

        Ölçüldü (2026-07-31/KADEME 3): `expert_review_queue`'ya 5 koşullu `allOf` bloğu
        eklendi; iki tarafta da liste şartı arandığı için dedektör **hiçbir şey**
        raporlamadı. Kısıt eklemenin görünmez olması, kapının sessizce gevşemesidir.
        """
        old = _wrap({"type": "object"})
        new = _wrap({key: [{"type": "object"}]})
        result = _run(tmp_path, old, new)
        assert result["has_breaking"], f"{key} hiç yokken eklenmesi görünmüyor"
        assert any(c["type"] == "COMPOSITION_BRANCH_CHANGED" for c in result["breaking"])

    def test_first_composition_can_be_declared(self, tmp_path: Path) -> None:
        """Beyanla indirilebilir — ama beyan RAPORDA görünür (sessiz istisna değil)."""
        old = _wrap({"type": "object"})
        new = _wrap({
            "allOf": [{"type": "object"}],
            "x-compat-accepted": {
                "change": "test", "date": "2026-07-31",
                "rationale": "ölçüldü: koşullu bloklar yalnız yeni alanlarda ateşlenir",
                "ref": "test",
            },
        })
        result = _run(tmp_path, old, new)
        assert not result["has_breaking"]
        assert any("ACCEPTED TIGHTENING" in c["message"] for c in result["non_breaking"])


class TestContextSubsets:
    """`x-context-subsets` — şema `enum`'u değişmeden bağlam sözlüğü daralabilir.

    Kanonik örnek: `enums/calibration_type.enum.v1.json` →
    `edge/calibrated_dataset_manifest: ["ABSOLUTE","RELATIVE"]`. Buradan değer düşerse
    o bağlamın üreticileri kırılır; klasik enum karşılaştırması bunu GÖREMEZ.
    """

    def test_subset_value_removed_is_breaking(self, tmp_path: Path) -> None:
        old = _wrap({"enum": ["A", "B", "C"],
                     "x-context-subsets": {"edge/x": ["A", "B"], "edge/y": ["A"]}})
        new = _wrap({"enum": ["A", "B", "C"],
                     "x-context-subsets": {"edge/x": ["A"], "edge/y": ["A"]}})
        result = _run(tmp_path, old, new)
        assert result["has_breaking"], "bağlam alt kümesinden değer düşmesi görünmüyor"

    def test_subset_value_added_is_not_breaking(self, tmp_path: Path) -> None:
        old = _wrap({"enum": ["A", "B"], "x-context-subsets": {"edge/x": ["A"]}})
        new = _wrap({"enum": ["A", "B"], "x-context-subsets": {"edge/x": ["A", "B"]}})
        assert not _run(tmp_path, old, new)["has_breaking"]

    def test_whole_context_removed_is_breaking(self, tmp_path: Path) -> None:
        old = _wrap({"enum": ["A"], "x-context-subsets": {"edge/x": ["A"], "edge/y": ["A"]}})
        new = _wrap({"enum": ["A"], "x-context-subsets": {"edge/x": ["A"]}})
        assert _run(tmp_path, old, new)["has_breaking"]

    def test_new_context_is_reported_as_non_breaking(self, tmp_path: Path) -> None:
        """Yeni bağlam kırıcı değildir ama GÖRÜNMEZ de olmamalı."""
        old = _wrap({"enum": ["A"], "x-context-subsets": {"edge/x": ["A"]}})
        new = _wrap({"enum": ["A"], "x-context-subsets": {"edge/x": ["A"], "platform/y": ["A"]}})
        result = _run(tmp_path, old, new)
        assert not result["has_breaking"]
        assert any(c["type"] == "CONTEXT_SUBSET_VALUE_ADDED" for c in result["non_breaking"])


class TestNormativeAnnotations:
    """Doğrulamayı değil DAVRANIŞI değiştiren `x-` blokları sessiz kalamaz.

    Somut vaka (D8): `calibration_type.enum` → `x-normalization` içindeki
    *"eksikse PANEL_ABSOLUTE varsay"* kuralı platform kodunda birebir uygulanıyordu
    (`worker_job_publisher.py:80-84`). Kuralı FAIL-CLOSED'a çevirmek hiçbir belgeyi
    geçersiz kılmaz — klasik şema diff'i bunu HİÇ görmez — ama tüketicinin kodunu
    değiştirmesi ZORUNLUDUR.
    """

    def test_normalization_rule_change_is_reported(self, tmp_path: Path) -> None:
        old = _wrap({"x-normalization": {"missing -> PANEL_ABSOLUTE": "güvenlik-ağı"}})
        new = _wrap({"x-normalization": {"missing": {"policy": "FAIL-CLOSED"}}})
        result = _run(tmp_path, old, new)
        reported = [c for c in result["non_breaking"]
                    if c["type"] == "NORMATIVE_ANNOTATION_CHANGED"]
        assert reported, "normatif kural değişimi raporlanmadı — tüketici davranışı sessizce kayar"
        assert "manual review" in reported[0]["message"].lower()

    def test_x_updated_is_not_noise(self, tmp_path: Path) -> None:
        """Her turda değişen tarih alanı rapora girmemeli (sinyal/gürültü)."""
        old = _wrap({"x-updated": "2026-07-30"})
        new = _wrap({"x-updated": "2026-07-31"})
        result = _run(tmp_path, old, new)
        assert not any(c["type"] == "NORMATIVE_ANNOTATION_CHANGED"
                       for c in result["non_breaking"]), "x-updated gürültü üretiyor"


class TestNoFalsePositives:
    """Kapı gürültü üretirse kimse ona bakmaz — yanlış alarm da bir arızadır."""

    def test_type_widened_to_nullable_is_not_breaking(self, tmp_path: Path) -> None:
        """C11'in `mission_date: ["string","null"]` deseni MINOR olmalı."""
        old = _wrap({"properties": {"d": {"type": "string"}}})
        new = _wrap({"properties": {"d": {"type": ["string", "null"]}}})
        result = _run(tmp_path, old, new)
        assert not result["has_breaking"]
        assert any(c["type"] == "TYPE_WIDENED" for c in result["non_breaking"])

    def test_new_optional_field_with_constraints_is_not_breaking(self, tmp_path: Path) -> None:
        """YENİ bir alanın iç kısıtları eski veriyi kıramaz (o alan zaten yoktu)."""
        old = _wrap({"properties": {"a": {"type": "string"}}})
        new = _wrap({"properties": {
            "a": {"type": "string"},
            "raw_frames": {"type": "array", "maxItems": 5000,
                           "items": {"properties": {"k": {"pattern": "^x$"}}}},
        }})
        result = _run(tmp_path, old, new)
        assert not result["has_breaking"], f"sahte breaking: {result['breaking']}"

    def test_constraint_relaxed_is_not_breaking(self, tmp_path: Path) -> None:
        old = _wrap({"properties": {"z": {"type": "array", "maxItems": 5000}}})
        new = _wrap({"properties": {"z": {"type": "array", "maxItems": 6000}}})
        assert not _run(tmp_path, old, new)["has_breaking"]

    def test_identical_schema_reports_nothing(self, tmp_path: Path) -> None:
        same = _wrap({"$defs": {"F": {"properties": {"a": {"enum": ["A"]}}}},
                      "properties": {"f": {"$ref": "#/$defs/F"}}})
        result = _run(tmp_path, json.loads(json.dumps(same)), json.loads(json.dumps(same)))
        assert result["total"] == 0, f"aynı şema fark üretti: {result}"


class TestAcceptedTightening:
    """`x-compat-accepted` — beyanlı istisna DAR olmalı, kaçış deliği değil (D7)."""

    ACCEPT = {
        "change": "test",
        "date": "2026-07-31",
        "rationale": "ölçüldü: üretici yok",
        "ref": "test",
    }

    def test_enum_added_where_none_existed_is_breaking(self, tmp_path: Path) -> None:
        """Serbest alanı kapalı vocabulary'ye çevirmek daraltmadır (yeni sınıf)."""
        old = _wrap({"properties": {"flags": {"type": "string"}}})
        new = _wrap({"properties": {"flags": {"type": "string", "enum": ["A", "B"]}}})
        result = _run(tmp_path, old, new)
        assert result["has_breaking"], "enum kısıtı EKLEMEK görünmüyor"
        assert any(c["type"] == "ENUM_CONSTRAINT_ADDED" for c in result["breaking"])

    @pytest.mark.parametrize(
        "tightening",
        [
            {"maxLength": 10},
            {"pattern": "^x$"},
            {"enum": ["A"]},
        ],
        ids=["maxLength", "pattern", "enum-constraint"],
    )
    def test_declaration_downgrades_tightenings(self, tmp_path: Path, tightening: dict) -> None:
        old = _wrap({"properties": {"f": {"type": "string"}}})
        new_prop = {"type": "string", "x-compat-accepted": self.ACCEPT, **tightening}
        result = _run(tmp_path, old, _wrap({"properties": {"f": new_prop}}))
        assert not result["has_breaking"], f"beyanlı daraltma indirilmedi: {result['breaking']}"
        accepted = [c for c in result["non_breaking"] if c.get("accepted")]
        assert accepted, "indirilen değişiklik 'accepted' damgası taşımalı"
        assert "ACCEPTED TIGHTENING" in accepted[0]["message"], (
            "indirme SESSİZ olamaz — gerekçe raporda görünmeli"
        )

    def test_declaration_cannot_downgrade_field_removal(self, tmp_path: Path) -> None:
        old = _wrap({"properties": {"a": {}, "b": {}}})
        new = _wrap({"properties": {"a": {}}, "x-compat-accepted": self.ACCEPT})
        assert _run(tmp_path, old, new)["has_breaking"], (
            "alan SİLME beyanla indirilemez — kaçış deliği açılmış"
        )

    def test_declaration_cannot_downgrade_enum_value_removal(self, tmp_path: Path) -> None:
        old = _wrap({"properties": {"k": {"enum": ["A", "B"]}}})
        new = _wrap({"properties": {"k": {"enum": ["A"], "x-compat-accepted": self.ACCEPT}}})
        assert _run(tmp_path, old, new)["has_breaking"], (
            "enum DEĞERİ silme beyanla indirilemez"
        )

    def test_declaration_cannot_downgrade_new_required_field(self, tmp_path: Path) -> None:
        old = _wrap({"properties": {"a": {}}, "required": []})
        new = _wrap({
            "properties": {"a": {}, "b": {}},
            "required": ["b"],
            "x-compat-accepted": self.ACCEPT,
        })
        assert _run(tmp_path, old, new)["has_breaking"], (
            "`required` genişletme beyanla indirilemez"
        )

    def test_declaration_cannot_downgrade_type_narrowing(self, tmp_path: Path) -> None:
        old = _wrap({"properties": {"d": {"type": ["string", "null"]}}})
        new = _wrap({"properties": {"d": {"type": "string", "x-compat-accepted": self.ACCEPT}}})
        assert _run(tmp_path, old, new)["has_breaking"], "tip DARALTMA beyanla indirilemez"


class TestGateCannotLieSilently:
    """Kapının kendisi çalışamıyorsa bunu SÖYLEMELİ — sessizce 'breaking yok' diyemez."""

    def test_unreadable_schema_is_recorded_not_swallowed(self, tmp_path: Path) -> None:
        old_dir = tmp_path / "old" / "schemas"
        new_dir = tmp_path / "new" / "schemas"
        old_dir.mkdir(parents=True)
        new_dir.mkdir(parents=True)
        (old_dir / "t.json").write_text('{"type": "object"}', encoding="utf-8")
        (new_dir / "t.json").write_text("{ bozuk json", encoding="utf-8")
        detector = BreakingChangeDetector(old_dir, new_dir)
        detector.detect_changes()
        assert detector.load_errors, "okunamayan şema sessizce yutuldu — kapı kör"

    def test_cli_json_output_is_parseable(self, tmp_path: Path) -> None:
        """CI regresyonu: `--json` çıktısı SAF JSON olmalı (banner stderr'e gider).

        Bu düşerse CI'daki `--json > breaking_changes.json` yönlendirmesi yine bozuk
        dosya üretir ve `has_breaking` DAİMA false okunur.
        """
        for side in ("old", "new"):
            (tmp_path / side / "schemas").mkdir(parents=True)
            (tmp_path / side / "schemas" / "t.json").write_text(
                '{"type": "object"}', encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(TOOL), "--old", str(tmp_path / "old"),
             "--new", str(tmp_path / "new"), "--json"],
            capture_output=True, text=True, encoding="utf-8",
        )
        assert proc.returncode == 0, proc.stderr
        parsed = json.loads(proc.stdout)  # banner sızarsa BURADA patlar
        assert parsed["has_breaking"] is False

    def test_cli_exit_code_one_on_breaking(self, tmp_path: Path) -> None:
        (tmp_path / "old" / "schemas").mkdir(parents=True)
        (tmp_path / "new" / "schemas").mkdir(parents=True)
        (tmp_path / "old" / "schemas" / "t.json").write_text(
            '{"properties": {"k": {"enum": ["A", "B"]}}}', encoding="utf-8")
        (tmp_path / "new" / "schemas" / "t.json").write_text(
            '{"properties": {"k": {"enum": ["A"]}}}', encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(TOOL), "--old", str(tmp_path / "old"),
             "--new", str(tmp_path / "new"), "--json"],
            capture_output=True, text=True, encoding="utf-8",
        )
        assert proc.returncode == 1, f"breaking varken çıkış kodu 1 olmalı: {proc.returncode}"

    def test_cli_exit_code_two_when_gate_is_blind(self, tmp_path: Path) -> None:
        """Okunamayan şema → exit 2. CI bunu 'breaking yok' (0) ile karıştırmamalı."""
        (tmp_path / "old" / "schemas").mkdir(parents=True)
        (tmp_path / "new" / "schemas").mkdir(parents=True)
        (tmp_path / "old" / "schemas" / "t.json").write_text('{"type":"object"}', encoding="utf-8")
        (tmp_path / "new" / "schemas" / "t.json").write_text("{ bozuk", encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(TOOL), "--old", str(tmp_path / "old"),
             "--new", str(tmp_path / "new"), "--json"],
            capture_output=True, text=True, encoding="utf-8",
        )
        assert proc.returncode == 2, f"kör kapı exit 2 vermeli: {proc.returncode}"


class TestLiveCanonicalSchema:
    """Sentetik değil, KANONİK dosya üstünde: denetimin yaptığı mutasyonun aynısı."""

    def test_removing_quarantine_caution_is_detected(self, tmp_path: Path) -> None:
        canonical = ROOT / "schemas" / "worker" / "expert_review_queue.v1.schema.json"
        doc = json.loads(canonical.read_text(encoding="utf-8"))
        values = doc["properties"]["escalation_reason"]["enum"]
        assert "QUARANTINE_CAUTION" in values, "kanonik enum değişmiş — testi güncelleyin"

        mutated = json.loads(json.dumps(doc))
        mutated["properties"]["escalation_reason"]["enum"] = [
            v for v in values if v != "QUARANTINE_CAUTION"
        ]
        result = _run(tmp_path, doc, mutated)
        assert result["has_breaking"], (
            "2026-07-31 denetiminin mutasyonu YİNE görünmüyor: escalation_reason'dan "
            "QUARANTINE_CAUTION silmek MAJOR breaking'dir"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
