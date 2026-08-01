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

🔴 ÖD-8 (2026-08-01) — **KAPI KAPSAMI İKİ YÖNDEN DARDI, GENİŞLETİLDİ.** Ölçüldü:

    ① **16 vendored dosyanın yalnız 9'u izleniyordu.** İzlenmeyen 7'nin içinde
       `analysis_job.v1` vardı — ÖD-2'nin (`scale` tel üstünde ölü) tam olarak geçtiği
       delik. Artık **16'sı da** izleniyor.
    ② **Karşılaştırma yalnız ÜST DÜZEY `properties`/`required` idi**; `$defs` ve
       **enum değerleri** hiç ölçülmüyordu. Bu körlükle ölçülen gerçek sapmalar:
         * edge `calibrated_dataset_manifest`: `raw_frames[].band` kanonikte **RGB**
           taşıyor (S7), vendored'da yok — beyansız
         * edge `calibrated_dataset_manifest`: `qc_report.flags` kanonikte 5 değerlik
           sözlük (D7 `crs_mismatch`), vendored'da **kısıtsız string**
         * worker `expert_labeling_card`: vendored `EGE` bölgesini taşıyor — kanonik
           onu **2026-06-26'da GAP-only kapsam kararıyla** çıkardı (`2d77024`)
         * worker `expert_review_queue`: vendored crop_type'ta terk edilmiş 5.x dalının
           meyve ağaçları (APPLE/CHERRY/FIG/PEACH)
         * edge `worker_result`: vendored crop_type **küçük harf** (AK-7/E16)
       Bunların hiçbiri properties/required düzeyinde görünmüyordu.

İKİ KARŞILAŞTIRMA KİPİ (ölçümle belirlendi — tek kip yanlış olurdu):
    * **MIRROR** — vendored kopya aynı sözleşmeyi iddia eder (yapı özdeş): `properties`,
      `required` ve **her pointer'daki enum** eşit olmalı.
    * **SUBSET** — vendored kopya kanoniğin **dar runtime alt kümesidir** (I-4). Ölçüldü:
      `intake_manifest`/`scan_report`/`transfer_batch` kanonikte `oneOf[$defs...]`,
      vendored'da **düz**; `analysis_job`/`analysis_result` vendored'da az sayıda alan
      taşıyor. Burada alan EKSİKLİĞİ normaldir; **çelişki değildir**. Zorlanan kural:
        (a) İKİ TARAFTA DA olan bir `$defs` adı → o alt ağaç **birebir** (vendored o
            tanımı uyguladığını iddia ediyor demektir — ÖD-2 tam burada yaşıyordu),
        (b) vendored'daki her enum değeri, aynı ALAN ADINI taşıyan kanonik enum'ların
            birleşiminde bulunmalı (alt küme daraltabilir, **uyduramaz**),
        (c) vendored'da olup kanonikte olmayan üst düzey alan = AK-4 sapması.
      ⚠️ (b) bilerek KABA: yapı farklı olduğu için pointer eşlemesi yapılamaz, ad
      üzerinden eşleşir. Aynı adın iki farklı sözlüğü varsa birleşim kullanılır — yani
      bu kural değer UYDURMAYI yakalar, yanlış BAĞLAMDA kullanmayı yakalamaz.

