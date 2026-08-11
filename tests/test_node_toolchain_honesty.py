"""`package.json` DÜRÜSTLÜK kapısı — ölü script ve ZARARLI script giremez.

NEDEN (2026-08-11 denetimi, ÖLÇÜLDÜ):

  ① **Hiç var olmamış bir TypeScript zinciri belgeleniyordu.** `package.json` 30 script
     taşıyordu; 6'sı doğrudan var olmayan bir dosyaya işaret ediyordu
     (`tools/validate.ts`, `generate-types.ts`, `generate-schema-index.ts`,
     `breaking-change-detector.ts`, `pin-version.ts`, `sync-to-repos.sh`) ve o dosyalar
     depoda **HİÇ VAR OLMADI** (`git log --all -- <yol>` → 0 commit; package.json ilk
     commit'ten (2026-01-30) beri iskele). Geri kalanı ya bunlara zincirleniyordu
     (`ci:gate`, `build`, `prebuild`, `validate:*`) ya da çalışacağı dosya yoktu:
     jest `tests/**/*.ts` arıyordu, `tests/` 42 `.py` + **0 `.ts`**; eslint 0 `.ts/.js`;
     `prepare: husky install` ama `.husky/` yok. `CLAUDE.md` bunları
     *"Full CI Gate (what runs in CI)"* başlığıyla belgeliyordu — CI o komutu hiç
     çağırmıyordu.

  ② **`format` script'i ÖLÜ DEĞİL ZARARLIYDI.**
         "format": "prettier --write \"**/*.{ts,js,json,yaml,yml,md}\""
     ve `.prettierignore` YOKTU. Ölçüm:
         npx prettier@3 --check "schemas/**/*.json" "enums/**/*.json" "api/**/*.yaml"
         -> "Code style issues found in 94 files"   (kapsamdaki 97 dosyanın 94'ü)
     Koşsaydı üç değişmez aynı anda kırılırdı: agrega checksum (`pin_version`) ·
     vendored bayt-paritesi · `dist/` tazeliği.

BU KAPI NE ZORLAR:
  * her `scripts` girdisinin dosya hedefi GERÇEKTEN var
  * prettier çağıran hiçbir script sözleşme ağaçlarını yeniden biçimlendiremez
  * `.prettierignore` sözleşme ağaçlarını kapsar (elle koşuma karşı da korur)
  * beyan edilen her `devDependency`'nin bir TÜKETİCİSİ var
  * çalışacağı dosya olmayan araç yapılandırması (jest/eslint/lint-staged) geri gelemez
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).parent.parent
PACKAGE_JSON = ROOT / "package.json"
PRETTIER_IGNORE = ROOT / ".prettierignore"

#: `tools/pin_version.py` agrega checksum'ının kapsamı + yayın ağacı. Bir biçimlendirici
#: buralara dokunursa checksum, vendored parite ve dist tazeliği birlikte kırılır.
CONTRACT_TREES = ("schemas", "enums", "api", "dist")

#: Script komutunda geçen dosya hedefi (uzantılı yol).
_FILE_TARGET = re.compile(r"(?:^|[\s\"'])((?:tools|scripts)/[A-Za-z0-9_.-]+\.[A-Za-z0-9]+)")


def _package() -> dict:
    return json.loads(PACKAGE_JSON.read_text(encoding="utf-8"))


class TestEveryScriptTargetExists:
    """① — belgelenen komut KOŞMALI."""

    def test_no_script_points_at_a_missing_file(self) -> None:
        missing: list[str] = []
        for name, command in _package().get("scripts", {}).items():
            for target in _FILE_TARGET.findall(command):
                if not (ROOT / target).exists():
                    missing.append(f"{name} -> {target}")
        assert not missing, (
            f"{len(missing)} script var olmayan bir dosyaya işaret ediyor:\n  "
            + "\n  ".join(missing)
            + "\nBelgelenen ama koşmayan komut, yanındaki her iddiayı da doğrulanamaz "
            "kılar (ÖD-16). Ya dosyayı ekleyin ya script'i silin."
        )

    def test_script_chains_resolve(self) -> None:
        """`npm run X` zinciri tanımlı bir script'e gitmeli."""
        scripts = _package().get("scripts", {})
        dangling: list[str] = []
        for name, command in scripts.items():
            for referenced in re.findall(r"npm run ([a-zA-Z0-9:_-]+)", command):
                if referenced not in scripts:
                    dangling.append(f"{name} -> npm run {referenced}")
        assert not dangling, f"tanımsız script'e zincirlenen komut(lar): {dangling}"

    def test_gate_would_catch_a_planted_dead_script(self) -> None:
        """MUTASYON — dikilen ölü hedef yakalanmalı."""
        planted = {"scripts": {"olu": "node tools/hic-yok.ts"}}
        missing = [
            target
            for command in planted["scripts"].values()
            for target in _FILE_TARGET.findall(command)
            if not (ROOT / target).exists()
        ]
        assert missing == ["tools/hic-yok.ts"], f"tarayıcı ölü hedefi görmedi: {missing}"


