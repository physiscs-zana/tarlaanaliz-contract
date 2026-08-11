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
import re
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
    """ÖD-13 ① — kapsam iddiası kaynak koda bakarak değil ÖLÇÜLEREK doğrulanır.

    ⚠️ 2026-08-11: bu sınıf uzun süre **AYNAYI** ölçtü. `validation_targets()` docstring'i
    *"main() bu listeyi kullanır"* diyordu ama `main()` aynı dört ağacı kendi `rglob`
    döngüleriyle yeniden geziyordu. Mutasyonla kanıtlandı (taze klon, master):
    `main()`'den `dist` bloğu silinince doğrulanan dosya **165 → 97** düştü ve bu sınıf
    **17 passed** ile yeşil kaldı. `main()` artık gerçekten bu listeyi dolaşıyor ve
    `TestMainActuallyUsesTheTargetList` bunu ölçüyor.
    """

    @staticmethod
    def _target_paths() -> set:
        return {target.path.resolve() for target in validate.validation_targets(ROOT)}

    def test_dist_files_are_in_the_validation_targets(self) -> None:
        targets = self._target_paths()
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
        targets = self._target_paths()
        for probe in (
            ROOT / "schemas" / "worker" / "analysis_job.v1.schema.json",
            ROOT / "enums" / "calibration_type.enum.v1.json",
            ROOT / "api" / "platform_public.v1.yaml",
        ):
            assert probe.resolve() in targets, f"{probe.name} kapsam dışına düşmüş"

    def test_every_target_declares_a_known_validator(self) -> None:
        """Hedefin `kind`'ı `_VALIDATORS` tablosunda YOKSA `main()` KeyError ile düşer."""
        bilinmeyen = sorted(
            {t.kind for t in validate.validation_targets(ROOT)} - set(validate._VALIDATORS)
        )
        assert not bilinmeyen, f"doğrulayıcısı olmayan hedef türü: {bilinmeyen}"

    def test_each_tree_is_routed_to_the_right_validator(self) -> None:
        """Yönlendirme ölçülür: enum dosyası şema doğrulayıcısına gitmemeli."""
        beklenen = {
            "schemas/worker/analysis_job.v1.schema.json": "schema",
            "enums/calibration_type.enum.v1.json": "enum",
            "dist/schemas/worker/analysis_job.v1.schema.json": "schema",
            "api/platform_public.v1.yaml": "openapi",
        }
        gercek = {
            t.path.relative_to(ROOT).as_posix(): t.kind for t in validate.validation_targets(ROOT)
        }
        for rel, kind in beklenen.items():
            assert gercek.get(rel) == kind, (
                f"{rel} -> {gercek.get(rel)!r}, beklenen {kind!r}. Yanlış doğrulayıcıya "
                "giden dosya sessizce YANLIŞ kuralla denetlenir."
            )


class TestMainActuallyUsesTheTargetList:
    """ÖD-13 ①-b — **AYNA KARŞITI**: kapı, `main()`'in GERÇEKTEN yaptığını ölçmeli.

    Bu sınıf 2026-08-11'de eklendi çünkü yukarıdaki kapsam testleri `main()`'i değil
    onun kopyasını ölçüyordu. Buradaki iki test o sınıfın geri gelmesini engeller:
    `validation_targets()` daraltılırsa `main()` de daralmak ZORUNDA.
    """

    def test_main_validates_exactly_the_declared_targets(self, monkeypatch, capsys) -> None:
        """`main()` listenin TAMAMINI işlemeli — sayı DA kimlik DE ölçülür.

        ⚠️ İlk yazımda buraya **tek** hedef veriyordum ve öz-denetimde ölçtüm:
        `main()` listeyi `[:1]` diye dilimlese bile test **yeşil kalıyordu** (21 passed).
        Yani "listeyi okuyor mu"yu ölçüyordum, "hepsini işliyor mu"yu değil. Üç hedefle
        ve çıktıdaki DOSYA ADLARIYLA ölçmek o kör noktayı kapatır.
        """
        secilen = validate.validation_targets(ROOT)[:3]
        assert len(secilen) == 3, "ön koşul: en az 3 hedef olmalı"
        monkeypatch.setattr(validate, "validation_targets", lambda base_dir: list(secilen))
        with pytest.raises(SystemExit):
            validate.main()
        cikti = capsys.readouterr().out
        assert "Total files validated: 3" in cikti, (
            "`main()` kendi dosya yürüyüşünü yapıyor ya da listeyi DARALTIYOR — kapsam "
            "`validation_targets()`'tan gelmiyor. Bu tam olarak ÖD-13'ün ayna hatasıdır: "
            "kapı listeyi ölçer, araç başka bir şey tarar.\n" + cikti[-400:]
        )
        eksik = [t.path.name for t in secilen if t.path.name not in cikti]
        assert not eksik, (
            f"Listede olan ama İŞLENMEYEN hedef(ler): {eksik}. Sayı tutup kimlik "
            "tutmuyorsa `main()` başka dosyaları sayıyor demektir."
        )

    def test_main_reports_zero_when_there_are_no_targets(self, monkeypatch, capsys) -> None:
        """MUTASYON: hedef listesi boşsa `main()` de HİÇBİR ŞEY doğrulamamalı."""
        monkeypatch.setattr(validate, "validation_targets", lambda base_dir: [])
        with pytest.raises(SystemExit):
            validate.main()
        assert "Total files validated: 0" in capsys.readouterr().out

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


