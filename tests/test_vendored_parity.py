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
    Bu test **kardeş depoları** okur. Bu deponun CI'ında kardeş depo checkout edilmez →
    47 test ATLANIR (2026-08-01 ölçümü: `972 passed, 47 skipped, 2 xfailed`).

    **D4-b kararı (2026-08-01) — kapı KARŞI TARAFTA koşar, burada değil.** Ölçüldü:
    bu depo **PUBLIC**, kardeş depoların üçü de (`tarlaanaliz-platform`,
    `tarlaanaliz_worker`, `tarlaanaliz_edgekiosk`) **PRIVATE**. Yani "contract CI'ına
    PAT verip kardeşleri çekmek", private depo anahtarını **public** bir deponun
    Actions ortamına koymak demektir — sır yüzeyini yanlış yöne açar. Ters yön ise
    bedava: kardeş depo CI'ı bu **public** depoyu `GITHUB_TOKEN` ile, ek sır olmadan
    checkout edebilir.

    Yön ayrıca **daha doğru**: vendored kopyayı değiştiren PR kardeş depoda açılır,
    sapma orada ve **üretildiği anda** yakalanır. Bu depodan bakıldığında görülen şey
    kardeş depo `main`'idir — açık PR'daki sapmayı zaten göremez.

    ⇒ Kardeş depo CI'ı bu dosyayı **olduğu gibi** koşar (E17/W10): kendi checkout'unu
    `<workspace>/<depo-adı>/`, bu depoyu `<workspace>/tarlaanaliz-contract/` altına alır
    ve `pytest tests/test_vendored_parity.py` çağırır. Test ikinci kez yazılmaz — tek
    kaynak burasıdır (kardeş depoya kopyalanan bir kapı, D16'nın kapattığı ikili-gövde
    hatasının test hâli olurdu).

    ⚠️ **Kapsam SINIRI:** yalnız açıklamasında parite iddiası taşıyan **9 şema** izlenir.
    `intake_manifest.v1` bu listede **DEĞİLDİR** — kanonik biçim `oneOf[PlatformForm, EdgeForm]`,
    edge vendored kopyası ise **düz (flat)** bir şemadır; ikisi yapısal olarak farklıdır ve
    parite iddiasında bulunmazlar. Bilinen AK-4 sapması (`sorties`, `mission_date` edge'de var
    kanonikte yok) tam da orada yaşar ve **C11** kalemiyle izlenir — bu dosya onu görmez.
