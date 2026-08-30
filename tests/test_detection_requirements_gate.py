"""`detection_requirements` kapısı — YETENEK İDDİASI ile SENSÖR arasında tutarlılık.

NEDEN VAR (2026-08-30, ürün sahibi talebi + literatür taraması):
    `index_requirements` bir İNDEKSİN hangi bandı gerektirdiğini söyler. Ama
    *"bu drone ile fıstıkta Verticillium tespit edebilir miyiz?"* sorusunun
    makine-okunur bir cevabı **yoktu**. Cevapsız soru sessizce "evet" sanılır
    ve ürün sahibine dayanaksız bir yetenek vaadi olarak geri döner.

    Yeni `detection_requirements` bloğu bir **yetenek ilanı değil, KISIT
    ilanıdır**: bugünkü referans donanımla (BASIC_4BAND) hiçbiri tespit
    edilemez ve blok tam olarak bunu söyler.

BU DOSYA blok ÇÜRÜMESİN diye vardır. Bir YAML bloğu, onu okuyan bir kapı
yoksa yorumdur — ve yorum iddiadır, kanıt değil.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

MATRIX = Path(__file__).resolve().parents[1] / "drone_capability_matrix.yaml"

#: `evidence_strength` KAPALI kümesi. Yeni bir değer eklemek bilinçli olmalı:
#: "kanıt gücü" alanına serbest metin girmek, ayrımı yok etmenin en kolay yolu.
GECERLI_KANIT = {
    "peer_reviewed_same_crop",
    "peer_reviewed_other_crop",
    "none",
}


@pytest.fixture(scope="module")
def matris() -> dict:
    return yaml.safe_load(MATRIX.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def tespitler(matris) -> dict:
    d = matris.get("detection_requirements")
    assert d, "detection_requirements bloğu YOK — kapı ölçecek bir şey bulamadı"
    return d


def test_her_kaydin_kanit_gucu_KAPALI_kumeden(tespitler) -> None:
    for ad, kayit in tespitler.items():
        g = kayit.get("evidence_strength")
        assert g in GECERLI_KANIT, f"{ad}: gecersiz evidence_strength={g!r}"


def test_kanit_YOKSA_hicbir_bant_sinifi_yeterli_ILAN_EDILEMEZ(tespitler) -> None:
    """`evidence_strength: none` iken "şu sensörle tespit edilir" demek uydurmadır.

    Bu, blokta yapılabilecek en tehlikeli hatadır: kanıtsız bir kalemin
    yanına bir bant sınıfı yazmak, donanım alındığında kapının kendiliğinden
    açılmasına ve dayanaksız bir teşhisin çiftçiye gitmesine yol açar.
    """
    for ad, kayit in tespitler.items():
        if kayit.get("evidence_strength") == "none":
            assert not kayit.get("detectable_with_band_class"), (
                f"{ad}: kanit YOK ama detectable_with_band_class dolu — "
                "kanitsiz yetenek ilani"
            )


def test_her_kayit_NE_ILE_TESPIT_EDILEMEDIGINI_soyler(tespitler) -> None:
    # Bir kısıt ilanının işlevi budur: neyin YETMEDİĞİNİ adıyla yazmak.
    for ad, kayit in tespitler.items():
        assert kayit.get("NOT_detectable_with"), f"{ad}: NOT_detectable_with bos"


def test_BUGUNKU_referans_donanimla_HICBIRI_tespit_edilemez(matris, tespitler) -> None:
    """🔴 Ürün gerçeği: DJI Mavic 3M (BASIC_4BAND) ile hiçbiri tespit edilemez.

    Bu test bir DURUM tespitidir, bir dilek değil. Donanım yükseltilirse
    KIRILIR — ve kırılması gerekir: o an blok ile filo bilinçli olarak
    yeniden hizalanmalıdır.
    """
    referans = matris["capabilities"]["DJI_MAVIC_3M"]["band_class"]
    assert referans == "BASIC_4BAND"
    for ad, kayit in tespitler.items():
        assert referans in kayit["NOT_detectable_with"], (
            f"{ad}: referans donanim {referans} icin tespit iddiasi var — "
            "bugun bu YETENEK YOK"
        )


def test_yeterli_ILAN_EDILEN_bant_sinifi_MATRISTE_TANIMLI(matris, tespitler) -> None:
    """Var olmayan bir bant sınıfına atıf, kapıyı sessizce kör bırakır."""
    tanimli = set(matris["band_classes"])
    for ad, kayit in tespitler.items():
        for bs in kayit.get("detectable_with_band_class") or []:
            assert bs in tanimli, f"{ad}: band_classes'ta TANIMSIZ sinif {bs!r}"


def test_kanit_VARSA_referans_gosterilir(tespitler) -> None:
    for ad, kayit in tespitler.items():
        if kayit.get("evidence_strength") != "none":
            assert kayit.get("references"), f"{ad}: kanit iddiasi var, referans YOK"


def test_ayni_crop_kaniti_olan_kalem_TERMAL_ile_acilir(tespitler) -> None:
    """POZİTİF KONTROL — kapı her şeyi reddetmiyor, ayrım yapıyor.

    `WATER_STRESS_TRUE` fıstıkta DOĞRUDAN gösterilmiş tek kalemdir ve termal
    bant onu açar. Bu satır olmasaydı yukarıdaki testler, blok tamamen boş
    olsa bile geçerdi.
    """
    su = tespitler["WATER_STRESS_TRUE"]
    assert su["evidence_strength"] == "peer_reviewed_same_crop"
    assert "pistachio" in su["evidence_crop"]
    assert "THERMAL" in su["detectable_with_band_class"]


def test_psillid_icin_HICBIR_sensor_yeterli_ILAN_EDILMEZ(tespitler) -> None:
    """Fıstık psillidi bir yetenek boşluğu değil, kalıcı bir YASAKTIR.

    Spektral olarak görülebilen şey fumajin örtüsüdür: geç, dolaylı ve
    başka nedenlerle karışan bir belirti. Sensör yükseltilse bile bu zararlı
    icin spektral tespit iddia EDILMEZ.
    """
    p = tespitler["PISTACHIO_PSYLLID"]
    assert p["evidence_strength"] == "none"
    assert not p["detectable_with_band_class"]
    assert "HYPERSPECTRAL_VNIR" in p["NOT_detectable_with"]
    assert p.get("alternative_method"), "tuzak tabanli alternatif YAZILMAMIS"
