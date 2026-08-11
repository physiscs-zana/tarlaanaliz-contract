"""Vendored kopyalarda ALAN SIZMASI POLİTİKASI paritesi — iki kapının kör noktası.

NEDEN (2026-08-11, kendi öz-denetimimde bulundu):
    Kanonikte 27 object düğümüne sızma politikası eklendikten sonra iki kapı da
    **yeşil** kaldı:

        tools/propagate_vendored.py --check  ->  "Bekleyen yayılım YOK" (exit 0)
        tests/test_vendored_parity.py        ->  185 passed

    ama elle ölçüm worker'ın vendored kopyalarında **5 sapma** buldu (kanonik kapalı,
    vendored beyansız). Sebep ikisinin de kapsamı:

      * `propagate_vendored.py` yalnız **enum değeri** ve **opsiyonel alan** yayılımını
        ölçer (docstring §"GENİŞLETME"); politika anahtarları kapsamında DEĞİL.
      * `test_vendored_parity.py::TestSubsetPairsMayOmitButNotContradict` yalnız ortak
        `$defs` **alanlarının** alt şemalarını karşılaştırır; `$.properties.*` altındaki
        iç içe düğümlerin politika anahtarına bakmaz.

    Sonuç: kanonik sıkılaşırken vendored kopya gevşek kalabiliyor ve **hiçbir kapı
    bunu söylemiyor**. Bu, worker için kozmetik değil: worker'ın gelen doğrulaması
    BLOKLAYICI (şema tutmazsa `REJECTED`), yani iki taraf farklı şeyi kabul ediyor.

BU KAPININ KURALI — I-4 ile UYUMLU:
    Vendored kopya düğüm **atlayabilir** (alt küme hakkı; `DÜĞÜM YOK` sapma değildir).
    Ama **iki tarafta da var olan** bir düğümün sızma politikası AYNI anlama gelmelidir.
    İdiom farkı normalize edilir (I-4): `unevaluatedProperties: false` ≡
    `additionalProperties: false` → KAPALI.

RATCHET: `KNOWN_POLICY_DIVERGENCE` yalnız KÜÇÜLÜR — yeni sapma kırmızı, bayat satır
da kırmızı (hizalandıysa satırı silin).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).parent.parent
WORKSPACE = ROOT.parent

sys.path.insert(0, str(ROOT / "tests"))

#: ✅ **BOŞ — ve boş KALMALI (2026-08-11).**
#:
#: Kapı kurulduğunda burada 3 satır vardı (`analysis_result.v1` → `index_maps` ·
#: `model_metadata` · `thermal_results`); üçü de bu turdan ÖNCE vardı ve hiçbir kapı
#: görmüyordu. Worker oturumuna bildirildi, **aynı gün hizalandı**
#: (worker `2139987` → 5 düğüm, `7e18abe` → 3 düğüm) ve ratchet'in "bayat baseline"
#: yönü beni bu satırları silmeye ZORLADI — kapı kendini temizledi.
#:
#: 🔒 Liste sıfırdan büyütülemez: yeni bir sapma buraya EKLENEREK geçirilemez.
#: Ya kanonikle hizalayın (idiom: vendored tarafta `additionalProperties`), ya da
#: bilinçli bir ayrışmaysa gerekçesini yazıp `test_baseline_is_empty`'yi bilerek
#: değiştirin — o değişiklik incelemede GÖRÜNÜR olur.
KNOWN_POLICY_DIVERGENCE: tuple[tuple[str, str], ...] = ()

#: Kardeş depo yoksa atlama gerekçesi — `tests/conftest.py::ALLOWED_SKIP_REASONS`
#: bu dizeyi ve BU DOSYAYI beyanlı sayar. Beyansız atlama oturumu düşürür.
#:
#: 🔴 **DÜZELTME (2026-08-11): "kardeş CI'ında koşar" İDDİASI BUGÜN YANLIŞTI.**
#: Bu dosya yazılırken `test_vendored_parity.py` ile aynı D4-b desenine güvendim ve
#: "kardeş depoda koşar" dedim. Worker oturumu düzeltti, ben de bağımsız ÖLÇTÜM —
#: iki ayrı engel var ve ikisi de bağımsız olarak yeterli:
#:   (a) worker `contracts_gate.yml::sibling-parity` contract'ı **pinli etikette**
#:       checkout ediyor (`ref: ${{ steps.pin.outputs.version }}` = `v7.6.1`);
#:       ölçüldü: `git ls-tree -r v7.6.1 | grep policy_parity` → **0**,
#:       `origin/master` → 1. Dosya o checkout'a hiç girmiyor.
#:   (b) pin düzelse bile koşmaz: o iş pytest'e **dosya adlarını tek tek** veriyor
#:       (`tests/test_vendored_parity.py`), glob değil.
#: Yani bu kapı BUGÜN **yalnız geliştirici-zamanı** çalışıyor: contract CI'da beyanlı
#: atlanır, worker CI'ında hiç çağrılmaz. "Koşuyor" varsaymak, olmayan bir kapıya
#: güvenmektir (worker'ın kendi kuralı: *"kapsamı ölçülmeyen kapı, olmayan kapıdır"*).
#: Kapanışı worker'ın re-pin turunda: pin `v7.7.0` + pytest çağrısına glob/ikinci dosya.
SKIP_REASON = "kardeş depo yok"


def _pairs() -> list[tuple[str, str]]:
    """Parite çiftleri TEK KAYNAKTAN — ikinci bir liste tutmak D16'nın hatası olurdu."""
    import test_vendored_parity as parity  # type: ignore[import-not-found]

    return list(parity.MIRROR_PAIRS) + list(parity.SUBSET_PAIRS)