Kapsam notu:
    Bu test **kardeş depoları** okur. Bu deponun CI'ında kardeş depo checkout edilmez →
    testler ATLANIR (2026-08-01 ölçümü, kapsam genişlemeden önce: `972 passed,
    47 skipped, 2 xfailed`; genişledikten sonra atlanan sayısı artar — sayı değil
    **gerekçe** beyanlıdır, bkz. `tests/conftest.py`).

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
"""

import json
from pathlib import Path
from typing import Any

import pytest

from release_state import REPIN_PENDING

ROOT = Path(__file__).parent.parent
WORKSPACE = ROOT.parent

# ── MIRROR: yapı özdeş, tam parite iddiası ───────────────────────────────────
# (kanonik yol, vendored yol) — açıklamasında parite iddiası taşıyan HER şema burada olmalı.
MIRROR_PAIRS = [
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
    # ÖD-8 ile eklendi — ölçüldü: yapı özdeş (üst düzey alanlar birebir aynı).
    (
        "schemas/worker/expert_labeling_card.v1.schema.json",
        "tarlaanaliz-worker/interface/contracts/expert_labeling_card.v1.schema.json",
    ),
    (
        "enums/analysis_type.enum.v1.json",
        "tarlaanaliz-worker/interface/contracts/analysis_type.enum.v1.json",
    ),
]

# ── SUBSET: vendored dar alt küme (I-4) — eksiklik normal, ÇELİŞKİ değil ──────
SUBSET_PAIRS = [
    (
        "schemas/worker/analysis_job.v1.schema.json",
        "tarlaanaliz-worker/interface/contracts/analysis_job.v1.schema.json",
    ),
    (
        "schemas/worker/analysis_result.v1.schema.json",
        "tarlaanaliz-worker/interface/contracts/analysis_result.v1.schema.json",
    ),
    (
        "schemas/edge/intake_manifest.v1.schema.json",
        "tarlaanaliz-edge/interface/contracts/schemas/edge/intake_manifest.v1.schema.json",
    ),
    (
        "schemas/edge/scan_report.v1.schema.json",
        "tarlaanaliz-edge/interface/contracts/schemas/edge/scan_report.v1.schema.json",
    ),
    (
        "schemas/edge/transfer_batch.v1.schema.json",
        "tarlaanaliz-edge/interface/contracts/schemas/edge/transfer_batch.v1.schema.json",
    ),
]

#: Geriye dönük ad — mevcut testler ve kardeş depo CI'ı bunu kullanıyor.
PARITY_PAIRS = MIRROR_PAIRS

IDS = [Path(c).name.replace(".v1.schema.json", "").replace(".enum.v1.json", "") for c, _ in MIRROR_PAIRS]
SUBSET_IDS = [Path(c).name.replace(".v1.schema.json", "") for c, _ in SUBSET_PAIRS]

#: Vendored kopyanın izlediği tüm dosyalar — kapsam ölçümü için (ÖD-8).
VENDORED_ROOTS = (
    "tarlaanaliz-edge/interface/contracts",
    "tarlaanaliz-worker/interface/contracts",
)


def _pair(canonical_rel: str, vendored_rel: str) -> tuple[dict, dict]:
    vendored = WORKSPACE / vendored_rel
    if not vendored.exists():
        pytest.skip(f"kardeş depo yok: {vendored_rel}")
    canonical = ROOT / canonical_rel
    return (
        json.loads(canonical.read_text(encoding="utf-8")),
        json.loads(vendored.read_text(encoding="utf-8")),
    )


def _enums_by_pointer(doc: Any) -> dict[str, set]:
    """Belgedeki her `enum` dizisini JSON pointer'ı ile döndür."""
    found: dict[str, set] = {}

    def rec(node: Any, ptr: str) -> None:
        if isinstance(node, dict):
            if isinstance(node.get("enum"), list):
                found[ptr] = set(node["enum"])
            for key, value in node.items():
                rec(value, f"{ptr}/{key}")
        elif isinstance(node, list):
            for index, value in enumerate(node):
                rec(value, f"{ptr}/{index}")

    rec(doc, "")
    return found


#: Prose sayılan anahtarlar (ÖD-10). Doğrulamaya girmezler; taşınmaları yükü şişirir.
PROSE_KEYS = ("description", "$comment", "why", "note", "notes")


def _prose_chars(doc: Any) -> int:
    """Belgedeki prose (açıklama) karakter toplamı."""
    total = 0
    if isinstance(doc, dict):
        for key, value in doc.items():
            if key in PROSE_KEYS and isinstance(value, str):
                total += len(value)
            else:
                total += _prose_chars(value)
    elif isinstance(doc, list):
        for value in doc:
            total += _prose_chars(value)
    return total


def _field_name(pointer: str) -> str:
    """`/$defs/EdgeForm/properties/calibration_type` → `calibration_type`.

    `items` ile biten pointer'larda bir üst adı verir (`.../flags/items` → `flags`).
    """
    tokens = [t for t in pointer.split("/") if t and t not in {"items", "properties", "$defs"}]
    return tokens[-1] if tokens else pointer


def _strip_annotations(node: Any) -> Any:
    """Prose ve `x-` izlerini at; yalnız doğrulama anlamı kalsın (idiom farkı hariç).

    `default` de atılır: JSON Schema'da doğrulama etkisi YOKTUR (ölçüldü — kanonik
    `detection_type` `"default": null` taşıyor, vendored taşımıyor; ikisi de aynı belgeleri
    kabul eder). Bunu fark saymak kapıyı gürültüyle doldurur, sinyali gizler.
    """
    annotation = {
        "description", "title", "$comment", "examples", "deprecated", "$id", "$schema", "default",
    }
    if isinstance(node, dict):
        out = {}
        for key, value in node.items():
            if key in annotation or key.startswith("x-"):
                continue
            # I-4 idiom farkı: vendored `additionalProperties`, kanonik `unevaluatedProperties`.
            out["__no_extra__" if key in {"additionalProperties", "unevaluatedProperties"} else key] = (
                _strip_annotations(value)
            )
        return out
    if isinstance(node, list):
        return [_strip_annotations(value) for value in node]
    return node


