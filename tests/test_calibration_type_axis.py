"""E13 kararı kapısı — `calibration_type` ekseni temiz kalsın.

E13 KARARI (2026-08-01): edge kalibre paket manifestine yazılacak değer **`ABSOLUTE`**.
Soru planda *"RELATIVE mi DLS2_RELATIVE mi"* diye kurulmuştu; ölçüm **ikisinin de
yanlış** olduğunu gösterdi.

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

SONUÇ — **C6 İŞ YOK.** `edge/calibrated_dataset_manifest` alt kümesi bugün
`["ABSOLUTE", "RELATIVE"]`; karar `ABSOLUTE` olduğu için **contract değişikliği
gerekmiyor** (alt küme genişletilmesi ve MINOR bump iptal). C8 töreninin önündeki
E13/C6 kilidi kalkar.

BU KAPI NEYİ KORUR: bir sonraki tur *"M3M'de de ışık sensörü var, DLS2_RELATIVE
ekleyelim"* diyebilir. O ekleme, yanlış donanım adını ve eksen karışıklığını kalibre
paket yüzeyine sokar. Kapı bunu kırmızıya çevirir ve gerekçeyi gösterir.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
ENUM = ROOT / "enums" / "calibration_type.enum.v1.json"
SSOT_TEXT = ROOT / "docs" / "TARLAANALIZ_SSOT_v1_2_0.txt"

#: E13 kararının değeri. Değişirse bu dosyanın gerekçesi de yeniden yazılmalıdır.
E13_DECISION = "ABSOLUTE"

#: Kalibre paket manifesti bağlamı — E13'ün yazdığı yüzey.
CALIBRATED_CONTEXT = "edge/calibrated_dataset_manifest"


def _enum_doc() -> dict:
    return json.loads(ENUM.read_text(encoding="utf-8"))


def _calibrated_subset() -> list[str]:
    subsets = _enum_doc()["x-context-subsets"]
    assert CALIBRATED_CONTEXT in subsets, (
        f"'{CALIBRATED_CONTEXT}' alt kümesi enum'dan kaybolmuş — E13'ün yazdığı yüzey "
        "artık bağlam-bazlı kısıtlanmıyor demektir."
    )
    return list(subsets[CALIBRATED_CONTEXT])


class TestE13DecisionHolds:
    def test_decided_value_is_accepted_by_the_calibrated_manifest(self) -> None:
        """E13 kararı bugünkü alt kümede GEÇERLİ olmalı — yoksa C6 yeniden açılır."""
        subset = _calibrated_subset()
        assert E13_DECISION in subset, (
            f"E13 kararı '{E13_DECISION}' ama {CALIBRATED_CONTEXT} alt kümesi {subset}. "
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
        subset = _calibrated_subset()
        assert "DLS2_RELATIVE" not in subset, (
            f"'DLS2_RELATIVE' {CALIBRATED_CONTEXT} alt kümesine eklenmiş. E13 kararı bunu "
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
    """E13'ün (a) gerekçesi: panel zorunlu olduğu için sonuç MUTLAK reflektanstır."""

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
