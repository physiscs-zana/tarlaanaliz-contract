"""ÖD-2 kapısı — **`CalibrationMetadata`'nın iki şema tanımı ayrışamaz.**

NEDEN BU DOSYA VAR (2026-08-01 öz-denetimi, ÖD-2):
    Aynı kavramın iki şema tanımı vardı ve **hiçbir kapı ikisini bağlamıyordu**:

        kanonik : schemas/worker/calibration_metadata.v1.schema.json   (8 alan)
        gömülü  : schemas/worker/analysis_job.v1 → $defs/CalibrationMetadata (4 alan)

    S5+W12 turunda `scale` yalnız **kanonik** dosyaya eklendi. İşi taşıyan belge ise
    `analysis_job.v1`'dir ve o `unevaluatedProperties: false` taşır. Ölçüm (jsonschema ile,
    2026-08-01): `scale` bloğu taşıyan bir iş belgesi

        Unevaluated properties are not allowed ('scale' was unexpected)

    ile **REDDEDİLİYORDU**. Yani W12'de worker'a yazılan okuma kodu
    (`resolve_reflectance_divisor`) veriyi asla göremezdi: sözleşme yarısı ile kod yarısı
    yeşil, **tel ölü**. S4'ün `calibration_method` alanı da aynı delikten düşüyordu.

BU KAPI NE YAPAR:
    ① Kanonikte olup gömülü kopyada olmayan her alan **beyanlı** olmalı (sessiz eksik yasak).
    ② Beyanın kendisi **ölçülür**: alan iş belgesinde başka bir taşıyıcıdaysa o taşıyıcı
       gerçekten var olmalı. Yazılı gerekçe yeterli değildir — gerekçe *doğrulanabilir* olmalı.
    ③ Ortak alanların **doğrulama anlamı** (enum/required/if-then/tip) birebir aynı olmalı;
       yalnız prose (description/$comment/x-*) ayrışabilir (D16 idiomu: tek normatif gövde,
       diğer yerde işaretçi).
    ④ Uçtan uca: `scale` taşıyan gerçek bir iş belgesi **geçmeli**, bozuk ölçek **düşmeli**.
       ③ tek başına yetmez — ÖD-2 tam olarak "şema doğru görünüyordu ama belge reddediliyordu"
       vakasıydı; belge düzeyinde ölçüm o yüzden ayrı bir testtir.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

try:
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource
except ImportError:  # pragma: no cover
    pytest.skip("jsonschema or referencing not installed", allow_module_level=True)

ROOT = Path(__file__).parent.parent
CANONICAL = ROOT / "schemas" / "worker" / "calibration_metadata.v1.schema.json"
JOB = ROOT / "schemas" / "worker" / "analysis_job.v1.schema.json"

#: Gömülü kopyanın taşımadığı alanlar — her biri GEREKÇELİ ve gerekçesi ÖLÇÜLEBİLİR olmalı.
#: `carrier`: iş belgesinde alanı taşıyan yol (JSON pointer). Kapı bu yolun varlığını ölçer.
DECLARED_OMISSIONS: dict[str, dict[str, str]] = {
    "sensor_model": {
        "carrier": "/properties/drone_metadata/properties/sensor_model",
        "why": (
            "ADR-002: worker drone_registry.yaml'ı okumaz; sensör kimliğini platform "
            "`drone_metadata` bloğunda gömer. İş belgesinde alanın ikinci bir kopyası "
            "olsaydı hangi kaynağın kazandığı belirsiz kalırdı."
        ),
    },
    "red_edge_center_nm": {
        "carrier": "/properties/drone_metadata/properties/red_edge_center_nm",
        "why": (
            "Aynı gerekçe: NDRE offset düzeltmesi için gereken dalga boyu sensör "
            "kapasitesidir, kalibrasyon çıktısı değil (worker domain modeli de onu "
            "`DroneMetadata` altında tutar — src/core/domain/analysis_job.py)."
        ),
    },
}

#: Doğrulamaya girmeyen, ayrışmasına İZİN VERİLEN anahtarlar (prose/iz).
ANNOTATION_KEYS = {"description", "title", "$comment", "default", "examples", "deprecated"}


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _canonical_props() -> dict[str, Any]:
    return _load(CANONICAL)["properties"]


def _job_def() -> dict[str, Any]:
    return _load(JOB)["$defs"]["CalibrationMetadata"]


def _job_props() -> dict[str, Any]:
    return _job_def()["properties"]


def _semantics(node: Any) -> Any:
    """Prose ve `x-` uzantılarını atarak yalnız DOĞRULAMA anlamını bırak."""
    if isinstance(node, dict):
        return {
            key: _semantics(value)
            for key, value in node.items()
            if key not in ANNOTATION_KEYS and not key.startswith("x-")
        }
    if isinstance(node, list):
        return [_semantics(value) for value in node]
    return node


def _pointer_exists(doc: Any, pointer: str) -> bool:
    node = doc
    for token in pointer.strip("/").split("/"):
        if not isinstance(node, dict) or token not in node:
            return False
        node = node[token]
    return True


def _validator() -> "Draft202012Validator":
    registry = Registry()
    for search_dir in (ROOT / "schemas", ROOT / "enums"):
        for json_file in search_dir.rglob("*.json"):
            try:
                contents = json.loads(json_file.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):  # pragma: no cover
                continue
            if isinstance(contents, dict) and contents.get("$id"):
                registry = registry.with_resource(
                    contents["$id"], Resource.from_contents(contents)
                )
    return Draft202012Validator(_load(JOB), registry=registry)


def _minimal_job(**calibration: Any) -> dict[str, Any]:
    """`analysis_job.v1`'in `required` alanlarını sağlayan en küçük geçerli belge."""
    return {
        "crop_type": "COTTON",
        "analysis_types": ["PEST"],
        "mission_id": "11111111-1111-4111-8111-111111111111",
        "field_id": "22222222-2222-4222-8222-222222222222",
        "calibration_metadata": {"calibration_type": "ABSOLUTE", **calibration},
    }


