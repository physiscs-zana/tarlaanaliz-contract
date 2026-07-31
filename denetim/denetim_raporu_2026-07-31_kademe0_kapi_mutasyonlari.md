# KADEME 0 — KAPI MUTASYON KANITLARI (2026-07-31)

> ## 📐 BU DOSYA **KANIT ARŞİVİDİR — İŞ LİSTESİ DEĞİLDİR**
> Yapılacak işler **yalnız** `docs/TARLAANALIZ_EYLEM_PLANI_2026-07-30.md` §14'tedir.
> Bu dosya, KADEME 0'da kurulan/onarılan her kapının **gerçekten koruduğunun** ölçüm kaydıdır.

**Kapsam:** eylem planı §14.0 · D1–D6 + plan dışı D3-b
**Yöntem:** her kapı için ① kapının koruduğu şeyi **boz** ② kapının düştüğünü **göster**
③ **geri al** ④ yeşile döndüğünü göster. Mutasyon geri alma = **dosya yedeği**
(`git checkout` bir mutasyon aracı DEĞİLDİR — commit'lenmemiş çalışmayı siler).

**İlke:** *"Yeşil ama yalan bir kapı, kırmızı bir kapıdan tehlikelidir."*
Bir aracın çıktısı, aracın o değişiklik sınıfını **gördüğü ölçülene kadar** kanıt değildir.

---

## 0. Turun temel ölçümü (kapılar onarıldıktan SONRA)

| Ölçüm | Değer |
|---|---|
| `pytest tests/ -rs` | **735 passed · 2 xfailed (beyanlı) · 0 skipped** · RC=0 |
| `python tools/validate.py` | 89 dosya · 0 hata |
| `breaking_change_detector` (master…HEAD) | **breaking 0** · non-breaking 8 · documentation 11 · exit 0 |
| Turdaki breaking durumu | **beyan edilmemiş breaking YOK** — ve bu artık *ölçülmüş* bir sıfır |

Özyinelemeli dedektörün turda **ilk kez** gördüğü değişiklikler (eski sürüm bunların
hiçbirini raporlamıyordu):

```
$defs.PlatformForm.priority_zones          FIELD_ADDED_OPTIONAL   (C2′)
$defs.file_artifact.band                   FIELD_ADDED_OPTIONAL   (C1′)
$defs.file_artifact.layer_type             FIELD_ADDED_OPTIONAL   (C1′)
properties.escalation_reason  (+AUDIT_SAMPLE)  ENUM_VALUE_ADDED   (AL-C1)
```

---

## 1. D3 — dedektör körlüğü (SD1/SD2/Y5)

### 1.1 Denetimin mutasyonu birebir tekrarlandı

**Mutasyon:** `schemas/worker/expert_review_queue.v1.schema.json` →
`properties.escalation_reason.enum` içinden `QUARANTINE_CAUTION` silindi (= MAJOR breaking).

| | Eski dedektör (2026-07-31 denetimi) | Yeni dedektör (bu tur) |
|---|---|---|
| Sonuç | `Breaking Changes: 0` | `breaking=1` · exit **1** |
| Mesaj | — | `Enum value removed: QUARANTINE_CAUTION at properties.escalation_reason in worker\expert_review_queue.v1.schema.json` |
| CI kapısı | (adım `continue-on-error: true`) | **BEYAN EDİLMEMİŞ breaking → BUILD DÜŞER** |

**Kök neden (`dosya:satır`):** eski `compare_schemas` yalnız kök düzeyi okuyordu —
`enum` karşılaştırması `compare_enums(old_schema, new_schema, ...)` (eski satır 175, 226-254),
alan karşılaştırması `old_schema.get('properties', {})` (eski satır 91-95). `$defs`, `items`,
`oneOf/allOf/if-then` ve **iç içe her `enum`** görünmezdi.

### 1.2 Kapının kendisi mutasyona uğratıldı (ters yön)

Yeni regresyon süiti (`tests/test_breaking_detector_recursion.py`, 25 test) **eski dedektörle**
koşuldu:

```
21 failed, 4 passed, 2 errors      # eski (özyinelemesiz) sürüm
25 passed                          # yeni sürüm
```

⇒ Süit gerçekten özyinelemeyi ölçüyor; "yeni testler zaten yeşildi" değil.

### 1.3 Plan dışı üç ek körlük (aynı sınıf, bu turda tarandı)

| # | Bulgu | Kanıt | Düzeltme |
|---|---|---|---|
| a | **`x-context-subsets` görünmüyordu.** `enums/calibration_type.enum.v1.json` bağlam-bazlı **kabul listeleri** taşıyor (`edge/calibrated_dataset_manifest: ["ABSOLUTE","RELATIVE"]`). Şema `enum`'u değişmeden bir bağlamdan değer düşerse o bağlamın üreticileri kırılır | enum dosyasında `x-context-subsets` haritası; dedektör bu anahtara hiç bakmıyordu | Enum ekseniyle **aynı ağırlıkta** karşılaştırılıyor (`CONTEXT_SUBSET_VALUE_REMOVED` = BREAKING) |
| b | **Okunamayan şema sessizce yutuluyordu** — `load_schema` `except` → `{}` döndürüyordu; bozuk bir dosya "değişiklik yok" gibi görünürdü | eski `load_schema` (satır 54-61) | `load_errors` sayacı + **exit 2** (`kapı KÖR` ≠ `breaking yok`) |
| c | **Araç Windows'ta HİÇ koşmuyordu** — `🔍` emoji cp1254 konsolunda `UnicodeEncodeError` ile çöküyordu ⇒ SDLC_GATES §1C *"detector çalıştırıldı"* maddesi fiilen uygulanamazdı | yerel koşum: `'charmap' codec can't encode character '\U0001f50d'` | `validate.py`'deki kalıcı düzeltmenin aynısı: `sys.stdout/stderr.reconfigure(encoding="utf-8")` |

---

## 2. D3-b — CI'ın ikinci (denetimde görülmemiş) yalanı 🆕

**Bulgu:** dedektör ilerleme başlığını **stdout**'a basıyordu:

```python
print(f"🔍 Comparing contracts (schemas/ + enums/)...")   # eski satır 406-408
```

CI adımı ise aynı akışı dosyaya yönlendiriyordu:

```bash
python3 tools/breaking_change_detector.py --old ../old --new . --json > breaking_changes.json
if python3 -c "import json; exit(0 if json.load(open('breaking_changes.json'))['has_breaking'] else 1)"; then
  echo "has_breaking=true" >> $GITHUB_OUTPUT
else
  echo "has_breaking=false" >> $GITHUB_OUTPUT      # <-- JSON PATLAYINCA DA BURAYA DÜŞER
fi
```

**Zincir:** banner + JSON → geçersiz JSON → `json.load` **JSONDecodeError** → `python3 -c`
sıfırdan farklı çıkış → `if` **else** dalı → `has_breaking=false`.
⇒ `continue-on-error: true` hiç olmasaydı bile kapı **daima "breaking yok"** raporlardı.
Bu, denetimin bulduğu `continue-on-error` yalanından **bağımsız ikinci bir mekanizmadır**.

**Düzeltme:** banner `stderr`'e alındı · CI'ya *"JSON parse edilemiyorsa **FAIL**, asla
'breaking yok' değil"* adımı eklendi · regresyon: `test_cli_json_output_is_parseable`
(alt süreçte `json.loads(proc.stdout)`).

---

## 3. D5/D6 — "beklenen kırmızı" beyanı (Q1/Ç6/SD4/SD7)

**Tasarım:** tur içi bilinçli kırmızılar tek bir **makine-okunur beyana** bağlandı —
`CONTRACTS_VERSION.md` → `**Checksum State:** PENDING_REPIN`. Beyanı **üç kapı** okur
(`tests/release_state.py` tek kaynak):

1. CI `verify-checksums` işi → beyanlıysa uyarı + geç, **beyansızsa build düşer**
2. `test_real_repo_checksum_verifies` → `xfail(strict=True)`
3. `test_pending_propagation_is_empty` → `xfail(strict=True)`

**Kendini temizler:** `tools/pin_version.py` CONTRACTS_VERSION.md'yi baştan ürettiği için
C8 re-pin'inde beyan **kaybolur** → üç kapı aynı anda sertleşir.

**Mutasyon (beyan silindi = release modu):**

```
FAILED tests/test_pin_version.py::test_real_repo_checksum_verifies
FAILED tests/test_vendored_parity.py::test_pending_propagation_is_empty
2 failed, 66 passed          # beyan yokken GERÇEK kırmızı
66 passed, 2 xfailed         # beyan geri konunca
```

**Deselect denemesi:** `pytest -m "not release_gate"` → `pytest.UsageError`, **RC=4**.
Kırmızıyı gizleme yolu kapatıldı (SD4).

---

## 4. D4 — sessiz atlama (Q2/Q3/Q7)

**Kök neden:** CI bağımlılıkları workflow içinde **elle** yazılıydı
(`pip install jsonschema pytest pytest-cov`) ve `pyproject.toml` ile ayrışmıştı → `pyyaml`
yoktu → `tests/test_calibrated_manifest_fields.py` modül düzeyinde `pytest.skip("pyyaml yok")`
ile **18 testi sessizce** atlıyordu. Ayrıca `paths:` filtresi yeni testlerin okuduğu
kaynakları (`ssot/**`, `docs/**`, `drone_capability_matrix.yaml`) kapsamadığı için CI o
değişikliklerde hiç tetiklenmiyordu.

**Düzeltme:** tek bağımlılık kaynağı `requirements-dev.txt` (+`pyyaml`, +`pytest-cov`) ·
`paths:` filtresi testlerin **ölçülen** okuma yollarından türetildi · `pytest -rs` ·
**`tests/conftest.py` atlama kapısı**: beyan edilmemiş her skip gerekçesi oturumu düşürür.

**Mutasyon:** geçici bir test `pytest.skip("pyyaml yok")` ile eklendi →

```
SKIP BÜTÇESİ: 1 test atlandı
  [BEYAN EDİLMEMİŞ] 1x Skipped: pyyaml yok
ATLAMA KAPISI DÜŞTÜ — ...
RC=1
```

Silinince RC=0. ⇒ Q2'nin sınıfı bir daha sessizce yeşile dönemez.

**⛔ KAPANMAYAN KISIM (plan D4-b):** vendored parite süiti CI'da **hâlâ ölçüm yapmıyor** —
kardeş depolar (`tarlaanaliz-edge`, `tarlaanaliz-worker`) GitHub Actions'ta checkout
edilmiyor, 45 test *beyanlı* atlanıyor. Bu tur atlamayı **görünür** kıldı (CI iş özetinde
"PARİTE KAPISI ÇALIŞMADI" uyarısı) ve C8'de **yerel koşum**u zorunlu yaptı; ama Y3/AR4'ün
kökü duruyor ve **koordinatör kararı** gerektiriyor (CI'a çapraz-repo erişimi mi, yazılı
"yalnız C8'de yerel ölçüm" kabulü mü).

---

## 5. D2 — KR çıkarıcısı (Q6/Q5/AR3)

**Ölçüm (varsayım değil):**

| Kaynak | Gerçek tanım sayısı | Eski çıkarıcının gördüğü |
|---|---|---|
| `ssot/kr_registry.md` | **54** (48 × `### KR-NNN` + 6 × `## KR-NNN`) | **6** (%89 kör — Q6 doğrulandı) |
| `docs/TARLAANALIZ_SSOT_v1_2_0.txt` | **51** (49 × `## [KR-NNN]` + 1 × `## # [KR-033]` + 3 × `### KR-NNN`) | 51 − köşeli parantezsiz 3'ü (ör. `### KR-017`) |
| Birleşim / kesişim | **55 / 50** | — |

⇒ `CLAUDE.md`'nin *"registry 6 KR tutar, iki kaynak tamamlayıcıdır"* iddiası **yanlıştı**
(AR3 doğrulandı): iki kaynak büyük ölçüde **iç içe**. Yalnız `KR-034` SSOT-metni-özel;
yalnız `KR-088…KR-091` registry-özel. CLAUDE.md ölçülen sayılarla düzeltildi; *"aynı KR iki
yerde gövdeyle tanımlanamaz"* kararı **D16'ya** (KADEME 4) bırakıldı — o bir karar, rename değil.

**Q5 (boş kapı):** `test_data_layer_kr_present_in_ssot_text` yalnız `kr in text` diyordu.
KR-088/KR-091 SSOT metninde **tanımlı değil**; yalnız bir çapraz-atıf satırında geçiyor
(`- **[KR-088] / [KR-091]:** ...`, satır 787) → kapı o ikisi için **tamamen boştu**.
Artık **tanım başlığı** şartı var ve gövdenin hangi kaynakta olduğu ölçümle sabitlendi.

**Mutasyonlar:**

| Mutasyon | Beklenen | Sonuç |
|---|---|---|
| `## KR-093` → `### KR-093` (Q6 senaryosu) | yanlış alarm **olmamalı** | 16 passed ✅ |
| KR-093 başlığı **iki kaynaktan da** silindi | kapı **düşmeli** | 3 failed (dangling + iki hizalama testi) ✅ |
| çıkarıcı `^## ` biçimine daraltılırsa | eşik testi düşer | `MIN_REGISTRY_DEFINITIONS=50` eşiği bunu yakalar |

---

## 5.1 KADEME 1 mutasyonları (aynı oturum, D7/D8/D9)

| # | Mutasyon | Beklenen | Sonuç |
|---|---|---|---|
| K1-1 | `observed_footprint_wkt`'e UTM metre WKT (`POLYGON((500000 4000000, …))`) | RED | ✅ şema reddetti (G1 zincirinin şema tarafı kesildi) |
| K1-2 | EWKT (`SRID=4326;POLYGON(…)`) | RED | ✅ reddedildi (`shapely.wkt.loads`'u kıran biçim) |
| K1-3 | Mevcut edge fixture'ı (`POLYGON((32.0 37.0, …))`) + yüksek ondalık hassasiyet | KABUL | ✅ geçti — daraltma gerçek üretimi kırmıyor |
| K1-4 | `x-compat-accepted` beyanları silindi | 3 BREAKING | ✅ `PATTERN_TIGHTENED` + `MIN_MAX_TIGHTENED` + `ENUM_CONSTRAINT_ADDED`; beyan geri konunca 0 |
| K1-5 | Beyanla **alan silme / enum değeri silme / required genişletme / tip daraltma** indirilmeye çalışıldı | indirilmemeli | ✅ dördü de BREAKING kaldı (kaçış deliği yok) |
| K1-6 | Enum'a fail-open kuralı (`missing -> PANEL_ABSOLUTE`) geri kondu | RED | ✅ `test_missing_type_is_fail_closed_not_promoted` düştü |
| K1-7 | 4 bantlı `DJI_MAVIC_3M`'e `EVI` (BLUE ister) eklendi | RED | ✅ `test_listed_indices_are_producible` düştü |
| K1-8 | `IRRIGATION_EFFICIENCY` **değer olarak** enum'a geri kondu | RED | ✅ 3 test düştü; **açıklamadaki tarihsel not** ise yanlış alarm üretmedi |

**Ölçüm — bant gereksinimleri uydurulmadı.** `index_requirements` doğrudan worker'ın
çalışan kodundan türetildi (`tarlaanaliz-worker/src/core/services/inference/feature_extraction.py:207-222`):
`SAVI = ((NIR−R)/(NIR+R+L))(1+L)` → **Blue gerekmez** · `EVI = 2.5(NIR−R)/(NIR+6R−7.5B+1)`
→ kod `B` yoksa EVI'yi **sıfırlıyor** ⇒ Blue zorunlu. `CHLOROPHYLL_A` formülü depoda
**tanımsız** (worker'daki `LCI` aynı ad değil) → `null` bırakıldı, açık kalem yazıldı.

**Ölçüm — yeniden adlandırma bedava mı?** `IRRIGATION_EFFICIENCY` üç kardeş depoda
(`platform/src`, `worker/src`, `edge/src`) **hiç geçmiyor**; `layer_type` bu turda eklendi
⇒ üretici yok ⇒ MAJOR değil. Sonraki turda MAJOR olurdu.

---

## 6. Bu turda kapanmayanlar (plana işlendi, burada tekrar edilmez)

* **D4-b** — parite kapısının CI'da fiilen koşması (koordinatör kararı) → plan §14.0
* **SD8** — etiketsiz 16 tarihsel sürüm: retro-tag mı, kayıt notu mu (koordinatör kararı) → plan §14.6
* **D16/AR1/AR3** — aynı KR'nin iki yerde normatif gövdesi olması → plan §14.4
* **`$ref` çözümü** — dedektör `$ref` hedeflerini çözmez; `REF_CHANGED` görünür kılınır ama
  sınıflandırılmaz (bilinen sınır, araç docstring'inde ve SDLC_GATES §3E'de yazılı)

---

*Kanıt arşivi. Yapılacak işler: eylem planı §14.*