# Açık bir sürüm turunda kanonik, vendored kopyanın ÖNÜNE geçebilir; bu NORMALDİR ve
# C8 release töreninde yayılır (I-1). Ama SESSİZ kalamaz — buraya yazılmak zorundadır.
# Ters yön (vendored ileri) NORMAL DEĞİLDİR: o bir AK-4 sapmasıdır ve sert hata verir.
#
# Biçim: {şema dosya adı: {"properties": {...}, "required": {...}, "enums": {pointer: {değer}},
#                          "why": "..."}}
# ✅ C8 (2026-08-01, v7.3.0): BEYAN BOŞALTILDI — yayılım YAPILDI.
#   * edge   `calibrated_dataset_manifest.v1` ← `raw_frames` (C3′/KG-0.c)
#   * worker `expert_review_queue.v1`        ← 8 denetim alanı (AL-C2/D12–D15)
#                                             + `escalation_reason` enum'una `AUDIT_SAMPLE`
#                                               (AL-C1, additive)
#                                             + 5 dallı `allOf` ölçüm-bütünlüğü bloğu
# Yayılım kopyalama DEĞİL, alan taşımadır: vendored idiom (`additionalProperties: false`)
# korundu, kanonikten gelen alt yapılarda `unevaluatedProperties` → `additionalProperties`
# çevrildi (I-4 — vendored kanoniğin dar alt kümesidir, bayt-özdeşlik beklenmez).
#
# ── YENİ TUR (v7.3.0 sonrası) ────────────────────────────────────────────────
PENDING_PROPAGATION: dict[str, dict] = {
    "calibration_metadata.v1.schema.json": {
        # ✅ `scale` (S5) beyandan ÇIKTI: worker W12 turunda hem okuma kodunu yazdı hem
        #    alanı vendor'ladı. Yayılımı C8'e bırakma kararı W12'de DEĞİŞTİ ve sebebi
        #    ölçüldü: vendored şema `additionalProperties: false` olduğu için, alan
        #    olmadan ölçek taşıyan GERÇEK bir belge reddedilirdi — yani sözleşme yarısı
        #    ile kod yarısı ayrı turlara bölünemezdi.
        "properties": {"calibration_method"},
        "required": set(),
        "enums": {"/properties/calibration_method"},
        "why": (
            "S4 (2026-08-01) — kalibrasyon MEKANİZMASI. Ölçüldü: `calibration_method` alanı "
            "platform/edge/datasets/events şemalarında VARDI ama worker'ın gördüğü yolda "
            "YOKTU; worker `ABSOLUTE` ile `PANEL_ABSOLUTE`'u ayırt edebiliyor ama hangi "
            "mekanizmayla (panel / irradyans / ampirik çizgi) kalibre edildiğini bilemiyordu "
            "— S5 ile birebir aynı desen. Sözlük `datasets/calibration_certificate.v1` ve "
            "`edge/calibration_result.v1` ile aynıdır (yeni ad icat edilmedi).\n\n"
            "⚠️ Yayılım C8'e bırakıldı çünkü S5'ten FARKLI olarak worker'da bu alanı OKUYAN "
            "bir tüketici henüz yok: K-3 fine-tuning uygunluğu bugün `calibration_type`'tan "
            "türetiliyor. Alanı okuyacak kod yazılmadan vendor'lamak ölü alan taşımaktır. "
            "Okuma tarafı ayrı kalem olarak plana yazıldı."
        ),
    },
    # ── ÖD-8 ile GÖRÜNÜR OLAN beyanlar: enum ekseni daha önce hiç ölçülmüyordu ──
    "calibrated_dataset_manifest.v1.schema.json": {
        "properties": set(),
        "required": set(),
        "enums": {
            "/properties/calibration_result/properties/calibration_type",
            "/properties/raw_frames/items/properties/band",
            "/properties/qc_report/properties/flags/items",
        },
        "why": (
            "Üç kanonik daraltma/genişletme edge vendored kopyasına henüz taşınmadı ve "
            "ÖD-8'e kadar **hiçbir kapı bunu göremiyordu** (parite yalnız üst düzey "
            "`properties`/`required` ölçüyordu):\n"
            "• `calibration_type` ← `PANEL_ABSOLUTE` (C6b/S2, 2026-08-01): intake bu değeri "
            "  zaten kabul ediyordu; kalibre manifestte yazılamaması aynı istasyonun iki "
            "  belgesi arasında sessiz daralmaydı.\n"
            "• `raw_frames[].band` ← `RGB` (S7): kompozit kare artık AÇIKÇA işaretlenebilir; "
            "  vendored kopya hâlâ yokluğu iki anlama gelen eski sözlükte.\n"
            "• `qc_report.flags` ← 5 değerlik sözlük (D7 `crs_mismatch` dâhil): vendored "
            "  tarafta alan hâlâ KISITSIZ string; edge yazdığı bayrağı uydurabilir.\n"
            "Üçü de additive/daraltma ve edge'de üretici yok (ölçüldü) → C8 töreninde yayılır."
        ),
    },
    # ✅ `analysis_job.v1.schema.json` beyanı **SİLİNDİ** (2026-08-01, aynı gün):
    #    ÖD-2'nin worker yarısı **W13** ile kapandı — vendored `$defs/CalibrationMetadata`
    #    artık `scale` + `calibration_method` taşıyor (worker PR #187, KR-041 hash
    #    f1447fb6… → 66747d4a…) ve `job_handler.py:136` ölçek taşıyan işi kabul ediyor.
    #    Beyan yerinde bırakılsaydı **liste yalan söylerdi**: "kanonik ileri, vendored
    #    almadı" derken ikisi de aynı yüzeyi taşıyor olurdu. Bayat beyan, gerçek bir
    #    gecikmeyi gizleyecek gürültüdür — bu yüzden aşağıdaki `defs` bayatlık kapısı
    #    da bu turda yazıldı (SUBSET çiftlerinde beyanın bayatlığını hiçbir kapı
    #    ölçmüyordu; bunu ancak elle fark ettim).
}