class TestOpenApiVersionTracksTheContractSet:
    """SD9 (2026-08-01, koordinatör onaylı) — `info.version` **set sürümünü** izler.

    ÖLÇÜLEN SORUN: üç spec de ilk commit'ten beri `1.0.0`'daydı; `api/` içeriği ise
    sürümler arasında değişiyor (v7.2.0→v7.3.0: D18-b) ve **checksum kapsamında**.
    Spec'ten istemci üreten bir tüketici hangi sözleşmeye baktığını `info.version`'dan
    anlayamıyordu.

    KARARIN DAYANAĞI (ölçüm, tahmin değil):
      * OpenAPI 3.1: *"The version of the OpenAPI Document (distinct from the OpenAPI
        Specification version or the version of the API being described)"* — alan
        **REQUIRED**, SemVer zorunlu değil. Bu depoda belge **set** olarak yayımlanır
        (I-1: üç depoda aynı sürüm dizesi) ⇒ setin sürümü belgenin sürümüdür.
      * *"API MAJOR hattını gösteriyor"* savunması düştü: hat zaten `servers.url`
        (`…/v1`) ve dosya adında (`*.v1.yaml`) yazılı.
      * Alanı okuyan tüketici **yok** (dört depoda 0 eşleşme) ⇒ geçiş kimseyi kırmaz.

    Elle yazılmaz: `tools/pin_version.py → sync_openapi_versions()` C8'de yazar.
    """

    @staticmethod
    def _contract_version() -> str:
        text = (ROOT / "CONTRACTS_VERSION.md").read_text(encoding="utf-8")
        match = re.search(r"^#{0,2}\s*\**Version:\**\s*v?(\d+\.\d+\.\d+)", text, re.M)
        assert match, "CONTRACTS_VERSION.md sürüm başlığı okunamadı"
        return match.group(1)

    @pytest.mark.parametrize(
        "spec_name",
        ["platform_public.v1.yaml", "platform_internal.v1.yaml", "edge_local.v1.yaml"],
    )
    def test_info_version_equals_contract_version(self, spec_name: str) -> None:
        yaml = pytest.importorskip("yaml", reason="pyyaml yok")
        doc = yaml.safe_load((ROOT / "api" / spec_name).read_text(encoding="utf-8"))
        assert str(doc["info"]["version"]) == self._contract_version(), (
            f"{spec_name}: `info.version` = {doc['info']['version']!r}, set sürümü ise "
            f"{self._contract_version()!r}. Bu alan ELLE yazılmaz — C8 töreninde "
            "`tools/pin_version.py` yazar (SD9). Elle tutulan sürüm sayısı bayatlıyor: "
            "bu oturumda iki kez ölçüldü (SD8 nüfusu · platform main.py log sabitleri)."
        )

    def test_api_line_is_still_expressed_where_it_belongs(self) -> None:
        """`info.version` set sürümünü aldıysa, API HATTI hâlâ görünür olmalı."""
        yaml = pytest.importorskip("yaml", reason="pyyaml yok")
        doc = yaml.safe_load((ROOT / "api" / "platform_public.v1.yaml").read_text(encoding="utf-8"))
        urls = [server["url"] for server in doc.get("servers", [])]
        assert any(url.rstrip("/").endswith("/v1") for url in urls), (
            f"API hattı `servers.url`'den kaybolmuş ({urls}). SD9 kararı 'hat zaten "
            "servers.url + dosya adında yazılı' ölçümüne dayanıyordu; o dayanak giderse "
            "karar yeniden açılmalıdır."
        )


