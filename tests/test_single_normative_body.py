"""D16 (Ç8) — "aynı KR iki yerde GÖVDEYLE tanımlanamaz" kapısı.

NEDEN (2026-07-31, denetim bulguları AR1/AR3/Y6):
    **AR1 (KRİTİK):** KR-093 aynı depoda İKİ normatif metinle tanımlı ve çelişiyorlar
    (içerik + statü haritası). Ölçüldü: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` gövdesi
    **10 satır**, `ssot/kr_registry.md` gövdesi **98 satır** (8 bölümlü kanonik format).
    İki gövde = iki gerçek; tüketici hangisine uyacağını bilemez ve biri sessizce bayatlar.

    **AR3:** sorun KR-093'e özgü değil — ölçüldü: SSOT metni **51**, registry **54** tanım
    taşıyor; **50 KR'nin gövdesi İKİ KAYNAKTA BİRDEN** var (birleşim 55, kesişim 50).

KAPI TASARIMI — neden "yasak" değil de "borç dondurma":
    Bugün 50 ikili gövde var. "İkili gövde yasak" diyen bir test 50 yerde düşerdi ve ilk
    işi devre dışı bırakılmak olurdu (yeşil-ama-yalan kapının kardeşi: kırmızı-ama-işe
    yaramaz kapı). Bunun yerine borç **donduruluyor**: liste yalnız KÜÇÜLEBİLİR.
    Yeni bir KR iki gövdeyle tanımlanırsa test kırmızıya döner.

    Göç kararının kendisi (hangi kaynak normatif kalacak) KOORDİNATÖR kararıdır ve
    çapraz-repo etkisi vardır — SSOT metni platform kopyasıyla bayt-özdeştir (C-SSOT),
    registry ise yalnız contract'ta yaşar. Karar verilmeden gövde taşımak, normatif
    içerik kaybı riski taşır. Bkz. eylem planı §14.4/D16.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest


ROOT = Path(__file__).parent.parent
KR_REGISTRY = ROOT / "ssot" / "kr_registry.md"
SSOT_TEXT = ROOT / "docs" / "TARLAANALIZ_SSOT_v1_2_0.txt"

# Çıkarıcıyı TEK yerden al (D2'de dört başlık biçimini tanır hâle getirildi).
import sys

sys.path.insert(0, str(Path(__file__).parent))
from test_kr_reference_integrity import (  # noqa: E402
    _registry_defined_krs,
    _ssot_defined_krs,
)


#: İKİ kaynakta birden **GÖVDESİ** olan KR sayısı.
#: 2026-07-31: 50 ölçüldü → KR-093 göçüyle 49 → **2026-08-01/D16-b2 ile 0**.
#: Borç kapandı; kapı artık "dondurma" değil **YASAK** kipinde. Yükseltilemez.
KNOWN_DUAL_BODY_COUNT = 0

#: Göçü TAMAMLANMIŞ KR'ler: registry'de yalnız işaretçi, gövde SSOT metninde.
#: D16-b (KR-093) + D16-b2 (kalan 49).
MIGRATED = (
    "KR-000", "KR-001", "KR-002", "KR-010", "KR-011", "KR-012", "KR-013", "KR-014",
    "KR-015", "KR-016", "KR-017", "KR-018", "KR-019", "KR-020", "KR-021", "KR-022",
    "KR-023", "KR-024", "KR-025", "KR-026", "KR-027", "KR-028", "KR-029", "KR-030",
    "KR-031", "KR-032", "KR-033", "KR-040", "KR-041", "KR-042", "KR-043", "KR-050",
    "KR-060", "KR-061", "KR-062", "KR-063", "KR-064", "KR-065", "KR-066", "KR-070",
    "KR-071", "KR-072", "KR-073", "KR-080", "KR-081", "KR-082", "KR-083", "KR-084",
    "KR-092", "KR-093",
)

#: Gövdesi registry'de KALAN KR'ler — SSOT metninde tanımlı DEĞİLLER (ölçüldü:
#: orada yalnız tek satırlık çapraz-atıfla anılırlar). Bunlara işaretçi konulamaz;
#: konulursa tanım tamamen kaybolur. Kapı bu ayrımı korur.
REGISTRY_ONLY_BODIES = ("KR-088", "KR-089", "KR-090", "KR-091")

#: D16-b2 öncesi ölçülen toplam tanım sayısı (SSOT ∪ registry). Göç bir TAŞIMA'dır,
#: silme değil — bu sayı düşerse bir KR tanımı yok olmuş demektir.
MIN_TOTAL_DEFINED_KRS = 55

#: Registry'nin navigasyon değeri: her KR bir başlıkla listelenir (işaretçi de başlıktır).
MIN_REGISTRY_HEADINGS = 54

#: Bir bölümün "gövde değil, işaretçi" olduğunu söyleyen makine-okunur damga.
POINTER_MARK = "TÜRETİLMİŞ İŞARETÇİ"


def _registry_sections() -> dict[str, str]:
    """`ssot/kr_registry.md` → {KR kimliği: bölüm metni}."""
    text = KR_REGISTRY.read_text(encoding="utf-8")
    sections: dict[str, str] = {}
    current: str | None = None
    buffer: list[str] = []
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("#") and re.search(r"KR-\d{3}", stripped):
            if current:
                sections[current] = "\n".join(buffer)
            match = re.search(r"KR-\d{3}", stripped)
            current, buffer = (match.group(0) if match else None), []
        elif current:
            buffer.append(line)
    if current:
        sections[current] = "\n".join(buffer)
    return sections


def _registry_body_krs() -> set[str]:
    """Registry'de GERÇEK gövdesi olan KR'ler — işaretçiler SAYILMAZ.

    ⚠️ Bu ayrım kapının canıdır: ilk yazımda başlık sayıyordum ve KR-093 göçünden
    SONRA bile onu "iki gövdeli" görüyordum (işaretçi de başlık taşıyor). Yani kapı
    göçü ölçemiyordu — yeşil ama yalan. Artık damgaya bakıyor.
    """
    return {kr for kr, body in _registry_sections().items() if POINTER_MARK not in body}


def _dual_body_krs() -> set[str]:
    return _ssot_defined_krs() & _registry_body_krs()


class TestDualBodyDebtIsFrozen:
    def test_debt_does_not_grow(self) -> None:
        dual = _dual_body_krs()
        assert len(dual) <= KNOWN_DUAL_BODY_COUNT, (
            f"ikili gövde: {sorted(dual)} — izin verilen {KNOWN_DUAL_BODY_COUNT}. "
            "Bir KR iki normatif gövdeyle tanımlanmış: aynı kural iki yerde yazılırsa "
            "biri sessizce bayatlar (AR1'in tam olarak yaşandığı senaryo — D16-b2'de "
            "KR-083 kaldırılmış bir rol adını taşırken bulundu). Gövdeyi TEK kaynakta "
            "tutun, diğerine `TÜRETİLMİŞ İŞARETÇİ` damgalı bir işaretçi koyun."
        )

    def test_migration_did_not_delete_definitions(self) -> None:
        """Göç TAŞIMA'dır, silme değil — toplam tanım sayısı düşemez.

        Bu kapı olmadan D16-b2 sessizce bir felakete dönüşebilirdi: 49 gövdeyi
        işaretçiye çevirmek, gövdesi YALNIZ registry'de olan bir KR'ye uygulanırsa
        o tanım hiçbir yerde kalmaz. (Ölçüldü: 4 KR tam olarak bu durumdaydı.)
        """
        total = _ssot_defined_krs() | _registry_defined_krs()
        assert len(total) >= MIN_TOTAL_DEFINED_KRS, (
            f"toplam tanımlı KR {len(total)} < {MIN_TOTAL_DEFINED_KRS}. Bir KR tanımı "
            "kaybolmuş: göç sırasında gövde, kanonik metne yazılmadan registry'den "
            "silinmiş olabilir."
        )

    def test_registry_keeps_navigation_headings(self) -> None:
        """İşaretçiye dönüşen KR registry'den KAYBOLMAZ — başlığı kalır."""
        headings = _registry_sections()
        assert len(headings) >= MIN_REGISTRY_HEADINGS, (
            f"registry başlık sayısı {len(headings)} < {MIN_REGISTRY_HEADINGS}. "
            "İşaretçi dönüşümü başlığı da silmiş; registry navigasyon değerini kaybeder."
        )

    @pytest.mark.parametrize("kr", REGISTRY_ONLY_BODIES)
    def test_registry_only_bodies_are_not_pointerised(self, kr: str) -> None:
        """SSOT metninde tanımı OLMAYAN KR'ye işaretçi konulamaz — tanım yok olur."""
        section = _registry_sections().get(kr, "")
        assert section, f"{kr} registry'den kaybolmuş — gövdesi YALNIZ burada yaşıyordu"
        assert POINTER_MARK not in section, (
            f"{kr} işaretçiye çevrilmiş, ama SSOT metninde tanımı YOK — işaretçi "
            "hiçbir yere işaret etmiyor ve normatif gövde tamamen kaybolmuş. Önce "
            "gövdeyi kanonik metne taşıyın, sonra işaretçi koyun."
        )
        assert kr not in _ssot_defined_krs(), (
            f"{kr} artık SSOT metninde de tanımlı — ikili gövde geri gelmiş. "
            "REGISTRY_ONLY_BODIES listesinden çıkarıp göçünü tamamlayın."
        )

    @pytest.mark.parametrize("kr", MIGRATED)
    def test_migrated_kr_has_pointer_in_registry(self, kr: str) -> None:
        """Göçü biten KR registry'de yalnız İŞARETÇİ tutar — gövde geri yazılamaz."""
        section = _registry_sections().get(kr, "")
        assert section, f"{kr} registry'den tamamen kaybolmuş (işaretçi de kalmalı)"
        assert POINTER_MARK in section, (
            f"{kr} registry'de yeniden GÖVDE kazanmış. Normatif metin tek yerde durur "
            "(docs/TARLAANALIZ_SSOT_v1_2_0.txt); ikinci gövde AR1'i geri getirir."
        )

    @pytest.mark.parametrize("kr", MIGRATED)
    def test_migrated_kr_body_lives_in_the_ssot_text(self, kr: str) -> None:
        assert kr in _ssot_defined_krs(), (
            f"{kr} göç ettirildi ama SSOT metninde başlığı yok — gövde KAYBOLMUŞ olabilir"
        )

    def test_migration_preserved_the_registry_only_musts(self) -> None:
        """Göç KAYIPSIZ olmalı: registry'ye özgü MUST maddeleri SSOT metnine geçti mi?

        Her girdi, göç sırasında registry'de VAR / SSOT metninde YOK ölçülen bir
        maddedir. Biri düşerse göç değil silme yapılmış demektir.
        """
        ssot = SSOT_TEXT.read_text(encoding="utf-8")
        for needle, what in (
            # D16-b — KR-093
            ("Aşama A tespit DEĞİLDİR", "Y-D: öncelik bölgesi tespit değildir kuralı"),
            ("yeni faz EKLENMEZ", "ADR-007 §2: yeni mission state/faz eklenmez kuralı"),
            ("analysis_priority_zones", "Aşama A içerik kaynağı"),
            # D16-b2 — KR-019 (eskalasyon katmanı)
            ("atlas_confidence", "KR-019 tetikleyici 3'ün ikinci (L1 atlas) sinyali"),
            ("quarantine_caution", "KR-019 tetikleyici 6 — FD ailesi karantina kaydı"),
            ("dynamic_thresholds.yaml", "KR-019 dinamik eşiğin makine-okunur kaynağı"),
            ("PARTIAL_REPORT", "KR-019 fail-closed kademe adı"),
            ("EscalationLevel", "KR-019 platform tarafı eskalasyon seviyesi"),
            # D16-b2 — KR-092 (takvim yükleyici + yetki)
            ("SEASONAL_CALENDAR_PARSE_SKIP", "KR-092 yükleyici parse-skip olayı"),
            ("SeasonalFlightCalendarError", "KR-092 fail-closed hata tipi"),
            ("WeeklyFlightDTO", "KR-092 taşınan tip adı"),
            ("negatif cache zehirlenmesi", "KR-092 cache davranışı kuralı"),
            # D16-b2 — KR-072
            ("evidence_bundle_ref", "KR-072 kanıt paketi referansı (3 şema ona atıf yapar)"),
        ):
            assert needle in ssot, (
                f"göçte KAYIP: {what} SSOT metninde bulunamadı ({needle!r}). Göç, gövdeyi "
                "taşımak demektir; silmek değil."
            )

    def test_kr092_limit_violation_is_fail_closed_not_clamped(self) -> None:
        """🔴 Bu kapı GERÇEK bir çelişkiden doğdu (2026-08-01/D16-b2).

        SSOT metni KR-092'de *"en yakın geçerli değere clamp edilir"* diyordu; registry
        gövdesi ise *"reddedilir → SeasonalFlightCalendarError (fail-closed)"*. İkisi
        aynı anda doğru olamaz. Kod ölçüldü ve registry haklı çıktı:
        `seasonal_flight_calendar.py` H/v < 3,9 veya irtifa > 120 m'de **hata yükseltiyor**,
        yükleyici o ürünü atlıyor. Metin düzeltildi.

        Neden kapı: "clamp" davranışı, SHGM irtifa sınırı ve sensör tetik aralığı gibi
        FİZİKSEL/MEVZUAT sınırlarını kâğıt üzerinde sağlanmış gösterirdi — sessiz uyumsuzluk.
        """
        ssot = SSOT_TEXT.read_text(encoding="utf-8")
        assert "clamp EDİLMEZ" in ssot, (
            "KR-092 sınır ihlali davranışı fail-closed olarak yazılmalı. Metin yine "
            "'clamp edilir' diyorsa, kodla (SeasonalFlightCalendarError) çelişir."
        )
        assert "en yakın geçerli değere clamp edilir" not in ssot, (
            "KR-092'nin eski, kodla ÇELİŞEN 'clamp edilir' ifadesi geri gelmiş."
        )


