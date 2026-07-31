"""D18 (K4) — PII kapısının KAPSAMI: `api/` de taranır, `phone`'un yeri bellidir.

NEDEN (2026-07-31, denetim bulgusu K4):
    `tools/validate.py` yalnız `schemas/` + `enums/` tarıyordu; CI'ın grep işi de yalnız
    `schemas/`. Yani **`api/` ağacı hiçbir PII kapısından geçmiyordu** — oysa kimlik
    yüzeyini (telefon + PIN) tanımlayan yer orası. Üstelik depo kendi checklist'inde
    (`SDLC_GATES` §1B) *"Hiçbir şema/enum/**API alanında** email/tckn/otp geçmiyor"*
    diyordu: **sözleşme, kendi iddiasının gerisindeydi.**

    İkinci sapma: `pyproject.toml` yasak listesi **3** değer taşırken `validate.py`
    **6** değer kontrol ediyordu — politika iki farklı şey söylüyordu.

    Üçüncüsü: `phone` KR-050'de yasak DEĞİL (kimlik modelinin kendisi), ama yeri belli —
    numara `user_pii.v1`de durur (`user.v1` kendi notunda *"Phone is stored in user_pii,
    NOT here"* diyor). Bu kural yazılıydı, **zorlanmıyordu**.
"""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path

import pytest


ROOT = Path(__file__).parent.parent
_TOOL = ROOT / "tools" / "validate.py"

_spec = importlib.util.spec_from_file_location("validate_tool", _TOOL)
assert _spec and _spec.loader
_validate = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_validate)


class TestForbiddenListIsSingleSourced:
    def test_pyproject_mirrors_the_tool(self) -> None:
        """İki kaynak ayrışırsa politika belirsizleşir (AK-4 ile aynı sınıf sapma)."""
        text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        block = re.search(r"^forbidden_fields\s*=\s*\[(.*?)\]", text, re.S | re.M)
        assert block, "pyproject.toml'da forbidden_fields bloğu yok"
        declared = set(re.findall(r'"([^"]+)"', block.group(1)))
        assert declared == set(_validate.FORBIDDEN_FIELDS), (
            f"pyproject={sorted(declared)} ↔ validate.py={sorted(_validate.FORBIDDEN_FIELDS)} "
            "AYRIŞMIŞ. Yasak alan politikası TEK yerde tanımlanır; ikisi birlikte değişir."
        )

    def test_hard_forbidden_set_is_not_silently_shrunk(self) -> None:
        assert set(_validate.FORBIDDEN_FIELDS) >= {
            "email", "e_mail", "tckn", "tc_kimlik_no", "otp", "one_time_password",
        }


class TestApiTreeIsScanned:
    def test_openapi_scanner_exists(self) -> None:
        assert hasattr(_validate, "validate_openapi_pii"), (
            "api/ ağacı için PII tarayıcısı yok — kapı, sözleşmenin iddia ettiği yeri "
            "hiç görmüyor demektir (K4)"
        )

    def test_forbidden_field_in_api_is_caught(self, tmp_path: Path) -> None:
        spec = tmp_path / "leaky.yaml"
        spec.write_text(
            "openapi: 3.1.0\n"
            "components:\n"
            "  schemas:\n"
            "    LoginRequest:\n"
            "      properties:\n"
            "        email:\n"
            "          type: string\n",
            encoding="utf-8",
        )
        errors = _validate.validate_openapi_pii(spec)
        assert errors and "email" in errors[0]

    def test_clean_api_file_passes(self, tmp_path: Path) -> None:
        spec = tmp_path / "clean.yaml"
        spec.write_text("openapi: 3.1.0\ncomponents:\n  schemas: {}\n", encoding="utf-8")
        assert not _validate.validate_openapi_pii(spec)

    def test_unreadable_spec_is_reported_not_swallowed(self, tmp_path: Path) -> None:
        spec = tmp_path / "broken.yaml"
        spec.write_text("openapi: [unclosed\n", encoding="utf-8")
        assert _validate.validate_openapi_pii(spec), "bozuk dosya sessizce geçilemez"


class TestPhoneIsScoped:
    """`phone` yasak değil ama YERİ belli — sızarsa hata."""

    def test_scope_rule_exists_for_phone(self) -> None:
        assert "phone" in _validate.SCOPED_FIELDS

    def test_phone_outside_its_scope_is_rejected(self) -> None:
        errors = _validate._check_forbidden_recursive(
            {"properties": {"phone": {"type": "string"}}},
            "$",
            ROOT / "schemas" / "core" / "mission.v1.schema.json",
        )
        assert any("OUT-OF-SCOPE" in e for e in errors), (
            "telefon numarası user_pii dışına sızabiliyor — user.v1'in kendi notu "
            "('Phone is stored in user_pii, NOT here') zorlanmıyor demektir"
        )

    def test_phone_inside_user_pii_is_allowed(self) -> None:
        errors = _validate._check_forbidden_recursive(
            {"properties": {"phone": {"type": "string"}}},
            "$",
            ROOT / "schemas" / "core" / "user_pii.v1.schema.json",
        )
        assert not errors

    def test_derived_names_are_not_false_positives(self) -> None:
        """`phone_verified` bir telefon NUMARASI değildir — eşleşme TAM ad üzerinden."""
        errors = _validate._check_forbidden_recursive(
            {"properties": {"phone_verified": {"type": "boolean"}}},
            "$",
            ROOT / "schemas" / "core" / "user.v1.schema.json",
        )
        assert not errors


class TestMetadataExceptionStaysNarrow:
    """İstisna listesi sessizce genişleyemez — her yeni satır bu testi de değiştirir."""

    def test_exception_list_is_exactly_the_declared_one(self) -> None:
        assert _validate.METADATA_EXCEPTIONS == {
            "api/platform_public.v1.yaml": ("$.info.contact.email",),
        }, (
            "PII istisna listesi değişmiş. Her istisna kapıyı zayıflatır: gerekçesini "
            "validate.py'de yazın, burada bilinçli olarak onaylayın ve eylem planına "
            "açık kalem ekleyin."
        )

    def test_exception_is_metadata_not_a_data_field(self) -> None:
        """İstisna yalnız BELGE KÜNYESİ yolunda olabilir; `components/paths` altında ASLA."""
        for _file, paths in _validate.METADATA_EXCEPTIONS.items():
            for path in paths:
                assert path.startswith("$.info."), (
                    f"veri yüzeyinde istisna: {path} — künye dışı istisna kabul edilemez"
                )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
