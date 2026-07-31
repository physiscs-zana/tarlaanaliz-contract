"""KR atıf bütünlüğü — sarkan (dangling) kanonik atıf kapısı.

Neden bu test var (2026-07-31 denetimi, D-7):
    `enums/report_phase.enum.v1.json` ve `schemas/events/analysis_preliminary_ready.v1.schema.json`
    **KR-093'e normatif atıf** yapıyordu, ama KR-093 contract'ın **hiçbir** kanonik kaynağında
    tanımlı değildi:
      - `ssot/kr_registry.md`            → KR-092'de bitiyordu
      - `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → KR-084'te bitiyordu (platform kopyası KR-093'e gidiyordu)
    Yani aynı adlı, aynı sürüm etiketli (`v1_2_0`) iki SSOT metni **ayrışmıştı** ve contract kendi
    şemasında var olmayan bir kurala dayanıyordu.

İki kanonik kaynak (2026-07-31 KADEME 0/D2'de YENİDEN ÖLÇÜLDÜ):
    - `docs/TARLAANALIZ_SSOT_v1_2_0.txt` — 49 `## [KR-NNN]` + 1 yazım hatalı `## # [KR-033]`
      + 3 köşeli-parantezsiz `### KR-NNN` başlık
    - `ssot/kr_registry.md`              — **54** tanım: 48 `### KR-NNN` + 6 `## KR-NNN`
    Kapı **birleşim** üzerinden kurulur: her atıf en az bir kaynakta tanımlı olmalı.

⚠️ ÇIKARICI KÖRLÜĞÜ (D2 — bu turda düzeltildi):
    Önceki sürüm registry'yi `^## (KR-\\d{3})` ile tarıyordu → **54 tanımın 6'sını**
    görüyordu (%89 kör, denetim bulgusu Q6). SSOT metni tarafı da `"[KR-"` şartı koştuğu
    için köşeli-parantezsiz `### KR-017` başlığını kaçırıyordu. Sonuç: kapı, aslında
    tanımlı olan KR'leri "sarkan atıf" sanabilir (yanlış alarm) ve daha kötüsü, başlık
    biçimi değişince (ör. `## KR-093` → `### KR-093`) hiçbir test bunu fark etmiyordu.
    Artık her iki kaynakta da **1-4 arası her başlık düzeyi** ve dört biçim tanınır.
"""

import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
KR_REGISTRY = ROOT / "ssot" / "kr_registry.md"
SSOT_TEXT = ROOT / "docs" / "TARLAANALIZ_SSOT_v1_2_0.txt"

# 2026-07-31 hizalamasında contract kopyasına giren, veri-katmanı genişlemesi KR'leri.
# Bunlar bir kez daha düşerse iki kopya yeniden ayrışmış demektir.
DATA_LAYER_KRS = ("KR-088", "KR-091", "KR-092", "KR-093")

# Dördünün NEREDE tanımlı olduğu ölçüldü (2026-07-31/D2) — varsayım değil:
#   KR-092 / KR-093 → SSOT metninde `## [KR-0xx]` BAŞLIĞIYLA tanımlı
#   KR-088 / KR-091 → SSOT metninde YALNIZ çapraz-atıf satırında geçer (satır 787);
#                     normatif gövdeleri `ssot/kr_registry.md`'dedir.
# Eski test `kr in text` (alt dize) diyordu; çapraz-atıf satırı bunu KENDİ BAŞINA
# geçiriyordu → kapı KR-088/091 için tamamen boştu (denetim bulgusu Q5).
SSOT_TEXT_HEADING_KRS = ("KR-092", "KR-093")
REGISTRY_BODY_KRS = ("KR-088", "KR-091")

# Registry'deki tanım sayısı bir REGRESYON EŞİĞİDİR: çıkarıcı yeniden `^## ` biçimine
# daralırsa bu sayı 54 → 6'ya düşer ve test kırmızıya döner (D2'nin mutasyon kapısı).
MIN_REGISTRY_DEFINITIONS = 50


def _collect_kr_refs() -> dict[str, set[str]]:
    """Her `x-kr-ref` değerini, atıfta bulunan dosyayla birlikte topla."""
    refs: dict[str, set[str]] = {}
    files = list((ROOT / "enums").glob("*.json"))
    files += list((ROOT / "schemas").rglob("*.json"))
    for path in files:
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue

        def walk(node: object) -> None:
            if isinstance(node, dict):
                for key, value in node.items():
                    if key == "x-kr-ref":
                        items = value if isinstance(value, list) else [value]
                        for item in items:
                            if isinstance(item, str) and re.fullmatch(r"KR-\d{3}", item):
                                refs.setdefault(item, set()).add(
                                    str(path.relative_to(ROOT)).replace("\\", "/")
                                )
                    walk(value)
            elif isinstance(node, list):
                for item in node:
                    walk(item)

        walk(doc)
    return refs


