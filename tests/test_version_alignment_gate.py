"""I-1 sürüm hizası kapısının kendi kapısı — AL-K30.

NEDEN BU DOSYA VAR:
    Kapının kendisi (`tools/check_version_alignment.py`) **kardeş depolarda** koşar; bu
    deponun CI'ında kardeş checkout'u yoktur. `v7.7.1`/`v7.7.2` turlarında acı yoldan
    öğrenilen ders tam buydu: **veriye dayalı bir kapı, verisi olmayan ortamda kördür**
    ve orada bozulması görünmez.

    Bu yüzden buradaki testlerin tamamı **sentetiktir** — kardeş depo, ağ ya da git
    etiketi gerektirmez, her CI'da koşar. Kapı bozulursa burada kırmızı verir.

KAPSAM:
    ① sürüm ayrıştırma — ÜÇ deponun GERÇEK biçimi (sentetik kopyalarıyla)
    ② etiket seçimi — `vX.Y.Z` dışı biçimler yok sayılır
    ③ karar tablosu — iki kip, gerilik, ilerilik, muafiyet, süresi dolmuş muafiyet
    ④ fail-closed davranışı — "ölçemedim" asla "hizalı" sayılmaz
"""

from __future__ import annotations

import importlib.util
import sys
from datetime import date
from pathlib import Path

import pytest


ROOT = Path(__file__).parent.parent


