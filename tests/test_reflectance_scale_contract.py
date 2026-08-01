"""S5 — reflektans ölçeği sözleşmesi kapısı.

NEDEN (2026-08-01, S5 · E13 kararıyla engeli kalkan kalem):
    Reflektans ölçeği bugüne kadar **yalnız platform** şemalarında tanımlıydı
    (`platform/calibration_result.v1` → `scale`, `platform/calibrated_dataset_manifest.v1`).
    Worker'ın vendor'ladığı 8 sözleşmenin ve kanonik `schemas/worker/*` şemalarının
    **hiçbirinde yoktu** — ölçüldü. Sonuç: worker ölçeği TÜM FİLO için tek bir global
    ortam değişkeninden okuyor (`src/shared/config.py:236` → `reflectance_scale = 10000.0`)
    ve worker kodu bunu zaten biliyor:

        "The canonical fix is a per-job scale field in the calibration contract;
         until that schema change lands, a deployment matches its producer's
         encoding via this env var."            — config.py:230-234
        "Kalıcı çözüm: per-job reflectance_scale'i calibration_metadata
         sözleşmesine ekleyip okumak."          — pipeline.py:2358

NEDEN SESSİZ BİR HATA SINIFI:
    NDVI = (NIR−Red)/(NIR+Red) bir **orandır** → ölçekten bağımsızdır ve yanlış ölçekte
    bile makul görünür. EVI'nin `− 7.5·Blue + 1.0` ve SAVI'nin `+ L` **toplama sabitleri**
    ise reflektansın 0–1 aralığında olduğunu VARSAYAR. Ölçek uyuşmazsa bu iki indeks
    sessizce bozulur **ve NDVI'nin doğru görünmesi hatayı gizler.**

BU KAPI NE YAPAR:
    ① Ölçek sözlüğü **iki şemada da aynı** olmalı — platform ve worker ayrışamaz
      (kullanıcının kalıcı direktifi: dört depo tek standart, yeni ad icat edilmez).
    ② `scaled_int` bir **bölen olmadan** kabul edilemez (S5'in doğduğu boşluğun ta kendisi:
      "ölçekli tamsayı" deyip neye böleceğini söylememek).
    ③ Ölçeğe duyarlı indeksler kanonik olarak **işaretli** kalmalı — biri ölçek alanını
      kaldırmayı düşünürse, neyin bozulacağı yazılı olsun.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent

PLATFORM_CALIBRATION_RESULT = ROOT / "schemas/platform/calibration_result.v1.schema.json"
WORKER_CALIBRATION_METADATA = ROOT / "schemas/worker/calibration_metadata.v1.schema.json"
PLATFORM_MANIFEST = ROOT / "schemas/platform/calibrated_dataset_manifest.v1.schema.json"

#: Ölçekten BAĞIMSIZ (oran) — hatayı gizleyen indeks.
SCALE_INVARIANT = "NDVI"

#: Toplama sabiti taşıdığı için ölçeğe DUYARLI indeksler.
SCALE_SENSITIVE = ("EVI", "SAVI")


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _scale_block(document: dict) -> dict:
    scale = document.get("properties", {}).get("scale")
    assert isinstance(scale, dict), "`scale` bloğu yok"
    return scale


class TestScaleVocabularyIsShared:
    def test_worker_has_a_scale_block(self) -> None:
        """S5'in özü: worker'ın gördüğü sözleşme ölçeği TAŞIMALI."""
        document = _load(WORKER_CALIBRATION_METADATA)
        assert "scale" in document.get("properties", {}), (
            "`worker/calibration_metadata.v1` ölçek bloğunu kaybetmiş. Bu alan olmadan "
            "worker ölçeği tüm filo için TEK global env'den okumak zorunda kalır "
            "(config.py:236) — S5'in tam olarak düzelttiği durum."
        )

    def test_enum_matches_platform_exactly(self) -> None:
        """ÖLÇEK SÖZLÜĞÜ AYRIŞAMAZ — platform ve worker aynı değer kümesini kullanır."""
        platform = _scale_block(_load(PLATFORM_CALIBRATION_RESULT))
        worker = _scale_block(_load(WORKER_CALIBRATION_METADATA))
        p_enum = platform["properties"]["reflectance_scale"]["enum"]
        w_enum = worker["properties"]["reflectance_scale"]["enum"]
        assert list(p_enum) == list(w_enum), (
            f"reflektans ölçeği sözlüğü AYRIŞMIŞ:\n  platform={p_enum}\n  worker  ={w_enum}\n"
            "Aynı kavram iki tarafta aynı değer kümesiyle geçer (dört depo tek standart). "
            "Bir tarafa değer eklenip diğerine eklenmezse, tüketici kendi sözlüğünü uydurur — "
            "AK-7'de ürün sözlüğünde tam olarak bu yaşandı."
        )

    def test_manifest_uses_the_same_vocabulary(self) -> None:
        """Üçüncü taşıyıcı (platform manifesti) de aynı sözlüğü kullanmalı."""
        manifest = _load(PLATFORM_MANIFEST)
        field = manifest["properties"].get("reflectance_scale")
        assert field, "`platform/calibrated_dataset_manifest.v1.reflectance_scale` kaybolmuş"
        platform = _scale_block(_load(PLATFORM_CALIBRATION_RESULT))
        assert list(field["enum"]) == list(platform["properties"]["reflectance_scale"]["enum"]), (
            "manifest ölçek sözlüğü `calibration_result` ile ayrışmış — aynı depo içinde "
            "iki farklı sözlük, çapraz-repo ayrışmadan daha kolay gözden kaçar."
        )


class TestScaledIntNeedsADivisor:
    def test_scaled_int_requires_scale_factor(self) -> None:
        """`scaled_int` + bölen YOK = S5'in doğduğu boşluk. Şema bunu reddetmeli."""
        worker = _scale_block(_load(WORKER_CALIBRATION_METADATA))
        branches = worker.get("allOf") or []
        conditional = [
            b for b in branches
            if b.get("if", {}).get("properties", {}).get("reflectance_scale", {}).get("const")
            == "scaled_int"
        ]
        assert conditional, (
            "`scaled_int` için koşullu kısıt yok. 'Ölçekli tamsayı' deyip neye böleceğini "
            "söylememek, tüketiciyi tahmine zorlar — worker'ın bugün 10000 varsaymasının sebebi "
            "tam olarak budur."
        )
        assert "scale_factor" in conditional[0].get("then", {}).get("required", []), (
            "`scaled_int` koşulu `scale_factor`'ü ZORUNLU kılmıyor."
        )

    def test_scale_factor_must_be_positive(self) -> None:
        """Bölen sıfır ya da negatif olamaz — sessiz bölme hatası/işaret ters çevirme."""
        worker = _scale_block(_load(WORKER_CALIBRATION_METADATA))
        factor = worker["properties"]["scale_factor"]
        assert factor.get("exclusiveMinimum") == 0 or factor.get("minimum", -1) > 0, (
            "`scale_factor` pozitiflik kısıtı taşımıyor: 0 bölme hatası, negatif ise "
            "reflektansın işaretini ters çevirir."
        )

    def test_reflectance_scale_is_required_within_the_block(self) -> None:
        """Blok varsa ölçek adı ZORUNLU — boş bir `scale: {}` hiçbir şey bildirmez."""
        worker = _scale_block(_load(WORKER_CALIBRATION_METADATA))
        assert "reflectance_scale" in worker.get("required", []), (
            "`scale` bloğu yazılmışsa `reflectance_scale` zorunlu olmalı; aksi hâlde "
            "'ölçek bildirdim' diyen ama hiçbir şey söylemeyen bir nesne geçerli olur."
        )


