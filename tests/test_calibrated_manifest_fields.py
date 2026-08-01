"""C1′ + C3′ — kalibre manifest alanları ve KELİME DAĞARCIĞI türetimi.

Neden bu test var (2026-07-31):
    Bu turun tekrar eden hata sınıfı **paralel vocabulary uydurmak**tı. Plan C1′ için
    `layer_type(ortho/ndvi/ndre/**ndwi**)` öneriyordu — oysa kanonik indeks kümesi
    `drone_capability_matrix.yaml → available_indices` altında yaşıyor ve **NDWI orada YOK**.
    Aynı şekilde plan `calibration_tier` diyordu; contract'ta öyle bir ad yok, kanonik ad
    `calibration_type` ve alt-kümeleri `calibration_type.enum.v1 → x-context-subsets`'te.

    Bu testler alanların **var olmasını** değil, **doğru kaynaktan türetilmiş olmasını** zorlar:
    yeni bir indeks/bant/kalibrasyon değeri ancak kanonik kaynakta varsa şemaya girebilir.
"""

import json
from pathlib import Path

import pytest

try:
    import yaml  # type: ignore[import-untyped]
except ImportError:  # pragma: no cover
    pytest.skip("pyyaml yok", allow_module_level=True)

ROOT = Path(__file__).parent.parent
PLATFORM_FORM = ROOT / "schemas" / "platform" / "calibrated_dataset_manifest.v1.schema.json"
EDGE_FORM = ROOT / "schemas" / "edge" / "calibrated_dataset_manifest.v1.schema.json"
INTAKE = ROOT / "schemas" / "edge" / "intake_manifest.v1.schema.json"
CAPABILITY_MATRIX = ROOT / "drone_capability_matrix.yaml"
CALIBRATION_ENUM = ROOT / "enums" / "calibration_type.enum.v1.json"

NON_INDEX_LAYERS = {"ORTHO", "DSM"}


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _matrix_indices() -> set[str]:
    """drone_capability_matrix.yaml'daki TÜM indeks adları (core+extended+thermal)."""
    doc = yaml.safe_load(CAPABILITY_MATRIX.read_text(encoding="utf-8"))
    found: set[str] = set()

    def walk(node: object) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if key == "available_indices" and isinstance(value, dict):
                    for group in value.values():
                        found.update(group or [])
                elif key == "thermal_indices":
                    found.update(value or [])
                else:
                    walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(doc)
    return found


def _canonical_bands() -> set[str]:
    """Kanonik bant kümesi: intake_manifest.available_bands."""
    intake = _load(INTAKE)
    return set(intake["$defs"]["EdgeForm"]["properties"]["available_bands"]["items"]["enum"])


class TestLayerTypeIsDerivedNotInvented:
    """C1′ — `layer_type` indeks değerleri kanonik matristen gelmeli."""

    def test_index_values_all_exist_in_capability_matrix(self) -> None:
        layer_types = set(
            _load(PLATFORM_FORM)["$defs"]["file_artifact"]["properties"]["layer_type"]["enum"]
        )
        invented = layer_types - NON_INDEX_LAYERS - _matrix_indices()
        assert not invented, (
            f"layer_type kanonik olmayan indeks taşıyor: {sorted(invented)}. "
            "İndeks vocabulary'si drone_capability_matrix.yaml → available_indices'tir; "
            "paralel bir liste uydurulamaz (planın önerdiği 'NDWI' bu yüzden ALINMADI)."
        )

    def test_ndwi_is_not_present(self) -> None:
        """Planın önerdiği ama kanonik olmayan değer regresyon kapısı."""
        layer_types = set(
            _load(PLATFORM_FORM)["$defs"]["file_artifact"]["properties"]["layer_type"]["enum"]
        )
        assert "NDWI" not in layer_types and "ndwi" not in layer_types

    def test_core_indices_are_covered(self) -> None:
        """M3M'in ürettiği çekirdek indeksler kapsanmalı, yoksa alan işe yaramaz."""
        layer_types = set(
            _load(PLATFORM_FORM)["$defs"]["file_artifact"]["properties"]["layer_type"]["enum"]
        )
        assert {"NDVI", "NDRE"} <= layer_types

    def test_layer_type_is_optional(self) -> None:
        artifact = _load(PLATFORM_FORM)["$defs"]["file_artifact"]
        assert "layer_type" not in artifact["required"], "MINOR kalmalı; zorunlu yapmak breaking"

    def test_registry_cross_reference_exists(self) -> None:
        """Türetim kaynağı şemada YAZILI olmalı (bir sonraki tur uydurma sanmasın)."""
        doc = _load(PLATFORM_FORM)
        sync = doc.get("x-registry-sync", {})
        assert "drone_capability_matrix" in json.dumps(sync)