def _headings_with_kr(text: str) -> set[str]:
    """Bir Markdown metnindeki TÜM KR tanım başlıklarını çıkar (biçimden bağımsız).

    Tanınan dört biçim (hepsi kaynaklarda ÖLÇÜLDÜ, uydurma değil):
      * ``## [KR-019] ...``            — SSOT metninde olağan biçim (49 adet)
      * ``## [KR-018 / KR-082] ...``   — BİRLEŞİK başlık, iki KR'yi birlikte tanımlar
      * ``## # [KR-033] ...``          — kaynaktaki yazım hatası (fazladan '#')
      * ``### KR-093 — ...``           — köşeli parantezsiz; registry'nin ana biçimi
                                         (48 adet) + SSOT metninde 3 adet

    Kural: satır `#` ile başlıyorsa ve içinde `KR-NNN` geçiyorsa, o satır bir tanım
    başlığıdır. Metin İÇİNDEKİ çapraz-atıflar (`- **[KR-088] / [KR-091]:** ...`) başlık
    olmadığı için SAYILMAZ — Q5'in kapattığı boşluk tam olarak budur.
    """
    krs: set[str] = set()
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("#") and "KR-" in stripped:
            krs.update(re.findall(r"KR-\d{3}", stripped))
    return krs


def _ssot_defined_krs() -> set[str]:
    """`docs/TARLAANALIZ_SSOT_v1_2_0.txt` içindeki tanım başlıkları."""
    return _headings_with_kr(SSOT_TEXT.read_text(encoding="utf-8"))


def _registry_defined_krs() -> set[str]:
    """`ssot/kr_registry.md` içindeki tanım başlıkları (`##` VE `###`)."""
    return _headings_with_kr(KR_REGISTRY.read_text(encoding="utf-8"))


def _defined_krs() -> set[str]:
    """İki kanonik kaynağın BİRLEŞİMİ.

    NOT: 2026-07-31 ölçümü bu ikisinin *tamamlayıcı* değil büyük ölçüde **iç içe**
    olduğunu gösterdi (registry 54 tanım taşıyor). Birleşim kapısı yine doğru kapıdır —
    ama "aynı KR iki yerde gövdeyle tanımlanamaz" sorunu ayrı bir kalemdir (§14.4/D16).
    """
    return _registry_defined_krs() | _ssot_defined_krs()


class TestNoDanglingKrReferences:
    def test_ssot_sources_are_readable(self) -> None:
        assert KR_REGISTRY.exists(), "ssot/kr_registry.md yok"
        assert SSOT_TEXT.exists(), "docs/TARLAANALIZ_SSOT_v1_2_0.txt yok"

    def test_at_least_one_reference_exists(self) -> None:
        """Toplayıcı bozulursa test sessizce boşa düşmesin."""
        assert _collect_kr_refs(), "x-kr-ref taraması hiç sonuç vermedi — toplayıcı bozuk olabilir"

    def test_extractor_handles_non_uniform_headings(self) -> None:
        """Çıkarıcı, birleşik ve hatalı-biçimli başlıkları da görmeli (yanlış alarm kapısı)."""
        ssot = _ssot_defined_krs()
        # '## [KR-018 / KR-082] ...' — birleşik başlık
        assert {"KR-018", "KR-082"} <= ssot, "birleşik başlık çıkarılamadı"
        # '## # [KR-033] ...' — kaynaktaki fazladan '#'
        assert "KR-033" in ssot, "hatalı-biçimli başlık çıkarılamadı"
        # '### KR-017 ...' — köşeli parantezsiz (eski çıkarıcı '[KR-' şartı yüzünden kaçırıyordu)
        assert "KR-017" in ssot, "köşeli parantezsiz '### KR-NNN' başlığı çıkarılamadı"

    def test_registry_extractor_sees_every_heading_level(self) -> None:
        """D2 mutasyon kapısı: çıkarıcı `^## ` biçimine daralırsa BURASI kırmızıya döner.

        Ölçüm (2026-07-31): `ssot/kr_registry.md` 54 tanım taşıyor — 48'i `### KR-NNN`,
        6'sı `## KR-NNN`. Eski regex (`^## (KR-\\d{3})`) yalnız 6'sını görüyordu (%89 kör).
        """
        registry = _registry_defined_krs()
        assert len(registry) >= MIN_REGISTRY_DEFINITIONS, (
            f"registry çıkarıcısı yalnız {len(registry)} tanım görüyor (eşik "
            f"{MIN_REGISTRY_DEFINITIONS}). Başlık düzeyi (## / ###) körlüğü geri gelmiş "
            "olabilir — bkz. denetim bulgusu Q6."
        )
        # `### KR-NNN` biçiminin fiilen görüldüğünü göster (sayı eşiği tek başına yeter
        # gibi görünse de, biçim iddiasını açıkça bağlıyoruz).
        assert "KR-070" in registry, "'### KR-070' tanımı görünmüyor — çıkarıcı biçime kör"

    def test_cross_reference_line_is_not_counted_as_definition(self) -> None:
        """Q5 kapısı: metin İÇİNDEKİ çapraz-atıf bir TANIM değildir.

        `docs/TARLAANALIZ_SSOT_v1_2_0.txt` içinde KR-088/KR-091 yalnız bir çapraz-atıf
        satırında (`- **[KR-088] / [KR-091]:** ...`) geçer. Eski `kr in text` alt-dize
        testi bunu "tanımlı" sayıyordu; bu kapı artık başlık şartı koşuyor.
        """
        assert "KR-088" in SSOT_TEXT.read_text(encoding="utf-8"), "ön koşul: metinde geçiyor"
        assert "KR-088" not in _ssot_defined_krs(), (
            "KR-088 SSOT metninde BAŞLIKLA tanımlı görünüyor — ölçüm değişmiş olabilir; "
            "böyleyse REGISTRY_BODY_KRS/SSOT_TEXT_HEADING_KRS listelerini güncelleyin."
        )

    def test_every_referenced_kr_is_defined(self) -> None:
        refs = _collect_kr_refs()
        defined = _defined_krs()
        dangling = {kr: sorted(src) for kr, src in refs.items() if kr not in defined}
        assert not dangling, (
            "Şemalar tanımı olmayan KR'lere normatif atıf yapıyor "
            f"(ne ssot/kr_registry.md ne docs/TARLAANALIZ_SSOT_v1_2_0.txt): {dangling}"
        )