class TestUndefinedQuantitiesAreDeclared:
    """A3 — atıf alan ama tanımı olmayan büyüklükler AÇIKÇA işaretli olmalı."""

    def test_stress_ratio_status_is_declared(self) -> None:
        enum_doc = json.loads(
            (ROOT / "enums" / "analysis_type.enum.v1.json").read_text(encoding="utf-8")
        )
        definitions = enum_doc["metadata"].get("indexDefinitions", {})
        entry = definitions.get("stress_ratio")
        assert entry, (
            "`stress_ratio` KR-093'ün zorunlu teslimat kaleminin kaynağı olarak anılıyor "
            "ama hiçbir yerde TANIMLI değil (A3: 3 atıf / 0 tanım). Tanımsız büyüklük ne "
            "üretilebilir ne denetlenebilir."
        )
        for key in ("status", "problem", "why_not_guessed", "blocked_on", "until_then"):
            assert str(entry.get(key, "")).strip(), f"beyanda eksik alan: {key}"

    def test_no_silent_undefined_quantity_in_preliminary_mapping(self) -> None:
        """Ön faz eşlemesi TANIMSIZ bir büyüklüğe dayanamaz."""
        report_phase = json.loads(
            (ROOT / "enums" / "report_phase.enum.v1.json").read_text(encoding="utf-8")
        )
        stage_b = report_phase["x-preliminary-content"]["stage_b_post_analysis"]
        text = json.dumps(stage_b, ensure_ascii=False)
        assert "stress_ratio" not in text, (
            "ön faz stage_b hâlâ tanımsız `stress_ratio`'ya dayanıyor — D17 ile "
            "WATER_STRESS çıkarıldı, eşleme de çıkmalıydı"
        )