#: 🔴 VENDORED İLERİ — I-5'e göre KALICI OLAMAZ, ama bugün var ve ÖLÇÜLDÜ (ÖD-8).
#: Her giriş bir BORÇTUR: nereye ait olduğu ve hangi plan kalemiyle kapanacağı yazılı.
#: Liste BÜYÜYEMEZ (`test_vendored_ahead_debt_does_not_grow`).
KNOWN_VENDORED_AHEAD: dict[str, dict] = {
    "expert_labeling_card.v1.schema.json": {
        "enums": {
            "/properties/endemic_regions/items": {"EGE"},
            "/properties/tr_resistance_notes/items/properties/region": {"EGE"},
        },
        "why": (
            "Kanonik bölge sözlüğü **GAP-only kapsam kararıyla** daraltıldı "
            "(`2d77024`, 2026-06-26: *'fix region leakage in ported examples "
            "(Aegean coords/ids → neutral GAP)'*). Worker'ın vendored kopyası `EGE`'yi "
            "taşımaya devam ediyor → worker `EGE` etiketli bir kart üretirse kanonik "
            "şema onu REDDEDER. Kapanış: worker deposunda değerin kaldırılması (W-kalemi) "
            "— kanonik absorbe ETMEZ, çünkü kapsam kararı bilinçlidir."
        ),
    },
    "expert_review_queue.v1.schema.json": {
        "enums": {
            "/properties/crop_type": {"APPLE", "CHERRY", "FIG", "PEACH"},
        },
        "why": (
            "Terk edilmiş worker 5.x dalından kalan meyve ağaçları. Kanonik `crop_type` "
            "GAP 8-ürün kümesidir (aynı `2d77024` kararı: *'Aegean CHERRY/FIG/APPLE/PEACH "
            "not adopted'*). Devir notunda 2026-07-05'ten beri *'ayrıca hizalanacak'* diye "
            "işaretli ama hiçbir kapı ölçmüyordu. Kapanış: worker deposu (W-kalemi)."
        ),
    },
    "worker_result.v1.schema.json": {
        "enums": {
            "/properties/crop_type": {"corn", "cotton", "grape", "pistachio", "rice"},
        },
        "why": (
            "AK-7 / **E16**: edge ürün sözlüğü küçük harf, kanonik tel-üstü sözlük BÜYÜK "
            "harf. Plan kalemi zaten açık (E16 — edge deposu); burada ölçülür ve kapanınca "
            "bu giriş silinir. ⚠️ Sıra kilidi: platform P1 (`enforce=True`) E16'dan ÖNCE "
            "açılırsa edge çıktısı runtime'da reddedilir. NOT: bu bir EKLEME değil "
            "**değiştirme** — aynı pointer'da kanonik de 'ileri' görünür (8 BÜYÜK harf "
            "değer vendored'da yok). Tek borç, iki yön: E16 ikisini birden kapatır."
        ),
    },
    "intake_manifest.v1.schema.json": {
        "enums": {
            "/properties/sorties/items/properties/crop_type": {
                "corn", "cotton", "grape", "pistachio", "rice",
            },
        },
        "why": (
            "Aynı E16 sınıfı, ikinci dosya: `sorties[].crop_type` üreticisi de küçük harf "
            "yazıyor (C11 absorpsiyonunda kanonik BÜYÜK harfe çevrildi, vendored kopya "
            "eski sözlükte kaldı). E16 kalemi bu iki dosyayı BİRLİKTE kapatmalı — yalnız "
            "`worker_result` düzeltilirse edge içinde iki ayrı sözlük kalır."
        ),
    },
}

#: Vendored formun kanonikten DAR olması TASARIM GEREĞİ olan yerler (kalıcı, I-4).
#: `PENDING_PROPAGATION` geçici borç içindir; burası "bu hiç yayılmayacak" beyanıdır.
DECLARED_NARROWER_DEFS: dict[str, dict[str, str]] = {
    "analysis_result.v1.schema.json": {
        "Detection": (
            "Worker bu şemayı KENDİ ÇIKTISINI doğrulamak için kullanır (SWE-12 outbound "
            "validation). Vendored form 17 alan taşıyor, kanonik 24 — eksik 7'si "
            "(`area_hectares`, `class`, `description`, `detection_id`, `geometry`, "
            "`severity`, `type`) worker'ın ÜRETMEDİĞİ alanlar. Ölçüldü: vendored `required` "
            "kanonikten GENİŞ (`class_id`, `class_name`, `risk_level` de zorunlu) — yani "
            "worker kendine daha SIKI davranıyor; ürettiği her belge kanoniği de geçer. "
            "Bu yön güvenlidir. ⚠️ Ters yön (analysis_job) güvenli DEĞİLDİR: orada vendored "
            "kopya GELEN belgeyi doğrular, eksik alan geçerli işi REDDEDER (ÖD-2)."
        ),
    },
}


def _pending(canonical: str, axis: str) -> set[str]:
    entry = PENDING_PROPAGATION.get(Path(canonical).name)
    return set(entry.get(axis, set())) if entry else set()


