# BOUND: TARLAANALIZ_SSOT_v1_2_0.txt – canonical rules are referenced, not duplicated.
"""`file_artifact` iki şemada KOPYA — sessizce çürümesin diye kapı [DK-28].

NEDEN KOPYA VAR
---------------
`outputs[]` girişleri hem `schemas/platform/calibrated_dataset_manifest.v1` hem
`schemas/edge/calibrated_dataset_manifest.v1` içinde aynı `file_artifact`
şeklini kullanır. Doğrusu tek tanıma `$ref` vermek olurdu; **ama bu depo
çapraz-dosya `$ref` KULLANMIYOR** — ölçüldü (2026-08-07):

    grep -rl '"$ref": "http' schemas/   -> hiç eşleşme yok
    schemas/edge/*.json içindeki tüm $ref'ler '#/$defs/...' biçiminde

Konvansiyonu tek bir alan için bozmak yerine tanım kopyalandı **ve bu kapı
yazıldı**. D16'nın dersi tam da buydu: *"ikinci bir gövde senkron kalmaz,
sessizce çürür"* — o yüzden kopya varsa kapısı da olmalı.

NE KİLİTLER
-----------
İki tanımın YAPISAL eşitliği: alan kümesi, tipler, enum değerleri, required,
unevaluatedProperties. `description` HARİÇ (edge kopyası bilerek ek açıklama
taşır — bu kapının kendisini işaret eder).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[1]
PLATFORM = ROOT / "schemas" / "platform" / "calibrated_dataset_manifest.v1.schema.json"
EDGE = ROOT / "schemas" / "edge" / "calibrated_dataset_manifest.v1.schema.json"


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _artifact(path: Path) -> dict[str, Any]:
    defs = _load(path).get("$defs", {})
    assert "file_artifact" in defs, f"{path.name}: $defs.file_artifact yok"
    return defs["file_artifact"]


def _strip_descriptions(node: Any) -> Any:
    """`description` alanlarını at — yapıyı karşılaştır, düzyazıyı değil."""
    if isinstance(node, dict):
        return {k: _strip_descriptions(v) for k, v in node.items() if k != "description"}
    if isinstance(node, list):
        return [_strip_descriptions(v) for v in node]
    return node


def test_file_artifact_yapisal_olarak_AYNI() -> None:
    """İki kopya ayrışırsa `outputs[]` iki şemada farklı şey kabul eder."""
    plat = _strip_descriptions(_artifact(PLATFORM))
    edge = _strip_descriptions(_artifact(EDGE))

    assert edge == plat, (
        "file_artifact kopyaları AYRIŞTI. Platform kanoniktir; edge kopyası ona "
        "hizalanmalı (ya da tersi bilinçliyse bu kapı ve gerekçesi güncellenmeli). "
        f"Yalnız-platform: {sorted(set(map(str, plat)) - set(map(str, edge)))} · "
        f"Yalnız-edge: {sorted(set(map(str, edge)) - set(map(str, plat)))}"
    )


def test_layer_type_ORTHO_iki_semada_da_var() -> None:
    """DK-28'in taban görüntüsü bu değere bağlı — ikisinden birinden düşerse
    zincir sessizce kopar."""
    for path in (PLATFORM, EDGE):
        enum = _artifact(path)["properties"]["layer_type"]["enum"]
        assert "ORTHO" in enum, f"{path.name}: layer_type enum'unda ORTHO yok"


@pytest.mark.parametrize("path", [PLATFORM, EDGE], ids=["platform", "edge"])
def test_outputs_alani_file_artifact_e_ref_veriyor(path: Path) -> None:
    """`outputs` doğrudan gömülü şema değil, `$defs`'e işaret etmeli —
    aksi hâlde ÜÇÜNCÜ bir kopya doğar."""
    outputs = _load(path)["properties"]["outputs"]
    assert outputs["items"] == {"$ref": "#/$defs/file_artifact"}, (
        f"{path.name}: outputs.items `$defs.file_artifact`'e ref vermiyor"
    )


def test_edge_outputs_OPSIYONEL_platformda_ZORUNLU() -> None:
    """POZİTİF KONTROL — iki şema BİLEREK farklı zorunluluk taşır.

    Platform formu kalibre PAKETİ tanımlar: çıktı listesi olmadan paket
    anlamsızdır → `required`. Edge formu kalibrasyon OLAYINI tanımlar ve mevcut
    paketler bu alanı taşımıyordu → opsiyonel (geriye uyumlu, MINOR).
    Bu test o farkı KİLİTLER; biri diğerine 'düzeltilirse' kırmızıya döner."""
    assert "outputs" in _load(PLATFORM)["required"], "platform: outputs zorunlu olmalı"
    assert "outputs" not in _load(EDGE).get("required", []), (
        "edge: outputs OPSİYONEL olmalı — zorunlu yapmak mevcut paketleri "
        "geriye dönük kırar (MAJOR)"
    )
