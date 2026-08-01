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

# --- ÖD-11 / ÖD-12 (2026-08-01) — damga ve başlık SAYMAK yetmiyor ------------
# ÖD-11: kapı bir bölümü "işaretçi" saymak için yalnız DAMGAYA bakıyordu → damga dururken
#        altına çelişkili bir normatif gövde yazılabilirdi ve kapı yeşil kalırdı.
# ÖD-12: "göç taşımadır, silme değil" kapısı BAŞLIK sayıyordu → bir KR'nin normatif gövdesi
#        silinip başlığı bırakılsa sayı değişmezdi.
#
# Eşikler ÖLÇÜLDÜ (2026-08-01), tahmin edilmedi:
#   damgalı (işaretçi) bölümler : min 286 · p50 340 · **max 1366** (KR-093)
#   damgasız (gerçek gövde)     : **min 1483** · p50 1885 · max 3935
# İki küme arasında temiz bir boşluk var; sınır oraya konur.
MAX_POINTER_SECTION_CHARS = 1500

#: SSOT metnindeki normatif gövdelerin toplam hacmi (2026-08-01 ölçümü: 117.738 karakter).
#: Kütlesel silmeyi yakalar; küçük düzenlemeler için ~%10 pay bırakıldı.
MIN_SSOT_BODY_CHARS = 105_000

#: Gövdesi OLMAYAN ama meşru KR başlıkları — bunlar bölüm/başlık girişleridir, kural değil
#: (ölçüldü: dördü de hemen ardından başka bir başlık geliyor). Yeni bir KR bu listeye
#: eklenmeden gövdesiz kalamaz.
SSOT_STRUCTURAL_HEADINGS = ("KR-010", "KR-012", "KR-020", "KR-060")

#: Bir KR gövdesi için anlamlı asgari uzunluk (ölçüldü: en kısa gerçek gövde KR-026 = 170).
MIN_KR_BODY_CHARS = 120


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