"""

import json
from pathlib import Path

import pytest

from release_state import REPIN_PENDING

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


# Açık bir sürüm turunda kanonik, vendored kopyanın ÖNÜNE geçebilir; bu NORMALDİR ve
# C8 release töreninde yayılır (I-1). Ama SESSİZ kalamaz — buraya yazılmak zorundadır.
# Ters yön (vendored ileri) NORMAL DEĞİLDİR: o bir AK-4 sapmasıdır ve sert hata verir.
#
# Biçim: {şema dosya adı: {"properties": {...}, "required": {...}, "why": "..."}}
PENDING_PROPAGATION: dict[str, dict] = {
    "calibrated_dataset_manifest.v1.schema.json": {
        "properties": {"raw_frames"},
        "required": set(),
        "why": "C3′ (KG-0.c seçilmiş ham kareler) — edge vendored kopyaya C8'de yayılır",
    },
    "expert_review_queue.v1.schema.json": {
        "properties": {
            "audit_sample",
            "audit_stratum",
            # KADEME 3 (D12–D15, 2026-07-31) — denetim satırının ÖLÇÜM BÜTÜNLÜĞÜ alanları.
            # Hepsi denetim satırında zorunlu, olağan incelemede opsiyonel; worker vendored
            # kopyasına C8'de yayılır. Worker üreticisi (audit_set_sampler) π_h ve bucket'ı
            # ZATEN hesaplıyor — yayılım, hesaplananı tele koymaktır.
            "tile_id",
            "consensus_participation",
            "audit_selection_rate",
            "audit_rotation_key",
            "audit_bucket",
            "spot_check_suppressed",
        },
        "required": set(),
        "why": (
            "AL-C2 (i.i.d. denetim-modu alanları) — worker vendored kopyaya C8'de yayılır. "
            "⚠️ AYRICA: AL-C1 `escalation_reason`'a additive `AUDIT_SAMPLE` ekledi. Bu kapı "
            "enum DEĞERLERİNİ karşılaştırmaz, ama worker tarafında "
            "tests/contract/test_expert_review_queue_schema.py::TestReasonEnumParity "
            "worker `EscalationReason` enum'unu kanonikle birebir bağlar → worker vendor "
            "edene kadar O TEST KIRMIZI kalır. Bu beklenen ve C8'de kapanır."
        ),
    },
}


def _pending(canonical: str, axis: str) -> set[str]:
    entry = PENDING_PROPAGATION.get(Path(canonical).name)
    return set(entry[axis]) if entry else set()


@pytest.mark.release_gate
@pytest.mark.xfail(
    REPIN_PENDING and bool(PENDING_PROPAGATION),
    strict=True,
    reason=(
        "Tur sürüyor (CONTRACTS_VERSION.md 'Checksum State: PENDING_REPIN') ve yayılım "
        "beyanları henüz açık — C8 töreninde vendored kopyalar senkronlanınca bu liste "
        "boşalır ve test normal GEÇER (strict: erken boşalırsa XPASS = hata)"
    ),
)
def test_pending_propagation_is_empty() -> None:
    """SD7 kapısı: C8 release töreni `PENDING_PROPAGATION`'ı BOŞALTMAK zorundadır.

    Bu liste *"kanonik ileri gitti, vendored kopya henüz almadı"* beyanıdır. Release
    checklist'inde hiç kontrol edilmediği için beyanlar bayatlayabiliyordu (SD7).
    Artık kapı tur durumuna bağlı: tur içinde beklenen kırmızı, **release'de gerçek
    kırmızı** (beyan satırı `pin_version.py` ile silindiği an sertleşir).
    """
    assert not PENDING_PROPAGATION, (
        "C8 release töreninde vendored yayılım tamamlanmadan sürüm yayımlanamaz — "
        f"açık beyanlar: {sorted(PENDING_PROPAGATION)}. "
        "Yayılımı yapın (tools/sync_to_repos.sh + vendored kopyalar) ve beyanları silin."
    )


class TestVendoredParity:
    """Asimetrik kapı: vendored ileri = HATA · kanonik ileri = BEYAN EDİLMİŞ olmalı."""

    @pytest.mark.parametrize(("canonical", "vendored"), PARITY_PAIRS, ids=IDS)
    def test_no_vendored_only_properties(self, canonical: str, vendored: str) -> None:
        """Vendored'da olup kanonikte olmayan alan = AK-4 sapması (I-5: kalıcı olamaz)."""
        cj, vj = _pair(canonical, vendored)
        vendored_only = set(vj.get("properties", {})) - set(cj.get("properties", {}))
        assert not vendored_only, (
            f"{Path(canonical).name}: vendored kopya kanonikten İLERİDE — {sorted(vendored_only)}. "
            "Bu bir AK-4 sapmasıdır; kanonik absorbe etmeli (bkz. C11/sorties emsali)."
        )

    @pytest.mark.parametrize(("canonical", "vendored"), PARITY_PAIRS, ids=IDS)
    def test_canonical_ahead_is_declared(self, canonical: str, vendored: str) -> None:
        """Kanonik ileri olabilir ama SESSİZ olamaz — PENDING_PROPAGATION'da yazılı olmalı."""
        cj, vj = _pair(canonical, vendored)
        ahead = set(cj.get("properties", {})) - set(vj.get("properties", {}))
        undeclared = ahead - _pending(canonical, "properties")
        assert not undeclared, (
            f"{Path(canonical).name}: kanonik ileri ama BEYAN EDİLMEMİŞ — {sorted(undeclared)}. "
            "Ya vendored kopyayı senkronla ya PENDING_PROPAGATION'a gerekçesiyle ekle."
        )

    @pytest.mark.parametrize(("canonical", "vendored"), PARITY_PAIRS, ids=IDS)
    def test_declared_propagation_is_not_stale(self, canonical: str, vendored: str) -> None:
        """C8 yayılımı bittiğinde beyan SİLİNMELİ; liste yalan söylememeli."""
        cj, vj = _pair(canonical, vendored)
        ahead = set(cj.get("properties", {})) - set(vj.get("properties", {}))
        stale = _pending(canonical, "properties") - ahead
        assert not stale, (
            f"{Path(canonical).name}: PENDING_PROPAGATION bayat — {sorted(stale)} artık "
            "vendored kopyada mevcut. Beyanı kaldırın."
        )

    @pytest.mark.parametrize(("canonical", "vendored"), PARITY_PAIRS, ids=IDS)
    def test_required_match(self, canonical: str, vendored: str) -> None:
        """`required` her iki yönde de eşit olmalı — beyan edilen ekler OPSİYONEL olmalıdır."""
        cj, vj = _pair(canonical, vendored)
        cr, vr = set(cj.get("required", [])), set(vj.get("required", []))
        cr -= _pending(canonical, "required")
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