class TestBandVocabularyIsShared:
    """`band` alanı kendi listesini uydurmamalı."""

    def test_platform_artifact_band_matches_canonical(self) -> None:
        bands = set(_load(PLATFORM_FORM)["$defs"]["file_artifact"]["properties"]["band"]["enum"])
        assert bands == _canonical_bands()

    def test_raw_frame_band_matches_canonical(self) -> None:
        """Ham kare `band`'i = kanonik bantlar **+ `RGB`** (S7, 2026-08-01).

        `RGB` bir SPEKTRAL BANT DEĞİLDİR — bir kare TÜRÜDÜR ve bu yüzden kanonik
        `available_bands` sözlüğüne eklenmedi. Yalnız bu alanda geçerlidir, çünkü S7'nin
        çözdüğü sorun tam olarak buydu: alan opsiyonelken `band` YOKLUĞU iki ayrı şeyi
        kodluyordu — (a) bu bir RGB kompozittir (b) bant bilinmiyor. Tüketici ayırt
        edemiyordu. Ayrımı taşıyacak bir değer gerekiyordu ve o değer bir "bant" olmadığı
        için kanonik sözlüğe SIZDIRILMADI.
        """
        frames = _load(EDGE_FORM)["properties"]["raw_frames"]["items"]
        band_enum = set(frames["properties"]["band"]["enum"])
        assert band_enum == _canonical_bands() | {"RGB"}, (
            "ham kare band sözlüğü kanonik bantlar + RGB olmalı. Fazladan bir değer "
            "eklendiyse: bu alan kendi sözlüğünü uyduramaz (AK-7 dersi). RGB eksikse: "
            "S7 geri alınmış demektir — `band` yokluğu yine iki anlama gelir."
        )
        assert "RGB" not in _canonical_bands(), (
            "`RGB` kanonik `available_bands` sözlüğüne sızmış. RGB bir kare TÜRÜDÜR, "
            "spektral bant değildir; oraya girerse sensör kapasitesi hesapları bozulur "
            "(KR-018 bant kapısı 4-bant minimumunu RGB ile sağlanmış sanabilir)."
        )


