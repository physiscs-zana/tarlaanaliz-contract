"""Vendored kopya paritesi — "birebir uyumludur" iddiasının GERÇEK hâli.

Neden bu test var (2026-07-31 denetimi):
    **Dokuz** kanonik şema açıklamasında *"... interface/contracts/... ile **birebir
    uyumludur**"* yazıyordu. Ölçüldü: **9/9'u bayt düzeyinde YANLIŞ.** Ama aynı ölçümde
    9/9'unun `properties` ve `required` kümeleri **birebir aynı** çıktı; tek fark tutarlı
    bir idiom:

        kanonik  : "unevaluatedProperties": false
        vendored : "additionalProperties": false

    9/9'da aynı olması bunun **çürüme değil, bilinçli bir tasarım konvansiyonu** olduğunu
    gösteriyor — yanlış olan şey **iddianın ifadesiydi**. Açıklamalar düzeltildi; bu test
    düzeltilmiş sözleşmeyi (properties + required paritesi) zorlar.

    NOT: ilk düzeltme turunda 6 şema bulunmuştu; `test_no_schema_claims_byte_identity`
    kapısı **kalan 3'ünü yakaladı** (worker: calibration_metadata, expert_feedback,
    expert_review_queue). Kapının kendisi eksik düzeltmeyi bulmuş oldu.

Kapsam notu:
    Bu test **kardeş depoları** okur. CI'da kardeş depo yoksa test ATLANIR (skip) — worker
    drift dedektörüyle aynı desen. Atlanması "geçti" anlamına gelmez; yerel çalıştırmada
    ve çapraz-repo turlarında (C8) koşar.
"""

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
WORKSPACE = ROOT.parent

# (kanonik yol, vendored yol) — açıklamasında parite iddiası taşıyan HER şema burada olmalı.
PARITY_PAIRS = [
    (
        "schemas/edge/attestation_record.v1.schema.json",
        "tarlaanaliz-edge/interface/contracts/schemas/edge/attestation_record.v1.schema.json",
    ),
    (
        "schemas/edge/calibrated_dataset_manifest.v1.schema.json",
        "tarlaanaliz-edge/interface/contracts/schemas/edge/calibrated_dataset_manifest.v1.schema.json",
    ),
    (
        "schemas/edge/evidence_bundle_ref.v1.schema.json",
        "tarlaanaliz-edge/interface/contracts/schemas/edge/evidence_bundle_ref.v1.schema.json",
    ),
    (
        "schemas/edge/upload_receipt.v1.schema.json",
        "tarlaanaliz-edge/interface/contracts/schemas/edge/upload_receipt.v1.schema.json",
    ),
    (
        "schemas/edge/worker_result.v1.schema.json",
        "tarlaanaliz-edge/interface/contracts/schemas/edge/worker_result.v1.schema.json",
    ),
    (
        "schemas/worker/calibrated_dataset.v1.schema.json",
        "tarlaanaliz-worker/interface/contracts/calibrated_dataset.v1.schema.json",
    ),
    (
        "schemas/worker/calibration_metadata.v1.schema.json",
        "tarlaanaliz-worker/interface/contracts/calibration_metadata.v1.schema.json",
    ),
    (
        "schemas/worker/expert_feedback.v1.schema.json",
        "tarlaanaliz-worker/interface/contracts/expert_feedback.v1.schema.json",
    ),
    (
        "schemas/worker/expert_review_queue.v1.schema.json",
        "tarlaanaliz-worker/interface/contracts/expert_review_queue.v1.schema.json",
    ),
]

IDS = [Path(c).name.replace(".v1.schema.json", "") for c, _ in PARITY_PAIRS]


def _pair(canonical_rel: str, vendored_rel: str) -> tuple[dict, dict]:
    vendored = WORKSPACE / vendored_rel
    if not vendored.exists():
        pytest.skip(f"kardeş depo yok: {vendored_rel}")
    canonical = ROOT / canonical_rel
    return (
        json.loads(canonical.read_text(encoding="utf-8")),
        json.loads(vendored.read_text(encoding="utf-8")),
    )


class TestVendoredParity:
    @pytest.mark.parametrize(("canonical", "vendored"), PARITY_PAIRS, ids=IDS)
    def test_properties_match(self, canonical: str, vendored: str) -> None:
        cj, vj = _pair(canonical, vendored)
        cp, vp = set(cj.get("properties", {})), set(vj.get("properties", {}))
        assert cp == vp, (
            f"{Path(canonical).name}: properties ayrışmış — "
            f"yalnız kanonikte {sorted(cp - vp)}, yalnız vendored'da {sorted(vp - cp)}"
        )

    @pytest.mark.parametrize(("canonical", "vendored"), PARITY_PAIRS, ids=IDS)
    def test_required_match(self, canonical: str, vendored: str) -> None:
        cj, vj = _pair(canonical, vendored)
        cr, vr = set(cj.get("required", [])), set(vj.get("required", []))
        assert cr == vr, (
            f"{Path(canonical).name}: required ayrışmış — "
            f"yalnız kanonikte {sorted(cr - vr)}, yalnız vendored'da {sorted(vr - cr)}"
        )

    @pytest.mark.parametrize(("canonical", "vendored"), PARITY_PAIRS, ids=IDS)
    def test_ids_match(self, canonical: str, vendored: str) -> None:
        """`$id` ayrışırsa iki dosya artık aynı sözleşme değildir."""
        cj, vj = _pair(canonical, vendored)
        assert cj["$id"] == vj["$id"]


class TestParityClaimWordingIsHonest:
    """Yanlış iddia geri gelmesin: 'birebir uyumludur' ifadesi yasak."""

    def test_no_schema_claims_byte_identity(self) -> None:
        offenders = []
        for path in list((ROOT / "schemas").rglob("*.json")) + list((ROOT / "enums").glob("*.json")):
            text = path.read_text(encoding="utf-8")
            if "birebir uyumludur" in text:
                offenders.append(str(path.relative_to(ROOT)).replace("\\", "/"))
        assert not offenders, (
            "Şu şemalar vendored kopyayla 'birebir uyumludur' iddiasında bulunuyor, ama ölçüm "
            f"9/9'unun bayt düzeyinde FARKLI olduğunu gösterdi: {offenders}. "
            "Doğru ifade: 'properties + required düzeyinde EŞDEĞERDİR; bayt-özdeşlik BEKLENMEZ'."
        )

    def test_idiom_difference_is_documented(self) -> None:
        """Farkın kaynağı (additionalProperties ↔ unevaluatedProperties) yazılı olmalı."""
        doc = json.loads(
            (ROOT / "schemas/edge/calibrated_dataset_manifest.v1.schema.json").read_text(
                encoding="utf-8"
            )
        )
        desc = doc["description"]
        assert "unevaluatedProperties" in desc and "additionalProperties" in desc, (
            "Parite ifadesi idiom farkını açıklamalı; aksi hâlde bir sonraki denetim bunu "
            "yeniden 'ayrışma' sanır."
        )


class TestCanonicalIdiomIsConsistent:
    """Kanonik taraf `unevaluatedProperties` idiomunu korumalı (validate.py da bunu şart koşar)."""

    @pytest.mark.parametrize(("canonical", "vendored"), PARITY_PAIRS, ids=IDS)
    def test_canonical_uses_unevaluated_properties(self, canonical: str, vendored: str) -> None:
        cj = json.loads((ROOT / canonical).read_text(encoding="utf-8"))
        assert cj.get("unevaluatedProperties") is False, (
            f"{Path(canonical).name}: kanonik şema unevaluatedProperties:false taşımalı"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