class TestNoScriptCanReformatTheContract:
    """② — biçimlendirici sözleşme ağaçlarına DOKUNAMAZ."""

    def test_prettierignore_exists(self) -> None:
        assert PRETTIER_IGNORE.exists(), (
            ".prettierignore YOK. Bir geliştiricinin elle koştuğu `npx prettier --write .` "
            "sözleşme ağaçlarını yeniden biçimlendirir; ölçüldü (2026-08-11): koruma "
            "olmadan 162 sözleşme dosyası değişiyor, korumayla 0."
        )

    @pytest.mark.parametrize("tree", CONTRACT_TREES)
    def test_prettierignore_covers_contract_tree(self, tree: str) -> None:
        satirlar = {
            line.strip().rstrip("/")
            for line in PRETTIER_IGNORE.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("#")
        }
        assert tree in satirlar, (
            f"`.prettierignore` `{tree}/` ağacını KAPSAMIYOR. O ağaç `pin_version` "
            "checksum kapsamında ve/veya vendored parite/dist tazeliği ile bağlı; "
            "yeniden biçimlendirilmesi üç değişmezi birden kırar."
        )

    def test_no_script_runs_a_formatter_over_the_repo(self) -> None:
        """`prettier --write` gibi bir komut geri gelirse kapı kırmızı döner."""
        offenders = [
            f"{name}: {command}"
            for name, command in _package().get("scripts", {}).items()
            if re.search(r"\bprettier\b.*--write", command)
        ]
        assert not offenders, (
            f"Depo genelinde biçimlendirme yapan script geri gelmiş: {offenders}. "
            "Bu, 2026-08-11'de ölçülen ZARARLI komutun aynısıdır (checksum kapsamındaki "
            "97 dosyanın 94'ünü değiştiriyordu). Gerekiyorsa hedefi DAR tutun ve "
            "`.prettierignore` korumasını doğrulayın."
        )


class TestDeclaredToolingHasAConsumer:
    """③ — beyan edilen bağımlılığın tüketicisi olmalı; yoksa o bir tedarik yüzeyidir."""

    @staticmethod
    def _repo_mentions(name: str) -> int:
        result = subprocess.run(
            ["git", "-C", str(ROOT), "grep", "-c", "-F", "--", name,
             "--", "tools", "tests", ".github", "package.json"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        return sum(int(line.rsplit(":", 1)[1]) for line in result.stdout.splitlines() if ":" in line)

    def test_every_dev_dependency_is_used(self) -> None:
        package = _package()
        unused = [
            name
            for name in list(package.get("devDependencies", {})) + list(package.get("dependencies", {}))
            if self._repo_mentions(name) <= 1  # yalnız package.json'da geçiyorsa tüketicisi yok
        ]
        assert not unused, (
            f"Tüketicisi olmayan bağımlılık(lar): {unused}. 2026-08-11 ölçümü: ölü "
            "zincir 676 paket ve `npm audit` 38 açık (2 kritik + 21 yüksek) taşıyordu; "
            "hiçbirinin tüketicisi yoktu. Beyan edilen her paket bir tedarik zinciri "
            "yüzeyidir — kullanılmıyorsa kaldırın."
        )

    def test_positive_control_the_used_tool_is_seen(self) -> None:
        """POZİTİF KONTROL: kullanıldığı BİLİNEN araç sayılabiliyor mu?"""
        assert self._repo_mentions("@redocly/cli") > 1, (
            "Tarayıcı `@redocly/cli`'yi göremiyor — 'tüketicisi yok' çıktısı da "
            "güvenilmez demektir."
        )


class TestNoConfigForToolsThatCannotRun:
    """④ — çalışacağı dosyası olmayan araç yapılandırması geri gelemez."""

    def test_no_jest_config_without_ts_tests(self) -> None:
        package = _package()
        if "jest" not in package:
            return
        ts_tests = list((ROOT / "tests").rglob("*.ts"))
        assert ts_tests, (
            "`package.json` jest yapılandırması taşıyor ama `tests/` altında tek bir "
            "`.ts` yok — jest hiçbir test bulamaz. Süit Python'dur (`pytest`)."
        )

    def test_no_eslint_or_lintstaged_config_without_js(self) -> None:
        package = _package()
        for block in ("eslintConfig", "lint-staged"):
            if block not in package:
                continue
            sources = list(ROOT.rglob("*.ts")) + [
                p for p in ROOT.rglob("*.js") if "node_modules" not in p.parts
            ]
            assert sources, (
                f"`{block}` yapılandırması var ama depoda JS/TS kaynağı YOK. "
                "Koşamayacak bir aracın yapılandırması, çalıştığı sanılan bir kapıdır."
            )