def _is_object(node: dict) -> bool:
    declared = node.get("type")
    return declared == "object" or (isinstance(declared, list) and "object" in declared)


def _policy(node: dict) -> str:
    """I-4 idiom farkını normalize eder: iki anahtar da AYNI anlamı taşır."""
    if node.get("unevaluatedProperties") is False or node.get("additionalProperties") is False:
        return "KAPALI"
    if node.get("additionalProperties") is True:
        return "AÇIK"
    if "additionalProperties" in node or "unevaluatedProperties" in node:
        value = node.get("additionalProperties", node.get("unevaluatedProperties"))
        return f"DİĞER({value!r})"
    return "BEYANSIZ"


def _object_nodes(doc: object) -> dict[str, dict]:
    found: dict[str, dict] = {}

    def walk(node: object, pointer: str) -> None:
        if isinstance(node, dict):
            if _is_object(node):
                found[pointer] = node
            for key, value in node.items():
                if key in {"examples", "example", "default", "const", "enum", "notes"}:
                    continue
                if key.startswith("x-"):
                    continue
                walk(value, f"{pointer}.{key}")
        elif isinstance(node, list):
            for index, value in enumerate(node):
                walk(value, f"{pointer}[{index}]")

    walk(doc, "$")
    return found


def scan() -> tuple[list[tuple[str, str, str, str]], int, int]:
    """(sapmalar, karşılaştırılan çift, karşılaştırılan ortak düğüm)."""
    divergences: list[tuple[str, str, str, str]] = []
    pairs_seen = 0
    nodes_compared = 0
    for canonical, vendored in _pairs():
        canonical_path, vendored_path = ROOT / canonical, WORKSPACE / vendored
        if not vendored_path.exists() or not canonical_path.exists():
            continue
        pairs_seen += 1
        canonical_nodes = _object_nodes(json.loads(canonical_path.read_text(encoding="utf-8")))
        vendored_nodes = _object_nodes(json.loads(vendored_path.read_text(encoding="utf-8")))
        for pointer in sorted(set(canonical_nodes) & set(vendored_nodes)):
            nodes_compared += 1
            left, right = _policy(canonical_nodes[pointer]), _policy(vendored_nodes[pointer])
            if left != right:
                divergences.append((canonical, pointer, left, right))
    return divergences, pairs_seen, nodes_compared


def _node_at(doc: object, pointer: str):
    """`$.a.b[0]` biçimli pointer'ı çözer (yalnız bu dosyanın ürettiği biçim)."""
    node = doc
    for part in pointer.split(".")[1:]:
        while part.endswith("]") and "[" in part:
            part, _, index = part[:-1].partition("[")
            if part:
                if not isinstance(node, dict) or part not in node:
                    return None
                node = node[part]
            if not isinstance(node, list) or int(index) >= len(node):
                return None
            node = node[int(index)]
            part = ""
        if part:
            if not isinstance(node, dict) or part not in node:
                return None
            node = node[part]
    return node


def _resolve_local_ref(doc: object, node: object) -> object:
    """Düğüm `#/...` yerel `$ref` ise hedefini döndürür; değilse düğümün kendisini.

    ⚠️ Bu satır bir öz-denetim düzeltmesidir: ilk yazımda `_narrowing_warnings` `$ref`'i
    ÇÖZMÜYORDU ve uyarı *"kanonik 0 alan"* diyordu — gerçek 9. **Yanlış sayı taşıyan
    uyarı, uyarı değildir.**
    """
    if not isinstance(node, dict):
        return node
    ref = node.get("$ref")
    if not isinstance(ref, str) or not ref.startswith("#/"):
        return node
    target: object = doc
    for part in ref[2:].split("/"):
        if not isinstance(target, dict) or part not in target:
            return node
        target = target[part]
    return target