class TestNoSilentDivergence:
    """① + ② — eksik alan sessiz olamaz; beyan ölçülebilir olmalı."""

    def test_every_missing_property_is_declared(self) -> None:
        missing = set(_canonical_props()) - set(_job_props())
        undeclared = sorted(missing - set(DECLARED_OMISSIONS))
        assert not undeclared, (
            f"Kanonik `calibration_metadata.v1`'de olup iş belgesinin gömülü kopyasında "
            f"OLMAYAN, beyansız alan(lar): {undeclared}.\n"
            "Bu tam olarak ÖD-2'nin sınıfıdır: alan kanoniğe eklenir, işi TAŞIYAN şemaya "
            "eklenmez, `unevaluatedProperties: false` yüzünden gerçek belge reddedilir ve "
            "tüketici kodu veriyi asla görmez. Alanı buraya taşıyın ya da "
            "DECLARED_OMISSIONS'a ölçülebilir bir gerekçeyle yazın."
        )

    def test_no_job_only_property(self) -> None:
        """Gömülü kopya kendi alanını UYDURAMAZ — kanonik tanım tek kaynaktır."""
        extra = sorted(set(_job_props()) - set(_canonical_props()))
        assert not extra, (
            f"Gömülü kopyada kanonikte olmayan alan(lar): {extra}. Bu bir I-5 sapmasıdır: "
            "kanonik tanım önce değişir, gömülü kopya onu yansıtır."
        )

    def test_declared_omission_is_not_stale(self) -> None:
        """Alan taşınmışsa beyan SİLİNMELİ — liste yalan söylememeli."""
        stale = sorted(set(DECLARED_OMISSIONS) & set(_job_props()))
        assert not stale, (
            f"DECLARED_OMISSIONS bayat — {stale} artık gömülü kopyada mevcut. Beyanı kaldırın."
        )

    @pytest.mark.parametrize("field", sorted(DECLARED_OMISSIONS))
    def test_declared_omission_has_a_real_carrier(self, field: str) -> None:
        """Beyan bir DİLEK değil ÖLÇÜM olmalı: gösterilen taşıyıcı gerçekten var mı?"""
        entry = DECLARED_OMISSIONS[field]
        assert entry["why"].strip(), f"{field}: gerekçe boş"
        assert _pointer_exists(_load(JOB), entry["carrier"]), (
            f"{field}: beyan '{entry['carrier']}' yolunun alanı taşıdığını söylüyor ama o "
            "yol iş belgesinde YOK. Gerekçe ölçülemiyorsa beyan değildir — ya taşıyıcı "
            "eklenmeli ya alan gömülü kopyaya taşınmalı."
        )


