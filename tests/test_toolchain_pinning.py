"""Kapıyı koşturan araç sabittir — yerel makine ile CI aynı pytest'te koşar (AK-4).

NEDEN (2026-07-31):
    `requirements-dev.txt` `pytest<9` diyordu; geliştirme makinesinde **9.0.2**, CI'da
    **8.4.2** koşuyordu. İkisinde de yeşildi, ama kapılar İKİ FARKLI sürümde
    doğrulanıyordu — bir kapının yerelde geçip CI'da farklı davranması, kapıya olan
    güveni yok eder. Kural (dört depo tek standart): **sürüm sapması da bir sapmadır.**

Bu dosya iki şeyi zorlar:
    ① `requirements-dev.txt` (CI'ın kaynağı) ile `pyproject.toml` (geliştirici kaynağı)
       AYNI sürümü söylüyor,
    ② testi KOŞTURAN pytest gerçekten o sürüm.

②'nin değeri: ①-only bir test, iki dosyayı hizalı tutar ama yanlış sürümle koşulduğunu
fark etmez. Bu test kendi çalışma ortamını ölçer.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest


ROOT = Path(__file__).parent.parent
REQUIREMENTS = ROOT / "requirements-dev.txt"
PYPROJECT = ROOT / "pyproject.toml"

#: Tam sürüme sabitlenen araçlar (kapıyı KOŞTURANLAR). Şema doğrulayan kütüphaneler
#: (jsonschema, pyyaml) bilerek aralıkla tutulur — onlar yama almalı.
PINNED_TOOLS = ("pytest", "pytest-cov")


def _requirement_pin(package: str) -> str | None:
    pattern = re.compile(rf"^{re.escape(package)}==([0-9][^\s#]*)", re.M)
    match = pattern.search(REQUIREMENTS.read_text(encoding="utf-8"))
    return match.group(1) if match else None


def _pyproject_pin(package: str) -> str | None:
    pattern = re.compile(rf'^{re.escape(package)}\s*=\s*"([^"^~<>=]+)"\s*$', re.M)
    match = pattern.search(PYPROJECT.read_text(encoding="utf-8"))
    return match.group(1) if match else None


@pytest.mark.parametrize("package", PINNED_TOOLS)
def test_tool_is_pinned_exactly(package: str) -> None:
    pinned = _requirement_pin(package)
    assert pinned, (
        f"{package} requirements-dev.txt'te TAM SÜRÜME sabitlenmemiş (`{package}==X.Y.Z`). "
        "Aralık bırakmak CI'ı sessizce farklı bir sürüme düşürür — AK-4 tam olarak buydu."
    )


@pytest.mark.parametrize("package", PINNED_TOOLS)
def test_both_sources_agree(package: str) -> None:
    from_requirements = _requirement_pin(package)
    from_pyproject = _pyproject_pin(package)
    assert from_requirements == from_pyproject, (
        f"{package}: requirements-dev.txt={from_requirements!r} ↔ "
        f"pyproject.toml={from_pyproject!r} AYRIŞMIŞ. İki kaynak da geliştiriciye/CI'a "
        "farklı sürüm söylüyorsa sapma geri gelmiş demektir; ikisini BİRLİKTE değiştirin."
    )


def test_running_interpreter_uses_the_pinned_pytest() -> None:
    """Bu süiti fiilen koşturan pytest, sabitlenen sürüm olmalı."""
    expected = _requirement_pin("pytest")
    assert pytest.__version__ == expected, (
        f"bu koşum pytest {pytest.__version__} ile yapılıyor ama sabit sürüm {expected}. "
        "Ya ortamı güncelleyin (`pip install -r requirements-dev.txt`) ya sabiti bilinçli "
        "olarak yükseltin (iki dosyada birden)."
    )
