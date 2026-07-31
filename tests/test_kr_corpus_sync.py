"""AK-10 — KR korpusu dağıtım/sapma dedektörünün kapısı.

NEDEN (2026-07-31 ölçümü):
    KR korpusu (`docs/TARLAANALIZ_SSOT_v1_2_0.txt` + `ssot/kr_registry.md`) **hiçbir
    senkron aracının kapsamında değildi** — `tools/sync_to_repos.sh` yalnız `schemas/`,
    `enums/` ve `CONTRACTS_VERSION.md` taşıyor. Sonuç ölçüldü:

        kr_registry.md  → platform 1211/1242, worker 936 satır; ÜÇÜNDE DE `KR-093` YOK
        SSOT metni      → platform farklı, **worker'da hiç yok**

    Yani KR-093'ü (demo kritik yolunun kanonik tanımı) UYGULAYACAK olan platform, kuralın
    metnini görmüyordu. C-SSOT-2 bu kök nedeni işaret etmişti; bu araç onu ölçülebilir yapar.

TASARIM NOTU (bilinçli): araç kardeş depolara **kendiliğinden yazmaz**. `--check` ölçer,
`--apply` yalnız operatör tarafından çalıştırılır ve sonucu kardeş depoda AYRI bir PR olur.
Sessiz kopyalama, C8 töreninin görünmez bir yan etkisi olurdu.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location("sync_kr_corpus", ROOT / "tools" / "sync_kr_corpus.py")
assert _spec and _spec.loader
_sync = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_sync)


class TestTargetsAreDeclaredWithReasons:
    def test_every_target_has_a_reason(self) -> None:
        """Bir dosyayı neden gönderdiğimiz yazılı olmalı; 'her ihtimale karşı' bir gerekçe değil."""
        for target in _sync.TARGETS:
            assert len(target.reason) >= 30, f"{target.repo}: gerekçe zayıf ({target.reason!r})"

    def test_worker_is_covered(self) -> None:
        """Worker KR korpusunu HİÇ taşımıyordu — kapsam dışı bırakmak sapmayı sürdürürdü."""
        repos = {t.repo for t in _sync.TARGETS}
        assert "tarlaanaliz-worker" in repos and "tarlaanaliz-platform" in repos

    def test_both_corpus_files_are_covered(self) -> None:
        sources = {t.source for t in _sync.TARGETS}
        assert sources == {"docs/TARLAANALIZ_SSOT_v1_2_0.txt", "ssot/kr_registry.md"}

    def test_sources_exist_in_this_repo(self) -> None:
        for target in _sync.TARGETS:
            assert (ROOT / target.source).exists(), f"kaynak yok: {target.source}"


class TestDriftDetection:
    """Dedektörün DAVRANIŞINI ölçer (kardeş depo gerektirmez — geçici dizinlerle)."""

    def _fake(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, content: bytes | None,
              destination: str = "docs/x.txt") -> str:
        # ⚠️ BAYTLA yazılır: Windows'ta `write_text` `\n`'i `\r\n`'e çevirir ve CRLF
        # vakasını kurmayı imkânsız kılar (ilk yazımda tam olarak buna düştüm).
        contract = tmp_path / "contract"
        (contract / "docs").mkdir(parents=True)
        (contract / "docs" / "src.txt").write_bytes(b"KANON\n")
        sibling = tmp_path / "sibling"
        if content is not None:
            path = sibling / destination
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        else:
            sibling.mkdir(parents=True, exist_ok=True)
        monkeypatch.setattr(_sync, "ROOT", contract)
        monkeypatch.setattr(_sync, "WORKSPACE", tmp_path)
        monkeypatch.setattr(_sync, "TARGETS", (
            _sync.Target("docs/src.txt", "sibling", destination, "test gerekçesi — yeterince uzun"),
        ))
        return _sync.survey()[0]["state"]

    def test_in_sync_is_detected(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        assert self._fake(tmp_path, monkeypatch, b"KANON\n") == "IN_SYNC"

    def test_stale_is_detected(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        assert self._fake(tmp_path, monkeypatch, b"BAYAT\n") == "STALE"

    def test_missing_is_detected(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        assert self._fake(tmp_path, monkeypatch, None) == "MISSING"

    def test_crlf_is_not_drift(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Windows satır sonu farkı SAPMA DEĞİLDİR — yoksa kapı sürekli yalan söyler."""
        assert self._fake(tmp_path, monkeypatch, b"KANON\r\n") == "IN_SYNC"

    def test_absent_repo_is_not_silently_ok(self, tmp_path: Path,
                                            monkeypatch: pytest.MonkeyPatch) -> None:
        """Kardeş depo yoksa 'IN_SYNC' DEĞİL, ölçülemedi denir (sessiz yeşil yasak)."""
        contract = tmp_path / "contract"
        (contract / "docs").mkdir(parents=True)
        (contract / "docs" / "src.txt").write_text("K\n", encoding="utf-8")
        monkeypatch.setattr(_sync, "ROOT", contract)
        monkeypatch.setattr(_sync, "WORKSPACE", tmp_path)
        monkeypatch.setattr(_sync, "TARGETS", (
            _sync.Target("docs/src.txt", "olmayan-depo", "docs/x.txt", "test gerekçesi — uzun"),
        ))
        assert _sync.survey()[0]["state"] == "REPO_ABSENT"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
