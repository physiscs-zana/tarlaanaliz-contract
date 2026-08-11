"""Betik ağacı kapısının kendi kapısı — AL-K32.

NEDEN BU DOSYA VAR:
    Bu deponun betik ağacı **tümden kapısızdı**: 3 dosya / 1021 satır, workflow'larda
    onları ayrıştıran **0 isabet**. Dört yeşil kapı o satırların hiçbirini görmüyordu.
    Uyarı edge oturumundan geldi (onların yeni kapısı, dokunulmamış bir dosyada gerçek
    bir sözdizimi hatası bulmuştu).

    Ölçüm burada **dürüst negatif** sonuç verdi — sözdizimi kusuru yok. Ama kök dizinde
    yetim ve **koşarsa zararlı** bir betik vardı: çalışma ağacının tamamını bir ZIP'le
    eziyor ve kullanıcıya kök `CLAUDE.md`'nin yasakladığı toplu ekleme komutunu
    yazdırıyordu. Dosya kaldırıldı; bu kapı sınıfın geri gelmesini engeller.

    Testlerin tamamı **sentetiktir** (yorumlayıcı çağıran ikisi hariç, onlar da
    `tmp_path` üzerinde çalışır) — depo ağacına bağlı değildir, `v7.7.1`/`v7.7.2`
    turlarında öğrenilen ders gereği: **veriye dayalı kapı, verisi olmayan ortamda
    kördür.**
"""

from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).parent.parent


