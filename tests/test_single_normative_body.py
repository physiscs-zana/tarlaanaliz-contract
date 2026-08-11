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


class TestDerivedQuantitiesAreDefined:
    """A3 → D12 — atıf alan her TÜRETİLMİŞ büyüklük tanımlı olmalı VE teslimat
    kuralı, ön fazın kapalı listesiyle makine düzeyinde ANLAŞMALI.

    Kapının iki ayrı hayatı oldu:

    * **A3 (2026-07-31):** `stress_ratio` 3 yerde atıf alıyordu, 0 yerde tanımlıydı.
      O günkü kapı yalnız "beyan var mı" diye bakıyordu (`status`, `problem`,
      `until_then` alanları dolu mu).
    * **D12 (2026-08-11):** beyanın KENDİSİ yanlış çıktı. *"ad var, üretim yok"*
      diyordu; ölçüm tersini gösterdi — üretici `feature_extraction.compute_indices_v2`
      içinde değil, worker'ın çıkarım hattındaydı (`inference/pipeline.py`) ve raster
      nesne deposuna yüklenip manifest'te listeleniyordu. Yani beyan-varlığını denetleyen
      kapı, İÇERİĞİ yanlış bir beyanı sorunsuz geçirdi.

    Bu yüzden kapı artık **beyan varlığını değil, iki makine-okunur kaynağın
    tutarlılığını** ölçer: `indexDefinitions[*].delivery_rule.preliminary` ile
    `report_phase.enum` → `x-preliminary-content.stage_b_post_analysis.fields`
    aynı şeyi söylemek ZORUNDADIR. Bu liste artık platformda gerçek bir kapıyı
    besliyor (`preliminary_content_gate.py`), yani ayrışma bir belge tutarsızlığı
    değil, doğrudan bir davranış hatasıdır.
    """

    def _enum_doc(self) -> dict:
        return json.loads(
            (ROOT / "enums" / "analysis_type.enum.v1.json").read_text(encoding="utf-8")
        )

    def _stage_b_fields(self) -> list[str]:
        report_phase = json.loads(
            (ROOT / "enums" / "report_phase.enum.v1.json").read_text(encoding="utf-8")
        )
        return list(
            report_phase["x-preliminary-content"]["stage_b_post_analysis"]["fields"]
        )

    def test_stress_ratio_is_defined_from_measured_code(self) -> None:
        """Tanım TAHMİNLE değil, ÜRETİCİ koddan ölçülerek yazılmış olmalı."""
        entry = self._enum_doc()["metadata"]["indexDefinitions"].get("stress_ratio")
        assert entry, (
            "`stress_ratio` KR-093 metinlerinde anılıyor ama `indexDefinitions`'ta yok. "
            "Tanımsız büyüklük ne üretilebilir ne denetlenebilir."
        )
        assert entry.get("status") == "DEFINED", (
            "D12 kararı: `stress_ratio` ÖLÇÜLEREK tanımlandı. Statü geri alınıyorsa "
            "gerekçesi ve yeni ölçüm bu kapıyla birlikte yazılmalı."
        )
        # Beklenen değer LİTERAL yazılır (uygulamadan türetilmez): 2026-08-11'de
        # `src/indices/stress_ratio.py` okunarak ölçüldü. Yön DE bağlayıcıdır —
        # `NDVI / NDRE` başka bir büyüklüktür ve eşikleri ters çevirir.
        assert entry.get("formula") == "stress_ratio = NDRE / NDVI", (
            f"formül ölçülen uygulamayla birebir olmalı, bulunan: {entry.get('formula')!r}"
        )
        # Sınır davranışı MAKİNE-OKUNUR: "yazı var mı" denetimi, D12'de görüldüğü gibi
        # içeriği yanlış bir beyanı da geçirir. Değerler uygulamadan ölçüldü
        # (`stress_ratio.py:59-60` → `np.where(ndvi > 0.0, ratio, 1.0)`); değiştirmek
        # için önce kodu yeniden ÖLÇMEK gerekir.
        guard = entry.get("domain_guard")
        assert isinstance(guard, dict), (
            "`domain_guard` yapılandırılmış olmalı (valid_where + outside_value); düz "
            "metin, tüketicinin sınır davranışını uydurmasına açık kapı bırakır."
        )
        assert guard.get("valid_where") == "NDVI > 0", (
            f"geçerlilik koşulu ölçülenle uyuşmuyor: {guard.get('valid_where')!r}"
        )
        assert guard.get("outside_value") == 1.0, (
            "geçerlilik dışı piksellerde NÖTR 1.0 yazılmalı — 0.0 yazmak 'tam stresli' "
            f"demektir ve su/gölge/toprağı hasta bitki gibi gösterir. Bulunan: "
            f"{guard.get('outside_value')!r}"
        )
        producers = entry.get("measured_producers") or []
        assert producers, "tanımın dayandığı ÜRETİCİ yollar yazılmalı (iddia = ölçüm)"
        for yol in producers:
            assert re.search(r":\d+", str(yol)), (
                f"üretici atfı `dosya:satır` taşımalı, bulunan: {yol!r} — 'şu dosyada var' "
                "demek ölçüm değildir."
            )

    def test_delivery_rule_agrees_with_preliminary_closed_list(self) -> None:
        """MAKİNE ↔ MAKİNE: teslimat bayrağı ile ön fazın kapalı listesi aynı şeyi demeli.

        Bu iki kaynak ayrışırsa, biri belgeyi diğeri kodu yönlendirdiği için sözleşme
        iki farklı davranış vaat eder. Kapı her iki yönü de yakalar: bayrağı `true`
        yapmak da, katmanı listeye eklemek de tek başına kırmızıya döndürür.
        """
        stage_b = self._stage_b_fields()
        definitions = self._enum_doc()["metadata"]["indexDefinitions"]
        kontrol_edilen = 0
        for ad, entry in definitions.items():
            if not isinstance(entry, dict):
                continue  # `description` gibi düz metin alanları
            rule = entry.get("delivery_rule")
            if not isinstance(rule, dict):
                continue
            katman = rule.get("feeds_layer")
            assert isinstance(katman, str) and katman, (
                f"{ad}: `delivery_rule` var ama hangi katmanı beslediği yazılmamış"
            )
            bayrak = rule.get("preliminary")
            assert isinstance(bayrak, bool), (
                f"{ad}: `delivery_rule.preliminary` bool olmalı (bulunan: {bayrak!r})"
            )
            assert bayrak == (katman in stage_b), (
                f"{ad}: `delivery_rule.preliminary={bayrak}` ile ön faz kapalı listesi "
                f"çelişiyor (`{katman}` stage_b'de {'VAR' if katman in stage_b else 'YOK'}). "
                "İkisi aynı commit'te güncellenmelidir — biri belgeyi, diğeri platformdaki "
                "`preliminary_content_gate` kapısını yönlendiriyor."
            )
            kontrol_edilen += 1
        # Sayaç kilidi: döngü hiç koşmazsa test boşuna geçmesin.
        assert kontrol_edilen > 0, (
            "hiçbir `indexDefinitions` girdisinde `delivery_rule` bulunamadı — kapı "
            "sessizce hiçbir şey ölçmüyor olabilir (anahtar adı mı değişti?)"
        )

    def test_proxy_layer_is_never_deliverable_in_preliminary(self) -> None:
        """`proxy_only` bir katmanı besleyen indeks ön fazda teslim EDİLEMEZ (D17)."""
        enum_doc = self._enum_doc()
        by_layer = enum_doc["metadata"]["bandRequirements"]["byLayer"]
        definitions = enum_doc["metadata"]["indexDefinitions"]
        kontrol_edilen = 0
        for ad, entry in definitions.items():
            if not isinstance(entry, dict):
                continue
            rule = entry.get("delivery_rule")
            if not isinstance(rule, dict):
                continue
            katman = rule.get("feeds_layer")
            if by_layer.get(katman, {}).get("availability") != "proxy_only":
                continue
            assert rule.get("preliminary") is False, (
                f"{ad}: `{katman}` bir VEKİL katman (`proxy_only`) — doğrudan ölçümü bu "
                "donanımda yok. Vekil gösterge uzman kapısı ÖNCESİNDE çiftçiye "
                "sunulamaz: doğrulanmış bir bulgu sanılır (KR-093 + KR-019)."
            )
            kontrol_edilen += 1
        assert kontrol_edilen > 0, (
            "hiçbir vekil-katman indeksi denetlenmedi — `byLayer` availability değerleri "
            "ya da `feeds_layer` adları değişmiş olabilir; kapı kör kalmış."
        )

    def test_no_silent_undefined_quantity_in_preliminary_mapping(self) -> None:
        """Ön faz eşlemesi ham indeks adına dayanamaz (D17'de çıkarıldı, öyle kalmalı)."""
        report_phase = json.loads(
            (ROOT / "enums" / "report_phase.enum.v1.json").read_text(encoding="utf-8")
        )
        stage_b = report_phase["x-preliminary-content"]["stage_b_post_analysis"]
        # `x-removed-…` / `x-enforcement-…` blokları KARARIN KAYDIDIR; yasak olan,
        # eşlemenin `fields` içinde YAŞAMASIDIR. Bu yüzden yalnız `fields` denetlenir —
        # aksi hâlde kararın gerekçesini yazmak kapıyı kırardı.
        alanlar = json.dumps(stage_b["fields"], ensure_ascii=False)
        assert "stress_ratio" not in alanlar, (
            "ön faz stage_b yine `stress_ratio`'ya dayanıyor — D17 ile WATER_STRESS "
            "çıkarıldı, eşleme de çıkmalıydı"
        )
        assert "WATER_STRESS" not in alanlar, (
            "D17/D12: `WATER_STRESS` vekil katmandır, ön fazın kapalı listesine geri "
            "eklenemez (geri ekleme kararı termal/SWIR donanım kararına bağlıdır)"
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

    def test_proxy_quantity_is_not_mandated_in_prose(self) -> None:
        """Hiçbir normatif gövde `stress_ratio`'yu ZORUNLU teslimat kaynağı sayamaz.

        Gerekçe D12'de (2026-08-11) DEĞİŞTİ, kural değişmedi: büyüklük artık tanımlıdır
        (`NDRE/NDVI`), ama beslediği katman VEKİLDİR (`proxy_only`) ve ön fazın kapalı
        listesi dışındadır. Yani yasağın dayanağı "tanımsız" değil, "doğrulanmamış vekil".
        Tanım geldi diye eşlemeyi geri yazmak, D17 kararını sessizce iptal ederdi.
        """
        for relative, label in self.SOURCES:
            text = (ROOT / relative).read_text(encoding="utf-8")
            assert "←stress_ratio" not in text, (
                f"{label}: `stress_ratio` bir teslimat kaleminin zorunlu kaynağı olarak "
                "yazılmış. Beslediği katman `proxy_only`; ön fazda teslim edilemez."
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
