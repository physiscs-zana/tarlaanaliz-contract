"""Belgelerde YAYIMLANAN komutlar KOŞMALI — ÖD-16'nın sınıfı, tüm belgelere yayıldı.

NEDEN (2026-08-11 denetimi, ÖLÇÜLDÜ):
    ÖD-16 (2026-08-01) *"yayımlanan üreteç koşmalı"* kuralını koymuştu ama kapısı
    yalnız **CHANGELOG'daki dedektör komutlarını** kapsıyordu
    (`test_publication_tree_gates.TestPublishedGeneratorRuns`). Sınıfın geri kalanı
    ölçülmemişti. Ölçüldüğünde çıkanlar:

      * `docs/versioning_policy.md` **5 yerde** `python tools/sync_to_repos.sh …`
        yazıyordu — bir **bash** betiği `python` ile çağrılıyor, üstelik kullanılan
        bayraklar (`--version`, `--notify`, `--repos`) betikte **YOK**.
        Ölçüm: `./tools/sync_to_repos.sh --version v2.0.0` → `✗ Unknown option`, exit 1.
        Betiğin tanıdıkları: `--target · --verify-only · --auto-commit · --all`.
      * `README.md` `python tools/validate.py --check-forbidden` yazıyordu —
        `validate.py` argüman ayrıştırmaz, bayrak sessizce yok sayılırdı.
      * `README.md` `python -m tools.generate_types` yazıyordu — ne öyle bir modül
        ne `tools/__init__.py` var.

    Bir sözleşme deposunda koşmayan bir komut, **yanındaki iddiayı da doğrulanamaz**
    kılar. Bu kapı sınıfı kapatır.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).parent.parent

#: Taranan belge türleri (tüm izli dosyalar arasından).
DOC_SUFFIXES = {".md", ".txt"}

#: Örnek/şema verisi taranmaz — oralar komut değil veri taşır.
SKIP_PREFIXES = ("dist/", "schemas/", "enums/", "docs/examples/", "denetim/")

_TOOL_REF = re.compile(r"tools/([A-Za-z0-9_.-]+\.(?:py|sh|ts|js))")
_PY_ON_SH = re.compile(r"python3?\s+tools/[A-Za-z0-9_.-]+\.sh")


def _docs() -> list[Path]:
    out = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    ).stdout.splitlines()
    return [
        ROOT / rel
        for rel in out
        if Path(rel).suffix.lower() in DOC_SUFFIXES and not rel.startswith(SKIP_PREFIXES)
    ]


def _shell_flags(script: Path) -> set[str]:
    """Betiğin `case` dalında TANIDIĞI uzun bayraklar."""
    text = script.read_text(encoding="utf-8", errors="replace")
    return set(re.findall(r"^\s*(--[a-z][a-z-]*)\)", text, re.M))


class TestNoDocInvokesAShellScriptWithPython:
    """Yorumlayıcı doğru olmalı."""

    def test_no_python_on_sh(self) -> None:
        hits = []
        for doc in _docs():
            for index, line in enumerate(doc.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                if _PY_ON_SH.search(line):
                    hits.append(f"{doc.relative_to(ROOT).as_posix()}:{index}: {line.strip()[:90]}")
        assert not hits, (
            f"{len(hits)} yerde bash betiği `python` ile çağrılıyor:\n  " + "\n  ".join(hits)
        )

    def test_detector_would_catch_it(self) -> None:
        """POZİTİF KONTROL — desen gerçekten yakalıyor mu?"""
        assert _PY_ON_SH.search("python tools/sync_to_repos.sh --version v2.0.0")
        assert not _PY_ON_SH.search("./tools/sync_to_repos.sh --target platform")


class TestEveryReferencedToolExists:
    def test_no_dangling_tool_reference(self) -> None:
        missing: dict[str, list[str]] = {}
        for doc in _docs():
            for index, line in enumerate(doc.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                for name in _TOOL_REF.findall(line):
                    if not (ROOT / "tools" / name).exists():
                        missing.setdefault(f"tools/{name}", []).append(
                            f"{doc.relative_to(ROOT).as_posix()}:{index}"
                        )
        assert not missing, (
            "Belgeler var olmayan araçlara atıf yapıyor:\n  "
            + "\n  ".join(f"{name} ← {', '.join(yer[:4])}" for name, yer in missing.items())
        )

    def test_positive_control_a_real_tool_is_seen(self) -> None:
        assert (ROOT / "tools" / "validate.py").exists()
        assert _TOOL_REF.findall("python tools/validate.py") == ["validate.py"]


class TestPublishedFlagsAreSupported:
    """Betiğin TANIMADIĞI bayrak belgelenemez."""

    SCRIPT = "sync_to_repos.sh"

    def test_documented_flags_exist_in_the_script(self) -> None:
        script = ROOT / "tools" / self.SCRIPT
        if not script.exists():
            pytest.skip(f"{self.SCRIPT} yok")
        supported = _shell_flags(script)
        assert supported, f"{self.SCRIPT}: hiç bayrak ayrıştırılamadı — tarayıcı kör"
        bad: list[str] = []
        pattern = re.compile(rf"{re.escape(self.SCRIPT)}((?:\s+--?[A-Za-z0-9][\w-]*(?:[ =]\S+)?)*)")
        for doc in _docs():
            for index, line in enumerate(doc.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                match = pattern.search(line)
                if not match:
                    continue
                for flag in re.findall(r"--[a-z][a-z-]*", match.group(1)):
                    if flag not in supported:
                        bad.append(
                            f"{doc.relative_to(ROOT).as_posix()}:{index}: {flag} "
                            f"(betiğin tanıdıkları: {sorted(supported)})"
                        )
        assert not bad, (
            f"{len(bad)} yerde DESTEKLENMEYEN bayrak belgelenmiş:\n  " + "\n  ".join(bad)
            + "\nÖlçüm (2026-08-11): `--version` → `✗ Unknown option`, exit 1."
        )

    def test_flag_parser_reads_the_real_script(self) -> None:
        """POZİTİF KONTROL — bilinen bayraklar okunabiliyor mu?"""
        script = ROOT / "tools" / self.SCRIPT
        if not script.exists():
            pytest.skip(f"{self.SCRIPT} yok")
        assert {"--target", "--all"} <= _shell_flags(script), _shell_flags(script)


class TestValidatePyTakesNoArguments:
    """`validate.py --check-forbidden` gibi hayalî bayraklar geri gelmesin."""

    def test_no_doc_passes_a_flag_to_validate_py(self) -> None:
        kaynak = (ROOT / "tools" / "validate.py").read_text(encoding="utf-8")
        if "argparse" in kaynak or "sys.argv" in kaynak:
            pytest.skip("validate.py artık argüman alıyor — bu kilit güncellenmeli")
        bad = []
        pattern = re.compile(r"validate\.py\s+(--[a-z][a-z-]*)")
        for doc in _docs():
            for index, line in enumerate(doc.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                found = pattern.search(line)
                if found:
                    bad.append(f"{doc.relative_to(ROOT).as_posix()}:{index}: {found.group(1)}")
        assert not bad, (
            "`tools/validate.py` argüman AYRIŞTIRMAZ; belgelenen bayrak sessizce yok "
            "sayılır (kullanıcı 'kontrol koştu' sanır):\n  " + "\n  ".join(bad)
        )