class TestCalibrationTypeUsesCanonicalName:
    """C1′ — `calibration_tier` diye bir alan YOKTUR."""

    def test_field_is_named_calibration_type(self) -> None:
        props = _load(PLATFORM_FORM)["properties"]
        assert "calibration_type" in props
        assert "calibration_tier" not in props

    def test_no_schema_defines_calibration_tier(self) -> None:
        offenders = [
            str(p.relative_to(ROOT)).replace("\\", "/")
            for p in (ROOT / "schemas").rglob("*.json")
            if '"calibration_tier"' in p.read_text(encoding="utf-8")
        ]
        assert not offenders, f"`calibration_tier` alanı tanımlanmış: {offenders}"

    def test_values_are_a_subset_of_canonical_enum(self) -> None:
        canonical = set(_load(CALIBRATION_ENUM)["enum"])
        used = set(_load(PLATFORM_FORM)["properties"]["calibration_type"]["enum"])
        assert used <= canonical, f"kanonik enum dışı değer: {sorted(used - canonical)}"

    def test_context_subset_is_registered_and_matches(self) -> None:
        """Alt-küme enum'da KAYITLI olmalı — C6'da bunun eksikliği 'iş yok' yanılgısı yaratmıştı."""
        subsets = _load(CALIBRATION_ENUM)["x-context-subsets"]
        key = "platform/calibrated_dataset_manifest"
        assert key in subsets, f"{key} alt-kümesi enum'a kaydedilmemiş"
        assert set(subsets[key]) == set(
            _load(PLATFORM_FORM)["properties"]["calibration_type"]["enum"]
        ), "şemadaki enum ile kayıtlı alt-küme ayrışmış"

    def test_none_is_representable_so_the_gate_can_fail_closed(self) -> None:
        """🔄 2026-07-31/D8 — bu testin İDDİASI TERSİNE ÇEVRİLDİ (denetim bulgusu S1).

        Eski hâli `assert "NONE" not in used` idi ve gerekçesi *"NONE = KR-018 hard
        reject; kalibre paket manifesti onu ilan edemez"* diye yazılmıştı. Gerekçe
        edge'in bakış açısıyla doğruydu (edge kalibrasyon başarısızsa manifest
        üretmez — `calibrated_validator` CHECK 2), ama bu form **platformun
        normalizasyon sınırıdır** ve orada yanlış sonuç veriyordu:

          * alan opsiyonel + alt-kümede NONE yok ⇒ kalibre EDİLMEMİŞ paketin dürüst
            değeri yazılamıyordu,
          * enum'un global kuralı eksik tipi **PANEL_ABSOLUTE**'a yükseltiyordu
            (worker spektral eşiklerinin REFERANS sınıfı),
          * kural canlı kodda birebir vardı: platform
            `worker_job_publisher.py:80-84` → *"status CALIBRATED → PANEL_ABSOLUTE
            (güvenlik-ağı)"*.

        Yani "NONE'u dışarıda tutmak" korumuyordu, tam tersine **fail-open**'ı zorunlu
        kılıyordu. Aynı fonksiyonun 4. adımı zaten NONE üretiyor — değer sistemde
        akıyor, yalnız bu manifestte yazılamıyordu.
        """
        used = set(_load(PLATFORM_FORM)["properties"]["calibration_type"]["enum"])
        assert "NONE" in used, (
            "Platform kalibre manifesti NONE yazamıyorsa, tipi bilinmeyen paket için "
            "dürüst değer yoktur ve sistem varsayıma (fail-open) mecbur kalır."
        )

    def test_hard_reject_semantics_are_still_declared(self) -> None:
        """NONE'un yazılabilir olması onu 'kabul edilebilir' yapmaz."""
        enum_doc = _load(CALIBRATION_ENUM)
        assert "NONE" in enum_doc["x-normalization"]["hard_reject"], (
            "NONE hâlâ KR-018/082 hard reject listesinde olmalı — yazılabilir olması "
            "analiz edilebilir olduğu anlamına GELMEZ"
        )

    def test_missing_type_is_fail_closed_not_promoted(self) -> None:
        """Fail-open 'güvenlik-ağı' kuralı geri gelmesin (S1 regresyon kapısı)."""
        norm = _load(CALIBRATION_ENUM)["x-normalization"]

        promoting_keys = [
            key for key in norm
            if key.lower().startswith("missing") and isinstance(norm[key], str)
        ]
        assert not promoting_keys, (
            f"'missing' için DÜZ METİN bir normalizasyon kuralı var: {promoting_keys}. "
            "Eksik tip bir eşleme kuralıyla çözülemez; bağlam-bazlı FAIL-CLOSED politikası "
            "gerekir (nesne biçimi)."
        )

        missing = norm.get("missing")
        assert isinstance(missing, dict), "`missing` bağlam-bazlı bir politika nesnesi olmalı"
        assert missing.get("policy") == "FAIL-CLOSED", (
            "eksik kalibrasyon tipi için politika FAIL-CLOSED olmalı"
        )
        text = json.dumps(missing, ensure_ascii=False)
        assert "PANEL_ABSOLUTE" not in text or "YASAK" in text or "YÜKSELT" in text, (
            "eksik tipi PANEL_ABSOLUTE'a yükselten bir ifade geri gelmiş olabilir"
        )

    def test_platform_subset_and_schema_agree_after_none(self) -> None:
        subsets = _load(CALIBRATION_ENUM)["x-context-subsets"]
        assert "NONE" in subsets["platform/calibrated_dataset_manifest"], (
            "alt-küme kaydı ile şema enum'u ayrışmış — biri NONE taşıyor diğeri taşımıyor"
        )

    def test_edge_calibrated_subset_matches_the_c6b_decision(self) -> None:
        """C6b KARARI VERİLDİ (2026-08-01) — kısmi hizalama, iki dışlama gerekçeli.

        Bu test eskiden alt-kümeyi `{ABSOLUTE, RELATIVE}`'te donduruyordu ve mesajı
        *"bu C6b/E13 kararıdır, sessizce yapılamaz"* idi. Karar artık verildi; test onu
        **kodluyor**, dondurmuyor.

        **Eklendi — `PANEL_ABSOLUTE`:** `edge/intake_manifest` bu değeri zaten kabul
        ediyordu. Kalibre manifestte yazılamaması, bir paketin intake'te panel bildirip
        aynı istasyonun ikinci belgesinde AYNI değeri yazamaması demekti (S2). Additive,
        üretici yok (ölçüldü: edge/src'de yalnız yorumlarda geçiyor).

        **Dışarıda — `NONE`:** edge kalibrasyon başarısızsa manifest hiç üretmez
        (`calibrated_validator` CHECK 2). D8'in gerekçesi geçerli.

        **Dışarıda — `DLS2_RELATIVE`:** E13 kararı bu değeri kalibre paket yüzeyinden
        reddetti (DLS2 = MicaSense donanım adı; irradyans yöntemi ayrı eksen). İlk C6b
        denemesinde alt-küme intake ile TAM hizalandı ve `tests/test_calibration_type_axis.py`
        bunu kırmızıya çevirdi — iki kararın çelişmesini kapı engelledi. Kalan tutarsızlık
        bilinçlidir ve **S3**'e (MAJOR pencere) bağlıdır.

        🔴 **ÖD-3 (2026-08-01):** bu test eskiden YALNIZ kayıt defterini okuyordu. Kararı
        uygulayan yüzey ise `schemas/edge/calibrated_dataset_manifest.v1` içindeki inline
        enum'dur ve ölçüldü ki o gün ayrışmıştı (defter üç değer, şema iki). Artık **iki
        yüzey de** ölçülüyor; eşitliğin kendisini `tests/test_context_subset_binding.py`
        zorluyor.
        """
        decision = {"ABSOLUTE", "RELATIVE", "PANEL_ABSOLUTE"}
        surfaces = {
            "kayıt defteri": set(
                _load(CALIBRATION_ENUM)["x-context-subsets"]["edge/calibrated_dataset_manifest"]
            ),
            "şema inline enum": set(
                _load(EDGE_FORM)["properties"]["calibration_result"]["properties"][
                    "calibration_type"
                ]["enum"]
            ),
        }
        for name, values in surfaces.items():
            assert values == decision, (
                f"edge kalibre **{name}** C6b kararından sapmış ({sorted(values)}). "
                "`NONE` eklendiyse: edge zaten başarısız kalibrasyonda manifest üretmiyor. "
                "`DLS2_RELATIVE` eklendiyse: E13 kararına aykırı (bkz. "
                "test_calibration_type_axis.py). Eksikse: karar kâğıt üzerinde kalmış demektir."
            )


