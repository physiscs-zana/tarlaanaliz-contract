"""Kanonik sözlük BAĞLAMA kapısı — "prose var, zorlanabilirlik yok" sınıfı (ratchet).

NEDEN (2026-08-11 denetimi, ÖLÇÜLDÜ):
    `enums/threat_type.enum.v1.json` 15 değerlik kanonik bir tehdit türü sözlüğü
    tanımlıyor. `datasets/scan_report.v1` (KR-073 AV tarama raporu) ise aynı alanı
    `{"type": "string"}` diye tanımlıyordu — yani sözlük VARDI ama şema onu
    **zorlamıyordu**. Gerçek doğrulayıcıyla ölçüldü:

        findings[0].threat_type = "UYDURMA_TEHDIT_TURU"  ->  0 hata

    Bu, deponun 2026-07-31'de `crop_type` için adını koyduğu sınıfın aynısıdır
    (`events/field_created.v1` içindeki `x-compat-accepted` notu): açıklama kanonik
    enum'a *atıf yapıyor*, şema hiçbir şeyi zorlamıyor. O turda tek alan düzeltilmişti;
    sınıfın geri kalanı ölçülmemişti.

BU KAPI NE YAPAR:
    Adı kanonik bir enum dosyasıyla eşleşen HER alanı tarar ve üç kovaya ayırır:
    BAĞLI (`$ref`) · INLINE (`enum` dizisi) · **SERBEST** (hiçbiri).
    SERBEST kova bir **ratchet**tir: yalnız küçülür.
      * baseline'da OLMAYAN yeni bir serbest alan  -> KIRMIZI
      * baseline'da olup artık serbest OLMAYAN     -> KIRMIZI (satırı silin)

NE YAPMAZ — ve neden:
    Bir alanı bağlamak **daraltmadır** ve daraltma üreticiyi kırabilir. Bu kapı
    "hepsini bağla" demez; **görünür ve sayılabilir** kılar. Her baseline satırı
    "ölçülmemiş ya da bilinçli ertelenmiş" demektir. Somut örnek: `quarantine_event`
    `decision` alanı BİLEREK bağlanmadı — edge'in ürettiği sözlük
    ({PASS, QUARANTINE, REJECT}) kanonikle **sıfır kesişimlidir**; bağlamak edge
    çıktısının %100'ünü reddederdi. Bu bir araç değil KARAR sorunudur.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest


ROOT = Path(__file__).parent.parent
SCHEMAS = ROOT / "schemas"
ENUMS = ROOT / "enums"

#: Alan ADI -> kanonik enum gövdesi. Eşleme POLİTİKADIR: bir alanın kanonik bir
#: sözlüğü olduğunu iddia etmek karardır, tahmin değil. Yeni satır eklerken o alanın
#: gerçekten o ekseni taşıdığını ÖLÇÜN (üreticiyi okuyun).
FIELD_TO_ENUM: dict[str, str] = {
    "threat_type": "threat_type",
    "decision": "quarantine_decision",
    "crop_type": "crop_type",
    "analysis_type": "analysis_type",
    "analysis_types": "analysis_type",
    "report_phase": "report_phase",
    "qc_status": "qc_status",
    "scan_stage": "scan_stage",
    "calibration_type": "calibration_type",
    "drone_type": "drone_type",
    "drone_model": "drone_type",
    "phenology_stage": "phenology_stage",
    "dataset_status": "dataset_status",
    "verification_status": "verification_status",
    "payment_method": "payment_method",
    "payment_status": "payment_status",
    "target_type": "payment_target_type",
    "role": "role",
    "roles": "role",
    "user_role": "role",
    "actor_role": "role",
    "radiometric_mode": "radiometric_mode",
    "mission_status": "mission_status",
}

#: 2026-08-11 ÖLÇÜMÜ. Her satır: "kanonik sözlük var ama bu alan onu zorlamıyor".
#: Liste yalnız KÜÇÜLÜR. Bir satırı silmek için alanı bağlayın (`$ref`) ve
#: `x-compat-accepted` ile üretici ölçümünü yazın.
KNOWN_UNBOUND: tuple[tuple[str, str], ...] = (
    ("schemas/core/user.v1.schema.json", "$.properties.roles.items"),
    ("schemas/edge/quarantine_event.v1.schema.json", "$.$defs.DecisionMaker.properties.user_role"),
    # ✅ KARAR VERİLDİ (2026-08-11, edge oturumu + kullanıcı): **BAĞLANMAYACAK** — ve bu
    # bir borç DEĞİL, KAVRAM AYRIMI. edge `decision` AV1'in EYLEM kararı
    # (`{PASS, QUARANTINE, REJECT}`), kanonik enum ise karantina kaydının YAŞAM DÖNGÜSÜ
    # DURUMU. Sıfır kesişim uyumsuzluk değil, iki farklı eksenin işareti.
    # Üç ölçüm bağımsız doğrulandı (bkz. şemadaki gerekçe): edge bu şemayı vendor'lamıyor ·
    # karar platforma `scan_report.v1 → result` üzerinden gidiyor ve kanoniğe TAM uyuyor ·
    # `quarantine_events` tablosuna yazan üretim kodu yok.
    # Satır listede KALIR (alan hâlâ serbest dize) ama artık "ölçülmemiş borç" değil,
    # **gerekçesi yazılı bilinçli karar**. Bağlanması ancak edge ayrı bir `lifecycle_state`
    # alanı yayınlarsa gündeme gelir — o zaman bu satır silinir, `decision` yine bağlanmaz.
    ("schemas/edge/quarantine_event.v1.schema.json", "$.properties.decision"),
    ("schemas/events/analysis_completed.v1.schema.json",
     "$.$defs.AnalysisCompletedData.properties.analysis_type"),
    ("schemas/events/analysis_preliminary_ready.v1.schema.json",
     "$.$defs.AnalysisPreliminaryReadyData.properties.report_phase"),
    ("schemas/events/analysis_review_requested.v1.schema.json",
     "$.$defs.AnalysisReviewRequestedData.properties.analysis_type"),
    ("schemas/events/dataset_ingested.v1.schema.json",
     "$.$defs.DatasetIngestedData.properties.payload.properties.drone_type"),
    ("schemas/events/field_created.v1.schema.json", "$.$defs.Actor.properties.actor_role"),
    ("schemas/events/mission_assigned.v1.schema.json", "$.$defs.Actor.properties.actor_role"),
    ("schemas/events/mission_assigned.v1.schema.json",
     "$.$defs.MissionAssignedData.properties.analysis_types.items"),
    ("schemas/platform/layer_registry.v1.schema.json",
     "$.$defs.LayerStyle.properties.analysis_type"),
    ("schemas/worker/analysis_result.v1.schema.json", "$.properties.analysis_type"),
)


def _enum_files() -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for path in ENUMS.glob("*.json"):
        stem = re.sub(r"\.enum\.v\d+\.json$|\.v\d+\.json$", "", path.name)
        out.setdefault(stem, []).append(path.name)
    return out


def _is_string_value(node: dict) -> bool:
    declared = node.get("type")
    return declared == "string" or (
        isinstance(declared, list) and set(declared) <= {"string", "null"}
    )


def scan() -> dict[str, list[tuple[str, str, str]]]:
    """(bağlı, inline, serbest) — üçü de aynı yürüyüşten çıkar."""
    enum_files = _enum_files()
    result: dict[str, list[tuple[str, str, str]]] = {"bagli": [], "inline": [], "serbest": []}

    def record(rel: str, pointer: str, name: str, node: dict) -> None:
        stem = FIELD_TO_ENUM.get(name)
        if stem is None or stem not in enum_files:
            return
        targets = enum_files[stem]
        ref = node.get("$ref", "")
        if isinstance(ref, str) and any(target in ref for target in targets):
            result["bagli"].append((rel, pointer, stem))
        elif isinstance(node.get("enum"), list):
            result["inline"].append((rel, pointer, stem))
        elif _is_string_value(node):
            result["serbest"].append((rel, pointer, stem))
        elif node.get("type") == "array" and isinstance(node.get("items"), dict):
            items = node["items"]
            if not items.get("$ref") and not isinstance(items.get("enum"), list):
                result["serbest"].append((rel, f"{pointer}.items", stem))

    def walk(node: object, pointer: str, rel: str) -> None:
        if isinstance(node, dict):
            properties = node.get("properties")
            if isinstance(properties, dict):
                for name, child in properties.items():
                    if isinstance(child, dict):
                        record(rel, f"{pointer}.properties.{name}", name, child)
            for key, value in node.items():
                walk(value, f"{pointer}.{key}", rel)
        elif isinstance(node, list):
            for index, value in enumerate(node):
                walk(value, f"{pointer}[{index}]", rel)

    for path in sorted(SCHEMAS.rglob("*.json")):
        walk(json.loads(path.read_text(encoding="utf-8")), "$", path.relative_to(ROOT).as_posix())
    return result


class TestScannerActuallyMeasures:
    """POZİTİF KONTROL — "0 serbest" çıktısı çoğu zaman aracın kusurudur."""

    def test_known_bound_fields_are_detected(self) -> None:
        bagli = {(rel, pointer) for rel, pointer, _ in scan()["bagli"]}
        # ⚠️ Bu işaretçiler TAHMİN EDİLMEZ, ÖLÇÜLÜR. İlk yazımda `EdgeForm` yazmıştım;
        # bu test kırmızı döndü ve gerçek yolun `PlatformForm` olduğunu gösterdi —
        # pozitif kontrolün kendisi bir varsayımı yakaladı.
        beklenen = (
            ("schemas/core/field.v1.schema.json", "$.properties.crop_type"),
            ("schemas/edge/intake_manifest.v1.schema.json",
             "$.$defs.PlatformForm.properties.av_scan_result.properties.findings.items"
             ".properties.threat_type"),
            # bu turda bağlananlar — regresyon kilidi
            ("schemas/datasets/scan_report.v1.schema.json",
             "$.properties.findings.items.properties.threat_type"),
            ("schemas/edge/quarantine_event.v1.schema.json", "$.properties.threat_type"),
        )
        eksik = [item for item in beklenen if item not in bagli]
        assert not eksik, (
            f"Tarayıcı BAĞLI olduğu bilinen alanları göremiyor: {eksik}. "
            "Bu durumda 'serbest alan yok' çıktısı da güvenilmezdir."
        )

    def test_scanner_finds_a_planted_free_field(self) -> None:
        """MUTASYON: serbest bir alan dikildiğinde tarayıcı görmeli."""
        node = {"type": "string", "description": "planted"}
        enum_files = _enum_files()
        assert "threat_type" in enum_files, "kanonik threat_type enum'u yok"
        assert _is_string_value(node), "değer şeması tanınmadı — tarayıcı kör"


class TestUnboundSetOnlyShrinks:
    """RATCHET — sınıf büyüyemez, baseline bayatlayamaz."""

    def test_no_new_unbound_field(self) -> None:
        current = {(rel, pointer) for rel, pointer, _ in scan()["serbest"]}
        yeni = sorted(current - set(KNOWN_UNBOUND))
        assert not yeni, (
            f"{len(yeni)} YENİ serbest dize alanı: kanonik sözlük var ama zorlanmıyor.\n  "
            + "\n  ".join(f"{rel}  {pointer}" for rel, pointer in yeni)
            + "\nYa alanı bağlayın (`$ref` + `x-compat-accepted` ile üretici ölçümü), "
            "ya da bilinçli bir kararsa KNOWN_UNBOUND'a gerekçesiyle ekleyin."
        )

    def test_baseline_has_no_stale_entry(self) -> None:
        current = {(rel, pointer) for rel, pointer, _ in scan()["serbest"]}
        bayat = sorted(set(KNOWN_UNBOUND) - current)
        assert not bayat, (
            f"{len(bayat)} baseline satırı artık SERBEST DEĞİL — bağlanmış ya da "
            "silinmiş olabilir. Bayat baseline, kapının o alanı hâlâ 'borç' sandığı "
            "anlamına gelir; satırları silin:\n  "
            + "\n  ".join(f"{rel}  {pointer}" for rel, pointer in bayat)
        )

    def test_baseline_does_not_grow(self) -> None:
        assert len(KNOWN_UNBOUND) <= 12, (
            f"Baseline {len(KNOWN_UNBOUND)} satır (2026-08-11 ölçümü: 12). Liste yalnız "
            "KÜÇÜLÜR — yeni bir serbest alan buraya eklenerek geçirilemez."
        )


class TestThreatTypeIsActuallyEnforced:
    """DAVRANIŞSAL KANIT — bağlama şemada yazılı olmakla kalmasın, GERÇEKTEN reddetsin.

    Bulgu bu testle ölçülmüştü: aynı belge değişiklik ÖNCESİ 0 hata veriyordu.
    """

    REL = "schemas/datasets/scan_report.v1.schema.json"

    TEMIZ = {
        "report_id": "11111111-1111-4111-8111-111111111111",
        "dataset_id": "22222222-2222-4222-8222-222222222222",
        "scan_stage": "AV1_EDGE",
        "engine_id": "clamav",
        "signatures_version": "27000",
        "started_at": "2026-08-11T10:00:00Z",
        "ended_at": "2026-08-11T10:05:00Z",
        "scanned_files": [{"path": "a.tif", "size_bytes": 10, "sha256": "a" * 64}],
        "result": "FAIL",
        "findings": [{"file": "a.tif", "threat_name": "Eicar-Test-Signature",
                      "threat_type": "MALWARE"}],
        "quarantined": True,
    }

    @staticmethod
    def _validator(rel: str):
        jsonschema = pytest.importorskip("jsonschema")
        referencing = pytest.importorskip("referencing")
        registry = referencing.Registry()
        for tree in ("schemas", "enums"):
            for path in (ROOT / tree).rglob("*.json"):
                try:
                    contents = json.loads(path.read_text(encoding="utf-8"))
                except (json.JSONDecodeError, OSError):
                    continue
                if isinstance(contents, dict) and contents.get("$id"):
                    registry = registry.with_resource(
                        contents["$id"], referencing.Resource.from_contents(contents)
                    )
        return jsonschema.Draft202012Validator(
            json.loads((ROOT / rel).read_text(encoding="utf-8")), registry=registry
        )

    def test_canonical_threat_type_is_accepted(self) -> None:
        """POZİTİF KONTROL — meşru değer hayatta kalmalı."""
        errors = list(self._validator(self.REL).iter_errors(self.TEMIZ))
        assert not errors, [error.message for error in errors]

    def test_invented_threat_type_is_rejected(self) -> None:
        belge = json.loads(json.dumps(self.TEMIZ))
        belge["findings"][0]["threat_type"] = "UYDURMA_TEHDIT_TURU"
        errors = list(self._validator(self.REL).iter_errors(belge))
        assert errors, (
            "Uydurma tehdit TÜRÜ kabul edildi — bağlama etkisiz. 2026-08-11 öncesi "
            "davranış tam buydu: KR-073 tarama raporu serbest metin kabul ediyordu."
        )

    def test_threat_name_stays_free_text(self) -> None:
        """POZİTİF KONTROL — `threat_name` AV motorunun serbest imza adıdır, KISITLANMAZ.

        Bu test olmadan bir sonraki tur `threat_name`'i de enum'a bağlamaya kalkabilir;
        o alanın kanonik sözlüğü YOKTUR (motor imza veritabanından gelir).
        """
        belge = json.loads(json.dumps(self.TEMIZ))
        belge["findings"][0]["threat_name"] = "Win.Trojan.Agent-1234567"
        assert not list(self._validator(self.REL).iter_errors(belge))