class TestSharedPropertiesAreSemanticallyIdentical:
    """③ — ortak alanların doğrulama anlamı birebir; yalnız prose ayrışabilir."""

    @pytest.mark.parametrize(
        "field", sorted(set(_canonical_props()) & set(_job_props()))
    )
    def test_validation_semantics_match(self, field: str) -> None:
        canonical = _semantics(_canonical_props()[field])
        embedded = _semantics(_job_props()[field])
        assert canonical == embedded, (
            f"`{field}` iki tanımda FARKLI doğrulanıyor:\n"
            f"  kanonik : {json.dumps(canonical, sort_keys=True, ensure_ascii=False)}\n"
            f"  gömülü  : {json.dumps(embedded, sort_keys=True, ensure_ascii=False)}\n"
            "Aynı kavramın iki doğrulama kuralı olamaz — biri belgeyi kabul edip diğeri "
            "reddettiğinde hangi tarafın haklı olduğu ölçülemez (D16'nın şema hâli)."
        )

    def test_required_matches(self) -> None:
        canonical = set(_load(CANONICAL).get("required", []))
        embedded = set(_job_def().get("required", []))
        assert canonical == embedded, (
            f"`required` ayrışmış — yalnız kanonikte {sorted(canonical - embedded)}, "
            f"yalnız gömülüde {sorted(embedded - canonical)}"
        )

    def test_both_forbid_field_drift(self) -> None:
        assert _load(CANONICAL).get("unevaluatedProperties") is False
        assert _job_def().get("unevaluatedProperties") is False, (
            "Gömülü kopya alan sürüklenmesine açık kalırsa ÖD-2'nin belirtisi gizlenir: "
            "yanlış yazılmış bir alan reddedilmek yerine sessizce yutulur."
        )


class TestScaleTravelsOnTheWire:
    """④ — asıl iddia belge düzeyinde ölçülür (şema 'doğru görünmesi' yetmez)."""

    def test_job_with_scale_is_accepted(self) -> None:
        errors = sorted(
            _validator().iter_errors(
                _minimal_job(scale={"reflectance_scale": "scaled_int", "scale_factor": 10000})
            ),
            key=lambda e: e.path,
        )
        assert not errors, (
            "Ölçek taşıyan iş belgesi REDDEDİLİYOR: "
            f"{[e.message for e in errors]}. ÖD-2'nin ta kendisi — W12'nin okuma kodu bu "
            "belgeyi hiç görmez."
        )

    def test_job_with_calibration_method_is_accepted(self) -> None:
        errors = list(_validator().iter_errors(_minimal_job(calibration_method="REFLECTANCE_PANEL")))
        assert not errors, (
            f"`calibration_method` taşıyan iş belgesi reddediliyor: {[e.message for e in errors]} "
            "(S4 aynı delikten düşüyordu)."
        )

    def test_scaled_int_without_divisor_is_rejected(self) -> None:
        """`scaled_int` bölensiz anlamsızdır — if/then kuralı gömülü kopyada da yaşamalı."""
        errors = list(_validator().iter_errors(_minimal_job(scale={"reflectance_scale": "scaled_int"})))
        assert errors, (
            "`scaled_int` bölen olmadan KABUL edildi. Kural kanonik dosyada var ama gömülü "
            "kopyaya taşınmamış demektir; worker `resolve_reflectance_divisor` bu durumu "
            "'invalid' sayıp filo varsayılanına düşer — sessiz ölçek hatası geri gelir."
        )

    def test_unknown_scale_name_is_rejected(self) -> None:
        errors = list(
            _validator().iter_errors(_minimal_job(scale={"reflectance_scale": "reflectance_0_255"}))
        )
        assert errors, (
            "Sözlük dışı bir ölçek adı kabul edildi — enum gömülü kopyada daralmış olabilir."
        )

    def test_unknown_calibration_field_is_still_rejected(self) -> None:
        """Kapıyı gevşetmedik: tanımsız alan hâlâ düşmeli."""
        errors = list(_validator().iter_errors(_minimal_job(reflectance_scale="reflectance_0_1")))
        assert errors, (
            "Tanımsız bir kalibrasyon alanı kabul edildi — `unevaluatedProperties: false` "
            "etkisiz kalmış olabilir."
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
