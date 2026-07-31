"""KR atıf bütünlüğü — sarkan (dangling) kanonik atıf kapısı.

Neden bu test var (2026-07-31 denetimi, D-7):
    `enums/report_phase.enum.v1.json` ve `schemas/events/analysis_preliminary_ready.v1.schema.json`
    **KR-093'e normatif atıf** yapıyordu, ama KR-093 contract'ın **hiçbir** kanonik kaynağında
    tanımlı değildi:
      - `ssot/kr_registry.md`            → KR-092'de bitiyordu
      - `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → KR-084'te bitiyordu (platform kopyası KR-093'e gidiyordu)
    Yani aynı adlı, aynı sürüm etiketli (`v1_2_0`) iki SSOT metni **ayrışmıştı** ve contract kendi
    şemasında var olmayan bir kurala dayanıyordu.

İki kaynak TAMAMLAYICIDIR, iç içe değil:
    - `docs/TARLAANALIZ_SSOT_v1_2_0.txt` — tam KR korpusu (48 tanım)
    - `ssot/kr_registry.md`              — ek registry (KR-088…KR-093, veri katmanı genişlemesi)
    Bu yüzden kapı **birleşim** üzerinden kurulur: her atıf en az bir kaynakta tanımlı olmalı.
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


def _ssot_defined_krs() -> set[str]:
    """SSOT metnindeki KR başlıklarını çıkar.

    Başlık biçimi TEK TİP DEĞİLDİR — çıkarıcı buna dayanıklı olmalı (2026-07-31'de
    dar bir regex yanlış alarm üretmişti):
      * ``## [KR-019] ...``            — olağan
      * ``## [KR-018 / KR-082] ...``   — BİRLEŞİK başlık, iki KR'yi birlikte tanımlar
      * ``## # [KR-033] ...``          — kaynaktaki yazım hatası (fazladan '#')
    """
    krs: set[str] = set()
    for line in SSOT_TEXT.read_text(encoding="utf-8").splitlines():
        stripped = line.lstrip()
        if stripped.startswith("#") and "[KR-" in stripped:
            krs.update(re.findall(r"KR-\d{3}", stripped))
    return krs


def _defined_krs() -> set[str]:
    """İki kanonik kaynağın BİRLEŞİMİ (tamamlayıcıdırlar, iç içe değil)."""
    registry = set(re.findall(r"^## (KR-\d{3})", KR_REGISTRY.read_text(encoding="utf-8"), re.M))
    return registry | _ssot_defined_krs()


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
    def test_data_layer_kr_present_in_ssot_text(self, kr: str) -> None:
        text = SSOT_TEXT.read_text(encoding="utf-8")
        assert kr in text, (
            f"{kr} SSOT metninden kayboldu — contract kopyası platform kopyasının gerisine düştü "
            "(2026-07-31'de hizalanmıştı)."
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