class TestApiReferencesResolve:
    """SD10 — `api/` ağacındaki her `$ref` HEDEFE varmalı (araçtan bağımsız kapı).

    NEDEN PYTHON TARAFINDA DA VAR: sarkan referansı bulan şey redocly'ydi, ama o kapı
    npm + ağ ister ve bu depoda spectral'ın **çöktüğü** ölçüldü. Bir sözleşme deposunda
    *"referans hedefe varıyor mu"* sorusu araç kurulumuna bağlı olamaz — bu yüzden aynı
    değişmez pytest süitinde de zorlanıyor.

    Ölçülen kusur (2026-08-01): `api/platform_public.v1.yaml` ödeme uçlarında iki kez
    `./components/schemas.yaml#/components/schemas/PaymentIntent`'e `$ref` veriyordu;
    o bileşen **yoktu**. İstemci üreticisi bu uçlar için bozuk tip üretir.
    """

    @staticmethod
    def _resolve(doc: object, pointer: str):
        node = doc
        for token in [t for t in pointer.split("/") if t]:
            token = token.replace("~1", "/").replace("~0", "~")
            if isinstance(node, dict) and token in node:
                node = node[token]
            elif isinstance(node, list) and token.isdigit() and int(token) < len(node):
                node = node[int(token)]
            else:
                return None, False
        return node, True

    def test_every_api_ref_resolves(self) -> None:
        yaml = pytest.importorskip("yaml", reason="pyyaml yok")
        api_dir = ROOT / "api"
        cache: dict[Path, object] = {
            path: yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(api_dir.rglob("*.yaml"))
        }

        problems: list[str] = []

        def walk(node: object, source: Path, path: str) -> None:
            if isinstance(node, dict):
                ref = node.get("$ref")
                if isinstance(ref, str):
                    file_part, _, ptr = ref.partition("#")
                    target: object = cache[source]
                    if file_part:
                        target_path = (source.parent / file_part).resolve()
                        if target_path.suffix in {".yaml", ".yml"}:
                            target = cache.get(target_path)
                            if target is None and target_path.exists():
                                target = yaml.safe_load(target_path.read_text(encoding="utf-8"))
                        elif target_path.suffix == ".json":
                            target = (
                                json.loads(target_path.read_text(encoding="utf-8"))
                                if target_path.exists()
                                else None
                            )
                        if target is None:
                            problems.append(f"{source.name}{path} → {ref} (DOSYA YOK)")
                            return
                    value, ok = self._resolve(target, ptr) if ptr else (target, True)
                    if not ok or value is None:
                        problems.append(f"{source.name}{path} → {ref} (HEDEF YOK)")
                for key, value in node.items():
                    walk(value, source, f"{path}.{key}")
            elif isinstance(node, list):
                for index, value in enumerate(node):
                    walk(value, source, f"{path}[{index}]")

        for path, doc in cache.items():
            walk(doc, path, "")

        assert not problems, (
            "OpenAPI ağacında SARKAN referans(lar):\n  " + "\n  ".join(problems) + "\n"
            "Sarkan `$ref` sessiz bir kusurdur: doğrulama araçları çöker ya da atlar, "
            "istemci üreticisi bozuk tip üretir."
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
                "ref. Yayımlanan üreteç koşmuyorsa yanındaki sayı da doğrulanamaz.\n"
                "⚠️ CI'da bu hatayı görüyorsanız önce CHECKOUT'a bakın: sığ (shallow) "
                "checkout **etiket getirmez** ve kapı komutu bozuk sanır. "
                "`.github/workflows/contract_validation.yml` → `fetch-depth: 0` + "
                "`fetch-tags: true` (2026-08-01/ÖD-16'da tam bu yüzden eklendi)."
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])


