"""E13 kararı kapısı — `calibration_type` ekseni temiz kalsın.

🔄 **E13-R (2026-08-01, ikinci oturum — koordinatör onaylı): KARAR TÜRETMEYE ÇEVRİLDİ.**
Aşağıdaki gerekçe *mutlak sınıf* sensörler için geçerliliğini korur, ama kalibre pakete
yazılacak değer **filo-geneli sabit değildir**: `drone_capability_matrix.yaml →
capabilities[drone_type].calibration_class`'tan türetilir (göreli sınıf → `RELATIVE`).
Türetme kuralının kapısı **ayrı dosyadadır**: `tests/test_calibration_type_derivation.py`.
Bu dosya eksenin *temizliğini* korur (yanlış donanım adı sızmasın, karar değeri şemadan
kaybolmasın); türetme mantığını değil.

E13 KARARI (2026-08-01, ilk hâli): edge kalibre paket manifestine yazılacak değer
**`ABSOLUTE`**. Soru planda *"RELATIVE mi DLS2_RELATIVE mi"* diye kurulmuştu; ölçüm
**ikisinin de yanlış** olduğunu gösterdi.

ÖLÇÜM (dosya:satır ile):
  ① **Panel ZORUNLU.** `docs/TARLAANALIZ_SSOT_v1_2_0.txt` KR-018: *"Reflectance Panel
     (yansıma paneli) kullanımı SOP'a göre zorunlu"*; KR-092: *"Her uçuşun başında ve
     sonunda CRP (kalibrasyon paneli) radyometrik kalibrasyonu yapılır (KR-018/082
     hard-gate); **DLS (ışık sensörü) tek başına yeterli değildir**"*.
  ② **Motor Pix4Dfields** (edge `src/core/services/calibration_gate/pix4d_runner.py`),
     ve kanonik enum `ABSOLUTE`'u tam olarak bu diye tanımlıyor: *"Mutlak reflektans
     (ör. **Pix4D panel-tabanlı**)"* → platform sınırında `PANEL_ABSOLUTE`'a normalize.
  ③ `RELATIVE` = *"Saha-bazlı göreli kalibrasyon (ör. DJI Mavic 3M çıktısı)"* — bu
     **panelsiz ham** M3M çıktısıdır. Panel + Pix4D işlemesi o sınıfı aşar; `RELATIVE`
     yazmak, yapılan kalibrasyonu **olduğundan zayıf** raporlamak olurdu.
  ④ `DLS2_RELATIVE` **iki kez** yanlış:
       (a) **Donanım adı yanlış.** Ölçüldü — SSOT KR-018: *"MicaSense RedEdge-P/Altum-PT:
           … **DLS2** + reflectance panel"*. DLS2 bir **MicaSense** parçasıdır; M3M'nin
           dahili güneş sensörü DLS2 değildir. Uygulaması olmayan bir adı sözleşmeye
           yazmak, `CHLOROPHYLL_A` dersinin tekrarı olurdu.
       (b) **Eksen karışıklığı.** Enum'un kendi `x-separate-axis` bloğu diyor ki
           `DLS_IRRADIANCE` bir **`calibration_method`**'dur, `calibration_type` değil —
           *"Bunlar sensör-tipine özgüdür ve calibration_type ile birleştirilmez."*
           `DLS2_RELATIVE` zaten bu ayrımı ihlal eden tarihsel bir değerdir.

SONUÇ — **C6 İŞ YOK.** Karar `ABSOLUTE` olduğu için alt kümeyi `DLS2_RELATIVE` ile
genişletmek gerekmedi; C8 töreninin önündeki E13/C6 kilidi kalktı.

⚠️ **Aynı gün, sonra:** C6b/S2 alt kümeye `PANEL_ABSOLUTE`'u **ekledi** (intake bu değeri
zaten kabul ediyordu; kalibre manifestte yazılamaması aynı istasyonun iki belgesi arasında
sessiz bir daralmaydı). Yani bugünkü alt küme `["ABSOLUTE", "RELATIVE", "PANEL_ABSOLUTE"]`
ve E13 yalnız `DLS2_RELATIVE`'i dışarıda tutar. Bu satır bir kez bayat kaldı — dosyanın
geri kalanı sayıyı değil **ölçümü** kullanır.

BU KAPI NEYİ KORUR: bir sonraki tur *"M3M'de de ışık sensörü var, DLS2_RELATIVE
ekleyelim"* diyebilir. O ekleme, yanlış donanım adını ve eksen karışıklığını kalibre
paket yüzeyine sokar. Kapı bunu kırmızıya çevirir ve gerekçeyi gösterir.

🔴 **ÖD-3 (2026-08-01) — bu kapı YALAN YEŞİLDİ ve düzeltildi.** `_calibrated_subset()`
yalnız `x-context-subsets` **kayıt defterini** okuyordu; belgeleri kabul/ret eden şey ise
şemanın **inline** enum'u. Ölçüldü: defter `PANEL_ABSOLUTE` diyorken şema hâlâ
`[ABSOLUTE, RELATIVE]` idi — kapı yeşil, karar uygulanmamış. Artık her iddia **iki yüzeyde
birden** ölçülüyor; ikisinin eşitliğini ayrıca `tests/test_context_subset_binding.py`
zorluyor (defterden ya da şemadan tek taraflı sapma kırmızıdır).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
ENUM = ROOT / "enums" / "calibration_type.enum.v1.json"
SSOT_TEXT = ROOT / "docs" / "TARLAANALIZ_SSOT_v1_2_0.txt"
CALIBRATED_SCHEMA = ROOT / "schemas" / "edge" / "calibrated_dataset_manifest.v1.schema.json"

#: E13 kararının değeri. Değişirse bu dosyanın gerekçesi de yeniden yazılmalıdır.
E13_DECISION = "ABSOLUTE"

#: Kalibre paket manifesti bağlamı — E13'ün yazdığı yüzey.
CALIBRATED_CONTEXT = "edge/calibrated_dataset_manifest"


def _enum_doc() -> dict:
    return json.loads(ENUM.read_text(encoding="utf-8"))


def _registry_subset() -> list[str]:
    """Kayıt defteri (`x-context-subsets`) — anlam ve gerekçenin yaşadığı yer."""
    subsets = _enum_doc()["x-context-subsets"]
    assert CALIBRATED_CONTEXT in subsets, (
        f"'{CALIBRATED_CONTEXT}' alt kümesi enum'dan kaybolmuş — E13'ün yazdığı yüzey "
        "artık bağlam-bazlı kısıtlanmıyor demektir."
    )
    return list(subsets[CALIBRATED_CONTEXT])


def _schema_subset() -> list[str]:
    """Şemanın inline enum'u — **belgeleri fiilen kabul/ret eden** yüzey (ÖD-3)."""
    doc = json.loads(CALIBRATED_SCHEMA.read_text(encoding="utf-8"))
    node = doc["properties"]["calibration_result"]["properties"]["calibration_type"]
    return list(node["enum"])


