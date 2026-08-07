"""AV-3 kapısı — `calibration_type` türetmesi **İKİ GİRDİLİDİR** (drone sınıfı × motor kipi).

NEDEN BU DOSYA VAR (2026-08-02, çok dilli motor araştırması):
    E13-R türetmeyi tek girdiye bağladı: `drone_capability_matrix.yaml` →
    `capabilities[drone_type].calibration_class`. O karar geçerli ama **eksikti**.

    Araştırma ölçtü: **DJI Terra'da radyometrik düzeltme KAPALIYKEN çıktı reflektans
    değil ham DN'dir** (dijital sayı — sensör sayımı). Resmi kılavuz:
    *"Multispectral images with radiometric correction can be reconstructed to a 2D
    multispectral map with an output of reflectance"* ⇒ düzeltme yoksa çıktı DN'dir.

    Tek girdili türetmede aynı M3M uçuşu bu kipte işlendiğinde sistem yine `RELATIVE`
    yazardı ve worker'ın NDVI eşikleri **ham DN'e** uygulanırdı. Bu, denetimde S1
    olarak kaydedilen fail-open bulgusunun birebir aynı sınıfıdır — farkı, hatanın
    platformda bir yükseltme adımında değil **edge'de doğuşta** üretilmesi.

BU KAPI NE KORUR:
    ① Yeni kanonik sözlük (`radiometric_mode.enum.v1.json`) var ve biçimli.
    ② Türetme tablosu **TAM** — her (sınıf × kip) çifti bir değer üretir, boş göz yok.
    ③ `RAW_DN` her sınıfta `NONE` üretir (fabrika kalibrasyonu ham DN'i telafi etmez).
    ④ Tablo ile E13-R'nin `map.allowed` bloğu **ayrışamaz**.
    ⑤ Tablonun kip anahtarları kanonik enum'un değerleriyle **birebir** aynı —
       iki dosya sessizce ayrışamaz (D16'nın kapattığı "ikili gerçek" deseni).
    ⑥ `DLS2_RELATIVE` hiçbir gözde üretilmez.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
CAL_ENUM = ROOT / "enums" / "calibration_type.enum.v1.json"
RAD_ENUM = ROOT / "enums" / "radiometric_mode.enum.v1.json"

AXIS_KEY = "x-radiometric-axis-2026-08-02"
HARD_REJECT = "NONE"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _axis() -> dict:
    derivation = _load(CAL_ENUM)["x-derivation"]
    assert AXIS_KEY in derivation, (
        f"`x-derivation` içinde `{AXIS_KEY}` yok — iki girdili türetme kuralı "
        "makine-okunur biçimde yaşamıyor demektir (yalnız prose kalırsa bir sonraki tur görmez)"
    )
    return derivation[AXIS_KEY]


# --------------------------------------------------------------------------
# ① Kanonik sözlük var ve biçimli
# --------------------------------------------------------------------------


def test_radiometric_mode_enum_exists_and_is_well_formed() -> None:
    assert RAD_ENUM.is_file(), (
        "radiometric_mode kanonik enum'u YOK. Bu kavram tüketici depoda (edge) "
        "uydurulamaz — worker CLAUDE.md §2.1: yeni sözlük kanonikten doğar."
    )
    data = _load(RAD_ENUM)
    for key in ("$schema", "$id", "title", "description", "type", "enum", "x-enum-descriptions"):
        assert key in data, f"radiometric_mode enum'unda zorunlu anahtar yok: {key}"
    assert data["type"] == "string"
    assert data["enum"] == ["PANEL", "SUN_IRRADIANCE", "SENSOR_CORRECTED", "RAW_DN"]
    # Her değerin açıklaması olmalı — açıklamasız değer, anlamı koda gömer.
    assert set(data["x-enum-descriptions"]) == set(data["enum"])


def test_radiometric_mode_declares_fail_closed_default() -> None:
    """Kip beyan edilmemişse en güçlü sınıf DEĞİL, `RAW_DN` varsayılır."""
    data = _load(RAD_ENUM)
    assert "x-fail-closed" in data, "fail-closed politikası beyan edilmemiş"
    policy = json.dumps(data["x-fail-closed"], ensure_ascii=False)
    assert "RAW_DN" in policy


# --------------------------------------------------------------------------
# ② + ③ Tablo tam ve ham DN her yerde hard reject
# --------------------------------------------------------------------------


def test_derivation_table_is_complete() -> None:
    """Her (calibration_class × radiometric_mode) çifti bir değer üretmeli — boş göz yok."""
    table = _axis()["table"]
    classes = ("relative", "absolute")
    modes = tuple(_load(RAD_ENUM)["enum"])

    expected_keys = {f"{c}|{m}" for c in classes for m in modes}
    assert set(table) == expected_keys, (
        f"tablo eksik ya da fazla göz taşıyor. Eksik: {sorted(expected_keys - set(table))} · "
        f"Fazla: {sorted(set(table) - expected_keys)}"
    )


def test_raw_dn_is_hard_reject_for_every_drone_class() -> None:
    """Fabrika kalibrasyonlu (absolute) sensör bile ham DN'i telafi etmez."""
    table = _axis()["table"]
    for key, value in table.items():
        if key.endswith("|RAW_DN"):
            assert value == HARD_REJECT, (
                f"{key} -> {value}. Ham DN reflektans DEĞİLDİR; `{HARD_REJECT}` olmalı. "
                "Bu gözü gevşetmek NDVI eşiklerini ham dijital sayıya uygulatır (S1 sınıfı)."
            )