def _known_ahead(canonical: str, pointer: str) -> set:
    entry = KNOWN_VENDORED_AHEAD.get(Path(canonical).name)
    return set(entry.get("enums", {}).get(pointer, set())) if entry else set()


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

    @pytest.mark.parametrize(("canonical", "vendored"), MIRROR_PAIRS, ids=IDS)
    def test_no_vendored_only_properties(self, canonical: str, vendored: str) -> None:
        """Vendored'da olup kanonikte olmayan alan = AK-4 sapması (I-5: kalıcı olamaz)."""
        cj, vj = _pair(canonical, vendored)
        vendored_only = set(vj.get("properties", {})) - set(cj.get("properties", {}))
        assert not vendored_only, (
            f"{Path(canonical).name}: vendored kopya kanonikten İLERİDE — {sorted(vendored_only)}. "
            "Bu bir AK-4 sapmasıdır; kanonik absorbe etmeli (bkz. C11/sorties emsali)."
        )

    @pytest.mark.parametrize(("canonical", "vendored"), MIRROR_PAIRS, ids=IDS)
    def test_canonical_ahead_is_declared(self, canonical: str, vendored: str) -> None:
        """Kanonik ileri olabilir ama SESSİZ olamaz — PENDING_PROPAGATION'da yazılı olmalı."""
        cj, vj = _pair(canonical, vendored)
        ahead = set(cj.get("properties", {})) - set(vj.get("properties", {}))
        undeclared = ahead - _pending(canonical, "properties")
        assert not undeclared, (
            f"{Path(canonical).name}: kanonik ileri ama BEYAN EDİLMEMİŞ — {sorted(undeclared)}. "
            "Ya vendored kopyayı senkronla ya PENDING_PROPAGATION'a gerekçesiyle ekle."
        )

    @pytest.mark.parametrize(("canonical", "vendored"), MIRROR_PAIRS, ids=IDS)
    def test_declared_propagation_is_not_stale(self, canonical: str, vendored: str) -> None:
        """C8 yayılımı bittiğinde beyan SİLİNMELİ; liste yalan söylememeli."""
        cj, vj = _pair(canonical, vendored)
        ahead = set(cj.get("properties", {})) - set(vj.get("properties", {}))
        stale = _pending(canonical, "properties") - ahead
        assert not stale, (
            f"{Path(canonical).name}: PENDING_PROPAGATION bayat — {sorted(stale)} artık "
            "vendored kopyada mevcut. Beyanı kaldırın."
        )

    @pytest.mark.parametrize(("canonical", "vendored"), MIRROR_PAIRS, ids=IDS)
    def test_required_match(self, canonical: str, vendored: str) -> None:
        """`required` her iki yönde de eşit olmalı — beyan edilen ekler OPSİYONEL olmalıdır."""
        cj, vj = _pair(canonical, vendored)
        cr, vr = set(cj.get("required", [])), set(vj.get("required", []))
        cr -= _pending(canonical, "required")
        assert cr == vr, (
            f"{Path(canonical).name}: required ayrışmış — "
            f"yalnız kanonikte {sorted(cr - vr)}, yalnız vendored'da {sorted(vr - cr)}"
        )

    @pytest.mark.parametrize(("canonical", "vendored"), MIRROR_PAIRS, ids=IDS)
    def test_ids_match(self, canonical: str, vendored: str) -> None:
        """`$id` ayrışırsa iki dosya artık aynı sözleşme değildir."""
        cj, vj = _pair(canonical, vendored)
        assert cj["$id"] == vj["$id"]


class TestEnumSurfaceParity:
    """🔴 ÖD-8 — enum DEĞERLERİ de ölçülür; sözlük sapması artık görünür."""

    @pytest.mark.parametrize(("canonical", "vendored"), MIRROR_PAIRS, ids=IDS)
    def test_vendored_invents_no_enum_value(self, canonical: str, vendored: str) -> None:
        """Vendored, kanonikte OLMAYAN bir değeri kabul edemez (AK-4'ün enum hâli)."""
        cj, vj = _pair(canonical, vendored)
        ce, ve = _enums_by_pointer(cj), _enums_by_pointer(vj)
        offenders: dict[str, list] = {}
        for pointer, values in ve.items():
            extra = values - ce.get(pointer, set()) - _known_ahead(canonical, pointer)
            if extra and pointer in ce:
                offenders[pointer] = sorted(extra, key=str)
        assert not offenders, (
            f"{Path(canonical).name}: vendored kopya kanonikte OLMAYAN enum değerleri "
            f"kabul ediyor: {offenders}.\n"
            "Bu bir AK-4 sapmasıdır ve tel üstünde iki yönlü kırılır: vendored o değeri "
            "ÜRETİRSE kanonik doğrulama reddeder. Ya kanonik absorbe etmeli ya kardeş "
            "depo değeri kaldırmalı (bilinçli borçsa KNOWN_VENDORED_AHEAD'e gerekçesiyle "
            "yazılır)."
        )

    @pytest.mark.parametrize(("canonical", "vendored"), MIRROR_PAIRS, ids=IDS)
    def test_canonical_enum_ahead_is_declared(self, canonical: str, vendored: str) -> None:
        """Kanonik sözlük ilerlediyse (değer eklendi ya da kısıt kondu) BEYAN edilmeli.

        Bir pointer `KNOWN_VENDORED_AHEAD`'de yazılıysa burada TEKRAR sayılmaz: sözlüğün
        DEĞİŞTİĞİ (küçük→BÜYÜK harf gibi) durumlarda aynı borç iki yönde birden görünür ve
        iki ayrı satır olarak raporlamak listeyi şişirip tek işi iki iş gibi gösterir.
        """
        cj, vj = _pair(canonical, vendored)
        ce, ve = _enums_by_pointer(cj), _enums_by_pointer(vj)
        declared = _pending(canonical, "enums")
        debt_pointers = set(KNOWN_VENDORED_AHEAD.get(Path(canonical).name, {}).get("enums", {}))
        undeclared: dict[str, list] = {}
        for pointer, values in ce.items():
            if pointer in declared or pointer in debt_pointers:
                continue
            missing = values - ve.get(pointer, set())
            if missing:
                undeclared[pointer] = sorted(missing, key=str)
        assert not undeclared, (
            f"{Path(canonical).name}: kanonik enum ileri ama BEYAN EDİLMEMİŞ: {undeclared}.\n"
            "Bu tam olarak ÖD-8'in kapattığı kör nokta: `properties` eşit olduğu için kapı "
            "yeşil kalıyordu, oysa vendored kopya kanonik sözlüğün eskisini zorluyordu."
        )

    @pytest.mark.parametrize(("canonical", "vendored"), MIRROR_PAIRS, ids=IDS)
    def test_declared_enum_propagation_is_not_stale(self, canonical: str, vendored: str) -> None:
        cj, vj = _pair(canonical, vendored)
        ce, ve = _enums_by_pointer(cj), _enums_by_pointer(vj)
        stale = sorted(
            pointer
            for pointer in _pending(canonical, "enums")
            if not (ce.get(pointer, set()) - ve.get(pointer, set()))
        )
        assert not stale, (
            f"{Path(canonical).name}: enum beyanı bayat — {stale} artık vendored kopyada "
            "senkron. Beyanı kaldırın."
        )


