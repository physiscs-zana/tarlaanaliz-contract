"""CI kapısının KENDİ dürüstlüğü — `paths:` filtresi ve `summary.needs` kapsamı.

NEDEN (2026-08-11 denetimi, ÖLÇÜLDÜ) — iki ayrı kusur, ikisi de daha önce bir kez
kapatılmış sınıfların GERİ DÖNÜŞÜ:

  ① `summary.needs` listesinde **`lint-openapi` yoktu.** Bu, SD5'te `verify-checksums`
     için kapatılan hatanın aynısı: iş kırmızı olsa bile özet kapısı onu görmüyordu,
     yani OpenAPI lint'i düşen bir PR *"Validation Summary: pass"* gösteriyordu.

  ② `paths:` filtresi **9 kök eksikti.** Q7'de "filtre testlerin GERÇEKTEN okuduğu
     yollardan türetildi" denmişti; ama `tools/check_doc_links.py` (AL-K20) `git ls-files`
     üzerinden TÜM izli `.md/.txt/.py/.yaml/.yml` dosyalarını tarıyor ve filtre onunla
     birlikte genişletilmemişti → `denetim/`, `README.md`, `CLAUDE.md`, `PATCH_NOTES.md`,
     `drone_registry.yaml`, `.redocly*`, `.github/workflows/auto_sync.yml` değişen bir
     PR'da **workflow HİÇ KOŞMUYORDU**. `dist/**` de yoktu: yayın ağacı tüketicilerin
     vendor'ladığı biçimdir ve yalnız `dist/` dokunan gerçek bir commit var (d6de514).

BU DOSYANIN İLKESİ: **liste ezberlenmez, TÜRETİLİR.** Gereken kök kümesi her koşumda
`git ls-files` + `check_doc_links.SCANNED_SUFFIXES` (TEK KAYNAK — ikinci kopya tutulmaz)
üzerinden yeniden hesaplanır ve filtreyle karşılaştırılır. Yeni bir kapı eklenip filtre
genişletilmezse test kırmızı döner.
"""

from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).parent.parent
WORKFLOW = ROOT / ".github" / "workflows" / "contract_validation.yml"

#: Şema kapılarının okuduğu ağaçlar. `check_doc_links` bunları taramaz (.json değil),
#: bu yüzden türetmeye AYRICA eklenir. Kaynak: tools/validate.py::validation_targets
#: (`schemas` + `enums` + `dist/schemas` + `api`).
SCHEMA_GATE_TREES = ("schemas", "enums", "api", "dist")


