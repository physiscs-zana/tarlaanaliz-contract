"""0.h Veri Yönetişimi kapısı — "sözleşmeye giren veri kategorisi saklama tablosuna yazılır".

NEDEN (2026-08-01, 0.h kararı — denetim bulguları K2/K3):
    Plan §0 *"kamu araştırma projesi → veri yönetim planı, çiftçi rızası, yayın/veri
    paylaşım politikası"* yükümlülüğünü tanıyordu ama bu, listedeki **tek eyleme
    dönüşmemiş** satırdı. Bu turlarda **üç yeni veri kategorisi** sözleşmeye girdi —
    öncelik bölgesi poligonları + ön faz görselleri · seçilmiş ham kareler · denetim
    örneklemi etiketleri — ve **hiçbiri** KR-090 saklama politikasında tanımlı değildi (K3).

    Saklama süresi olmayan kişisel/konumsal veri, "süresiz saklanır"ın sessiz hâlidir:
    kimse silmez çünkü kimse silmekle görevli değildir.

KAPI NE YAPAR:
    Her yönde bir yalanı yakalar —
      * ileri yön: sözleşmede TAŞIYICISI olan bir kategori KR-090'da anılmıyorsa → kırmızı
        ("yeni veri kategorisi eklendi, saklama satırı yazılmadı")
      * geri yön: KR-090'da anılan kategorinin sözleşmede taşıyıcısı kalmamışsa → kırmızı
        ("kayıt bayatladı; kaldırılan alanın saklama satırı hâlâ duruyor")
      * içerik: her satır **süre** ve **gerekçe** taşımalı; çıplak bir ad yeterli değil

⚠️ BİLİNEN SINIR (AK-3 ile aynı sınıf):
    `DATA_CATEGORIES` **elle tutulan** bir listedir. Sözleşmeye bu listeye yazılmadan
    yeni bir kategori eklenirse kapı onu göremez — kapı "her yeni kategoriyi bulurum"
    demiyor, "listedeki her kategorinin kaydı var mı" diyor. Bu sınır bilinçlidir:
    "hangi alan kişisel/konumsal veridir" sorusu hukuki bir yargıdır, mekanik bir tarama
    değil. Sınırı kapatan şey PR incelemesidir (`SDLC_GATES` §3).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
KR_REGISTRY = ROOT / "ssot" / "kr_registry.md"

#: Sözleşmeye giren kişisel/konumsal veri kategorileri.
#: (kategori anahtarı, taşıyıcı yolları, insan-okunur ad, taşıma BİÇİMİ)
#:
#: ⚠️ `kind` alanı BİR MUTASYONDAN DOĞDU (2026-08-01). İlk sürüm üçünü de aynı sanıp
#: `key in json.dumps(şema)` diyordu — yani METİNDE geçmesini "taşıyor" sayıyordu.
#: Mutasyon testi kapıyı KÖR buldu: `raw_frames` property'sini şemadan sildim, kapı
#: yeşil kaldı. İki kök neden vardı ve ikisi de gerçek kusurdu:
#:   ① `raw_frames` edge şemasında İKİ kez geçiyor — biri gerçek property, diğeri bir
#:     alan-sahipliği listesinin ("raw_manifest_ref", "raw_frames") elemanı. Property
#:     silinince liste geçişi kapıyı yeşil tutuyordu.
#:   ② Platform `calibrated_dataset_manifest` `raw_frames` **taşımıyor** — yalnız
#:     açıklamasında ondan BAHSEDİYOR ("edge formu — seçilmiş ham kareler…").
#:     Taşıyıcı listem yanlıştı; bahsetmek taşımak değildir.
#: Bu, D16'nın kapattığı "prose var, zorlanabilirlik yok" sınıfının saklama tarafındaki
#: hâliydi — kapının kendisi o hataya düşmüştü.
DATA_CATEGORIES: tuple[tuple[str, tuple[str, ...], str, str], ...] = (
    (
        # Enum metadata'sında bir İÇERİK ADI olarak yaşar (x-preliminary-content),
        # şema property'si değil — bu yüzden "token".
        "analysis_priority_zones",
        (
            "enums/report_phase.enum.v1.json",
            "schemas/events/analysis_preliminary_ready.v1.schema.json",
        ),
        "öncelik bölgesi poligonları + ön faz görselleri",
        "token",
    ),
    (
        # ÖLÇÜLDÜ: yalnız EDGE formunda gerçek property. Platform formunda yok.
        "raw_frames",
        ("schemas/edge/calibrated_dataset_manifest.v1.schema.json",),
        "seçilmiş ham kareler",
        "property",
    ),
    (
        "audit_sample",
        ("schemas/worker/expert_review_queue.v1.schema.json",),
        "denetim örneklemi etiketleri",
        "property",
    ),
)

#: Bir saklama satırının taşımak ZORUNDA olduğu şeyler (alt dize / desen).
#: Süre: ya gün sayısı ya açık "ASLA silinmez" beyanı.
_DURATION = re.compile(r"\b\d{2,4}\s*gün\b|ASLA silinmez", re.IGNORECASE)
_RATIONALE = "Gerekçe:"


def _kr090_body() -> str:
    """KR-090 bölümünün gövdesi (bir sonraki KR başlığına kadar)."""
    text = KR_REGISTRY.read_text(encoding="utf-8")
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        stripped = line.lstrip()
        if stripped.startswith("#") and "KR-090" in stripped:
            start = index
            break
    assert start is not None, (
        "KR-090 başlığı ssot/kr_registry.md'de bulunamadı. Saklama politikasının gövdesi "
        "BURADA yaşar (SSOT metninde tanımlı değil — D16-b2'de ölçüldü)."
    )
    body: list[str] = []
    for line in lines[start + 1 :]:
        stripped = line.lstrip()
        if stripped.startswith("#") and re.search(r"KR-\d{3}", stripped):
            break
        body.append(line)
    return "\n".join(body)


def _schema_property_names(node: object, out: set[str]) -> None:
    """`properties` / `patternProperties` / `$defs` ANAHTARLARINI topla.

    Değerlerin içine bakmaz — bir alan adının açıklama metninde ya da bir
    sahiplik listesinde geçmesi, o alanın TANIMLI olduğu anlamına gelmez.
    """
    if isinstance(node, dict):
        for key, value in node.items():
            if key in ("properties", "patternProperties", "$defs") and isinstance(value, dict):
                out.update(value.keys())
            _schema_property_names(value, out)
    elif isinstance(node, list):
        for item in node:
            _schema_property_names(item, out)


def _carrier_declares(path_rel: str, key: str, kind: str) -> bool:
    """Taşıyıcı dosya bu kategoriyi gerçekten TAŞIYOR mu?

    `kind="property"` → şemada tanımlı bir alan olmalı (metinde geçmesi YETMEZ).
    `kind="token"`    → enum metadata'sında içerik adı olarak geçmesi yeterli.
    """
    path = ROOT / path_rel
    if not path.exists():
        return False
    if path.suffix != ".json":
        return key in path.read_text(encoding="utf-8")

    document = json.loads(path.read_text(encoding="utf-8"))
    if kind == "property":
        names: set[str] = set()
        _schema_property_names(document, names)
        return key in names
    return key in json.dumps(document, ensure_ascii=False)


class TestEveryDataCategoryHasRetention:
    @pytest.mark.parametrize(
        ("key", "carriers", "label", "kind"),
        DATA_CATEGORIES,
        ids=[key for key, _c, _l, _k in DATA_CATEGORIES],
    )
    def test_category_is_declared_in_retention_policy(
        self, key: str, carriers: tuple[str, ...], label: str, kind: str
    ) -> None:
        """İLERİ YÖN: sözleşmede taşıyıcısı olan kategori KR-090'da anılmalı."""
        assert key in _kr090_body(), (
            f"'{key}' ({label}) sözleşmede taşınıyor ama KR-090 saklama tablosunda YOK.\n"
            "Saklama süresi olmayan kişisel/konumsal veri, 'süresiz saklanır'ın sessiz "
            "hâlidir: kimse silmez çünkü kimse silmekle görevli değildir.\n"
            "0.h kararı: contract'a giren her yeni veri kategorisi AYNI TURDA KR-090'a "
            "bir satır ekler (süre + silme yolu + gerekçe). Kayıt yoksa kalem C8'e giremez."
        )

    @pytest.mark.parametrize(
        ("key", "carriers", "label", "kind"),
        DATA_CATEGORIES,
        ids=[key for key, _c, _l, _k in DATA_CATEGORIES],
    )
    def test_carriers_still_exist(
        self, key: str, carriers: tuple[str, ...], label: str, kind: str
    ) -> None:
        """GERİ YÖN: kayıt bayatlamamalı — taşıyıcının en az biri hâlâ bu anahtarı taşımalı."""
        alive = [c for c in carriers if _carrier_declares(c, key, kind)]
        assert alive, (
            f"'{key}' ({label}) için KR-090'da saklama satırı var ama sözleşmede hiçbir "
            f"taşıyıcı bu anahtarı içermiyor (bakılan: {list(carriers)}).\n"
            "Ya alan kaldırıldı ve saklama satırı bayatladı, ya taşıyıcı yolu değişti. "
            "Bayat saklama kaydı, var olmayan bir veriyi yönetiyormuş gibi görünür."
        )

    @pytest.mark.parametrize(
        ("key", "carriers", "label", "kind"),
        DATA_CATEGORIES,
        ids=[key for key, _c, _l, _k in DATA_CATEGORIES],
    )
    def test_retention_row_states_duration_and_rationale(
        self, key: str, carriers: tuple[str, ...], label: str, kind: str
    ) -> None:
        """İÇERİK: çıplak ad yetmez — satır SÜRE ve GEREKÇE taşımalı.

        Süresiz bir 'kategori anıldı' satırı kapıyı yeşile boyar ama hiçbir şey
        yönetmez; tam olarak D16'da kapatılan 'prose var, zorlanabilirlik yok'
        sınıfının saklama tarafındaki hâli olurdu.
        """
        body = _kr090_body()
        window = _category_window(body, key)
        assert _DURATION.search(window), (
            f"'{key}' ({label}) KR-090'da anılıyor ama SÜRE yazılmamış. Geçerli biçim: "
            "gün sayısı (ör. '730 gün') ya da açık 'ASLA silinmez' beyanı."
        )
        assert _RATIONALE in window, (
            f"'{key}' ({label}) satırında '{_RATIONALE}' yok. Süre bir sayı değil bir "
            "KARARDIR; neden o süre olduğu yazılmazsa bir sonraki tur onu gerekçesiz "
            "uzatır (veri minimizasyonu sessizce erir)."
        )


