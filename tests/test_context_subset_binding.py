"""ÖD-1/ÖD-3 kapısı — **enum kayıt defteri ile şemanın inline enum'u BAĞLI olsun.**

NEDEN BU DOSYA VAR (2026-08-01 öz-denetimi, ÖD-1):
    `enums/calibration_type.enum.v1.json` → `x-context-subsets` bir **kayıt defteridir**;
    belgeleri doğrulayan şey ise şemaların **inline** enum'udur. İkisi ayrışabiliyordu ve
    **hiçbir kapı ikisini bağlamıyordu.** Ölçüm (2026-08-01):

        defter  edge/calibrated_dataset_manifest = [ABSOLUTE, RELATIVE, PANEL_ABSOLUTE]
        şema    .../calibration_result/calibration_type.enum = [ABSOLUTE, RELATIVE]

    Yani **C6b/S2 kararı kâğıt üzerinde kaldı**: karar "eklendi" diye yazılmış, `PANEL_ABSOLUTE`
    taşıyan bir kalibre manifest o gün de reddediliyordu. Bu, D16'nın metin tarafında kapattığı
    *"aynı gerçeğin iki gövdesi"* deseninin **şema tarafındaki** hâlidir.

    ÖD-3 aynı kökün kapı tarafıydı: `test_calibration_type_axis.py` ve
    `test_calibrated_manifest_fields.py` kararı **yalnız defterden** okuyordu. Kararın değeri
    şemadan silinse o kapılar **yeşil kalırdı** — korudukları iddia edilen yüzeyi ölçmüyorlardı.

BU KAPI NE YAPAR:
    ① Defterdeki HER bağlam anahtarı gerçek bir şema yüzeyine çözülmeli (ölü kayıt yasak).
    ② O yüzeydeki inline enum, defterdeki alt-küme ile **küme olarak eşit** olmalı.
    ③ Ters yön: kalibrasyon sözlüğü kullanan ama defterde **kayıtlı olmayan** bir yüzey
       (yeni şema, yeni `$defs` kopyası) kırmızı verir — ÖD-2'nin doğduğu delik buydu.

    Yüzey keşfi **ad listesiyle değil ölçümle** yapılır: `schemas/` altındaki her `enum`,
    değerleri kanonik kalibrasyon sözlüğünün alt kümesiyse ve ayırt edici bir değer
    taşıyorsa (`ABSOLUTE`/`PANEL_ABSOLUTE`/`DLS2_RELATIVE`/`AGNOSTIC`) bir kalibrasyon
    yüzeyidir. Ölçüldü (2026-08-01): kural tam **8** yüzey buluyor, yanlış pozitif yok —
    bir alan adı listesi ise `calibration_assumed` gibi yeni adları kaçırırdı.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).parent.parent
ENUM_PATH = ROOT / "enums" / "calibration_type.enum.v1.json"

#: Bir enum'u "kalibrasyon yüzeyi" yapan ayırt edici değerler. `RELATIVE`/`NONE` tek
#: başına başka bir sözlükte de geçebilir; bunlar geçemez.
DISTINCTIVE = {"ABSOLUTE", "PANEL_ABSOLUTE", "DLS2_RELATIVE", "AGNOSTIC"}


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _enum_doc() -> dict[str, Any]:
    return _load(ENUM_PATH)


def _canonical_values() -> set[str]:
    return set(_enum_doc()["enum"])


def _subsets() -> dict[str, list[str]]:
    """Defterdeki bağlam → alt-küme eşlemesi (`description` anahtarı hariç)."""
    return {
        key: value
        for key, value in _enum_doc()["x-context-subsets"].items()
        if isinstance(value, list)
    }


def _discover_surfaces(doc: Any, canonical: set[str]) -> list[tuple[str, dict[str, Any]]]:
    """Bir şema belgesindeki tüm kalibrasyon enum yüzeylerini (JSON pointer, düğüm) döndür."""
    out: list[tuple[str, dict[str, Any]]] = []

    def rec(node: Any, ptr: str) -> None:
        if isinstance(node, dict):
            values = node.get("enum")
            if isinstance(values, list):
                non_null = {v for v in values if v is not None}
                if non_null and non_null <= canonical and non_null & DISTINCTIVE:
                    out.append((ptr, node))
            for key, value in node.items():
                rec(value, f"{ptr}/{key}")
        elif isinstance(node, list):
            for index, value in enumerate(node):
                rec(value, f"{ptr}/{index}")

    rec(doc, "")
    return out


def _schema_path(part: str) -> tuple[Path, str | None]:
    """`edge/intake_manifest` → dosya · `worker/expert_labeling_card.calibration_assumed` → dosya + alan."""
    field = None
    if "." in part.rsplit("/", 1)[-1]:
        part, field = part.rsplit(".", 1)
    return ROOT / "schemas" / f"{part}.v1.schema.json", field


def _context_surfaces(part: str) -> list[tuple[str, dict[str, Any]]]:
    path, field = _schema_path(part)
    if not path.exists():
        return []
    surfaces = _discover_surfaces(_load(path), _canonical_values())
    if field is not None:
        surfaces = [(ptr, node) for ptr, node in surfaces if ptr.endswith(f"/{field}")]
    return surfaces


def _context_parts() -> list[tuple[str, str]]:
    """(bağlam anahtarı, tek şema parçası) — virgülle birleştirilmiş anahtarlar açılır."""
    pairs: list[tuple[str, str]] = []
    for key in _subsets():
        for part in key.split(","):
            pairs.append((key, part.strip()))
    return pairs


PARTS = _context_parts()
PART_IDS = [part for _, part in PARTS]


class TestRegistryResolvesToRealSurfaces:
    """① Defterde yazan her bağlam gerçek bir şema yüzeyine çözülmeli."""

    @pytest.mark.parametrize(("context", "part"), PARTS, ids=PART_IDS)
    def test_context_key_points_at_an_existing_schema(self, context: str, part: str) -> None:
        path, _ = _schema_path(part)
        assert path.exists(), (
            f"`x-context-subsets['{context}']` → `{part}` diye bir şema YOK "
            f"({path.relative_to(ROOT)}). Defter var olmayan bir yüzeyi kısıtlıyor: "
            "ya anahtar bayat ya şema taşındı."
        )

    @pytest.mark.parametrize(("context", "part"), PARTS, ids=PART_IDS)
    def test_context_key_points_at_an_inline_enum(self, context: str, part: str) -> None:
        assert _context_surfaces(part), (
            f"`{part}` şemasında kalibrasyon enum'u bulunamadı, ama defter "
            f"`{context}` altında bir alt-küme kaydediyor. Alt-küme kaydı, doğrulamayı "
            "YAPAN inline enum olmadan hiçbir belgeyi kısıtlamaz (ÖD-1 dersi)."
        )


class TestInlineEnumEqualsRegistry:
    """② Asıl kapı: şema ile defter **küme olarak** eşit."""

    @pytest.mark.parametrize(("context", "part"), PARTS, ids=PART_IDS)
    def test_surface_matches_registered_subset(self, context: str, part: str) -> None:
        registered = set(_subsets()[context])
        for ptr, node in _context_surfaces(part):
            inline = {v for v in node["enum"] if v is not None}
            assert inline == registered, (
                f"{part}{ptr}: inline enum {sorted(inline)} ≠ defter "
                f"`x-context-subsets['{context}']` {sorted(registered)}.\n"
                "Karar hangi tarafta verildiyse DİĞERİ de değişmeli — defter tek başına "
                "hiçbir belgeyi kabul/ret etmez. (ÖD-1: C6b/S2 tam bu boşlukta kâğıt "
                "üzerinde kaldı: defter PANEL_ABSOLUTE diyordu, şema reddediyordu.)"
            )

    @pytest.mark.parametrize(("context", "part"), PARTS, ids=PART_IDS)
    def test_null_in_enum_implies_nullable_type(self, context: str, part: str) -> None:
        """`null` yalnız bir NULLABILITY işaretidir; tip beyanı ile tutarlı olmalı."""
        for ptr, node in _context_surfaces(part):
            if None not in node["enum"]:
                continue
            declared = node.get("type")
            types = declared if isinstance(declared, list) else [declared]
            assert "null" in types, (
                f"{part}{ptr}: enum'da `null` var ama `type` {declared!r} — ölü değer. "
                "Ya tipe `null` eklenmeli ya enum'dan çıkarılmalı."
            )


class TestNoUnregisteredCalibrationSurface:
    """③ Ters yön — defterde kaydı olmayan bir kalibrasyon yüzeyi kalmasın."""

    def test_every_calibration_enum_is_registered(self) -> None:
        canonical = _canonical_values()
        registered: set[tuple[str, str]] = set()
        for _, part in PARTS:
            path, _field = _schema_path(part)
            for ptr, _node in _context_surfaces(part):
                registered.add((str(path.relative_to(ROOT)).replace("\\", "/"), ptr))

        found: set[tuple[str, str]] = set()
        for path in sorted((ROOT / "schemas").rglob("*.schema.json")):
            for ptr, _node in _discover_surfaces(_load(path), canonical):
                found.add((str(path.relative_to(ROOT)).replace("\\", "/"), ptr))

        orphans = sorted(found - registered)
        assert not orphans, (
            "Kalibrasyon sözlüğünü kullanan ama `x-context-subsets`'te KAYITLI OLMAYAN "
            f"yüzey(ler): {orphans}.\n"
            "Kayıtsız yüzey, kararların görmediği ikinci bir gerçektir — ÖD-2 tam böyle "
            "doğdu (`analysis_job.v1 → $defs/CalibrationMetadata` kanonik "
            "`calibration_metadata.v1`'den sessizce ayrıştı). Yüzeyi deftere kaydedin ya "
            "da kanonik tanıma bağlayın."
        )


class TestGateCoversTheSurfacesItClaims:
    """Kapının kendi kapsamı ölçülür — 'yeşil ama boş' kapı olmasın."""

    def test_expected_context_count(self) -> None:
        assert len(_subsets()) >= 5, (
            f"Defterde yalnız {len(_subsets())} bağlam var; 2026-08-01'de 5 idi. "
            "Bir bağlam silindiyse o yüzey artık kısıtlanmıyor demektir."
        )

    def test_discovers_every_known_surface(self) -> None:
        """8 yüzey ölçülmüştü; kapı hepsini görüyor mu (parametreler boş dönmesin)?"""
        total = sum(len(_context_surfaces(part)) for _, part in PARTS)
        assert total >= 8, (
            f"Kapı yalnız {total} yüzey buluyor, 2026-08-01 ölçümü 8 idi. Keşif kuralı "
            "daralmışsa kapı sessizce boşalır (bu dosyanın kapatmaya çalıştığı hatanın "
            "kendisi)."
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
