"""D16 (Ç8) — "aynı KR iki yerde GÖVDEYLE tanımlanamaz" kapısı.

NEDEN (2026-07-31, denetim bulguları AR1/AR3/Y6):
    **AR1 (KRİTİK):** KR-093 aynı depoda İKİ normatif metinle tanımlı ve çelişiyorlar
    (içerik + statü haritası). Ölçüldü: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` gövdesi
    **10 satır**, `ssot/kr_registry.md` gövdesi **98 satır** (8 bölümlü kanonik format).
    İki gövde = iki gerçek; tüketici hangisine uyacağını bilemez ve biri sessizce bayatlar.

    **AR3:** sorun KR-093'e özgü değil — ölçüldü: SSOT metni **51**, registry **54** tanım
    taşıyor; **50 KR'nin gövdesi İKİ KAYNAKTA BİRDEN** var (birleşim 55, kesişim 50).

KAPI TASARIMI — neden "yasak" değil de "borç dondurma":
    Bugün 50 ikili gövde var. "İkili gövde yasak" diyen bir test 50 yerde düşerdi ve ilk
    işi devre dışı bırakılmak olurdu (yeşil-ama-yalan kapının kardeşi: kırmızı-ama-işe
    yaramaz kapı). Bunun yerine borç **donduruluyor**: liste yalnız KÜÇÜLEBİLİR.
    Yeni bir KR iki gövdeyle tanımlanırsa test kırmızıya döner.

    Göç kararının kendisi (hangi kaynak normatif kalacak) KOORDİNATÖR kararıdır ve
    çapraz-repo etkisi vardır — SSOT metni platform kopyasıyla bayt-özdeştir (C-SSOT),
    registry ise yalnız contract'ta yaşar. Karar verilmeden gövde taşımak, normatif
    içerik kaybı riski taşır. Bkz. eylem planı §14.4/D16.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest


ROOT = Path(__file__).parent.parent

# Çıkarıcıyı TEK yerden al (D2'de dört başlık biçimini tanır hâle getirildi).
import sys

sys.path.insert(0, str(Path(__file__).parent))
from test_kr_reference_integrity import (  # noqa: E402
    _registry_defined_krs,
    _ssot_defined_krs,
)


#: 2026-07-31 ölçümü — İKİ kaynakta birden gövdesi olan KR sayısı (bilinen borç).
#: Bu sayı YALNIZ KÜÇÜLEBİLİR. Arttıysa yeni bir ikili gövde eklenmiş demektir.
KNOWN_DUAL_BODY_COUNT = 50

#: Göçün İLK hedefi: veri-katmanı KR'leri (yalnız registry'de gövdeli olanlar hariç).
#: KR-093 denetimde KRİTİK olarak işaretlendi (AR1) — çelişen iki gövde.
PRIORITY_MIGRATION = ("KR-093",)


def _dual_body_krs() -> set[str]:
    return _ssot_defined_krs() & _registry_defined_krs()


class TestDualBodyDebtIsFrozen:
    def test_debt_does_not_grow(self) -> None:
        dual = _dual_body_krs()
        assert len(dual) <= KNOWN_DUAL_BODY_COUNT, (
            f"ikili gövde sayısı {len(dual)} — dondurulan borç {KNOWN_DUAL_BODY_COUNT}. "
            "Yeni bir KR iki normatif gövdeyle tanımlanmış: aynı kural iki yerde yazılırsa "
            "biri sessizce bayatlar (AR1'in tam olarak yaşandığı senaryo). Gövdeyi TEK "
            "kaynakta tutun, diğerine işaretçi koyun."
        )

    def test_debt_shrinks_are_recorded(self) -> None:
        """Borç azaldıysa sayacı güncelleyin — kapı gevşek kalmasın."""
        dual = _dual_body_krs()
        assert len(dual) >= KNOWN_DUAL_BODY_COUNT - 5, (
            f"ikili gövde sayısı {len(dual)}'e düşmüş (dondurulan {KNOWN_DUAL_BODY_COUNT}). "
            "Göç ilerlemiş: KNOWN_DUAL_BODY_COUNT'ü güncelleyin ki kapı yeni borcu yine "
            "yakalasın."
        )

    def test_priority_migration_target_is_still_tracked(self) -> None:
        """KR-093 göçü tamamlanınca bu test güncellenir (sessizce unutulmasın)."""
        dual = _dual_body_krs()
        for kr in PRIORITY_MIGRATION:
            if kr not in dual:
                pytest.fail(
                    f"{kr} artık tek gövdeli — göç TAMAMLANMIŞ olabilir. PRIORITY_MIGRATION "
                    "listesini ve KNOWN_DUAL_BODY_COUNT'ü güncelleyin, eylem planı §14.4/D16'yı "
                    "kapatın."
                )


class TestUndefinedQuantitiesAreDeclared:
    """A3 — atıf alan ama tanımı olmayan büyüklükler AÇIKÇA işaretli olmalı."""

    def test_stress_ratio_status_is_declared(self) -> None:
        enum_doc = json.loads(
            (ROOT / "enums" / "analysis_type.enum.v1.json").read_text(encoding="utf-8")
        )
        definitions = enum_doc["metadata"].get("indexDefinitions", {})
        entry = definitions.get("stress_ratio")
        assert entry, (
            "`stress_ratio` KR-093'ün zorunlu teslimat kaleminin kaynağı olarak anılıyor "
            "ama hiçbir yerde TANIMLI değil (A3: 3 atıf / 0 tanım). Tanımsız büyüklük ne "
            "üretilebilir ne denetlenebilir."
        )
        for key in ("status", "problem", "why_not_guessed", "blocked_on", "until_then"):
            assert str(entry.get(key, "")).strip(), f"beyanda eksik alan: {key}"

    def test_no_silent_undefined_quantity_in_preliminary_mapping(self) -> None:
        """Ön faz eşlemesi TANIMSIZ bir büyüklüğe dayanamaz."""
        report_phase = json.loads(
            (ROOT / "enums" / "report_phase.enum.v1.json").read_text(encoding="utf-8")
        )
        stage_b = report_phase["x-preliminary-content"]["stage_b_post_analysis"]
        text = json.dumps(stage_b, ensure_ascii=False)
        assert "stress_ratio" not in text, (
            "ön faz stage_b hâlâ tanımsız `stress_ratio`'ya dayanıyor — D17 ile "
            "WATER_STRESS çıkarıldı, eşleme de çıkmalıydı"
        )


class TestMachineAndProseAgree:
    """🔴 MAKİNE ile METİN aynı şeyi söylemeli — bu kapı BENİM HATAMDAN doğdu.

    2026-07-31/D17'de `WATER_STRESS` **enum'dan** (makine-okunur `x-preliminary-content`)
    çıkarıldı ama KR-093'ün **iki prose gövdesi** (SSOT metni + registry) onu hâlâ
    *"[ZORUNLU] PRELIMINARY içeriği"* olarak sayıyordu. Yani sözleşme iki farklı şey
    söyler hâle geldi — AR1'in (ikili gövde çürümesi) tam olarak yaşandığı senaryonun
    **yenisini ben ürettim**. Düzeltildi; bu kapı tekrarını engelliyor.

    Ders: makine-okunur bir listeyi değiştirirken, aynı listeyi **prose olarak** tekrar
    eden her normatif metin de aynı commit'te güncellenmelidir.
    """

    SOURCES = (
        ("docs/TARLAANALIZ_SSOT_v1_2_0.txt", "SSOT metni (çapraz-repo)"),
        ("ssot/kr_registry.md", "KR registry (contract-only)"),
    )

    def _proxy_only_layers(self) -> set[str]:
        analysis_type = json.loads(
            (ROOT / "enums" / "analysis_type.enum.v1.json").read_text(encoding="utf-8")
        )
        by_layer = analysis_type["metadata"]["bandRequirements"]["byLayer"]
        return {
            name for name, spec in by_layer.items()
            if isinstance(spec, dict) and spec.get("availability") == "proxy_only"
        }

    @pytest.mark.parametrize(("relative", "label"), SOURCES)
    def test_prose_does_not_mandate_a_proxy_layer(self, relative: str, label: str) -> None:
        text = (ROOT / relative).read_text(encoding="utf-8")
        for layer in self._proxy_only_layers():
            # "zorunlu içerik" bağlamı: katman adının indeks-eşlemesi olarak anılması.
            mandated = f"`{layer}`←" in text
            assert not mandated, (
                f"{label}: `{layer}` hâlâ ön fazın ZORUNLU içerik eşlemesinde görünüyor, "
                "oysa katman `proxy_only` (analysis_type). Makine-okunur liste ile normatif "
                "metin ayrışmış — ikisi aynı commit'te güncellenmelidir."
            )

    def test_undefined_quantity_is_not_mandated_in_prose(self) -> None:
        """`stress_ratio` tanımsız olduğu sürece hiçbir gövde onu ZORUNLU sayamaz."""
        for relative, label in self.SOURCES:
            text = (ROOT / relative).read_text(encoding="utf-8")
            assert "←stress_ratio" not in text, (
                f"{label}: tanımsız `stress_ratio` bir teslimat kaleminin kaynağı olarak "
                "zorunlu tutuluyor (A3). Tanım gelene kadar eşleme askıdadır."
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