class TestMissingScaleBehaviourIsDeclared:
    """Eksik ölçek davranışı YAZILI olmalı — sessiz varsayım yasak."""

    def test_normalization_block_declares_the_fallback(self) -> None:
        document = _load(WORKER_CALIBRATION_METADATA)
        norm = document.get("x-normalization", {})
        entry = norm.get("scale.missing")
        assert entry, (
            "`x-normalization.scale.missing` yok. Ölçek bildirilmediğinde ne olacağı "
            "yazılmazsa, her tüketici kendi varsayımını yapar — S5'in kök nedeni budur."
        )
        for key in ("policy", "description", "existing_detector"):
            assert str(entry.get(key, "")).strip(), f"beyanda eksik alan: {key}"

    def test_fallback_is_declared_as_temporary(self) -> None:
        """I-5: sapma yalnız GEÇİCİ olabilir; beyan bunu söylemeli."""
        entry = _load(WORKER_CALIBRATION_METADATA)["x-normalization"]["scale.missing"]
        text = json.dumps(entry, ensure_ascii=False)
        assert "GEÇİCİ" in text or "FAIL_CLOSED" in text, (
            "Fallback beyanı kalıcı bir muafiyet gibi okunuyor. I-5 gereği sapma geçicidir: "
            "üretici alanı yazmaya başladığında politika FAIL_CLOSED'a çevrilmelidir — bu "
            "niyet beyanda yazılı olmalı, yoksa 'geçici' sessizce kalıcılaşır."
        )


class TestScaleSensitivityIsDocumented:
    """Ölçeğin NEDEN önemli olduğu kanonik metinde kalmalı."""

    @pytest.mark.parametrize("index_name", SCALE_SENSITIVE)
    def test_sensitive_indices_are_named(self, index_name: str) -> None:
        text = WORKER_CALIBRATION_METADATA.read_text(encoding="utf-8")
        assert index_name in text, (
            f"{index_name} ölçek açıklamasından çıkarılmış. Bu iki indeks TOPLAMA sabiti "
            "taşıdığı için ölçeğe duyarlıdır; hangi indekslerin bozulacağı yazılı olmazsa "
            "bir sonraki tur alanı 'gereksiz' sanıp kaldırabilir."
        )

    def test_the_masking_index_is_named(self) -> None:
        """Hatayı GİZLEYEN indeks de yazılı olmalı — asıl tehlike odur."""
        text = WORKER_CALIBRATION_METADATA.read_text(encoding="utf-8")
        assert SCALE_INVARIANT in text, (
            "NDVI açıklamada anılmıyor. NDVI bir orandır → yanlış ölçekte bile doğru görünür "
            "ve EVI/SAVI'deki bozulmayı maskeler. Bu maskeleme etkisi yazılmazsa, 'NDVI "
            "düzgün, demek ki veri iyi' yanılgısı tekrar üretilir."
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