def _narrowing_warnings(pairs: list) -> str:
    """Sapma raporuna 'KAPATMA — aşırı kısıtlama olur' uyarısı ekler.

    ⚠️ Bu, worker oturumunun 2026-08-11'de ÖLÇÜP bildirdiği kuraldır ve benim kapımın
    tavsiyesini düzeltir: vendored düğüm kanoniğin **dar alt kümesiyse**
    `additionalProperties: false` yazmak hizalama değil **bug**tur — meşru kanonik
    alanlar reddedilir. Kapı, alan kümelerini karşılaştırmadan "hizala" DİYEMEZ.
    """
    satirlar = []
    for rel, pointer in pairs:
        canonical_path = ROOT / rel
        vendored_rel = dict(_pairs()).get(rel)
        if vendored_rel is None or not (WORKSPACE / vendored_rel).exists():
            continue
        cd = json.loads(canonical_path.read_text(encoding="utf-8"))
        vd = json.loads((WORKSPACE / vendored_rel).read_text(encoding="utf-8"))
        cn = _resolve_local_ref(cd, _node_at(cd, pointer))
        vn = _resolve_local_ref(vd, _node_at(vd, pointer))
        if not isinstance(cn, dict) or not isinstance(vn, dict):
            continue
        kset, vset = set(cn.get("properties", {})), set(vn.get("properties", {}))
        if kset != vset:
            satirlar.append(
                f"    {rel} {pointer}: ALAN KÜMELERİ AYRIŞIK "
                f"(kanonik {len(kset)} · vendored {len(vset)}) → **KAPATMAYIN**, "
                f"{len(kset - vset)} meşru kanonik alan reddedilirdi."
            )
    if not satirlar:
        return ""
    return (
        "\n\n🔴 AŞIRI KISITLAMA UYARISI — bu düğümlerde alan kümesi ayrışıyor; "
        "`additionalProperties: false` yazmak hizalama DEĞİL bug olur:\n"
        + "\n".join(satirlar)
    )


@pytest.fixture(scope="module")
def measurement():
    divergences, pairs_seen, nodes_compared = scan()
    if pairs_seen == 0:
        pytest.skip(
            f"{SKIP_REASON} — bu kapı BUGÜN yalnız geliştirici-zamanı koşar "
            "(worker CI pinli etikette checkout ediyor ve pytest'e dosya adlarını "
            "tek tek veriyor; ölçüldü 2026-08-11). Kardeş depoları yan yana "
            "tutup yerelde koşun."
        )
    return divergences, pairs_seen, nodes_compared


class TestPolicyDivergenceOnlyShrinks:
    """RATCHET — iki yön."""

    def test_no_new_divergence(self, measurement) -> None:
        divergences, _, _ = measurement
        current = {(rel, pointer) for rel, pointer, _, _ in divergences}
        new = sorted(current - set(KNOWN_POLICY_DIVERGENCE))
        detail = {(rel, pointer): (left, right) for rel, pointer, left, right in divergences}
        # ⚠️ TAVSİYE GÜVENLİĞİ (worker oturumunun 2026-08-11'de ölçtüğü kural):
        # vendored düğüm kanoniğin DAR ALT KÜMESİYSE `additionalProperties: false`
        # yazmak hizalama değil **aşırı kısıtlamadır** — meşru kanonik alanları reddeder.
        # Bu yüzden mesaj, alan kümelerini karşılaştırmadan "hizala" DEMEZ.
        uyari = _narrowing_warnings(new)
        assert not new, (
            f"{len(new)} YENİ politika sapması — kanonik ile vendored kopya sızma "
            "konusunda FARKLI şey söylüyor:\n  "
            + "\n  ".join(
                f"{rel} {pointer}\n      kanonik={detail[(rel, pointer)][0]} "
                f"vendored={detail[(rel, pointer)][1]}"
                for rel, pointer in new
            )
            + "\n\nKanonikte politika değiştirdiyseniz vendored kopyaya da yayın "
            "(idiom: vendored tarafta `additionalProperties`). ⚠️ Yayılım bir "
            "DARALTMADIR — `tools/propagate_vendored.py` docstring'inin kuralı gereği "
            "önce ÜRETİCİYİ ölçün. Ne `propagate_vendored --check` ne de "
            "`test_vendored_parity` bu sınıfı görür; kapı budur."
            + uyari
        )

    def test_baseline_has_no_stale_entry(self, measurement) -> None:
        divergences, _, _ = measurement
        current = {(rel, pointer) for rel, pointer, _, _ in divergences}
        stale = sorted(set(KNOWN_POLICY_DIVERGENCE) - current)
        assert not stale, (
            f"{len(stale)} baseline satırı artık sapma DEĞİL — hizalanmış olabilir. "
            "Bayat baseline, kapının o düğümü hâlâ 'borç' sandığı anlamına gelir; "
            "satırları SİLİN:\n  " + "\n  ".join(f"{rel}  {pointer}" for rel, pointer in stale)
        )

    def test_baseline_is_empty(self) -> None:
        """Ratchet SIFIRA indi — borç listesi artık bir kaçış deliği değil."""
        assert len(KNOWN_POLICY_DIVERGENCE) == 0, (
            f"Baseline {len(KNOWN_POLICY_DIVERGENCE)} satır; 2026-08-11'de **0**'a indi. "
            "Yeni bir sapma buraya EKLENEREK geçirilemez: ya vendored kopyayı kanonikle "
            "hizalayın, ya da ayrışma bilinçliyse gerekçesini yazıp bu testi kasıtlı "
            "olarak değiştirin — o değişiklik incelemede görünür olur."
        )