def _load():
    spec = importlib.util.spec_from_file_location(
        "check_scripts", ROOT / "tools" / "check_scripts.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["check_scripts"] = module
    spec.loader.exec_module(module)
    return module


gate = _load()


class TestTheRepositoryIsCleanToday:
    def test_no_syntax_error_and_no_forbidden_command(self, capsys) -> None:
        code = gate.main()
        assert code == 0, capsys.readouterr().out

    def test_it_reports_how_many_files_it_scanned(self, capsys) -> None:
        """'0 bulgu' ile '0 dosya taradım' AYNI ŞEY DEĞİLDİR — sayı basılmalı."""
        gate.main()
        assert "taranan betik:" in capsys.readouterr().out


class TestForbiddenCommandsAreDetected:
    """Kaldırılan betiğin GERÇEK satırları — kapı onları yakalamalı."""

    def test_bulk_add_is_caught(self) -> None:
        # Kaldırılan betiğin 143. satırının yapısal kopyası.
        satir = "Write-Host '  git add -A' -ForegroundColor White"
        bulgular = gate.forbidden_hits(satir, "powershell")
        assert [b.rule for b in bulgular] == ["toplu-ekleme"], bulgular

    @pytest.mark.parametrize("bicim", ["git add -A", "git add --all", "git add ."])
    def test_every_bulk_form_is_caught(self, bicim: str) -> None:
        assert gate.forbidden_hits(f"  {bicim}", "bash"), bicim

    def test_whole_tree_overwrite_is_caught(self) -> None:
        # Kaldırılan betiğin 93. satırı: ZIP'i deponun köküne açıyordu.
        satir = "Copy-UpdateFiles $gecici (Get-Location).Path"
        bulgular = gate.forbidden_hits(satir, "powershell")
        assert [b.rule for b in bulgular] == ["calisma-agacini-ezme"], bulgular

    @pytest.mark.parametrize(
        "satir",
        ["rm -rf .", 'rm -rf "$PWD"', "Remove-Item -Recurse -Force (Get-Location)"],
    )
    def test_root_deletion_is_caught(self, satir: str) -> None:
        aile = "powershell" if "Remove-Item" in satir else "bash"
        assert any(b.rule == "kok-dizini-silme" for b in gate.forbidden_hits(satir, aile)), satir


class TestLegitimateCodeIsNotFlagged:
    """POZİTİF KONTROL — kapı meşru kodu kırmızıya çevirirse ilk fırsatta kapatılır.

    Buradaki satırların hepsi depodaki GERÇEK kodun kopyasıdır (2026-08-11 ölçümü):
    `sync_to_repos.sh`'teki 4 `git add` kullanımının hepsi yol-sınırlı; `generate_types.sh`
    yalnız kendi üretim dizinini siliyor (tırnaklı, varlık kontrolüyle).
    """

    @pytest.mark.parametrize(
        "satir",
        [
            "    git add contracts/",
            "    git add src/types/contracts/ 2>/dev/null || true",
            '        rm -rf "$GENERATED_DIR"',
            "    cp -r schemas/ dist/schemas/",
            "    git add -- tools/validate.py",
        ],
    )
    def test_real_repository_lines_stay_green(self, satir: str) -> None:
        assert gate.forbidden_hits(satir, "bash") == [], satir

    def test_comment_lines_are_not_scanned(self) -> None:
        """Bir kuralı betiğin İÇİNDE gerekçelendirmek mümkün olmalı.

        Bu oturumda DÖRT kez, bir kusuru yasaklayan kapı, kusuru anlatan metne takıldı
        (`check_doc_links` üç kez, CHANGELOG bir kez). Aynı hatayı burada tekrarlamamak
        bilinçli bir tasarım kararıdır.
        """
        assert gate.forbidden_hits("# git add -A KULLANMAYIN — yol-sınırlı ekleyin", "bash") == []
        assert gate.forbidden_hits("  # rm -rf . asla", "bash") == []

    def test_but_a_real_command_on_the_same_line_still_fires(self) -> None:
        """Yorum muafiyeti bir kaçış deliği olmasın: satır yorumla BAŞLAMIYORSA taranır."""
        assert gate.forbidden_hits("git add -A  # tek seferlik", "bash")


class TestSyntaxLayer:
    @staticmethod
    def _yaz(tmp_path: Path, ad: str, govde: str) -> Path:
        p = tmp_path / ad
        p.write_text(govde, encoding="utf-8")
        return p

    @pytest.mark.skipif(not shutil.which("bash"), reason="bash yok")
    def test_broken_bash_is_caught(self, tmp_path: Path) -> None:
        p = self._yaz(tmp_path, "bozuk.sh", 'f() {\n  if [ -z "$x" ; then\n')
        assert gate.syntax_errors(p, "bash", tmp_path), "bozuk betik temiz sayıldı"

    @pytest.mark.skipif(not shutil.which("bash"), reason="bash yok")
    def test_valid_bash_is_clean(self, tmp_path: Path) -> None:
        """POZİTİF KONTROL — geçerli betik yanlış alarm üretmemeli."""
        p = self._yaz(tmp_path, "iyi.sh", '#!/usr/bin/env bash\nset -e\necho "merhaba"\n')
        assert gate.syntax_errors(p, "bash", tmp_path) == []

    @pytest.mark.skipif(not shutil.which("bash"), reason="bash yok")
    def test_crlf_working_copy_is_not_a_false_red(self, tmp_path: Path) -> None:
        """🔴 Kapının KENDİ yanlış-kırmızısı — bu test onun nöbetçisi.

        İlk hâl dosyayı çalışma ağacından ayrıştırıyordu; bu makinede
        (`core.autocrlf=true`) `bash -n` HER betikte CRLF hatası verdi ve neredeyse
        *"betikler bozuk"* diye rapor edecektim. Ölçüm çürüttü: `git ls-files --eol`
        indeks tarafını **lf** gösterdi — kusur betiklerde değil, kapının ölçüm
        ortamındaydı.

        İkinci tuzak: CR'yi temizleyip stdin'e METİN olarak yazınca Python onu Windows'ta
        geri `\\r\\n` yapıyordu. Artık stdin'e **bayt** veriliyor.

        📌 Mutasyonla ölçüldü ve sonuç gizlenmiyor: bu testi **öldüren** şey bayt kipini
        metin kipine çevirmektir (4 kırmızı). Araçtaki açık CR temizliğini kaldırmak
        **hiçbir testi öldürmez**, çünkü `read_text()` zaten evrensel satır sonu çevirimi
        yapıyor — o çağrı savunma derinliğidir, tek koruma değil.
        """
        p = self._yaz(tmp_path, "crlf.sh", '#!/usr/bin/env bash\r\nf() {\r\n  echo hi\r\n}\r\n')
        assert gate.syntax_errors(p, "bash", tmp_path) == [], (
            "CRLF'li çalışma kopyası yanlış kırmızı üretiyor — kapı CI (Linux) ile aynı "
            "şeyi ölçmüyor demektir."
        )


class TestCommittedLineEndings:
    def test_repository_scripts_are_lf_in_the_index(self) -> None:
        assert gate.committed_crlf(ROOT) == []

    def test_gate_reads_the_index_not_the_worktree(self, tmp_path: Path) -> None:
        """POZİTİF KONTROL — İNDEKSTE CRLF olan betik yakalanmalı.

        Çalışma ağacındaki CRLF masumdur (Windows checkout'u), indekstekiyse gerçek
        kusurdur: Linux'ta betik ayrıştırılamaz. Kapı ikisini AYIRMALI.
        """
        subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
        for komut in (["config", "user.email", "t@t"], ["config", "user.name", "t"],
                      ["config", "core.autocrlf", "false"]):
            subprocess.run(["git", "-C", str(tmp_path), *komut], check=True)
        (tmp_path / "k.sh").write_bytes(b"#!/usr/bin/env bash\r\necho hi\r\n")
        subprocess.run(["git", "-C", str(tmp_path), "add", "k.sh"], check=True)
        subprocess.run(["git", "-C", str(tmp_path), "commit", "-qm", "crlf"], check=True)
        bozuk = gate.committed_crlf(tmp_path)
        assert bozuk and "k.sh" in bozuk[0], bozuk


class TestDiscoveryFailsClosed:
    def test_no_scripts_means_error_not_success(self, tmp_path: Path, monkeypatch, capsys) -> None:
        """'Hiç betik bulamadım' ASLA yeşil sayılmaz — keşif bozulmuş olabilir."""
        monkeypatch.setattr(gate, "tracked_scripts", lambda root: [])
        assert gate.main() == 1
        assert "fail-closed" in capsys.readouterr().out

    def test_only_tracked_files_are_scanned(self, tmp_path: Path) -> None:
        """İzlenmeyen dosya taranmaz — kapı git'in gördüğü ağacı ölçer.

        Bu ayrım bu oturumda pahalıya mal oldu: `check_doc_links` yerelde yeşil verdi
        çünkü yeni dosya henüz `git add` edilmemişti; CI'da kırmızı geldi.
        """
        subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
        (tmp_path / "izlenmeyen.sh").write_text("git add -A\n", encoding="utf-8")
        assert gate.tracked_scripts(tmp_path) == []
