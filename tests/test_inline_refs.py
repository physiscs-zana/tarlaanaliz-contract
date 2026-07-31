"""E3 / §14.2.1 — satır içi yayın biçiminin kapısı (koordinatör onaylı karar).

NEDEN (2026-07-31 denetimi, bulgu E3):
    Kanonik şemalar `enums/` altına **göreli harici `$ref`** veriyor; vendored kopyalarda
    bu referanslar YOK (değerler satır içi). Hava-boşluklu M1 kanonik biçimi ÇÖZEMİYOR
    (`Unresolvable`). Ölçüm bu turda genişledi: E3 sorunu **3 referans** sanıyordu, gerçek
    **38 referans / 23 dosya / 13 enum**.

KARAR (onaylı): kaynak DRY kalır (`$ref` korunur), **yayın biçimi satır içidir**.
Bu dosya kararın dört şartını zorlar:
    ① üretim ARAÇLA (elle kopya yasak) ② `x-inlined-from` izi ③ satır içi ≡ kanonik enum
    ④ bayat `dist/` yakalanır (release checklist §3G'nin karşılığı)
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).parent.parent
DIST = ROOT / "dist" / "schemas"

_spec = importlib.util.spec_from_file_location("inline_refs", ROOT / "tools" / "inline_refs.py")
assert _spec and _spec.loader
_inline = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_inline)


def _walk(node: object, fn) -> None:
    if isinstance(node, dict):
        fn(node)
        for value in node.values():
            _walk(value, fn)
    elif isinstance(node, list):
        for value in node:
            _walk(value, fn)


class TestPublicationFormIsSelfContained:
    def test_dist_exists(self) -> None:
        assert DIST.exists(), (
            "dist/ yok — yayın biçimi hiç üretilmemiş. `python tools/inline_refs.py --write`"
        )

    def test_no_external_refs_remain(self) -> None:
        offenders: list[str] = []
        for path in sorted(DIST.rglob("*.json")):
            doc = json.loads(path.read_text(encoding="utf-8"))

            def check(node: dict, _p=path) -> None:
                ref = node.get("$ref")
                if isinstance(ref, str) and not ref.startswith("#"):
                    offenders.append(f"{_p.relative_to(ROOT).as_posix()} -> {ref}")

            _walk(doc, check)
        assert not offenders, (
            "yayın biçiminde HARİCİ $ref kalmış — hava-boşluklu M1 bunu çözemez:\n  "
            + "\n  ".join(offenders[:10])
        )

    def test_every_inlined_node_carries_its_trace(self) -> None:
        """`x-inlined-from` olmadan değerin nereden geldiği ölçülemez (şart ②)."""
        missing: list[str] = []
        for path in sorted(DIST.rglob("*.json")):
            doc = json.loads(path.read_text(encoding="utf-8"))

            def check(node: dict, _p=path) -> None:
                trace = node.get("x-inlined-from")
                if trace is None:
                    return
                for key in ("ref", "keys", "note"):
                    if not trace.get(key):
                        missing.append(f"{_p.relative_to(ROOT).as_posix()}: iz eksik ({key})")

            _walk(doc, check)
        assert not missing, missing[:5]


class TestInlinedValuesMatchCanonical:
    """Şart ③ — C-PARİTE deseni: kopya kanonikten AYRILAMAZ."""

    def test_every_inlined_enum_equals_its_source(self) -> None:
        mismatches: list[str] = []
        for path in sorted(DIST.rglob("*.json")):
            doc = json.loads(path.read_text(encoding="utf-8"))

            def check(node: dict, _p=path) -> None:
                trace = node.get("x-inlined-from")
                if not trace:
                    return
                source = (ROOT / "schemas" / _p.relative_to(DIST)).parent / trace["ref"]
                canonical = json.loads(source.resolve().read_text(encoding="utf-8"))
                for key in trace["keys"]:
                    if node.get(key) != canonical.get(key):
                        mismatches.append(
                            f"{_p.relative_to(ROOT).as_posix()}::{key} kanonikten AYRIŞMIŞ"
                        )

            _walk(doc, check)
        assert not mismatches, (
            "satır içi kopya kanonik enum'dan ayrışmış (bayat dist/ ya da elle düzenleme):\n  "
            + "\n  ".join(mismatches[:10])
        )

    def test_source_still_uses_refs(self) -> None:
        """Kaynak DRY kalmalı — satır içi biçim kaynağın YERİNE geçmez."""
        found = 0
        for path in sorted((ROOT / "schemas").rglob("*.json")):
            doc = json.loads(path.read_text(encoding="utf-8"))

            def check(node: dict) -> None:
                nonlocal found
                ref = node.get("$ref")
                if isinstance(ref, str) and not ref.startswith("#"):
                    found += 1

            _walk(doc, check)
        assert found >= 30, (
            f"kaynakta yalnız {found} harici $ref kaldı — biri satır içi biçimi KAYNAĞA "
            "yazmış olabilir; enum tek yerde tanımlı kalmalıdır (DRY)"
        )


class TestStaleDistIsCaught:
    """Şart ④ — enum değişip `dist/` üretilmezse kapı KIRMIZI olmalı."""

    def test_check_mode_reports_current_state(self) -> None:
        produced, warnings = _inline.build()
        assert not warnings, f"çözülemeyen referans: {warnings[:3]}"
        stale = [
            rel for rel, content in produced.items()
            if not (DIST / rel).exists() or (DIST / rel).read_text(encoding="utf-8") != content
        ]
        assert not stale, (
            f"dist/ bayat ({len(stale)} dosya). Enum değiştiyse yayın biçimi yeniden "
            "üretilmelidir: `python tools/inline_refs.py --write` (SDLC_GATES §3G)."
        )

    def test_generator_detects_a_changed_enum(self) -> None:
        """Mutasyon: üretilen içerik kanonik enum'a GERÇEKTEN bağlı mı?

        ⚠️ Ölçüm DÜĞÜM üzerinden yapılır, dosya metni üzerinden DEĞİL: `DJI_MAVIC_3M`
        aynı dosyada AÇIKLAMA metninde de geçiyor ("birincil/önerilen"), naif bir metin
        araması bu yüzden yanlış sonuç verir (ilk yazımda tam olarak buna düştüm).
        """
        sample = "edge/intake_manifest.v1.schema.json"

        def drone_enum(produced: dict) -> list:
            doc = json.loads(produced[sample])
            return doc["$defs"]["PlatformForm"]["properties"]["drone_model"]["enum"]

        before, _ = _inline.build()
        assert "DJI_MAVIC_3M" in drone_enum(before), "ön koşul: drone enum'u satır içi alınmış"

        enum_path = ROOT / "enums" / "drone_type.enum.v1.json"
        backup = enum_path.read_text(encoding="utf-8")
        try:
            doc = json.loads(backup)
            doc["enum"] = [v for v in doc["enum"] if v != "DJI_MAVIC_3M"]
            enum_path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n",
                                 encoding="utf-8")
            mutated, _ = _inline.build()
            assert "DJI_MAVIC_3M" not in drone_enum(mutated), (
                "enum'dan değer silindi ama üretilen düğüm DEĞİŞMEDİ — üretici kanonik "
                "kaynağa bağlı değil (satır içi kopya donmuş olabilir)"
            )
        finally:
            enum_path.write_text(backup, encoding="utf-8")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