def _ssot_bodies() -> dict[str, str]:
    """SSOT metni → {KR kimliği: başlığının ALTINDAKİ gövde}.

    ÖD-12 için gerekli: "kaç KR tanımlı" sorusu başlık sayar, "gövde duruyor mu" sorusu
    İÇERİK ister. Birleşik başlıklarda (`## [KR-018 / KR-082]`) gövde her iki kimliğe de
    yazılır — ikisi de o metinle tanımlıdır.
    """
    lines = SSOT_TEXT.read_text(encoding="utf-8").splitlines()
    heads: list[tuple[int, list[str]]] = []
    for index, line in enumerate(lines):
        stripped = line.lstrip()
        if stripped.startswith("#") and re.search(r"KR-\d{3}", stripped):
            heads.append((index, sorted(set(re.findall(r"KR-\d{3}", stripped)))))

    bodies: dict[str, str] = {}
    for position, (start, krs) in enumerate(heads):
        end = heads[position + 1][0] if position + 1 < len(heads) else len(lines)
        body = "\n".join(lines[start + 1:end]).strip()
        for kr in krs:
            # ⚠️ `setdefault` ŞART: boş gövde de sözlüğe girmeli. İlk yazımda yalnız
            #    "daha uzunsa yaz" vardı ve boş gövdeler sözlüğe HİÇ girmiyordu → gövdesi
            #    silinmiş bir KR, "boş gövde" kapısının görüş alanı DIŞINDA kalıyordu.
            #    Mutasyonla yakalandı (KR-000 gövdesi silindi, kapı yeşil kaldı).
            bodies.setdefault(kr, "")
            if len(body) > len(bodies[kr]):
                bodies[kr] = body
    return bodies


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

    def test_migration_did_not_empty_the_bodies(self) -> None:
        """🔴 ÖD-12 — BAŞLIK saymak silmeyi göremez; İÇERİK ölçülür.

        Yukarıdaki test KR *kimliklerini* sayar. Bir KR'nin normatif gövdesi silinip
        başlığı bırakılsaydı sayı değişmez, kapı yeşil kalırdı — "göç taşımadır" iddiası
        ölçülmemiş olurdu. Burada iki şey ölçülür: her gövdenin anlamlı uzunlukta olması
        ve toplam normatif hacmin çökmemesi.
        """
        bodies = _ssot_bodies()
        empty = sorted(
            kr for kr, body in bodies.items()
            if len(body) < MIN_KR_BODY_CHARS and kr not in SSOT_STRUCTURAL_HEADINGS
        )
        assert not empty, (
            f"SSOT metninde başlığı olup gövdesi (neredeyse) BOŞ olan KR(ler): {empty}. "
            "Göç sırasında gövde silinmiş olabilir. Gerçekten bir bölüm başlığıysa "
            "SSOT_STRUCTURAL_HEADINGS'e gerekçesiyle eklenir — sessizce boş kalamaz."
        )

        volume = sum(len(body) for body in bodies.values())
        assert volume >= MIN_SSOT_BODY_CHARS, (
            f"toplam normatif gövde hacmi {volume} < {MIN_SSOT_BODY_CHARS} karakter "
            "(2026-08-01 ölçümü: 117.738). Kütlesel bir silme olmuş olabilir; başlık "
            "sayısı bunu göstermez."
        )

    @pytest.mark.parametrize("kr", SSOT_STRUCTURAL_HEADINGS)
    def test_structural_heading_declaration_is_not_stale(self, kr: str) -> None:
        """Bölüm başlığı gövde kazandıysa beyan SİLİNMELİ — liste yalan söylememeli."""
        body = _ssot_bodies().get(kr, "")
        assert len(body) < MIN_KR_BODY_CHARS, (
            f"{kr} artık {len(body)} karakterlik bir gövde taşıyor ama hâlâ "
            "SSOT_STRUCTURAL_HEADINGS'te 'gövdesiz başlık' olarak beyanlı. Beyanı kaldırın."
        )

    def test_pointer_sections_stay_pointers(self) -> None:
        """🔴 ÖD-11 — damga bir MUAFİYET değildir: altına gövde yazılamaz.

        Kapı bir bölümü "işaretçi" saymak için yalnız damgaya bakıyordu. Damga dururken
        altına kanonik metinle **çelişen** bir normatif gövde yazmak mümkündü ve
        `_registry_body_krs()` onu görmezdi — ikili gövde sayısı 0 kalırdı.

        Ölçülmüş ayrım: işaretçiler ≤ 1366 karakter, gerçek gövdeler ≥ 1483.
        """
        oversized = {
            kr: len(body)
            for kr, body in _registry_sections().items()
            if POINTER_MARK in body and len(body) > MAX_POINTER_SECTION_CHARS
        }
        assert not oversized, (
            f"`{POINTER_MARK}` damgası taşıyan bölüm(ler) gövde boyutuna ulaşmış: "
            f"{oversized}. Damga, altına normatif gövde yazmak için bir muafiyet değildir; "
            "kural kanonik metinde yaşar, burada yalnız işaretçi durur (D16-b2). Bölüm "
            "gerçekten büyümesi gerekiyorsa bu eşik BİLİNÇLİ olarak yükseltilir."
        )

    def test_pointer_sections_actually_point_somewhere(self) -> None:
        """İşaretçi bir HEDEF göstermeli — yoksa 'gövde yok' demekten ibarettir."""
        blind = [
            kr
            for kr, body in _registry_sections().items()
            if POINTER_MARK in body and "TARLAANALIZ_SSOT" not in body
        ]
        assert not blind, (
            f"İşaretçi damgası taşıyıp hedef göstermeyen bölüm(ler): {blind}. "
            "Okuyucu kuralın nerede yaşadığını bulamazsa göç yarım kalmıştır."
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