class TestDeclaredLintExceptionsStayNarrow:
    """SD11 KARARI (2026-08-01) — `notes`/`metadata` kanonikte KALIR; `x-` göçü YAPILMAZ.

    KARARIN KANITI (dördü de ölçüldü):
      ① Bu dosyalar **önce JSON Schema belgesidir** (`$schema: draft 2020-12`) ve üç depoda
         doğrudan validator'lara veriliyor. JSON Schema bilinmeyen anahtarları **açıkça
         tolere eder** (annotation'dır). `x-` öneki ise **OpenAPI**'nin uzantı
         konvansiyonudur — kural, gömüldüğü yerde geçerlidir, kaynağında değil.
      ② Yeniden adlandırma **her okuyucuyu kırar**: `metadata.bandRequirements` KR-018 bant
         kapısının kaynağıdır ve worker `analysis_type.enum.v1`'i `metadata` ile
         **vendor'lar** → göç = 12 kanonik dosya + vendored kopyalar + dört depodaki
         okuyucular + KR-041/CONTRACTS_SHA256 pinleri. Tam bir çapraz-repo turu.
      ③ Kazanç **sıfır davranış**: bu anahtarlar hiçbir doğrulama kararını etkilemez;
         yalnız redocly'nin `struct` kuralı gömme yerinde şikâyet ediyor.
      ④ İstisna **dar, ölçülü ve kapılı**: 23 giriş, TEK sınıf; `struct` kuralı geri kalan
         her yapısal hatayı yakalamaya devam ediyor (bugün 3 gerçek kusur buldu).

    BU KAPI NE KORUR: istisna listesi bir **kaçış deliğine** dönüşmesin. Yalnız `struct`
    kuralı ve yalnız `notes`/`metadata` pointer'ları listelenebilir; başka bir kural ya da
    başka bir pointer eklenirse kırmızı döner (yani "susturarak geçirme" mümkün değil).
    """

    IGNORE_FILE = ROOT / ".redocly.lint-ignore.yaml"
    ALLOWED_POINTERS = {"#/notes", "#/metadata"}

    def _ignore(self) -> dict:
        yaml = pytest.importorskip("yaml", reason="pyyaml yok")
        return yaml.safe_load(self.IGNORE_FILE.read_text(encoding="utf-8")) or {}

    def test_only_struct_rule_is_ignored(self) -> None:
        offenders = {
            path: sorted(set(rules) - {"struct"})
            for path, rules in self._ignore().items()
            if isinstance(rules, dict) and set(rules) - {"struct"}
        }
        assert not offenders, (
            f"İstisna listesine `struct` DIŞINDA kural eklenmiş: {offenders}. "
            "SD11 kararı yalnız `notes`/`metadata` anahtar sınıfını kapsar; başka bir "
            "bulguyu susturmak kapıyı yeniden kör eder."
        )

    def test_only_notes_and_metadata_pointers_are_ignored(self) -> None:
        offenders = {
            path: sorted(set(pointers) - self.ALLOWED_POINTERS)
            for path, rules in self._ignore().items()
            if isinstance(rules, dict)
            for _rule, pointers in rules.items()
            if set(pointers) - self.ALLOWED_POINTERS
        }
        assert not offenders, (
            f"İstisna listesinde `notes`/`metadata` dışında pointer var: {offenders}. "
            "Kararın kapsamı budur; genişletmek ayrı bir karar gerektirir."
        )

    def test_exception_list_does_not_grow(self) -> None:
        total = sum(
            len(pointers)
            for rules in self._ignore().values()
            if isinstance(rules, dict)
            for pointers in rules.values()
        )
        assert total <= 23, (
            f"İstisna sayısı {total} > 23 (2026-08-01 ölçümü). Liste yalnız KÜÇÜLÜR: yeni bir "
            "`struct` ihlali buraya eklenerek geçirilemez — ya şema düzeltilir ya karar yeniden açılır."
        )