def test_reflectance_modes_never_produce_hard_reject() -> None:
    """Düzeltme uygulanmışsa paket kalibre sayılmalı — aksi hâlde kapı fail-closed'a saplanır."""
    table = _axis()["table"]
    for key, value in table.items():
        if not key.endswith("|RAW_DN"):
            assert value != HARD_REJECT, f"{key} -> {value}: reflektans kipi reddedilemez"


# --------------------------------------------------------------------------
# ④ + ⑤ İki blok ve iki dosya ayrışamaz
# --------------------------------------------------------------------------


def test_table_agrees_with_e13r_allowed_sets() -> None:
    """Tablonun reflektans gözleri E13-R'nin `map.<class>.allowed` kümesinin İÇİNDE olmalı."""
    derivation = _load(CAL_ENUM)["x-derivation"]
    table = derivation[AXIS_KEY]["table"]
    for key, value in table.items():
        drone_class, mode = key.split("|", 1)
        if mode == "RAW_DN":
            continue
        allowed = derivation["map"][drone_class]["allowed"]
        assert value in allowed, (
            f"{key} -> {value} ama E13-R `map.{drone_class}.allowed` = {allowed}. "
            "İki blok ayrıştı — aynı kuralın iki gerçeği olamaz (D16 dersi)."
        )


def test_table_mode_keys_match_canonical_enum_exactly() -> None:
    """Tablonun kip anahtarları kanonik enum değerleriyle birebir aynı olmalı."""
    canonical = set(_load(RAD_ENUM)["enum"])
    used = {key.split("|", 1)[1] for key in _axis()["table"]}
    assert used == canonical, (
        f"tablo kipleri {sorted(used)} ≠ kanonik enum {sorted(canonical)}. "
        "İki dosya sessizce ayrışamaz."
    )


def test_table_never_produces_forbidden_values() -> None:
    """`DLS2_RELATIVE` hiçbir gözde üretilmez — hiçbir drone sınıfı için türetilemez."""
    produced = set(_axis()["table"].values())
    assert "DLS2_RELATIVE" not in produced, (
        "DLS2_RELATIVE türetildi. Bu değer `forbidden.relative` içinde ve `absolute` "
        "sınıfının izinli kümesinde de yok; yalnız içe aktarılan üçüncü-parti veri seti etiketidir."
    )


def test_produced_values_fit_the_calibrated_surface_or_hard_reject() -> None:
    """Üretilen her değer ya kalibre yüzeyin bağlam alt-kümesinde olmalı ya da NONE."""
    data = _load(CAL_ENUM)
    surface = set(data["x-context-subsets"]["edge/calibrated_dataset_manifest"])
    for key, value in _axis()["table"].items():
        assert value in surface or value == HARD_REJECT, (
            f"{key} -> {value}: kalibre yüzeyin alt-kümesinde ({sorted(surface)}) yok "
            f"ve {HARD_REJECT} de değil — şema bu belgeyi reddeder."
        )


# --------------------------------------------------------------------------
# Karar dayanağı silinirse kapı kırmızıya döner
# --------------------------------------------------------------------------


def test_axis_carries_its_measured_evidence() -> None:
    """Gerekçe silinirse karar dayanaksız kalır — E13-R kapısıyla aynı hüküm."""
    axis = _axis()
    why = axis.get("why", "")
    assert "DN" in why, "ham DN gerekçesi kayıp"
    assert "reflectance" in why, "resmi kılavuz alıntısı kayıp"
    assert axis.get("second_source", "").startswith("radiometric_mode.enum"), (
        "ikinci girdinin kanonik kaynağı beyan edilmemiş"
    )
    assert "invariants" in axis and len(axis["invariants"]) >= 4