class TestSubsetPairsMayOmitButNotContradict:
    """SUBSET kipi — dar alt küme olmak ÇELİŞME hakkı vermez (ÖD-8)."""

    @pytest.mark.parametrize(("canonical", "vendored"), SUBSET_PAIRS, ids=SUBSET_IDS)
    def test_shared_defs_do_not_contradict(self, canonical: str, vendored: str) -> None:
        """İki tarafta da tanımlı bir `$defs` — dar olabilir, ÇELİŞEMEZ.

        Ölçümle belirlenen üç kural (tek kural yanlış olurdu — bkz. `Detection` emsali):
          (a) ortak alanların doğrulama anlamı AYNI,
          (b) vendored alan UYDURAMAZ,
          (c) vendored `required` kanoniği KAPSAMALI — daha sıkı olmak serbest (ürettiği
              belge kanoniği de geçer), daha GEVŞEK olmak kanoniğin zorunlu kıldığı alanı
              atlatır.
        """
        cj, vj = _pair(canonical, vendored)
        cd, vd = cj.get("$defs", {}), vj.get("$defs", {})
        problems: list[str] = []
        for name in sorted(set(cd) & set(vd)):
            cprops, vprops = cd[name].get("properties", {}), vd[name].get("properties", {})
            for field in sorted(set(cprops) & set(vprops)):
                if _strip_annotations(cprops[field]) != _strip_annotations(vprops[field]):
                    problems.append(f"{name}.{field}: doğrulama anlamı farklı")
            invented = sorted(set(vprops) - set(cprops))
            if invented:
                problems.append(f"{name}: vendored uydurma alan {invented}")
            looser = sorted(set(cd[name].get("required", [])) - set(vd[name].get("required", [])))
            if looser:
                problems.append(f"{name}: vendored `required` GEVŞEK — kanonikte zorunlu {looser}")
        assert not problems, (
            f"{Path(canonical).name}: ortak `$defs` çelişiyor:\n  " + "\n  ".join(problems)
        )

    @pytest.mark.parametrize(("canonical", "vendored"), SUBSET_PAIRS, ids=SUBSET_IDS)
    def test_closed_vendored_def_carries_every_canonical_property(
        self, canonical: str, vendored: str
    ) -> None:
        """🔴 ÖD-2'nin tam kuralı: **KAPALI** bir vendored form eksik alan taşıyamaz.

        `additionalProperties: false` (ya da `unevaluatedProperties: false`) taşıyan bir
        kopya, kanonikte var olan bir alanı ATLARSA artık "dar alt küme" değildir —
        kanoniğin KABUL ettiği belgeyi **REDDEDEN** bir kapıdır. ÖD-2 tam buydu:
        `analysis_job → $defs/CalibrationMetadata` kapalıydı ve `scale` taşımıyordu, yani
        platform ölçek yazdığı anda iş worker'ın kapısında düşecekti.

        İki beyan mekanizması:
          * `PENDING_PROPAGATION[...]['defs']` → GEÇİCİ (C8'de yayılır, liste boşalır)
          * `DECLARED_NARROWER_DEFS`           → KALICI (worker o alanı hiç üretmez)
        """
        cj, vj = _pair(canonical, vendored)
        cd, vd = cj.get("$defs", {}), vj.get("$defs", {})
        pending = set(PENDING_PROPAGATION.get(Path(canonical).name, {}).get("defs", set()))
        permanent = set(DECLARED_NARROWER_DEFS.get(Path(canonical).name, {}))
        offenders: dict[str, list] = {}
        for name in sorted(set(cd) & set(vd)):
            if name in pending or name in permanent:
                continue
            closed = vd[name].get("additionalProperties") is False or (
                vd[name].get("unevaluatedProperties") is False
            )
            if not closed:
                continue
            missing = sorted(set(cd[name].get("properties", {})) - set(vd[name].get("properties", {})))
            if missing:
                offenders[name] = missing
        assert not offenders, (
            f"{Path(canonical).name}: KAPALI vendored `$defs` kanonik alanları taşımıyor: "
            f"{offenders}.\nBu form, kanoniğin geçerli saydığı belgeyi reddeder. Ya alanı "
            "taşıyın, ya PENDING_PROPAGATION['defs'] (geçici) ya DECLARED_NARROWER_DEFS "
            "(kalıcı, gerekçeli) ile beyan edin."
        )

    @pytest.mark.parametrize(("canonical", "vendored"), SUBSET_PAIRS, ids=SUBSET_IDS)
    def test_vendored_values_exist_in_canonical_vocabulary(
        self, canonical: str, vendored: str
    ) -> None:
        """Alan adı bazlı KABA eşleme: vendored bir değer UYDURAMAZ (bkz. modül docstring'i)."""
        cj, vj = _pair(canonical, vendored)
        canonical_by_field: dict[str, set] = {}
        for pointer, values in _enums_by_pointer(cj).items():
            canonical_by_field.setdefault(_field_name(pointer), set()).update(values)

        offenders: dict[str, list] = {}
        for pointer, values in _enums_by_pointer(vj).items():
            field = _field_name(pointer)
            if field not in canonical_by_field:
                continue  # kanonikte o ad için hiç enum yok → kıyas tabanı yok
            extra = values - canonical_by_field[field] - _known_ahead(canonical, pointer)
            if extra:
                offenders[pointer] = sorted(extra, key=str)
        assert not offenders, (
            f"{Path(canonical).name}: vendored kopya kanonik sözlükte OLMAYAN değer(ler) "
            f"kabul ediyor: {offenders}. Dar alt küme daraltabilir, değer UYDURAMAZ (I-4/I-5)."
        )

    @pytest.mark.parametrize(("canonical", "vendored"), SUBSET_PAIRS, ids=SUBSET_IDS)
    def test_declared_def_propagation_is_not_stale(self, canonical: str, vendored: str) -> None:
        """Yayılım bittiğinde `defs` beyanı SİLİNMELİ — liste yalan söylemesin.

        Bu kapı 2026-08-01'de **eksikliği elle fark edildiği için** yazıldı: W13 worker
        vendored kopyasını senkronladıktan sonra `PENDING_PROPAGATION['analysis_job']`
        beyanı bayatladı ve hiçbir test bunu görmedi (bayatlık kapıları yalnız MIRROR
        çiftlerinin `properties`/`enums` eksenini ölçüyordu). Bayat beyan, gerçek bir
        gecikmeyi gizleyen gürültüdür.
        """
        cj, vj = _pair(canonical, vendored)
        cd, vd = cj.get("$defs", {}), vj.get("$defs", {})
        declared = set(PENDING_PROPAGATION.get(Path(canonical).name, {}).get("defs", set()))
        stale = sorted(
            name
            for name in declared
            if name in cd and name in vd
            and not (set(cd[name].get("properties", {})) - set(vd[name].get("properties", {})))
        )
        assert not stale, (
            f"{Path(canonical).name}: `defs` beyanı bayat — {stale} artık vendored kopyada "
            "senkron. Beyanı kaldırın (C8 kontrol listesi bu listeyi boş görmek ister)."
        )

    @pytest.mark.parametrize(("canonical", "vendored"), SUBSET_PAIRS, ids=SUBSET_IDS)
    def test_no_vendored_only_top_level_property(self, canonical: str, vendored: str) -> None:
        """Düz vendored biçim, kanonikte HİÇBİR yerde olmayan bir alan taşıyamaz."""
        cj, vj = _pair(canonical, vendored)
        canonical_fields = set(cj.get("properties", {}))
        for definition in cj.get("$defs", {}).values():
            canonical_fields |= set(definition.get("properties", {}))
        extra = sorted(set(vj.get("properties", {})) - canonical_fields)
        assert not extra, (
            f"{Path(canonical).name}: vendored kopyada kanoniğin HİÇBİR formunda olmayan "
            f"alan(lar): {extra} — AK-4 sapması."
        )


