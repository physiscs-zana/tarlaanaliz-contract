"""C11 — `sorties[]` + `mission_date` AK-4 absorpsiyonunun kapısı (KADEME 2 / D10-E2).

NEDEN (2026-07-31 denetimi, bulgu E2):
    Bu iki alan edge'in **vendored sözleşmesinde CANLIYDI** ama kanonikte YOKTU. I-5
    değişmezi sapmanın yalnız GEÇİCİ olabileceğini söyler ("kalıcı divergence YASAK").

    Bu oturumda ölçüldü: edge'in `tests/fixtures/intake_manifest_valid.json` dosyası
    kanonik şemaya karşı **2 hata** veriyordu ve ikisinin de tek sebebi buydu —
    `sorties`/`mission_date` kanonikte tanımsız olduğu için `oneOf` hiçbir dala uymuyor,
    ardından `unevaluatedProperties: false` her alanı reddediyordu. Yani edge'in GERÇEK
    çıktısı kanonik sözleşmeye göre geçersizdi.

    D10/E2 kilidi: C11, **C8 release töreninden ÖNCE** girmeli — aksi hâlde sürüm,
    tüketicisinin fiilen ürettiği belgeyi reddeden bir sözleşmeyi dondurur.

✅ E16 KAPANDI (2026-08-01, edge PR #50) — bu blok eskiden *"BİLİNÇLİ SAPMA: edge
`crop_type`'ı KÜÇÜK harf yazıyor, eşlemeyi edge C8'de yapacak"* diyordu. Karar
(koordinatör): **edge sınırda normalize eder** — `_canonical_crop()` `strip().upper()`
uyguluyor, iki vendored enum kanonik 8 ürüne çekildi. Absorpsiyon zaten KANONİK biçimle
(BÜYÜK harf) yapılmıştı; artık edge'in gerçek çıktısı düzeltme olmadan kanoniği geçiyor
ve bunu `test_crop_case_gap_is_closed` ölçüyor (kapanış geri alınırsa kırmızı döner).

⚠️ KAPSAM UYARISI (2026-08-01 öz-denetimi, bulgu Ö1/Ö2): bu dosya **kardeş depoyu okur**
→ bu deponun CI'ında 2 test ATLANIR. Ölçüldü: CI run 30710485267 `1093 passed, 134
skipped`; 134'ün 2'si buradan. Yani buradaki kırmızı **contract CI'ında görünmez** —
ee4aed7 tam bu yüzden yeşil CI ile push edildi. Kapı kardeş depo CI'ında koşmalı
(E17/W10, `test_vendored_parity.py` ile **birlikte**) ve C8 töreninde YEREL koşum şart.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

try:
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource
except ImportError:  # pragma: no cover
    pytest.skip("jsonschema or referencing not installed", allow_module_level=True)


ROOT = Path(__file__).parent.parent
WORKSPACE = ROOT.parent
SCHEMA_PATH = ROOT / "schemas" / "edge" / "intake_manifest.v1.schema.json"
CROP_ENUM = ROOT / "enums" / "crop_type.enum.v1.json"
EDGE_FIXTURE = WORKSPACE / "tarlaanaliz-edge" / "tests" / "fixtures" / "intake_manifest_valid.json"


def _schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def _edge_form() -> dict:
    return _schema()["$defs"]["EdgeForm"]


def _sortie_item() -> dict:
    return _edge_form()["properties"]["sorties"]["items"]


def _validator() -> "Draft202012Validator":
    registry = Registry()
    for search_dir in (ROOT / "schemas", ROOT / "enums"):
        for json_file in search_dir.rglob("*.json"):
            try:
                contents = json.loads(json_file.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            if isinstance(contents, dict) and contents.get("$id"):
                registry = registry.with_resource(contents["$id"], Resource.from_contents(contents))
    return Draft202012Validator(_schema(), registry=registry)


class TestAbsorption:
    def test_both_fields_are_now_canonical(self) -> None:
        properties = _edge_form()["properties"]
        assert "sorties" in properties, "AK-4 sapması kanoniğe absorbe edilmemiş"
        assert "mission_date" in properties

    def test_they_live_in_the_edge_form_only(self) -> None:
        """Kaynak EDGE'dir — platform formu bunları üretmez (C0 rol ayrımı)."""
        platform = _schema()["$defs"]["PlatformForm"]["properties"]
        assert "sorties" not in platform
        assert "mission_date" not in platform

    def test_array_stays_optional(self) -> None:
        """Geriye uyumluluk: sortie yazmayan üreticiler kırılmamalı (MINOR)."""
        assert "sorties" not in _edge_form()["required"]
        assert "mission_date" not in _edge_form()["required"]

    def test_bbox_is_required_when_a_sortie_exists(self) -> None:
        """Eski C4 sorusunun cevabı: sortie varsa bbox ZORUNLU; sortie yoksa soru yok."""
        assert set(_sortie_item()["required"]) == {"sortie_id", "field_id", "crop_type", "bbox"}

    def test_bounds_match_the_vendored_contract(self) -> None:
        """Absorpsiyon, edge'in beklediği sınırları korumalı (aksi hâlde sessiz kırılma)."""
        assert _edge_form()["properties"]["sorties"]["maxItems"] == 100


