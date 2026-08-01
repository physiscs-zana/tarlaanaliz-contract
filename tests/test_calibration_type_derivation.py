"""E13-R kapısı — kalibrasyon tipi **drone başına türetilir**, filo-geneli sabit DEĞİLDİR.

NEDEN BU DOSYA VAR (ÖD-5, 2026-08-01 ikinci oturum):
    E13'ün ilk hâli kalibre pakete yazılacak değeri filo-geneli **`ABSOLUTE`** olarak
    sabitledi. Gerekçesi kendi içinde tutarlıydı (panel zorunlu · motor Pix4Dfields ·
    enum `ABSOLUTE`'u *"Pix4D panel-tabanlı"* diye tanımlıyor) ama **kararı reddeden üç
    kanonik kaynağı hiç ölçmemişti**:

      1. `drone_capability_matrix.yaml` → `DJI_MAVIC_3M.calibration_class: relative`
         (+ notu: *"Pix4Dfields göreli kalibrasyon sağlar"*)
      2. `docs/TARLAANALIZ_SSOT_v1_2_0.txt:79` ve `:1014` → *"Pix4Dfields, M3M için tam
         radyometrik kalibrasyon DEĞİL, göreli (relative) kalibrasyon sağlar"*
      3. platform `src/core/domain/value_objects/calibration_class.py:41` →
         `DJI_MAVIC_3M: RELATIVE` (2.0× tolerans gevşemesi bu sınıfa bağlı)

    Sonucu ölçüldü: sabit `ABSOLUTE` yazılırsa worker'ın `FINETUNE_ALLOWED_CALIBRATIONS`
    kümesi (`src/core/domain/enums.py:73`) M3M verisini **ince ayara uygun** sayardı —
    K-3'ün *"fine-tuning: SADECE PANEL+DLS2"* kuralı sessizce delinirdi.

    Karar (koordinatör onayı, 2026-08-01): **E13-R** — değer matristen türetilir.

BU KAPI NE KORUR:
    Türetme kuralı yalnız prose olarak yaşarsa bir sonraki tur onu görmez. Burada
    kural **makine-okunur** (`enums/calibration_type.enum.v1.json → x-derivation`) ve
    bu dosya onu matrisle, kanonik sözlükle ve bağlam alt-kümesiyle bağlar. Kararın
    DAYANAĞI olan üç ölçüm de ayrıca korunur — dayanak silinirse karar da dayanaksız
    kalır ve bu kapı kırmızıya döner.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

try:
    import yaml  # type: ignore[import-untyped]
except ImportError:  # pragma: no cover
    pytest.skip("pyyaml yok", allow_module_level=True)

ROOT = Path(__file__).parent.parent
ENUM = ROOT / "enums" / "calibration_type.enum.v1.json"
MATRIX = ROOT / "drone_capability_matrix.yaml"
SSOT_TEXT = ROOT / "docs" / "TARLAANALIZ_SSOT_v1_2_0.txt"
CALIBRATED_CONTEXT = "edge/calibrated_dataset_manifest"

#: Demo/pilot filosunun ana aracı. Sınıfı değişirse E13-R'nin gerekçesi de değişmiştir.
FLEET_PRIMARY_DRONE = "DJI_MAVIC_3M"


def _enum_doc() -> dict:
    return json.loads(ENUM.read_text(encoding="utf-8"))


def _derivation() -> dict:
    doc = _enum_doc()
    assert "x-derivation" in doc, (
        "`x-derivation` bloğu silinmiş — E13-R kararı makine-okunur kaynağını kaybetti. "
        "Kural yalnız prose'da yaşarsa bir sonraki tur onu görmez (E13'ün ilk hâlinin "
        "düştüğü hata tam buydu)."
    )
    return doc["x-derivation"]


def _matrix_classes() -> dict[str, str]:
    doc = yaml.safe_load(MATRIX.read_text(encoding="utf-8"))
    return {
        drone: entry["calibration_class"]
        for drone, entry in doc["capabilities"].items()
        if isinstance(entry, dict) and "calibration_class" in entry
    }


class TestDerivationIsWiredToTheMatrix:
    """Türetme kaynağı gerçek olmalı — 'matristen türetilir' demek yetmez."""

    def test_every_drone_declares_a_calibration_class(self) -> None:
        doc = yaml.safe_load(MATRIX.read_text(encoding="utf-8"))
        missing = sorted(set(doc["capabilities"]) - set(_matrix_classes()))
        assert not missing, (
            f"Matriste `calibration_class` taşımayan drone(lar): {missing}. Türetme "
            "kaynağı eksikse edge o paket için değer UYDURMAK zorunda kalır."
        )

    def test_every_matrix_class_is_mapped(self) -> None:
        mapped = set(_derivation()["map"])
        unmapped = sorted(set(_matrix_classes().values()) - mapped)
        assert not unmapped, (
            f"Matriste geçen ama türetme tablosunda karşılığı OLMAYAN sınıf(lar): {unmapped}. "
            "Eşlemesiz sınıf, kuralın sessizce atlandığı yerdir."
        )

    def test_mapped_values_exist_in_canonical_vocabulary(self) -> None:
        canonical = set(_enum_doc()["enum"])
        for klass, entry in _derivation()["map"].items():
            unknown = sorted(set(entry["allowed"]) - canonical)
            assert not unknown, f"`{klass}` için kanonik sözlükte olmayan değer(ler): {unknown}"

    def test_mapped_values_are_writable_on_the_calibrated_surface(self) -> None:
        """Türetilen değer kalibre manifeste YAZILABİLİR olmalı — yoksa kural uygulanamaz."""
        subset = set(_enum_doc()["x-context-subsets"][CALIBRATED_CONTEXT])
        for klass, entry in _derivation()["map"].items():
            unwritable = sorted(set(entry["allowed"]) - subset)
            assert not unwritable, (
                f"`{klass}` sınıfı için türetilen {unwritable} değeri kalibre paket "
                f"alt-kümesinde YOK ({sorted(subset)}). Kural kâğıt üzerinde kalır: "
                "edge o değeri yazmak istese şema reddeder (ÖD-1'in aynısı)."
            )


class TestRelativeStaysRelative:
    """🔴 E13'ün ilk hâlinin hatası — regresyon kapısı."""

    def test_relative_class_cannot_produce_an_absolute_label(self) -> None:
        derivation = _derivation()
        allowed = set(derivation["map"]["relative"]["allowed"])
        absolute_values = {"ABSOLUTE", "PANEL_ABSOLUTE"}
        assert not (allowed & absolute_values), (
            f"Göreli sınıf mutlak etiket üretiyor: {sorted(allowed & absolute_values)}. "
            "Bu tam olarak E13'ün geri alınan hâlidir; worker'ın FINETUNE_ALLOWED_"
            "CALIBRATIONS kümesi o etiketi ince ayara uygun sayar ve göreli veri model "
            "eğitimine girer (K-3 ihlali)."
        )

    def test_forbidden_list_is_explicit(self) -> None:
        forbidden = _derivation()["forbidden"]
        assert set(forbidden.get("relative", [])) >= {"ABSOLUTE", "PANEL_ABSOLUTE"}, (
            "Yasak listesi mutlak değerleri açıkça saymalı — 'allowed'da yok' demek, "
            "bir sonraki turda 'acaba unutuldu mu?' sorusuna açık kapı bırakır."
        )

    def test_fleet_primary_drone_is_still_relative(self) -> None:
        """Filo ana aracının sınıfı E13-R'nin dayanağıdır; değişirse karar yeniden açılır."""
        classes = _matrix_classes()
        assert classes.get(FLEET_PRIMARY_DRONE) == "relative", (
            f"{FLEET_PRIMARY_DRONE} matriste artık '{classes.get(FLEET_PRIMARY_DRONE)}'. "
            "E13-R bu değere dayanıyordu (ve bedeli — M3M verisinin ince ayara girmemesi — "
            "bilerek kabul edilmişti). Sınıf değiştiyse karar yeniden ölçülmelidir."
        )


