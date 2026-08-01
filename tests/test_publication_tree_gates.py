"""ÖD-13 + ÖD-16 kapıları — **yayın ağacı** ve **yayımlanan üreteç**.

ÖD-13 (2026-08-01): `dist/schemas/` hava-boşluklu M1'in tükettiği biçimdir (harici `$ref`
    yok) ve bugüne kadar **hiçbir içerik kapısından** geçmiyordu: `validate.py` yalnız
    `schemas/`+`enums/`+`api/` tarıyordu, CI'ın grep işi yalnız `schemas/`. Sonuç: kaynağa
    giremeyen bir PII alanı yayın ağacına elle eklenebilir, ya da kaynağı silinmiş bir şema
    **yetim** olarak orada yaşamaya devam edebilirdi. `--write` yetimi silmez (yalnız
    üzerine yazar), yani sapma kendiliğinden kapanmaz.

ÖD-16 (2026-08-01): CHANGELOG `tools/breaking_change_detector.py --old v7.2.0 --new .`
    komutunu **yayımlıyordu** ve aracın kendi kullanım satırı da tag biçimini gösteriyordu,
    ama kod yalnız DİZİN kabul ediyordu → yayımlanan komut
    `❌ Old directory not found: v7.2.0` ile düşüyordu. Bu, deponun *"sayıyı değil ÜRETECİ
    yayınla"* kuralının ihlaliydi: koşmayan bir üreteç, yanındaki sayıyı da doğrulanamaz
    kılar.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent


def _load(module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, ROOT / "tools" / f"{module_name}.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


validate = _load("validate")
inline_refs = _load("inline_refs")


class TestPublicationTreeIsValidated:
    """ÖD-13 ① — kapsam iddiası kaynak koda bakarak değil ÖLÇÜLEREK doğrulanır."""

    def test_dist_files_are_in_the_validation_targets(self) -> None:
        targets = {path.resolve() for path in validate.validation_targets(ROOT)}
        dist_files = list((ROOT / "dist" / "schemas").rglob("*.json"))
        assert dist_files, "yayın ağacı boş — `python tools/inline_refs.py --write` koşulmamış"
        missing = sorted(str(p.relative_to(ROOT)) for p in dist_files if p.resolve() not in targets)
        assert not missing, (
            f"Yayın ağacındaki {len(missing)} dosya doğrulama kapsamı DIŞINDA: {missing[:5]}. "
            "M1'in tükettiği biçim denetlenmiyorsa, kaynağa giremeyen bir alan oraya elle "
            "eklenebilir."
        )

    def test_source_and_api_trees_are_still_covered(self) -> None:
        """Kapsam genişletilirken daralmasın (regresyon)."""
        targets = {path.resolve() for path in validate.validation_targets(ROOT)}
        for probe in (
            ROOT / "schemas" / "worker" / "analysis_job.v1.schema.json",
            ROOT / "enums" / "calibration_type.enum.v1.json",
            ROOT / "api" / "platform_public.v1.yaml",
        ):
            assert probe.resolve() in targets, f"{probe.name} kapsam dışına düşmüş"

    def test_dist_inherits_the_pii_scope_of_its_source(self) -> None:
        """`user_pii` yayın ikizi meşrudur — kapı onu 'kapsam dışı' saymamalı.

        Aksi hâlde kapı gürültüye boğulur ve ilk refleks onu kapatmak olur.
        """
        source = ROOT / "schemas" / "core" / "user_pii.v1.schema.json"
        published = ROOT / "dist" / "schemas" / "core" / "user_pii.v1.schema.json"
        assert published.exists(), "user_pii yayın kopyası yok — dist bayat olabilir"
        assert validate._rel(published) == validate._rel(source), (
            "Yayın kopyası kaynağının kapsamını devralmıyor; `phone` gibi meşru bir alan "
            "yayın tarafında yanlış yere 'kapsam dışı' hatası üretir."
        )

    def test_published_pii_scan_finds_a_planted_violation(self, tmp_path: Path) -> None:
        """Kapı gerçekten ÖLÇÜYOR mu: dikilen bir ihlal yakalanmalı."""
        planted = tmp_path / "planted.v1.schema.json"
        planted.write_text(
            json.dumps({"type": "object", "properties": {"email": {"type": "string"}}}),
            encoding="utf-8",
        )
        errors = validate._check_forbidden_recursive(
            json.loads(planted.read_text(encoding="utf-8")), "$", planted
        )
        assert any("FORBIDDEN field 'email'" in error for error in errors)


class TestOrphanPublicationFilesAreCaught:
    """ÖD-13 ② — dist'te olup kaynağı olmayan dosya."""

    def test_no_orphans_today(self) -> None:
        produced, warnings = inline_refs.build()
        assert not warnings, f"yayın üretimi uyarı verdi: {warnings}"
        assert not inline_refs.find_orphans(produced, inline_refs.DIST)

    def test_orphan_detector_flags_a_planted_file(self, tmp_path: Path) -> None:
        dist = tmp_path / "schemas"
        (dist / "worker").mkdir(parents=True)
        (dist / "worker" / "ghost.v1.schema.json").write_text("{}", encoding="utf-8")
        (dist / "worker" / "real.v1.schema.json").write_text("{}", encoding="utf-8")
        orphans = inline_refs.find_orphans({"worker/real.v1.schema.json": "{}"}, dist)
        assert orphans == ["worker/ghost.v1.schema.json"], (
            "Kaynağı silinen bir şema yayın ağacında yaşamaya devam ederse hava-boşluklu "
            "M1 onu geçerli sözleşme sanar; `--write` onu silmez."
        )


class TestPublishedGeneratorRuns:
    """ÖD-16 — yayımlanan komut KOŞMALI."""

    def test_detector_accepts_a_git_ref(self) -> None:
        detector = _load("breaking_change_detector")
        cleanups: list = []
        try:
            materialized = detector._materialize("HEAD", cleanups)
            assert (materialized / "schemas").is_dir(), (
                "git ref bir çalışma ağacına çıkarılamadı — CHANGELOG'da yayımlanan "
                "`--old v7.2.0` biçimi yine düşerdi"
            )
        finally:
            for cleanup in cleanups:
                cleanup()

    def test_detector_rejects_an_unknown_ref(self) -> None:
        detector = _load("breaking_change_detector")
        with pytest.raises(SystemExit) as exc:
            detector._materialize("v0.0.0-yok", [])
        assert exc.value.code == 1

    def test_changelog_commands_use_a_resolvable_form(self) -> None:
        """CHANGELOG'da yayımlanan dedektör komutları bugün çözülebilir olmalı."""
        text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        refs = set()
        for line in text.splitlines():
            if "breaking_change_detector.py --old" in line:
                token = line.split("--old", 1)[1].strip().split()[0].strip("`'\"")
                refs.add(token)
        assert refs, "CHANGELOG hiç dedektör komutu yayımlamıyor (üreteç yayınlanmalı)"
        for ref in sorted(refs):
            if (ROOT / ref).exists():
                continue
            resolved = subprocess.run(
                ["git", "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}"],
                cwd=ROOT, capture_output=True, text=True,
            )
            assert resolved.returncode == 0, (
                f"CHANGELOG `--old {ref}` yayımlıyor ama bu ne dizin ne çözülebilir bir git "
                "ref. Yayımlanan üreteç koşmuyorsa yanındaki sayı da doğrulanamaz."
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