class TestRawFramesOwnership:
    """C3′ — ham kareler edge formunda ve object_key TAŞIMAZ."""

    def test_raw_frames_live_in_edge_form_only(self) -> None:
        assert "raw_frames" in _load(EDGE_FORM)["properties"]
        assert "raw_frames" not in _load(PLATFORM_FORM)["properties"]

    def test_raw_frames_carry_no_object_key(self) -> None:
        """KG-0.a-EK kural 1: anahtarı platform üretir; kiosk-emitted form anahtar bildiremez."""
        item = _load(EDGE_FORM)["properties"]["raw_frames"]["items"]
        assert "object_key" not in item["properties"], (
            "raw_frames[].object_key eklenmiş — edge anahtarı ÜRETEMEZ (KG-0.a-EK kural 1); "
            "C2′'de patches için verilen kararla çelişir"
        )

    def test_relative_path_blocks_traversal_and_absolute(self) -> None:
        """E5 (2026-07-31): desen GERÇEK çıktıyı kabul etmeli, traversal'ı hâlâ reddetmeli.

        Eski desen ölçümden ÖNCE dondurulmuştu ve M1'in fiilen ürettiği dosyaları
        reddediyordu: `odm_orthophoto.original.tif` (ODM'nin gerçek adı — iki nokta),
        `*.tif.aux.xml` (GDAL yan dosyası), boşluklu ve Türkçe klasör adları. Yani
        manifest, paketin içindeki dosyayı GÖSTEREMİYORDU.
        """
        import re

        pattern = _load(EDGE_FORM)["properties"]["raw_frames"]["items"]["properties"][
            "relative_path"
        ]["pattern"]
        rx = re.compile(pattern)

        # Kabul edilmesi ZORUNLU olanlar (hepsi gerçek dünyadan)
        for accepted in (
            "frames/DJI_0001_MS_G.tif",
            "a/b/c/x.tif",
            "odm_orthophoto.original.tif",
            "layers/ndvi.tif.aux.xml",
            "Tarla Verileri/ndvi.tif",
            "kırmızı/ndvi.tif",
        ):
            assert rx.match(accepted), f"gerçek çıktı reddedildi: {accepted}"

        # Güvenlik sınırları — gevşetme bunları KAYBETMEMELİ
        for rejected, why in (
            ("/frames/x.tif", "mutlak yol"),
            ("../frames/x.tif", "traversal"),
            ("a/../b/x.tif", "iç traversal"),
            ("a/./b.tif", "nokta segmenti"),
            ("a//b.tif", "boş segment"),
            ("C:/x.tif", "Windows sürücü / ADS"),
            ("a\\b.tif", "ters bölü"),
            ("noextension", "uzantısız"),
        ):
            assert not rx.match(rejected), f"{why} kabul edildi: {rejected}"

    def test_raw_frames_optional_and_bounded(self) -> None:
        doc = _load(EDGE_FORM)
        assert "raw_frames" not in doc["required"], "zorunlu yapmak MAJOR breaking olurdu"
        assert doc["properties"]["raw_frames"]["maxItems"] > 0, "DoS sınırı yok"

    def test_minimum_provenance_is_required(self) -> None:
        """Asgari köken (provenance) + SEÇİM GEREKÇESİ zorunludur.

        ⚠️ 2026-07-31/D7 ile genişletildi: `sees_patch_ids` eklendi. C3′ turunda küme
        `{frame_id, relative_path}` idi; Ç7 kararından sonra bir karenin listede
        bulunmasının TEK meşru gerekçesi "işaretli bir yamayı görüyor olması"dır
        (KG-0.c). Gerekçesiz kare = gereksiz veri = HC-02/KVKK yüzeyi.

        🔴 2026-08-01/S7: `band` BU KÜMEYE GİRMEDİ ve bu bilinçli. Alanı zorunlu kılmak
        `FIELD_MADE_REQUIRED` = MAJOR'dır; bu turun penceresi MINOR. Üstelik ölçüldü ki
        dedektör `x-compat-accepted` beyanını bu değişiklik tipinde **kontrol etmiyor**
        (`breaking_change_detector.py:615-630`), yani "üretici yok" gerekçesi beyanla
        geçirilemiyor. S7'nin MINOR yarısı yapıldı (`band` enum'una `RGB` eklendi → kompozit
        AÇIKÇA işaretlenebilir); zorunluluk **S7-b** olarak MAJOR penceresine, dedektör
        tutarsızlığı **AK-11** olarak plana yazıldı.
        """
        item = _load(EDGE_FORM)["properties"]["raw_frames"]["items"]
        assert set(item["required"]) == {"frame_id", "relative_path", "sees_patch_ids"}, (
            "`sees_patch_ids` düşerse gerekçesiz kare aktarımı serbest kalır (Ç7). "
            "`band` EKLENDİYSE: bu MAJOR bir daraltmadır (S7-b) — sürüm penceresi kararı "
            "olmadan yapılamaz."
        )

    def test_form_role_owns_raw_frames(self) -> None:
        assert "raw_frames" in _load(EDGE_FORM)["x-form-role"]["owns"]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