class TestTheBasisIsPreserved:
    """Kararın dayanağı silinemez — silinirse karar da dayanaksız kalır."""

    def test_matrix_note_still_says_relative_for_the_primary_drone(self) -> None:
        text = MATRIX.read_text(encoding="utf-8")
        assert "göreli kalibrasyon" in text, (
            "Matristeki 'Pix4Dfields göreli kalibrasyon sağlar' notu kaybolmuş — E13-R'nin "
            "birinci dayanağı buydu."
        )

    def test_normative_text_still_rejects_absolute_for_the_primary_drone(self) -> None:
        text = SSOT_TEXT.read_text(encoding="utf-8")
        assert "göreli (relative) kalibrasyon" in text and "Mavic 3M" in text, (
            "SSOT'un M3M radyometri notu kaybolmuş (`:79` / `:1014`). E13-R'nin ikinci "
            "dayanağı buydu; normatif metin değiştiyse karar yeniden ölçülmelidir."
        )

    def test_reversal_is_recorded_with_its_cost(self) -> None:
        """Geri alınan karar SESSİZCE silinemez — neden ve bedeli yazılı kalmalı."""
        superseded = _derivation().get("x-superseded-e13-2026-08-01")
        assert superseded, "E13'ün geri alınma kaydı silinmiş"
        for field in ("what", "why_reversed", "what_survives", "cost_accepted"):
            assert superseded.get(field, "").strip(), f"geri alma kaydında `{field}` boş"

    def test_dls2_rejection_survives_the_reversal(self) -> None:
        """E13'ün DLS2_RELATIVE reddi geçerliliğini korur (S3'e kadar)."""
        subset = set(_enum_doc()["x-context-subsets"][CALIBRATED_CONTEXT])
        assert "DLS2_RELATIVE" not in subset
        for entry in _derivation()["map"].values():
            assert "DLS2_RELATIVE" not in entry["allowed"], (
                "Türetme tablosu `DLS2_RELATIVE` üretiyor — E13'ün ayakta kalan yarısı bu "
                "değeri kalibre paket yüzeyinden reddediyordu (satıcı adı + eksen karışıklığı)."
            )


class TestConsumerObligationsAreWritten:
    """Türetme üç depoda uygulanır; kimin ne yapacağı yazılı olmalı (kapı burada değil)."""

    @pytest.mark.parametrize("consumer", ["edge", "platform", "worker"])
    def test_obligation_exists(self, consumer: str) -> None:
        obligations = _derivation()["consumer_obligation"]
        assert obligations.get(consumer, "").strip(), (
            f"`{consumer}` için tüketici yükümlülüğü yazılmamış. Türetme kuralı bu depoda "
            "zorlanamaz (kalibre manifest `drone_type` taşımaz — değer edge'de türetilir), "
            "o yüzden yükümlülüğün YAZILI olması kuralın tek taşıyıcısıdır."
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
