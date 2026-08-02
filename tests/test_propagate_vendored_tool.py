"""C8-a: `tools/propagate_vendored.py` GERÇEKTEN yayıyor mu?

Neden bu dosya var — ölçülmüş bir sessiz hata:
    Aracın ilk sürümünde `--check` kusursuz görünüyordu (eksik enum değerini doğru
    buluyor, doğru raporluyordu) ama `--apply` **hiçbir şey yazmıyordu**:
    `"0 genisletme yazildi"` + **exit 0**. Yani araç başarıyla hiçbir iş yapmıyordu ve
    çıktısı başarı gibi okunuyordu. Kök neden: `_enums_by_pointer` pointer'ı enum'u
    İÇEREN düğüme verir, enum LİSTESİNE değil; kod sözlüğün ANAHTARLARINI geziyordu.

    Bu ancak **mutasyonla** görüldü. Dolayısıyla mutasyonun kendisi teste çevrildi:
    aşağıdaki testler sentetik bir kanonik/vendored çifti kurar, gerçekten bozar ve
    aracın (a) bulduğunu (b) **yazdığını** ölçer. `--check`'i test etmek yetmez.

İkinci ölçülen hata: araç SUBSET çiftlerini de yayılım adayı sanıyordu ve 28 sahte
öneri üretiyordu. Uygulansaydı worker'ın **kasıtlı** dar runtime formunu kanonik
superset'e şişirirdi (I-4 ihlali).
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

_TOOL_PATH = Path(__file__).resolve().parents[1] / "tools" / "propagate_vendored.py"


def _tool():
    spec = importlib.util.spec_from_file_location("propagate_vendored", _TOOL_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _canonical() -> dict:
    return {
        "type": "object",
        "unevaluatedProperties": False,
        "required": ["kept"],
        "properties": {
            "kept": {"type": "string"},
            "opsiyonel_yeni": {
                "type": "string",
                "description": "Uzun kanonik gerekçe metni " * 20,
            },
            "kutu": {
                "type": "object",
                "properties": {
                    "tip": {
                        "type": "string",
                        "enum": ["A", "B", "YENI"],
                        "description": "Uzun kanonik gerekçe " * 20,
                    }
                },
            },
            "kisitsizdi": {"type": "string", "enum": ["X", "Y"]},
        },
    }


def _vendored() -> dict:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["kept"],
        "properties": {
            "kept": {"type": "string"},
            "kutu": {
                "type": "object",
                "properties": {"tip": {"type": "string", "enum": ["A", "B"]}},
            },
            "kisitsizdi": {"type": "string"},  # enum YOK -> kanonik kısıtladı
        },
    }


class TestFindsWhatIsActuallyMissing:
    def test_missing_enum_value_is_found(self) -> None:
        findings = _tool().analyse(_canonical(), _vendored(), "t.json")
        enum_hits = [f for f in findings if f.kind == "ENUM"]
        assert len(enum_hits) == 1
        assert "YENI" in enum_hits[0].detail

    def test_missing_optional_field_is_found(self) -> None:
        findings = _tool().analyse(_canonical(), _vendored(), "t.json")
        fields = [f.pointer for f in findings if f.kind == "FIELD"]
        assert fields == ["/properties/opsiyonel_yeni"]

    def test_constraint_tightening_is_reported_but_NOT_a_widening(self) -> None:
        """`kisitsizdi`: vendored'da serbest string, kanonikte enum → DARALTMA.

        v7.4.0'da `qc_report.flags` tam buydu. Otomatik uygulanmaz: o alana bugün
        yazan bir üretici, yeni kısıtın dışında bir değer yazıyor olabilir.
        """
        findings = _tool().analyse(_canonical(), _vendored(), "t.json")
        narrowings = [f for f in findings if f.kind == "NARROWING"]
        assert any(f.pointer == "/properties/kisitsizdi" for f in narrowings)

    def test_identical_pair_reports_nothing(self) -> None:
        doc = _vendored()
        assert _tool().analyse(doc, json.loads(json.dumps(doc)), "t.json") == []


class TestApplyActuallyWrites:
    """🔴 Aracın sessiz hatası tam buradaydı: `--check` doğru, `--apply` boş."""

    def test_enum_value_is_really_appended(self) -> None:
        tool = _tool()
        canonical, vendored = _canonical(), _vendored()
        findings = [f for f in tool.analyse(canonical, vendored, "t.json") if f.kind == "ENUM"]
        applied = tool.apply_widenings(canonical, vendored, findings)
        assert applied == 1, "arac 'bulundu' deyip HICBIR SEY yazmadi (eski sessiz hata)"
        assert vendored["properties"]["kutu"]["properties"]["tip"]["enum"] == ["A", "B", "YENI"]

    def test_optional_field_is_really_added(self) -> None:
        tool = _tool()
        canonical, vendored = _canonical(), _vendored()
        findings = [f for f in tool.analyse(canonical, vendored, "t.json") if f.kind == "FIELD"]
        assert tool.apply_widenings(canonical, vendored, findings) == 1
        assert "opsiyonel_yeni" in vendored["properties"]

    def test_applying_twice_is_idempotent(self) -> None:
        """İkinci koşuda aynı genişletmeler YENİDEN önerilmemeli.

        Aksi hâlde `--apply` her turda aynı değeri tekrar ekler (enum'da kopya) ve
        araç "hep bir şey var" diyerek asla temiz duruma yakınsamaz.
        """
        tool = _tool()
        canonical, vendored = _canonical(), _vendored()
        widenings = [
            f for f in tool.analyse(canonical, vendored, "t.json") if f.kind in ("ENUM", "FIELD")
        ]
        assert widenings, "onkosul: uygulanacak genisletme olmali"
        tool.apply_widenings(canonical, vendored, widenings)

        after = {(f.kind, f.pointer) for f in tool.analyse(canonical, vendored, "t.json")}
        assert not {
            k for k in after if k[0] in ("ENUM", "FIELD")
        }, f"ikinci kosuda genisletme yeniden onerildi: {sorted(after)}"
        # Daraltma kalemi DURMALI: o insan karari bekliyor, uygulanmadi.
        assert ("NARROWING", "/properties/kisitsizdi") in after
        # Enum'a kopya deger eklenmemis olmali.
        enum = vendored["properties"]["kutu"]["properties"]["tip"]["enum"]
        assert enum == ["A", "B", "YENI"], f"enum bozuldu: {enum}"


class TestVendoredIdiomAndProseAreRespected:
    """I-4: yayılım KOPYALAMA değil ALAN TAŞIMADIR."""

    def test_prose_is_cropped_not_carried(self) -> None:
        """C8'de kanonik prose vendored'a taşındı ve worker'da 45 test cp1254'te kırıldı."""
        tool = _tool()
        canonical, vendored = _canonical(), _vendored()
        fields = [f for f in tool.analyse(canonical, vendored, "t.json") if f.kind == "FIELD"]
        tool.apply_widenings(canonical, vendored, fields)
        carried = vendored["properties"]["opsiyonel_yeni"]["description"]
        original = canonical["properties"]["opsiyonel_yeni"]["description"]
        assert len(carried) < len(original) / 10, "prose kirpilmadi"
        assert "kanonik" in carried, "isaretci birakilmali"

    def test_unevaluated_properties_becomes_additional_properties(self) -> None:
        tool = _tool()
        nested = {"unevaluatedProperties": False, "properties": {"a": {"type": "string"}}}
        out = tool._crop_prose(nested)
        assert out["additionalProperties"] is False
        assert "unevaluatedProperties" not in out


class TestSubsetPairsAreNotTouched:
    def test_subset_mode_is_skipped_by_the_pair_walker(self) -> None:
        """SUBSET'te alan EKSİKLİĞİ normaldir; ilk sürüm 28 sahte yayılım öneriyordu."""
        source = _TOOL_PATH.read_text(encoding="utf-8")
        assert 'if mode != "MIRROR":' in source, (
            "arac SUBSET ciftlerini de yaymaya kalkiyor -- worker'in KASITLI dar runtime "
            "formunu kanonik superset'e sisirir (I-4 ihlali)"
        )


class TestPairListHasNoSecondCopy:
    def test_pairs_are_read_from_the_parity_gate(self) -> None:
        """D16 dersi: ikinci bir liste tutmak, listelerin ayrışmasına davetiyedir."""
        tool = _tool()
        import test_vendored_parity as parity  # noqa: PLC0415 — testin konusu bu bagimlilik

        expected = len(parity.MIRROR_PAIRS) + len(parity.SUBSET_PAIRS)
        assert len(tool._pairs()) == expected


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