def _calibrated_surfaces() -> dict[str, list[str]]:
    """İki yüzey birden. E13 iddiaları **ikisinde de** doğrulanır.

    Tek yüzey ölçmek ÖD-1'in oluşmasına izin verdi: karar deftere yazıldı, şema
    güncellenmedi, kapı yeşil kaldı ve `PANEL_ABSOLUTE` taşıyan belge reddedilmeye
    devam etti.
    """
    return {"kayıt defteri": _registry_subset(), "şema inline enum": _schema_subset()}


class TestE13DecisionHolds:
    def test_decided_value_is_accepted_by_the_calibrated_manifest(self) -> None:
        """E13 kararı bugünkü alt kümede GEÇERLİ olmalı — yoksa C6 yeniden açılır."""
        for surface, subset in _calibrated_surfaces().items():
            assert E13_DECISION in subset, (
                f"E13 kararı '{E13_DECISION}' ama {CALIBRATED_CONTEXT} **{surface}** {subset}. "
                "Karar değeri kabul edilmiyorsa contract değişikliği (C6) yeniden ZORUNLU "
                "hâle gelir; 'C6 iş yok' hükmü bu satıra dayanıyordu."
            )

    def test_decision_value_exists_in_canonical_vocabulary(self) -> None:
        assert E13_DECISION in _enum_doc()["enum"], (
            f"'{E13_DECISION}' kanonik vocabulary'den çıkarılmış — bu MAJOR bir değişiklik "
            "ve E13 kararını geçersiz kılar."
        )

    def test_dls2_relative_stays_out_of_the_calibrated_package_surface(self) -> None:
        """🔴 Yanlış donanım adı kalibre paket yüzeyine SIZAMAZ.

        `DLS2` ölçülmüş bir MicaSense parçasıdır (SSOT KR-018). M3M'nin dahili güneş
        sensörünü onunla adlandırmak, uygulaması olmayan bir adı sözleşmeye yazmaktır.
        Ayrıca irradyans **yöntemi** ayrı eksendir (`x-separate-axis`).
        """
        for surface, subset in _calibrated_surfaces().items():
            self._assert_no_dls2(surface, subset)

    @staticmethod
    def _assert_no_dls2(surface: str, subset: list[str]) -> None:
        assert "DLS2_RELATIVE" not in subset, (
            f"'DLS2_RELATIVE' {CALIBRATED_CONTEXT} **{surface}**'ine eklenmiş. E13 kararı bunu "
            "iki gerekçeyle reddetti: (a) DLS2 bir MicaSense donanımıdır (SSOT KR-018: "
            "'MicaSense RedEdge-P/Altum-PT: DLS2 + reflectance panel'), M3M'nin güneş "
            "sensörü DLS2 değildir; (b) enum'un kendi x-separate-axis bloğu irradyans "
            "yöntemini (DLS_IRRADIANCE) AYRI eksen ilan ediyor — calibration_type ile "
            "birleştirilmez. Gerçekten gerekiyorsa önce o eksen kararı değişmeli."
        )

    def test_irradiance_method_is_still_a_separate_axis(self) -> None:
        """Kararın dayandığı eksen ayrımı sessizce kaldırılamaz."""
        axis = _enum_doc().get("x-separate-axis") or {}
        text = json.dumps(axis, ensure_ascii=False)
        assert "calibration_method" in axis, (
            "`x-separate-axis.calibration_method` kaldırılmış. E13 kararının (b) gerekçesi "
            "bu ayrıma dayanıyordu: irradyans/panel bir YÖNTEMDİR, kalibrasyon TİPİ değil."
        )
        assert "DLS_IRRADIANCE" in text, (
            "`DLS_IRRADIANCE` yöntem ekseninden çıkarılmış — o zaman irradyans nereye "
            "yazılacak? Eksen ayrımı belgesiz kalırsa DLS2_RELATIVE geri döner."
        )