class TestMachineAndProseAgree:
    """🔴 MAKİNE ile METİN aynı şeyi söylemeli — bu kapı BENİM HATAMDAN doğdu.

    2026-07-31/D17'de `WATER_STRESS` **enum'dan** (makine-okunur `x-preliminary-content`)
    çıkarıldı ama KR-093'ün **iki prose gövdesi** (SSOT metni + registry) onu hâlâ
    *"[ZORUNLU] PRELIMINARY içeriği"* olarak sayıyordu. Yani sözleşme iki farklı şey
    söyler hâle geldi — AR1'in (ikili gövde çürümesi) tam olarak yaşandığı senaryonun
    **yenisini ben ürettim**. Düzeltildi; bu kapı tekrarını engelliyor.

    Ders: makine-okunur bir listeyi değiştirirken, aynı listeyi **prose olarak** tekrar
    eden her normatif metin de aynı commit'te güncellenmelidir.
    """

    SOURCES = (
        ("docs/TARLAANALIZ_SSOT_v1_2_0.txt", "SSOT metni (çapraz-repo)"),
        ("ssot/kr_registry.md", "KR registry (contract-only)"),
    )

    def _proxy_only_layers(self) -> set[str]:
        analysis_type = json.loads(
            (ROOT / "enums" / "analysis_type.enum.v1.json").read_text(encoding="utf-8")
        )
        by_layer = analysis_type["metadata"]["bandRequirements"]["byLayer"]
        return {
            name for name, spec in by_layer.items()
            if isinstance(spec, dict) and spec.get("availability") == "proxy_only"
        }

    @pytest.mark.parametrize(("relative", "label"), SOURCES)
    def test_prose_does_not_mandate_a_proxy_layer(self, relative: str, label: str) -> None:
        text = (ROOT / relative).read_text(encoding="utf-8")
        for layer in self._proxy_only_layers():
            # "zorunlu içerik" bağlamı: katman adının indeks-eşlemesi olarak anılması.
            mandated = f"`{layer}`←" in text
            assert not mandated, (
                f"{label}: `{layer}` hâlâ ön fazın ZORUNLU içerik eşlemesinde görünüyor, "
                "oysa katman `proxy_only` (analysis_type). Makine-okunur liste ile normatif "
                "metin ayrışmış — ikisi aynı commit'te güncellenmelidir."
            )

    def test_undefined_quantity_is_not_mandated_in_prose(self) -> None:
        """`stress_ratio` tanımsız olduğu sürece hiçbir gövde onu ZORUNLU sayamaz."""
        for relative, label in self.SOURCES:
            text = (ROOT / relative).read_text(encoding="utf-8")
            assert "←stress_ratio" not in text, (
                f"{label}: tanımsız `stress_ratio` bir teslimat kaleminin kaynağı olarak "
                "zorunlu tutuluyor (A3). Tanım gelene kadar eşleme askıdadır."
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