class TestSsotTextStaysAlignedWithPlatformCopy:
    """2026-07-31 hizalamasının regresyon kapısı."""

    @pytest.mark.parametrize("kr", DATA_LAYER_KRS)
    def test_data_layer_kr_is_defined_not_merely_mentioned(self, kr: str) -> None:
        """Dördü de **bir tanım başlığıyla** bulunmalı; anılmak yetmez (Q5).

        Eski hâli `kr in text` idi: çapraz-atıf satırı bile geçiriyordu, yani KR-088 ve
        KR-091 için kapı TAMAMEN BOŞTU.
        """
        assert kr in _defined_krs(), (
            f"{kr} hiçbir kanonik kaynakta BAŞLIKLA tanımlı değil — contract kopyası "
            "platform kopyasının gerisine düşmüş olabilir (2026-07-31'de hizalanmıştı)."
        )

    @pytest.mark.parametrize("kr", SSOT_TEXT_HEADING_KRS)
    def test_ssot_text_still_carries_its_own_kr_bodies(self, kr: str) -> None:
        """KR-092/093 gövdesi SSOT METNİNDE durmalı — hizalamanın asıl kanıtı budur."""
        assert kr in _ssot_defined_krs(), (
            f"{kr} SSOT metninden kayboldu — iki kopya yeniden ayrıştı demektir."
        )

    @pytest.mark.parametrize("kr", REGISTRY_BODY_KRS)
    def test_registry_carries_the_data_layer_bodies(self, kr: str) -> None:
        """KR-088/091'in normatif gövdesi registry'dedir (SSOT metninde yalnız atıf var)."""
        assert kr in _registry_defined_krs(), (
            f"{kr} `ssot/kr_registry.md`'den kayboldu; SSOT metninde de yalnız çapraz-atıf "
            "olduğu için bu KR tanımsız kalır."
        )

    def test_kr083_uses_current_role_name(self) -> None:
        """Rol yeniden adlandırması geri gelmesin: IL_OPERATOR → DISTRICT_REP (2026-06-26)."""
        text = SSOT_TEXT.read_text(encoding="utf-8")
        assert "## [KR-083] İlçe Temsilcisi" in text, (
            "KR-083 başlığı 'İlçe Temsilcisi' olmalı. Eski 'İl Operatörü' metni, contract'ın "
            "kendi enums/role.enum.v1.json'ı (DISTRICT_REP kanonik, IL_OPERATOR DEPRECATED) ile "
            "ÇELİŞİR — bu, 2026-07-31'de düzeltilen bayat kopyanın işaretidir."
        )

    def test_role_enum_and_ssot_text_agree_on_district_rep(self) -> None:
        role_enum = json.loads((ROOT / "enums" / "role.enum.v1.json").read_text(encoding="utf-8"))
        assert "DISTRICT_REP" in role_enum["enum"], "role.enum.v1 DISTRICT_REP taşımalı"
        assert "DISTRICT_REP" in SSOT_TEXT.read_text(encoding="utf-8"), (
            "SSOT metni kanonik rol adını içermiyor"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