class TestPanelRequirementIsTheBasis:
    """E13'ün (a) gerekçesi: panel zorunlu olduğu için MUTLAK SINIF sensörde sonuç mutlaktır.

    🔄 **E13-R düzeltmesi:** panel zorunluluğu tek başına *ayırt edici* değildir — SOP
    gereği panel HER uçuşta kullanılır (KR-018/KR-092), yani göreli sınıf bir sensörde de
    kullanılır. Ayırt edici olan **sensör sınıfıdır** (`calibration_class`). Aşağıdaki
    testler kararın mutlak-sınıf ayağını korur; göreli sınıf kuralı
    `tests/test_calibration_type_derivation.py`'de zorlanır.
    """

    def test_panel_is_mandatory_in_normative_text(self) -> None:
        text = SSOT_TEXT.read_text(encoding="utf-8")
        assert "Reflectance Panel" in text and "zorunlu" in text, (
            "KR-018'in panel zorunluluğu normatif metinden kaybolmuş. E13 kararı "
            "'panel zorunlu ⇒ mutlak reflektans ⇒ ABSOLUTE' zincirine dayanıyor; ilk "
            "halka kopa̧rsa karar da dayanaksız kalır."
        )

    def test_dls_alone_is_declared_insufficient(self) -> None:
        text = SSOT_TEXT.read_text(encoding="utf-8")
        assert "tek başına yeterli değildir" in text, (
            "KR-092'nin 'DLS (ışık sensörü) tek başına yeterli değildir' kuralı "
            "kaybolmuş. Bu cümle olmadan DLS2_RELATIVE'ı reddeden gerekçe zayıflar."
        )

    def test_absolute_is_documented_as_panel_based(self) -> None:
        descriptions = _enum_doc()["x-enum-descriptions"]
        assert "panel" in descriptions[E13_DECISION].lower(), (
            f"'{E13_DECISION}' açıklaması artık panel-tabanlı olduğunu söylemiyor. "
            "E13 kararı bu tanıma dayanıyor (Pix4D panel-tabanlı mutlak reflektans)."
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