def _load_doc_links():
    spec = importlib.util.spec_from_file_location(
        "check_doc_links", ROOT / "tools" / "check_doc_links.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["check_doc_links"] = module
    spec.loader.exec_module(module)
    return module


def _workflow_text() -> str:
    return WORKFLOW.read_text(encoding="utf-8")


def _paths_block(trigger: str) -> list[str]:
    """`on.<trigger>.paths` listesi — YAML ayrıştırıcısına bağımlı olmadan."""
    text = _workflow_text()
    match = re.search(rf"^  {trigger}:\n(.*?)(?=^  \w|^\w)", text, re.S | re.M)
    assert match, f"`on.{trigger}` bloğu bulunamadı — workflow yapısı değişmiş olabilir"
    return re.findall(r"^\s+- '([^']+)'", match.group(1), re.M)


def _jobs() -> list[str]:
    return re.findall(r"^  ([a-z][a-z0-9-]*):\n    name:", _workflow_text(), re.M)


def _summary_needs() -> list[str]:
    match = re.search(r"^    needs: \[([^\]]+)\]", _workflow_text(), re.M)
    assert match, "`summary.needs` bulunamadı"
    return [name.strip() for name in match.group(1).split(",")]


def _fail_condition() -> str:
    match = re.search(
        r"- name: Fail if critical checks failed\n\s+if: \|\n(.*?)\n\s+run:",
        _workflow_text(), re.S,
    )
    assert match, "`Fail if critical checks failed` adımı bulunamadı"
    return match.group(1)


def _tracked() -> list[str]:
    out = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    assert out.returncode == 0, f"git ls-files başarısız: {out.stderr[:200]}"
    return [line for line in out.stdout.splitlines() if line]


#: Testlerin KÖK DÜZEYDE okuduğu dosyaları yakalayan desen — `ROOT / "package.json"`,
#: `ROOT / ".prettierignore"` gibi. 2026-08-11'de eklendi: türetme yalnız doc-link
#: sonek evrenini (.md/.txt/.py/.yaml/.yml) + şema ağaçlarını kapsıyordu, dolayısıyla
#: `package.json` / `package-lock.json` / `.prettierignore` **filtre dışındaydı** —
#: oysa `tests/test_node_toolchain_honesty.py` üçünü de okuyor. Yani yalnız
#: `package.json` değiştiren bir PR'da o kapı HİÇ KOŞMAZDI. Kapı kendi kör noktasını
#: ölçümle buldu; liste yerine TÜRETME eklendi.
_ROOT_FILE_READ = re.compile(r'ROOT\s*/\s*"([^"/]+\.[A-Za-z0-9]+|\.[A-Za-z][A-Za-z0-9.-]*)"')


def _files_read_by_tests() -> set[str]:
    """`tests/*.py` içinde `ROOT / "<kök dosya>"` diye okunan dosyalar."""
    found: set[str] = set()
    for path in (ROOT / "tests").rglob("*.py"):
        for name in _ROOT_FILE_READ.findall(path.read_text(encoding="utf-8", errors="replace")):
            if (ROOT / name).is_file():
                found.add(name)
    return found


def required_path_patterns() -> set[str]:
    """Kapıların okuduğu her kök için GitHub `paths:` deseni — TÜRETİLİR."""
    suffixes = {s.lower() for s in _load_doc_links().SCANNED_SUFFIXES}
    patterns: set[str] = {f"{tree}/**" for tree in SCHEMA_GATE_TREES}
    for path in _tracked():
        if Path(path).suffix.lower() not in suffixes:
            continue
        patterns.add(f"{path.split('/')[0]}/**" if "/" in path else path)
    # Sonek evrenine girmeyen ama bir KAPININ okuduğu kök dosyalar (package.json gibi)
    patterns |= _files_read_by_tests()
    return patterns


class TestSummaryGateCoversEveryJob:
    """① — özet kapısı hiçbir işi atlamamalı."""

    def test_every_job_is_in_summary_needs(self) -> None:
        jobs = [job for job in _jobs() if job != "summary"]
        needs = _summary_needs()
        eksik = [job for job in jobs if job not in needs]
        assert not eksik, (
            f"`summary.needs` {eksik} işini KAPSAMIYOR. Kapsanmayan bir iş kırmızı olsa "
            "bile 'Validation Summary' yeşil kalır — SD5'te `verify-checksums` için "
            "kapatılan hatanın aynısı."
        )

    def test_every_needed_job_is_in_the_fail_condition(self) -> None:
        """`needs`'te olmak yetmez — DÜŞÜRME koşulunda da adı geçmeli."""
        condition = _fail_condition()
        eksik = [job for job in _summary_needs() if f"needs.{job}.result" not in condition]
        assert not eksik, (
            f"{eksik} `needs` listesinde ama 'Fail if critical checks failed' koşulunda "
            "YOK. `needs`'e eklemek işi bekletir; koşula eklemek onu ZORUNLU kılar — "
            "ikisi ayrı şeydir ve yalnız ilkini yapmak kapıyı yine kör bırakır."
        )

    def test_fail_condition_only_references_needed_jobs(self) -> None:
        """SİMETRİK YÖN — koşul, `needs`'te OLMAYAN bir işe atıf yapmamalı.

        Bu test mutasyon sırasında doğdu: `lint-openapi` yalnız `needs`'ten çıkarılınca
        tek test kırmızı döndü, ama koşulda kalan `needs.lint-openapi.result` atfı
        GitHub'da bağımsız bir hatadır (bağımlı olmayan işin sonucu okunamaz) ve
        hiçbir test onu görmüyordu.
        """
        needs = set(_summary_needs())
        atiflar = set(re.findall(r"needs\.([a-z0-9-]+)\.result", _fail_condition()))
        hayalet = sorted(atiflar - needs)
        assert not hayalet, (
            f"Düşürme koşulu `needs`'te olmayan işe atıf yapıyor: {hayalet}. "
            "GitHub bağımlı olmayan bir işin sonucunu okuyamaz — koşul sessizce "
            "hiçbir zaman doğru olmaz."
        )

    def test_no_stale_job_in_needs(self) -> None:
        jobs = set(_jobs())
        hayalet = [job for job in _summary_needs() if job not in jobs]
        assert not hayalet, (
            f"`summary.needs` var olmayan iş(ler)e bağlı: {hayalet}. GitHub bu workflow'u "
            "hiç başlatmaz (geçersiz bağımlılık)."
        )


class TestPathFilterCoversWhatTheGatesRead:
    """② — filtre ezberlenmez, TÜRETİLİR."""

    @pytest.mark.parametrize("trigger", ["pull_request", "push"])
    def test_filter_covers_every_required_root(self, trigger: str) -> None:
        filtre = set(_paths_block(trigger))
        eksik = sorted(required_path_patterns() - filtre)
        assert not eksik, (
            f"`on.{trigger}.paths` {len(eksik)} kökü KAPSAMIYOR:\n  "
            + "\n  ".join(eksik)
            + "\n\nBu köklerdeki bir değişiklik workflow'u HİÇ TETİKLEMEZ — kapı sessizce "
            "atlanır ve PR yeşil görünür. Yeni bir kapı eklediyseniz filtreyi de "
            "genişletin (ya da kapının okumadığını kanıtlayın)."
        )

    def test_pull_request_and_push_filters_are_identical(self) -> None:
        pr, push = _paths_block("pull_request"), _paths_block("push")
        assert set(pr) == set(push), (
            "PR ve push filtreleri AYRIŞMIŞ.\n"
            f"  yalnız PR'da  : {sorted(set(pr) - set(push))}\n"
            f"  yalnız push'ta: {sorted(set(push) - set(pr))}\n"
            "Ayrışma, dalda koşan kapı ile master'da koşan kapının FARKLI şeyi "
            "denetlemesi demektir."
        )


class TestDerivationActuallyMeasures:
    """POZİTİF KONTROL — "eksik yok" çıktısı çoğu zaman türetmenin kusurudur."""

    def test_derivation_is_not_empty(self) -> None:
        patterns = required_path_patterns()
        assert len(patterns) >= 10, (
            f"Türetme yalnız {len(patterns)} desen üretti — `git ls-files` boş dönmüş ya "
            "da sonek kümesi okunamamış olabilir. Boş türetme, HER filtreyi 'yeterli' "
            "gösterir; kapı kör olur."
        )

    def test_derivation_finds_known_roots(self) -> None:
        patterns = required_path_patterns()
        for beklenen in ("schemas/**", "tools/**", "docs/**", "denetim/**", "dist/**",
                         "CHANGELOG.md"):
            assert beklenen in patterns, (
                f"Türetme bilinen kök `{beklenen}`'i üretemedi — mantık bozuk."
            )

    def test_suffix_set_comes_from_the_tool_not_a_copy(self) -> None:
        """Sonek kümesi TEK KAYNAKTAN gelmeli; ikinci kopya sessizce ayrışır."""
        suffixes = _load_doc_links().SCANNED_SUFFIXES
        assert {".md", ".txt", ".py", ".yaml", ".yml"} <= {s.lower() for s in suffixes}, (
            f"check_doc_links.SCANNED_SUFFIXES beklenenden dar: {suffixes}. Bu küme "
            "daralırsa türetme de daralır ve filtre eksikliği görünmez olur."
        )

    def test_a_planted_missing_root_is_detected(self) -> None:
        """MUTASYON: filtreden bir kök çıkarılırsa karşılaştırma onu YAKALAMALI."""
        filtre = set(_paths_block("pull_request"))
        assert "denetim/**" in filtre, "ön koşul: denetim/** filtrede olmalı"
        eksilmis = filtre - {"denetim/**"}
        assert "denetim/**" in (required_path_patterns() - eksilmis), (
            "Karşılaştırma mantığı çıkarılan kökü fark etmedi — kapı kör."
        )
