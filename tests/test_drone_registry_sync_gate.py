"""`drone_type` enum ↔ `drone_registry.yaml` ↔ `drone_capability_matrix.yaml` kapısı.

NEDEN (2026-08-11 denetimi, ÖLÇÜLDÜ):
    Kanonik enum'un **kendi üstverisi** var olmayan bir kapıyı adıyla çağırıyordu:

        enums/drone_type.enum.v1.json → x-registry-sync.ci_check
        = "tools/validate.py — drone_type enum değerleri drone_registry.yaml ile eşleşmeli"

    Ölçüm: `tools/validate.py` içinde `drone_registry` geçen **0 satır**; testlerde
    dosyayı okuyan **0** (2 isabetin ikisi de prose). `docs/checklists/SDLC_GATES.md`
    ayrıca **üç** yerde (§56 · §88 · §133) kapı olarak listeliyordu.

    Veri o gün **hizalıydı** (enum 5 · registry 5 · matrix 5, sıfır fark) — yani eksik
    olan **kural değil KAPIYDI**. Bir sözleşme deposunda "CI şunu kontrol eder" yazan
    kanonik bir dosya, kontrol etmeyen bir CI'a atıf yapıyordu.

BU DOSYA: kapının GERÇEKTEN koştuğunu, `main()`'e bağlı olduğunu ve dikilen sapmaları
yakaladığını ölçer.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).parent.parent


def _load():
    spec = importlib.util.spec_from_file_location("validate_drone", ROOT / "tools" / "validate.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["validate_drone"] = module
    spec.loader.exec_module(module)
    return module


validate = _load()


class TestRepositoryIsInSyncToday:
    def test_no_drift_between_the_three_sources(self) -> None:
        errors = validate.validate_drone_registry_sync(ROOT)
        assert not errors, "drone kaynakları ayrışmış:\n  " + "\n  ".join(errors)

    def test_all_three_sources_exist(self) -> None:
        for rel in ("enums/drone_type.enum.v1.json", "drone_registry.yaml",
                    "drone_capability_matrix.yaml"):
            assert (ROOT / rel).exists(), f"{rel} yok — kapı fail-closed döner"


class TestTheClaimInTheCanonicalFileIsNowTrue:
    """Kanonik dosya bir kapı VAAT EDİYORSA o kapı var olmalı."""

    def test_enum_metadata_names_a_gate_that_exists(self) -> None:
        enum = json.loads(
            (ROOT / "enums" / "drone_type.enum.v1.json").read_text(encoding="utf-8")
        )
        iddia = enum.get("x-registry-sync", {}).get("ci_check", "")
        assert "validate.py" in iddia, (
            f"`x-registry-sync.ci_check` artık `validate.py`'yi işaret etmiyor: {iddia!r}. "
            "İddia değiştiyse kapının yeri de bu testte güncellenmeli."
        )
        kaynak = (ROOT / "tools" / "validate.py").read_text(encoding="utf-8")
        assert "drone_registry" in kaynak, (
            "Kanonik enum `validate.py`'nin drone_registry'yi denetlediğini İDDİA ediyor "
            "ama araçta o dosyanın adı geçmiyor. 2026-08-11 öncesi durum tam buydu: "
            "belgelenmiş ama uygulanmayan kural bir dilektir."
        )

    def test_main_runs_the_cross_file_checks(self, monkeypatch, capsys) -> None:
        """AYNA KARŞITI: `main()` çapraz-dosya kontrollerini GERÇEKTEN koşmalı."""
        cagrildi: list = []

        def sahte(base_dir):
            cagrildi.append(base_dir)
            return ["DIKILMIS ÇAPRAZ-DOSYA HATASI"]

        monkeypatch.setattr(validate, "cross_file_checks", sahte)
        monkeypatch.setattr(validate, "validation_targets", lambda base_dir: [])
        with pytest.raises(SystemExit) as exc:
            validate.main()
        cikti = capsys.readouterr().out
        assert cagrildi, "`main()` `cross_file_checks`'i HİÇ çağırmadı — kapı bağlı değil."
        assert "DIKILMIS ÇAPRAZ-DOSYA HATASI" in cikti, cikti[-300:]
        assert exc.value.code == 1, "çapraz-dosya hatası çıkış kodunu 1 yapmalı"


class TestGateCatchesPlantedDrift:
    """MUTASYON — kapı gerçekten ÖLÇÜYOR mu?"""

    @staticmethod
    def _tree(tmp_path: Path, enum_values, registry_keys, matrix_keys) -> Path:
        (tmp_path / "enums").mkdir()
        (tmp_path / "enums" / "drone_type.enum.v1.json").write_text(
            json.dumps({"enum": list(enum_values)}), encoding="utf-8"
        )
        (tmp_path / "drone_registry.yaml").write_text(
            "drones:\n" + "".join(f"  {k}:\n    x: 1\n" for k in registry_keys), encoding="utf-8"
        )
        (tmp_path / "drone_capability_matrix.yaml").write_text(
            "capabilities:\n" + "".join(f"  {k}:\n    x: 1\n" for k in matrix_keys), encoding="utf-8"
        )
        return tmp_path

    def test_enum_value_missing_from_registry_is_caught(self, tmp_path: Path) -> None:
        root = self._tree(tmp_path, ["A", "B"], ["A"], ["A", "B"])
        errors = validate.validate_drone_registry_sync(root)
        assert any("drone_registry.yaml içinde YOK" in e and "'B'" in e for e in errors), errors

    def test_registry_entry_missing_from_enum_is_caught(self, tmp_path: Path) -> None:
        root = self._tree(tmp_path, ["A"], ["A", "C"], ["A"])
        errors = validate.validate_drone_registry_sync(root)
        assert any("drone_type enum'unda YOK" in e and "'C'" in e for e in errors), errors

    def test_capability_matrix_drift_is_caught(self, tmp_path: Path) -> None:
        root = self._tree(tmp_path, ["A", "B"], ["A", "B"], ["A"])
        errors = validate.validate_drone_registry_sync(root)
        assert any("capability_matrix" in e for e in errors), errors

    def test_missing_file_is_fail_closed(self, tmp_path: Path) -> None:
        """Dosya yoksa 'atla' DEĞİL HATA — sessiz atlama yeşil sayılmaz."""
        (tmp_path / "enums").mkdir()
        (tmp_path / "enums" / "drone_type.enum.v1.json").write_text(
            json.dumps({"enum": ["A"]}), encoding="utf-8"
        )
        errors = validate.validate_drone_registry_sync(tmp_path)
        assert len(errors) >= 2 and all("koşamaz" in e for e in errors), errors

    def test_aligned_tree_is_silent(self, tmp_path: Path) -> None:
        """POZİTİF KONTROL — hizalı ağaçta kapı SUSMALI (yanlış alarm yok)."""
        root = self._tree(tmp_path, ["A", "B"], ["A", "B"], ["A", "B"])
        assert validate.validate_drone_registry_sync(root) == []
