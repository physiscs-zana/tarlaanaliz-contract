"""Bağımlılık kaynakları ÇELİŞEMEZ — AK-4'ün üçüncü kaynağı da kapıya bağlandı.

NEDEN (2026-08-11 denetimi, ÖLÇÜLDÜ):
    AK-4 kararı şunu der: *"kapıyı KOŞTURAN araç TAM SÜRÜME sabitlenir — geliştirme
    makinesiyle CI birebir aynı sürümde koşar."* Bu karar iki dosyada yazılıydı
    (`pyproject.toml` + `requirements-dev.txt`, ikisi de `pytest 9.0.2`) ama **üçüncü
    bir kaynak sessizce çelişiyordu**:

        poetry.lock  ->  pytest 7.4.4      (2026-03-22'den kalma)
        pyproject    ->  pytest 9.0.2
        requirements ->  pytest 9.0.2

    `poetry install` diyen biri kapıları **7.4.4** ile koştururdu — yani AK-4'ün
    tam olarak yasakladığı sapma. Bu, D4/Q2'de bir kez kapatılan sınıfın (workflow
    içi elle liste ↔ pyproject ayrışması) üçüncü kopyasıydı.

    `poetry lock` ile düzeltildi (lock artık 9.0.2). Bu kapı **geri gelmesini** yasaklar.

KAPSAM: yalnız **tam sürüme sabitlenmiş** araçlar (`==` / kesin sürüm). Aralıklı
bağımlılıklar (`jsonschema>=4.20,<5`) bilinçli olarak esnektir — onları karşılaştırmak
yanlış alarm üretirdi.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest


ROOT = Path(__file__).parent.parent

#: Kapıyı KOŞTURAN araçlar — AK-4 gereği tam sürüme sabit olmak zorunda.
PINNED_TOOLS = ("pytest", "pytest-cov")


def _requirements_pins() -> dict[str, str]:
    pins = {}
    for line in (ROOT / "requirements-dev.txt").read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        match = re.fullmatch(r"([A-Za-z0-9_.-]+)==([0-9][0-9A-Za-z.+-]*)", line)
        if match:
            pins[match.group(1).lower()] = match.group(2)
    return pins


def _pyproject_pins() -> dict[str, str]:
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    block = text.split("[tool.poetry.group.dev.dependencies]", 1)
    if len(block) < 2:
        return {}
    block = block[1].split("\n[", 1)[0]
    pins = {}
    for line in block.splitlines():
        line = line.split("#", 1)[0].strip()
        match = re.fullmatch(r'([A-Za-z0-9_.-]+)\s*=\s*"([0-9][0-9A-Za-z.+-]*)"', line)
        if match:  # yalnız TAM sürüm; "^3.5.0" gibi aralıklar atlanır
            pins[match.group(1).lower()] = match.group(2)
    return pins


def _lock_versions() -> dict[str, str]:
    lock = ROOT / "poetry.lock"
    if not lock.exists():
        return {}
    versions: dict[str, str] = {}
    name = None
    for line in lock.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith('name = "'):
            name = stripped.split('"')[1].lower()
        elif stripped.startswith('version = "') and name:
            versions.setdefault(name, stripped.split('"')[1])
            name = None
    return versions


class TestPinnedToolsAgreeAcrossSources:
    """Üç kaynak da aynı sürümü söylemeli."""

    @pytest.mark.parametrize("tool", PINNED_TOOLS)
    def test_requirements_and_pyproject_agree(self, tool: str) -> None:
        req, pyp = _requirements_pins().get(tool), _pyproject_pins().get(tool)
        assert req and pyp, f"{tool} iki kaynağın birinde TAM sürüme sabit değil: req={req} pyproject={pyp}"
        assert req == pyp, (
            f"{tool}: requirements-dev.txt={req} · pyproject.toml={pyp}. AK-4 gereği "
            "kapıyı koşturan araç TAM SÜRÜME sabittir ve iki dosya BİRLİKTE değişir; "
            "ayrışırlarsa yerel ile CI farklı sürümde koşar."
        )

    @pytest.mark.parametrize("tool", PINNED_TOOLS)
    def test_lockfile_does_not_contradict(self, tool: str) -> None:
        """`poetry.lock` ÜÇÜNCÜ kaynaktır — sessizce çelişebilir, ölçüldü."""
        lock = _lock_versions()
        if not lock:
            pytest.skip("poetry.lock yok")
        pinned = _requirements_pins().get(tool)
        assert pinned, f"{tool} requirements-dev.txt'te tam sürüme sabit değil"
        locked = lock.get(tool)
        assert locked is not None, (
            f"{tool} `poetry.lock`'ta yok — lock bayat olabilir (`poetry lock`)."
        )
        assert locked == pinned, (
            f"{tool}: poetry.lock={locked} · requirements-dev.txt={pinned}.\n"
            "2026-08-11 ölçümü: lock **7.4.4** derken diğer iki kaynak **9.0.2** diyordu; "
            "`poetry install` kapıları YANLIŞ sürümle koştururdu — AK-4'ün tam olarak "
            "yasakladığı sapma. Düzeltme: `poetry lock` (ya da lock'u tamamen kaldırma "
            "kararı — ama sessiz çelişki bırakmayın)."
        )


class TestGateActuallyReadsTheFiles:
    """POZİTİF KONTROL — üç ayrıştırıcı da gerçekten değer üretiyor mu?"""

    def test_all_three_parsers_return_something(self) -> None:
        req, pyp, lock = _requirements_pins(), _pyproject_pins(), _lock_versions()
        assert "pytest" in req, f"requirements ayrıştırıcısı boş döndü: {req}"
        assert "pytest" in pyp, f"pyproject ayrıştırıcısı boş döndü: {list(pyp)[:5]}"
        assert "pytest" in lock, f"lock ayrıştırıcısı boş döndü: {len(lock)} paket"

    def test_ranged_dependencies_are_ignored(self) -> None:
        """`jsonschema>=4.20,<5` gibi aralıklar TAM PİN sayılmamalı (yanlış alarm)."""
        assert "jsonschema" not in _requirements_pins(), (
            "Aralıklı bağımlılık tam pin sayılıyor — kapı yanlış alarm verir."
        )
        assert "pytest-xdist" not in _pyproject_pins(), (
            "`^3.5.0` gibi caret aralığı tam pin sayılıyor."
        )