class TestVendoredCopiesStayLean:
    """ÖD-10 — vendored kopya kanoniğin DAR alt kümesidir; prose de kırpılır.

    NEDEN (C8, 2026-08-01): kanonikten vendored'a **12 KB prose** taşındı ve worker'da
    **45 test** Windows cp1254 altında kırıldı. Tetikleyici düzeltildi ama *"16 dosyanın
    13'ü hâlâ şişkin olabilir"* varsayımı ölçülmemişti.

    **ÖLÇÜLDÜ (2026-08-01) — varsayım büyük ölçüde ÇÜRÜDÜ:** hiçbir vendored dosya
    kanoniğinden fazla prose taşımıyor (0/16); vendored toplam prose 37.336 karakter,
    kanonik 71.490 (≈%52). Kalan risk yükte değil **okuyucuda**: kodlamasız `open()`
    (worker `contract_validator.py:233` — **W11**, hâlâ açık).

    Bu kapı olayın tam şeklini yasaklar: kanonik prose'u toptan vendored'a taşımak.
    """

    @pytest.mark.parametrize(
        ("canonical", "vendored"), MIRROR_PAIRS + SUBSET_PAIRS, ids=IDS + SUBSET_IDS
    )
    def test_vendored_prose_does_not_exceed_canonical(self, canonical: str, vendored: str) -> None:
        cj, vj = _pair(canonical, vendored)
        canonical_prose, vendored_prose = _prose_chars(cj), _prose_chars(vj)
        assert vendored_prose <= canonical_prose, (
            f"{Path(canonical).name}: vendored kopya kanonikten FAZLA prose taşıyor "
            f"({vendored_prose} > {canonical_prose}). I-4 gereği vendored dar alt kümedir; "
            "prose işaretçiye indirilir. C8'de bu kural çiğnendiğinde 45 test cp1254'te "
            "kırılmıştı."
        )