class TestRefInlineAsymmetryIsVisible:
    """KÖR NOKTA GÖRÜNÜR OLSUN — worker oturumunun 2026-08-11'de bildirdiği sınıf.

    Karşılaştırma **pointer tabanlıdır**: bir tarafta `$ref`, diğerinde INLINE olan
    aynı mantıksal düğüm iki farklı biçimde durur ve kesişime GİRMEZ. Ölçüldü:
    bugün **tam 1** böyle düğüm var —

        `schemas/worker/analysis_result.v1.schema.json` → `$.properties.summary`
        kanonik: `$ref` → `$defs.ResultSummary` (9 alan, KAPALI)
        vendored: INLINE, **1 alan** (`yield_estimate`), BEYANSIZ

    ⚠️ Bu düğüm karşılaştırmaya SOKULMAMALI: alan kümeleri ayrışık olduğu için
    "hizala" tavsiyesi **8 meşru kanonik alanı reddettirirdi**. Yani burada
    karşılaştırmamak doğru davranıştır — ama **sessiz** kalmamalı; sayı kilitli.
    """

    MEASURED_ASYMMETRIC = 1

    @staticmethod
    def _asymmetric() -> list:
        found = []
        for canonical, vendored in _pairs():
            cp, vp = ROOT / canonical, WORKSPACE / vendored
            if not (cp.exists() and vp.exists()):
                continue
            cd = json.loads(cp.read_text(encoding="utf-8"))
            vd = json.loads(vp.read_text(encoding="utf-8"))
            cobj, vobj = _object_nodes(cd), _object_nodes(vd)

            def refs(doc):
                out = {}

                def walk(node, pointer):
                    if isinstance(node, dict):
                        if isinstance(node.get("$ref"), str):
                            out[pointer] = node["$ref"]
                        for key, value in node.items():
                            if key in {"examples", "example", "default", "const", "enum", "notes"}:
                                continue
                            if key.startswith("x-"):
                                continue
                            walk(value, f"{pointer}.{key}")
                    elif isinstance(node, list):
                        for index, value in enumerate(node):
                            walk(value, f"{pointer}[{index}]")

                walk(doc, "$")
                return out

            for pointer in refs(cd):
                if pointer in vobj and pointer not in cobj:
                    found.append((canonical, pointer, "kanonik=$ref vendored=INLINE"))
            for pointer in refs(vd):
                if pointer in cobj and pointer not in vobj:
                    found.append((canonical, pointer, "kanonik=INLINE vendored=$ref"))
        return found

    def test_asymmetry_count_is_locked(self, measurement) -> None:
        found = self._asymmetric()
        assert len(found) <= self.MEASURED_ASYMMETRIC, (
            f"{len(found)} asimetrik ($ref ↔ inline) düğüm var; ölçülen taban "
            f"{self.MEASURED_ASYMMETRIC}. Bu düğümler pointer tabanlı karşılaştırmaya "
            "GİRMEZ — yani politika sapmaları bu kapının kör noktasındadır. Sayı "
            "artıyorsa kör nokta büyüyor: ya vendored kopyayı `$ref`'e taşıyın, ya "
            "artışı gerekçesiyle bu tabana yazın.\n  "
            + "\n  ".join(f"{rel} {ptr} [{tur}]" for rel, ptr, tur in found)
        )

    def test_the_known_asymmetry_is_still_a_narrow_subset(self, measurement) -> None:
        """Bilinen tek asimetri GERÇEKTEN dar alt küme mi — yoksa kapatılabilir mi?"""
        found = self._asymmetric()
        if not found:
            pytest.skip("asimetri kalmamış — `MEASURED_ASYMMETRIC` 0'a çekilebilir")
        rel, pointer, _ = found[0]
        cd = json.loads((ROOT / rel).read_text(encoding="utf-8"))
        vd = json.loads((WORKSPACE / dict(_pairs())[rel]).read_text(encoding="utf-8"))
        hedef = _node_at(cd, pointer) or {}
        ref = hedef.get("$ref", "")
        cozum = cd
        for part in ref[2:].split("/") if ref.startswith("#/") else []:
            cozum = cozum.get(part, {}) if isinstance(cozum, dict) else {}
        kset = set(cozum.get("properties", {})) if isinstance(cozum, dict) else set()
        vset = set((_node_at(vd, pointer) or {}).get("properties", {}))
        assert vset and vset < kset, (
            f"{rel} {pointer}: vendored artık kanoniğin DAR ALT KÜMESİ değil "
            f"(kanonik {sorted(kset)} · vendored {sorted(vset)}). Alt küme olmaktan "
            "çıktıysa bu düğüm ya `$ref`'e taşınmalı ya da politikası hizalanmalı — "
            "'kapatma' kararının dayanağı değişti."
        )