def _category_window(body: str, key: str) -> str:
    """Kategorinin geçtiği maddeyi kabaca izole et (numaralı madde sınırına kadar)."""
    index = body.find(key)
    if index == -1:
        return ""
    tail = body[index:]
    match = re.search(r"\n\s*\d{1,2}\)\s", tail[1:])
    return tail[: match.start() + 1] if match else tail


class TestThirdPartyDataRuleIsRecorded:
    """0.h madde 4 — komşu parsel (üçüncü kişi) verisi kuralı YAZILI olmalı.

    Ölçüldü (2026-08-01): tekil kare izdüşümü sözleşmede yok (C7 Tur 2'ye ertelendi),
    ama `raw_frames` seçilmiş kareleri listeler ve bir kare komşu parseli GÖREBİLİR.
    Kural yazılı olmazsa, C7 Tur 2'de geldiğinde bu soru hiç sorulmaz.
    """

    def test_rule_exists(self) -> None:
        body = _kr090_body()
        assert "Üçüncü kişi verisi" in body, (
            "0.h madde 4 (komşu parsele taşan görüntü/izdüşüm taşınmaz) KR-090'da yazılı "
            "değil. Bugün ihlal edilmiyor olması kuralı gereksiz yapmaz — C7 (tekil kare "
            "şeması, Tur 2) geldiğinde bu soruyu soracak yazılı bir yer gerekir."
        )

    def test_known_gap_is_named_not_hidden(self) -> None:
        """Kapatılmamış boşluk GİZLENMEZ — plan kalemi adıyla anılır."""
        body = _kr090_body()
        assert "0.h-a" in body, (
            "`raw_frames` kırpma (crop) garantisinin sözleşmede olmadığı ölçüldü; bu boşluk "
            "bir plan kalemi adıyla (0.h-a) anılmalı. Adsız boşluk, kapanmış boşluktan "
            "ayırt edilemez."
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