class TestCropVocabularyStaysCanonical:
    def test_matches_canonical_enum_exactly(self) -> None:
        canonical = json.loads(CROP_ENUM.read_text(encoding="utf-8"))["enum"]
        used = _sortie_item()["properties"]["crop_type"]["enum"]
        assert used == canonical, (
            "sorties[].crop_type kanonik enum'dan ayrıştı. Bu alan satır içi tutuluyor "
            "(air-gap M1 harici $ref çözemez — E3), ama vocabulary TEK olmalı."
        )

    def test_vocabulary_source_is_declared(self) -> None:
        assert (
            _sortie_item()["properties"]["crop_type"]["x-vocabulary-source"]
            == "enums/crop_type.enum.v1.json"
        )

    def test_values_are_uppercase(self) -> None:
        """E16 kararının kilidi: küçük harf vocabulary kanoniğe SIZAMAZ."""
        used = _sortie_item()["properties"]["crop_type"]["enum"]
        assert all(v == v.upper() for v in used), (
            "küçük harf ürün adı kanoniğe girmiş — edge'in sapması absorbe edilmiş olabilir; "
            "kanonik biçim BÜYÜK harftir (10/10 şemada ölçüldü)"
        )


class TestBboxIsAnExtentNotAPoint:
    """HC-02/HC-08: kapsam dikdörtgeni serbest, atomik GPS yasak."""

    @pytest.mark.parametrize(
        ("bbox", "valid"),
        [
            ({"lat_min": 37.0, "lat_max": 37.1, "lon_min": 32.0, "lon_max": 32.1}, True),
            ({"lat_min": 91.0, "lat_max": 92.0, "lon_min": 32.0, "lon_max": 32.1}, False),
            ({"lat_min": 37.0, "lat_max": 37.1, "lon_min": -181.0, "lon_max": 32.1}, False),
            ({"lat_min": 37.0, "lat_max": 37.1, "lon_min": 32.0}, False),
        ],
        ids=["gecerli", "enlem-sinir-disi", "boylam-sinir-disi", "eksik-kenar"],
    )
    def test_bbox_bounds(self, bbox: dict, valid: bool) -> None:
        sortie = {
            "sortie_id": "S1",
            "field_id": "F1",
            "crop_type": "COTTON",
            "bbox": bbox,
        }
        errors = list(Draft202012Validator(_sortie_item()).iter_errors(sortie))
        assert (not errors) is valid

    def test_extra_keys_are_rejected(self) -> None:
        """`additionalProperties: false` — sortie'ye gizli GPS alanı eklenemez."""
        sortie = {
            "sortie_id": "S1",
            "field_id": "F1",
            "crop_type": "COTTON",
            "bbox": {"lat_min": 37.0, "lat_max": 37.1, "lon_min": 32.0, "lon_max": 32.1},
            "takeoff_gps": {"lat": 37.05, "lon": 32.05},
        }
        assert list(Draft202012Validator(_sortie_item()).iter_errors(sortie))


class TestEdgeRealOutputAgainstCanonical:
    """Absorpsiyonun ASIL ölçüsü: edge'in gerçek çıktısı artık geçiyor mu?

    Kardeş depo yoksa atlanır (CI'da normaldir; C8 töreninde YEREL koşulur —
    `docs/checklists/SDLC_GATES.md` §3C).
    """

    def _fixture(self) -> dict:
        if not EDGE_FIXTURE.exists():
            pytest.skip(f"kardeş depo yok: {EDGE_FIXTURE.name}")
        return json.loads(EDGE_FIXTURE.read_text(encoding="utf-8"))

    def test_structural_gap_is_closed(self) -> None:
        """Ürün adları kanonikleştirilince edge fixture'ı kanoniğe UYMALI.

        C11 öncesi bu belge 2 hata veriyordu (`sorties`/`mission_date` tanımsız →
        `unevaluatedProperties`). Bu test, yapısal boşluğun kapandığını ölçer.
        """
        document = self._fixture()
        for sortie in document.get("sorties", []):
            sortie["crop_type"] = str(sortie.get("crop_type", "")).upper()
        errors = sorted(_validator().iter_errors(document), key=lambda e: list(e.path))
        assert not errors, (
            "edge'in gerçek çıktısı kanoniğe hâlâ uymuyor: "
            + "; ".join(f"{list(e.path)}: {e.message[:120]}" for e in errors[:3])
        )

    def test_crop_case_gap_is_closed(self) -> None:
        """✅ E16 KAPANDI (2026-08-01) — bu testin İDDİASI TERSİNE ÇEVRİLDİ.

        Eski hâli *"kalan TEK fark ürün adı biçimidir"* diyordu ve edge fixture'ının
        **küçük harf** yazdığını doğruluyordu. Koordinatör kararı (2026-08-01):
        **edge sınırda normalize eder** — `_canonical_crop()` eklendi, iki vendored enum
        kanonik BÜYÜK harfe çekildi (edge PR #50). Dolayısıyla edge'in gerçek çıktısı
        artık kanoniği **olduğu gibi** geçer; biçim düzeltmesi (`.upper()`) gerekmez.

        Test, kapanışın **geri alınmadığını** ölçer: fixture küçük harfe dönerse ya da
        kanonik doğrulama hata verirse kırmızıya döner.
        """
        document = self._fixture()
        crops = [s.get("crop_type") for s in document.get("sorties", [])]
        if not crops:
            pytest.skip("kardeş depo yok: fixture sortie taşımıyor")
        assert all(c == c.upper() for c in crops), (
            f"edge fixture'ı hâlâ küçük harf ürün yazıyor: {crops}. E16 geri alınmış "
            "olabilir — edge `_canonical_crop` normalizasyonu ve vendored enum'lar kontrol edilmeli."
        )
        errors = sorted(_validator().iter_errors(document), key=lambda e: list(e.path))
        assert not errors, (
            "edge'in gerçek çıktısı DÜZELTME OLMADAN kanoniği geçmiyor: "
            + "; ".join(f"{list(e.path)}: {e.message[:120]}" for e in errors[:3])
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