class TestGateActuallyCompares:
    """POZİTİF KONTROL — "sapma yok" çıktısı çoğu zaman kapının kendi körlüğüdür."""

    #: 2026-08-11 ÖLÇÜMÜ (tahmin DEĞİL): 18 çift · 48 ortak düğüm. İlk yazımda eşiği
    #: 50 diye **uydurmuştum** ve test kırmızı döndü — kapının kendisi değil, benim
    #: ölçmeden yazdığım sayı yanlıştı. Ratchet: sayı DÜŞERSE kapı körelmiştir.
    MEASURED_PAIRS = 18
    MEASURED_NODES = 48

    def test_it_compared_something(self, measurement) -> None:
        _, pairs_seen, nodes_compared = measurement
        assert pairs_seen >= self.MEASURED_PAIRS and nodes_compared >= self.MEASURED_NODES, (
            f"Karşılaştırma DÜŞTÜ: {pairs_seen} çift / {nodes_compared} ortak düğüm "
            f"(ölçülen taban: {self.MEASURED_PAIRS} / {self.MEASURED_NODES}). Ya vendored "
            "kopya düğüm attı, ya kanonik küçüldü, ya yürüyüş mantığı bozuldu — üçünde de "
            "kapı körleşir. Meşru şekilde arttıysa tabanı yükseltin (ratchet)."
        )

    def test_idiom_difference_is_not_a_divergence(self) -> None:
        """I-4: vendored `additionalProperties: false` ≡ kanonik `unevaluatedProperties: false`."""
        assert _policy({"type": "object", "unevaluatedProperties": False}) == _policy(
            {"type": "object", "additionalProperties": False}
        ), "İdiom farkı sapma sayılıyor — kapı her vendored dosyada yanlış alarm verir."

    def test_undeclared_is_distinguished_from_closed(self) -> None:
        assert _policy({"type": "object"}) == "BEYANSIZ"
        assert _policy({"type": "object", "additionalProperties": True}) == "AÇIK"
        assert _policy({"type": "object"}) != _policy({"type": "object", "additionalProperties": False})

    def test_union_typed_objects_are_seen(self) -> None:
        """`["object","null"]` — ilk ölçüm aracım bunları kaçırmıştı."""
        nodes = _object_nodes({"properties": {"x": {"type": ["object", "null"], "properties": {}}}})
        assert "$.properties.x" in nodes, f"birleşik tipli düğüm görülmedi: {list(nodes)}"

    def test_missing_vendored_node_is_not_a_divergence(self) -> None:
        """I-4 hakkı: vendored kopya düğüm ATLAYABİLİR."""
        canonical = _object_nodes({"properties": {"a": {"type": "object", "unevaluatedProperties": False}}})
        vendored = _object_nodes({"properties": {}})
        assert not (set(canonical) & set(vendored)), (
            "Yalnız kanonikte olan düğüm karşılaştırmaya girmemeli — girerse kapı meşru "
            "alt-küme atlamalarını sapma sayar ve gürültüye boğulur."
        )
