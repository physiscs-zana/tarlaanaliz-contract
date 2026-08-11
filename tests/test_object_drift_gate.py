"""Alan sızması (field drift) kapısı — ağacın TAMAMI, dizi öğeleri dahil.

NEDEN (2026-08-11 denetimi, ÖLÇÜLDÜ):
    `tools/validate.py` yalnız KÖK şemayı ve `$defs` altındaki BİRİNCİ seviye
    object'leri denetliyordu. `schemas/` ağacındaki 310 object düğümünün 79'u o iki
    konumun dışındaydı ve **28'i hiçbir koruma taşımıyordu**. Davranışsal kanıt
    (KR-073 AV tarama raporu, `datasets/scan_report.v1`):

        kök'e tanımsız alan     -> 1 hata   (kapı çalışıyor)
        findings[]'e aynı alan  -> 0 hata   (SESSİZCE GEÇİYOR)

    Yani gözetim zincirinin (chain of custody) dizi öğeleri sözleşmede TANIMSIZ
    alanları kabul ediyordu. İlk tarayıcı ayrıca `"type": ["object", "null"]`
    BİRLEŞİK tiplerini kaçırmıştı (7 düğüm daha) — ölçüm aracının kendi kusuru.

BU DOSYA NE KORUR:
    ① kapının KAPSAMI daralmasın (dizi öğeleri + birleşik tipler + iç içe nesneler),
    ② kapı gerçekten ÖLÇSÜN (dikilmiş ihlal yakalanmalı — mutasyon),
    ③ meşru serbest biçimli düğümler HAYATTA KALSIN (pozitif kontrol),
    ④ parite-kilitli istisna listesi BÜYÜMESİN,
    ⑤ davranışsal kanıt: gerçek doğrulayıcıda dizi öğesine sızma REDDEDİLSİN.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).parent.parent


def _load(module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, ROOT / "tools" / f"{module_name}.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


validate = _load("validate")


def _object_nodes(doc: object, pointer: str = "$"):
    """Ağaçtaki her object düğümü — kapının kullandığı tanımın AYNISI."""
    if isinstance(doc, dict):
        if validate._is_object_node(doc):
            yield pointer, doc
        for key, value in doc.items():
            if key in validate._NON_SCHEMA_KEYS or key.startswith("x-"):
                continue
            yield from _object_nodes(value, f"{pointer}.{key}")
    elif isinstance(doc, list):
        for index, value in enumerate(doc):
            yield from _object_nodes(value, f"{pointer}[{index}]")


class TestEveryObjectDeclaresItsPolicy:
    """① + ② — kapsam ölçülür, sayı ezberlenmez."""

    def test_no_silent_object_in_source_or_publication_tree(self) -> None:
        offenders: list[str] = []
        for tree in ("schemas", "dist/schemas"):
            base = ROOT / tree
            if not base.exists():
                continue
            for path in sorted(base.rglob("*.json")):
                errors = validate._check_object_policy(
                    json.loads(path.read_text(encoding="utf-8")), path
                )
                offenders.extend(errors)
        assert not offenders, (
            f"{len(offenders)} object düğümü sızma politikasını BEYAN ETMİYOR:\n  "
            + "\n  ".join(offenders[:10])
            + "\nBeyansız object, sözleşmede tanımsız alanları sessizce kabul eder."
        )

    def test_gate_sees_array_items(self) -> None:
        """MUTASYON: dizi öğesindeki politikayı kaldır → kapı KIRMIZI dönmeli.

        İlk kapı tam burada kördü; bu test o körlüğün geri gelmesini engeller.
        """
        planted = {
            "type": "object",
            "unevaluatedProperties": False,
            "properties": {
                "files": {
                    "type": "array",
                    "items": {"type": "object", "properties": {"path": {"type": "string"}}},
                }
            },
        }
        errors = validate._check_object_policy(planted, Path("planted.v1.schema.json"))
        assert any("files.items" in error for error in errors), (
            "Dizi öğesindeki beyansız object yakalanmadı — kapı yine `$defs` birinci "
            f"seviyesine körelmiş olabilir. Dönen hatalar: {errors}"
        )

    def test_gate_sees_union_typed_objects(self) -> None:
        """MUTASYON: `"type": ["object", "null"]` — ilk ÖLÇÜMÜM bunu kaçırmıştı."""
        planted = {
            "type": "object",
            "unevaluatedProperties": False,
            "properties": {"bbox": {"type": ["object", "null"], "properties": {}}},
        }
        errors = validate._check_object_policy(planted, Path("planted.v1.schema.json"))
        assert any("bbox" in error for error in errors), (
            f"Birleşik tipli object beyansız geçti: {errors}"
        )

    def test_gate_rejects_a_non_false_unevaluated(self) -> None:
        planted = {
            "type": "object",
            "unevaluatedProperties": False,
            "properties": {"x": {"type": "object", "unevaluatedProperties": True}},
        }
        errors = validate._check_object_policy(planted, Path("planted.v1.schema.json"))
        assert any("must be false" in error for error in errors), errors


class TestLegitimateOpennessSurvives:
    """③ POZİTİF KONTROL — kapı yalnız SESSİZLİĞİ yasaklar, açıklığı değil.

    Bu test olmadan kapı "her object kapansın"a kayabilir ve `metadata` uzantı
    blokları ile keyfi GeoJSON geometrileri yanlışlıkla daraltılırdı.
    """

    def test_declared_open_object_is_accepted(self) -> None:
        planted = {
            "type": "object",
            "unevaluatedProperties": False,
            "properties": {"metadata": {"type": "object", "additionalProperties": True}},
        }
        assert validate._check_object_policy(planted, Path("planted.v1.schema.json")) == []

    def test_real_free_form_nodes_are_still_open(self) -> None:
        """Kanonikte BİLİNÇLİ açık bırakılan düğümler gerçekten açık kalmalı."""
        serbest = [
            ("schemas/core/field.v1.schema.json", ["properties", "metadata"]),
            ("schemas/worker/analysis_result.v1.schema.json", ["properties", "affected_zone"]),
        ]
        for rel, path in serbest:
            node = json.loads((ROOT / rel).read_text(encoding="utf-8"))
            for step in path:
                node = node[step]
            assert node.get("additionalProperties") is True, (
                f"{rel} {'.'.join(path)}: serbest biçimli düğüm kapatılmış. Bu bir KARAR "
                "değişikliğidir — uzantı/geometri alanlarını daraltmak tüketicileri kırar."
            )

    def test_annotation_blocks_are_not_scanned(self) -> None:
        """`examples`/`notes` içindeki veri ŞEMA DEĞİLDİR — yanlış alarm üretmemeli."""
        planted = {
            "type": "object",
            "unevaluatedProperties": False,
            "examples": [{"type": "object", "nested": {"type": "object"}}],
            "notes": {"aciklama": {"type": "object"}},
        }
        assert validate._check_object_policy(planted, Path("planted.v1.schema.json")) == []


class TestParityLockedExceptionStaysNarrow:
    """④ — istisna bir MAZERETTİR; büyümesi kapının kapsamını daraltır."""

    def test_exception_list_has_at_most_one_entry(self) -> None:
        toplam = sum(len(pointers) for pointers in validate._PARITY_LOCKED_OPEN.values())
        assert toplam <= 1, (
            f"Parite-kilitli istisna sayısı {toplam} > 1. Her yeni giriş, kapının o düğümü "
            "artık DENETLEMEDİĞİ anlamına gelir. Eklemeden önce çelişkinin gerçekten "
            "I-4 parite kilidinden geldiğini ÖLÇ (test_vendored_parity kırmızı mı?), "
            "gerekçesini ve ÇIKIŞ KOŞULUNU yaz."
        )

    def test_every_exception_points_at_a_real_node(self) -> None:
        """Bayat istisna, kapının görmediği bir yolu 'korunuyor' sanmaktır."""
        for rel, pointers in validate._PARITY_LOCKED_OPEN.items():
            doc = json.loads((ROOT / rel).read_text(encoding="utf-8"))
            mevcut = {pointer for pointer, _ in _object_nodes(doc)}
            for pointer in pointers:
                assert pointer in mevcut, (
                    f"{rel}: istisna `{pointer}` artık şemada YOK. Bayat istisna kapıyı "
                    "sessizce gevşetir — girişi silin."
                )

    def test_excepted_node_is_in_a_vendored_subset_file(self) -> None:
        """İstisnanın GEREKÇESİ doğrulanır: dosya gerçekten parite çiftinin parçası mı?"""
        sys.path.insert(0, str(ROOT / "tests"))
        import test_vendored_parity as parity  # type: ignore[import-not-found]

        eslesen = {canonical for canonical, _ in parity.SUBSET_PAIRS}
        for rel in validate._PARITY_LOCKED_OPEN:
            assert rel in eslesen, (
                f"{rel} bir SUBSET parite çiftinde DEĞİL — 'parite kilidi' gerekçesi geçersiz. "
                "İstisnayı kaldırın ve düğümü kapatın."
            )


class TestDriftIsActuallyRejectedByAValidator:
    """⑤ DAVRANIŞSAL KANIT — kural şemada yazılı olmakla kalmasın, GERÇEKTEN reddetsin.

    Bulgunun kendisi bu testle ölçülmüştü: aynı payload değişiklik ÖNCESİ geçiyordu.
    """

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
        schema = json.loads((ROOT / rel).read_text(encoding="utf-8"))
        return jsonschema.Draft202012Validator(schema, registry=registry)

    #: KR-073 AV tarama raporu — geçerli asgari belge.
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
        "findings": [{"file": "a.tif", "threat_name": "Eicar", "threat_type": "MALWARE"}],
        "quarantined": True,
    }

    REL = "schemas/datasets/scan_report.v1.schema.json"

    def test_clean_document_is_valid(self) -> None:
        """Temel geçerli olmadan aşağıdaki deltalar anlamsızdır."""
        errors = list(self._validator(self.REL).iter_errors(self.TEMIZ))
        assert not errors, [error.message for error in errors]

    @pytest.mark.parametrize("path", [("findings",), ("scanned_files",)])
    def test_undeclared_field_inside_an_array_item_is_rejected(self, path: tuple) -> None:
        belge = json.loads(json.dumps(self.TEMIZ))
        belge[path[0]][0]["SIZDIRILAN_ALAN"] = "sözleşmede tanımsız"
        errors = list(self._validator(self.REL).iter_errors(belge))
        assert errors, (
            f"`{path[0]}[]` içine dikilen TANIMSIZ alan kabul edildi. Bu tam olarak "
            "2026-08-11'de ölçülen sızmadır: gözetim zinciri belgesi, sözleşmede "
            "olmayan alanı sessizce taşır."
        )

    def test_undeclared_field_at_root_is_still_rejected(self) -> None:
        """Regresyon: kök kapısı zaten çalışıyordu, bozulmasın."""
        belge = json.loads(json.dumps(self.TEMIZ))
        belge["SIZDIRILAN_ALAN"] = "x"
        assert list(self._validator(self.REL).iter_errors(belge))