def _load():
    spec = importlib.util.spec_from_file_location(
        "check_version_alignment", ROOT / "tools" / "check_version_alignment.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["check_version_alignment"] = module
    spec.loader.exec_module(module)
    return module


gate = _load()

TODAY = date(2026, 8, 11)

#: Satır sonu — çok satırlı sentetik dosya içerikleri bununla kuruluyor.
NL = "\n"


class TestVersionParsingHandlesAllThreeRealFormats:
    """Üç depo ÜÇ ayrı biçim kullanıyor — ayrıştırıcı üçünü de okumalı.

    Biçimler 2026-08-11'de gerçek dosyalardan **ölçüldü**; buradaki örnekler onların
    sentetik kopyasıdır (kardeş depo gerektirmesin diye).
    """

    @pytest.mark.parametrize(
        ("etiket", "metin", "beklenen"),
        [
            ("contract", "# Lock\n\n## Version: 7.7.2\n**Release Date:** 2026-08-11\n", (7, 7, 2)),
            ("worker", "# Contracts\n\nVersion: v7.7.2\nHash: aeb7131e\n", (7, 7, 2)),
            ("edge", "| **Upstream Contract Set (SSOT)** | `7.7.2` (SSOT `7.7.2` = ...) |\n", (7, 7, 2)),
        ],
    )
    def test_real_world_formats_parse(self, etiket: str, metin: str, beklenen) -> None:
        assert gate.parse_version(metin) == beklenen, f"{etiket} biçimi okunamadı"

    def test_v_prefix_is_optional(self) -> None:
        assert gate.parse_version("v1.2.3") == gate.parse_version("1.2.3") == (1, 2, 3)

    def test_no_version_is_none_not_zero(self) -> None:
        """POZİTİF KONTROL — sürüm yoksa `None` dönmeli; `0.0.0` sessiz fail-open olurdu."""
        assert gate.parse_version("burada sürüm yok") is None
        assert gate.parse_version("") is None

    def test_two_part_version_is_not_matched(self) -> None:
        assert gate.parse_version("7.7") is None


class TestPinnedExtractionRefusesToGuess:
    """🔴 Bu sınıf, kapının GERÇEK VERİYE karşı koşturulmasıyla bulunan kusurdan doğdu.

    İlk yazımda kural *"dosyadaki ilk sürüm eşleşmesi"*ydi ve sentetik testlerin hepsi
    yeşildi. Gerçek dosyalara karşı koşturunca **yanlış sayıyı okudu**:

        edge/CONTRACTS_VERSION.md
          satır  3 : CONTRACTS_VERSION=1.7.0     ← edge'in KENDİ SemVer'i
          satır 11 : | **Upstream Contract Set (SSOT)** | `7.7.2`   ← ASIL PIN

    Kapı `1.7.0` okudu ve "I-1 KIRIK" dedi — **doğru cevabı yanlış gerekçeyle**. Sürüm
    dizeleri bir gün örtüşseydi **yanlış YEŞİL** verecekti.

    Ölçüm: üç sürüm dosyasında sırasıyla 30 · 22 · 27 FARKLI sürüm dizesi var (değişiklik
    geçmişi aynı dosyada duruyor). "İlk eşleşme" bir tahmindi.
    """

    #: Gerçek edge dosyasının yapısal kopyası (sentetik — kardeş depo gerekmez).
    EDGE = NL.join([
        "# Edge Contracts",
        "",
        "CONTRACTS_VERSION=1.7.0",
        "",
        "**Version:** 1.7.0",
        "",
        "| **Upstream Contract Set (SSOT)** | `7.7.2` (SSOT `7.7.2` = ...) |",
        "",
    ])

    def test_label_selects_the_right_line(self) -> None:
        version, gerekce = gate.extract_pinned(self.EDGE, "Upstream Contract Set")
        assert (version, gerekce) == ((7, 7, 2), "ok"), (version, gerekce)

    def test_without_label_it_fails_closed_instead_of_guessing(self) -> None:
        version, gerekce = gate.extract_pinned(self.EDGE)
        assert version is None, f"tahmin etti: {version} — sessizce yanlış satırı okuyor"
        assert "TAHMİN EDİLEMEZ" in gerekce and "--label" in gerekce, gerekce

    def test_the_old_first_match_rule_would_have_read_the_wrong_value(self) -> None:
        """MUTASYON KANITI — eski kural bugün de yanlış cevabı verirdi."""
        assert gate.parse_version(self.EDGE) == (1, 7, 0), (
            "İlk-eşleşme kuralı artık 1.7.0 okumuyorsa bu test bayatlamıştır; kusurun "
            "gerçekten var olduğunu kanıtlayan pozitif kontrol budur."
        )
        assert gate.extract_pinned(self.EDGE, "Upstream Contract Set")[0] == (7, 7, 2)

    def test_single_version_file_needs_no_label(self) -> None:
        """POZİTİF KONTROL — belirsizlik YOKSA etiket zorunlu olmamalı (gereksiz sürtünme)."""
        version, gerekce = gate.extract_pinned("Version: v7.7.2" + NL)
        assert (version, gerekce) == ((7, 7, 2), "ok")

    def test_label_with_no_match_fails_closed(self) -> None:
        version, gerekce = gate.extract_pinned(self.EDGE, "Boyle Bir Satir Yok")
        assert version is None and "içeren satır yok" in gerekce, gerekce

    def test_label_line_without_a_version_fails_closed(self) -> None:
        metin = NL.join(["Upstream Contract Set: bilinmiyor", "Version: 7.7.2", ""])
        version, gerekce = gate.extract_pinned(metin, "Upstream Contract Set")
        assert version is None and "sürüm dizesi yok" in gerekce, gerekce

    def test_repeated_same_version_is_not_ambiguous(self) -> None:
        """Aynı sürüm birden çok kez geçiyorsa belirsizlik YOKTUR — yanlış alarm olmasın."""
        metin = NL.join(["Version: 7.7.2", "yine 7.7.2", "ve v7.7.2", ""])
        assert gate.extract_pinned(metin)[0] == (7, 7, 2)


class TestNewestTagIgnoresNonCanonicalNames:
    def test_highest_wins_not_lexicographic(self) -> None:
        """`v7.10.0` > `v7.9.0` — sözlük sırası burada yanlış cevap verir."""
        assert gate.newest_tag(["v7.9.0", "v7.10.0", "v7.7.2"]) == (7, 10, 0)

    def test_non_canonical_tags_are_ignored(self) -> None:
        assert gate.newest_tag(["v7.7.2", "release-8.0.0", "v9.0.0-rc1", "8.0.0"]) == (7, 7, 2)

    def test_empty_is_none(self) -> None:
        """Fail-closed kaynağı: etiket yoksa `None` — çağıran bunu hata sayar."""
        assert gate.newest_tag([]) is None
        assert gate.newest_tag(["main", "HEAD"]) is None


class TestConsumerMode:
    """Kardeş depo: pin en yeni yayımlanmış sürüme EŞİT olmalı."""

    def test_aligned_passes(self) -> None:
        code, msg = gate.evaluate("consumer", (7, 7, 2), (7, 7, 2), TODAY)
        assert code == 0, msg

    def test_silent_lag_fails(self) -> None:
        """2026-08-11'de ölçülen gerçek olay: edge 7.6.1'i hiç pinlemedi."""
        code, msg = gate.evaluate("consumer", (7, 6, 0), (7, 6, 1), TODAY)
        assert code == 1 and "I-1 KIRIK" in msg, msg

    def test_pinning_ahead_of_published_fails(self) -> None:
        """Yayımlanmamış sürüme pinlenemez — etiket yoksa checkout da edilemez."""
        code, msg = gate.evaluate("consumer", (7, 8, 0), (7, 7, 2), TODAY)
        assert code == 1 and "yayımlanmamış" in msg, msg

    def test_dated_waiver_with_reason_passes(self) -> None:
        code, msg = gate.evaluate(
            "consumer", (7, 7, 1), (7, 7, 2), TODAY,
            allow_lag_until=date(2026, 8, 20), reason="re-pin PR'ı bekliyor",
        )
        assert code == 0 and "GEÇİCİ SAPMA" in msg, msg

    def test_waiver_without_reason_fails(self) -> None:
        """Gerekçesiz muafiyet, kuralın sessizce kapatılmasıdır."""
        for gerekce in (None, "", "   "):
            code, msg = gate.evaluate(
                "consumer", (7, 7, 1), (7, 7, 2), TODAY,
                allow_lag_until=date(2026, 8, 20), reason=gerekce,
            )
            assert code == 1 and "GEREKÇESİZ" in msg, (gerekce, msg)

    def test_expired_waiver_fails(self) -> None:
        """I-5: sapma yalnız GEÇİCİ. Süresi dolmuş muafiyet kalıcı ayrışmadır."""
        code, msg = gate.evaluate(
            "consumer", (7, 7, 1), (7, 7, 2), TODAY,
            allow_lag_until=date(2026, 8, 10), reason="unutuldu",
        )
        assert code == 1 and "SÜRESİ DOLDU" in msg, msg

    def test_waiver_on_its_last_day_still_passes(self) -> None:
        """Sınır günü dahildir — kapalı aralık."""
        code, _ = gate.evaluate(
            "consumer", (7, 7, 1), (7, 7, 2), TODAY,
            allow_lag_until=TODAY, reason="son gün",
        )
        assert code == 0


class TestCanonicalMode:
    """Contract'ın kendisi: sürüm etiketin GERİSİNDE olamaz, ilerisinde olabilir."""

    def test_equal_passes(self) -> None:
        assert gate.evaluate("canonical", (7, 7, 2), (7, 7, 2), TODAY)[0] == 0

    def test_ahead_passes_because_release_is_in_flight(self) -> None:
        """Release PR'ının NORMAL hâli: sürüm yükseltildi, etiket henüz basılmadı.

        Bu kip ayrımı olmasaydı kapı her release PR'ında yanlış kırmızı verirdi —
        yani ilk fırsatta devre dışı bırakılırdı.
        """
        code, msg = gate.evaluate("canonical", (7, 7, 3), (7, 7, 2), TODAY)
        assert code == 0 and "release uçuşta" in msg, msg

    def test_behind_fails(self) -> None:
        code, msg = gate.evaluate("canonical", (7, 7, 1), (7, 7, 2), TODAY)
        assert code == 1 and "gerilemesidir" in msg, msg

    def test_canonical_does_not_use_the_waiver(self) -> None:
        """POZİTİF KONTROL — muafiyet yalnız tüketici kipine ait; kanonikte geçmemeli."""
        code, _ = gate.evaluate(
            "canonical", (7, 7, 1), (7, 7, 2), TODAY,
            allow_lag_until=date(2030, 1, 1), reason="olmaz",
        )
        assert code == 1, "kanonik kip muafiyeti kabul ediyor — sürüm gerilemesi gizlenir"


class TestFailClosedBehaviour:
    """'Ölçemedim' asla 'hizalı' sayılmaz."""

    def test_missing_pin_file_exits_1(self, tmp_path: Path, capsys) -> None:
        # ⚠️ Sahte dosya adı BİLEREK uzantısızdır. İlk yazımda belge uzantılı bir ad
        # kullandım; sarkan atıf kapısı onu kırık belge bağlantısı sandı ve CI kırmızıya
        # döndü. Sonra kusuru yorumda ADIYLA anlattım — kapı ONU da yakaladı. Kural:
        # sahte dosya adına belge uzantısı verme ve gerekçesinde de yazma.
        code = gate.main([
            "--mode", "consumer",
            "--pinned-file", str(tmp_path / "olmayan-pin-dosyasi"),
            "--latest", "7.7.2",
        ])
        assert code == 1 and "fail-closed" in capsys.readouterr().out

    def test_unparseable_pin_exits_1(self, tmp_path: Path, capsys) -> None:
        dosya = tmp_path / "CONTRACTS_VERSION.md"
        dosya.write_text("burada sürüm yok\n", encoding="utf-8")
        code = gate.main(["--mode", "consumer", "--pinned-file", str(dosya), "--latest", "7.7.2"])
        assert code == 1 and "bulunamadı" in capsys.readouterr().out

    def test_no_tags_exits_1(self, tmp_path: Path, capsys) -> None:
        """Etiketsiz depoda kapı susmaz — fail-closed kapanır."""
        code = gate.main([
            "--mode", "consumer", "--pinned", "7.7.2", "--latest-from-git", str(tmp_path),
        ])
        assert code == 1 and "fail-closed" in capsys.readouterr().out

    def test_bad_date_exits_1(self, tmp_path: Path, capsys) -> None:
        code = gate.main([
            "--mode", "consumer", "--pinned", "7.7.1", "--latest", "7.7.2",
            "--allow-lag-until", "20 Ağustos", "--reason", "x",
        ])
        assert code == 1 and "fail-closed" in capsys.readouterr().out

    def test_it_prints_what_it_read(self, tmp_path: Path, capsys) -> None:
        """Sessizce YANLIŞ satırı okumak en sinsi hatadır — okunan değer basılmalı."""
        dosya = tmp_path / "CONTRACTS_VERSION.md"
        dosya.write_text("Version: v7.7.2\n", encoding="utf-8")
        gate.main(["--mode", "consumer", "--pinned-file", str(dosya), "--latest", "7.7.2"])
        cikti = capsys.readouterr().out
        assert "okunan pin      : 7.7.2" in cikti and "okunan en yeni  : 7.7.2" in cikti, cikti


class TestEndToEndOnASyntheticRepo:
    """POZİTİF KONTROL — kapı gerçekten git etiketi okuyabiliyor mu?"""

    @staticmethod
    def _repo(tmp_path: Path, tags: list[str]) -> Path:
        import subprocess

        subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
        for komut in (
            ["git", "-C", str(tmp_path), "config", "user.email", "t@t"],
            ["git", "-C", str(tmp_path), "config", "user.name", "t"],
        ):
            subprocess.run(komut, check=True)
        (tmp_path / "x.txt").write_text("x", encoding="utf-8")
        subprocess.run(["git", "-C", str(tmp_path), "add", "x.txt"], check=True)
        subprocess.run(["git", "-C", str(tmp_path), "commit", "-qm", "ilk"], check=True)
        for tag in tags:
            subprocess.run(["git", "-C", str(tmp_path), "tag", "-a", tag, "-m", tag], check=True)
        return tmp_path

    def test_reads_tags_and_passes_when_aligned(self, tmp_path: Path, capsys) -> None:
        repo = self._repo(tmp_path, ["v7.7.0", "v7.7.2"])
        code = gate.main([
            "--mode", "consumer", "--pinned", "7.7.2", "--latest-from-git", str(repo),
        ])
        assert code == 0, capsys.readouterr().out

    def test_reads_tags_and_catches_lag(self, tmp_path: Path, capsys) -> None:
        repo = self._repo(tmp_path, ["v7.7.0", "v7.7.2"])
        code = gate.main([
            "--mode", "consumer", "--pinned", "7.7.0", "--latest-from-git", str(repo),
        ])
        assert code == 1 and "I-1 KIRIK" in capsys.readouterr().out