class TestVendoredAheadDebtIsBounded:
    """Borç listesi bir MAZERET değil, ÖLÇÜLEN ve KÜÇÜLEN bir listedir."""

    #: 2026-08-01 ÖLÇÜMÜ (tahmin değil): EGE ×2 pointer · meyve ağaçları ×4 değer ·
    #: küçük harf crop_type ×5 değer, İKİ dosyada (worker_result + intake_manifest.sorties).
    #: Toplam 4 dosya girişi / 5 pointer / 16 değer.
    MEASURED_DEBT_VALUES = 16

    def test_debt_does_not_grow(self) -> None:
        total = sum(
            len(values)
            for entry in KNOWN_VENDORED_AHEAD.values()
            for values in entry.get("enums", {}).values()
        )
        assert total <= self.MEASURED_DEBT_VALUES, (
            f"KNOWN_VENDORED_AHEAD büyümüş ({total} > {self.MEASURED_DEBT_VALUES}). Yeni bir "
            "vendored-ileri sapma borç listesine EKLENEREK geçirilemez; ya kanonik absorbe "
            "eder ya kardeş depo düzeltir. Borç yalnız KÜÇÜLÜR — küçüldüğünde bu sayı da "
            "düşürülür (aksi hâlde eşik, kapanan borcun yerine yenisini almaya izin verir)."
        )

    @pytest.mark.parametrize("name", sorted(KNOWN_VENDORED_AHEAD))
    def test_each_debt_entry_has_a_reason(self, name: str) -> None:
        assert KNOWN_VENDORED_AHEAD[name]["why"].strip(), f"{name}: gerekçe boş"

    @pytest.mark.parametrize("name", sorted(KNOWN_VENDORED_AHEAD))
    def test_debt_entry_is_not_stale(self, name: str) -> None:
        """Kardeş depo düzelttiyse giriş SİLİNMELİ — liste yalan söylememeli."""
        pairs = {Path(c).name: (c, v) for c, v in MIRROR_PAIRS + SUBSET_PAIRS}
        canonical_rel, vendored_rel = pairs[name]
        cj, vj = _pair(canonical_rel, vendored_rel)
        ve = _enums_by_pointer(vj)
        ce = _enums_by_pointer(cj)
        stale = {
            pointer: sorted(values, key=str)
            for pointer, values in KNOWN_VENDORED_AHEAD[name]["enums"].items()
            if not (values & (ve.get(pointer, set()) - ce.get(pointer, set())))
        }
        assert not stale, (
            f"{name}: borç kaydı bayat — {stale} artık vendored kopyada yok (ya da kanonik "
            "absorbe etmiş). Girişi silin ki liste gerçek borcu göstersin."
        )


class TestGateCoversEveryVendoredFile:
    """🔴 ÖD-8'in asıl dersi: kapsamı ölçülmeyen kapı, olmayan kapıdır."""

    def test_every_vendored_file_is_tracked(self) -> None:
        tracked = {Path(v).name for _, v in MIRROR_PAIRS + SUBSET_PAIRS}
        present: set[str] = set()
        for root in VENDORED_ROOTS:
            directory = WORKSPACE / root
            if not directory.exists():
                pytest.skip(f"kardeş depo yok: {root}")
            present |= {path.name for path in directory.rglob("*.json")}
        untracked = sorted(present - tracked)
        assert not untracked, (
            f"Vendored dosya var ama parite kapısı onu İZLEMİYOR: {untracked}.\n"
            "2026-08-01'de 16 dosyanın 7'si böyleydi ve ÖD-2 tam o boşluktan geçti "
            "(`analysis_job.v1`). Yeni bir vendored dosya MIRROR ya da SUBSET listesine "
            "yazılmadan depoya giremez."
        )


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

    @pytest.mark.parametrize(("canonical", "vendored"), MIRROR_PAIRS, ids=IDS)
    def test_canonical_uses_unevaluated_properties(self, canonical: str, vendored: str) -> None:
        cj = json.loads((ROOT / canonical).read_text(encoding="utf-8"))
        if cj.get("type") != "object":
            return  # enum dosyaları nesne değildir
        assert cj.get("unevaluatedProperties") is False, (
            f"{Path(canonical).name}: kanonik şema unevaluatedProperties:false taşımalı"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
