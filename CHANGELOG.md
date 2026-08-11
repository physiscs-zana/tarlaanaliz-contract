# Changelog

All notable changes to `tarlaanaliz-contracts` will be documented in this file.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)  
Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

---

## [Unreleased] — Alan sızması (field drift) kapatıldı: dizi öğeleri ve iç içe nesneler

> **Sürüm önerisi: 7.7.0 (MINOR).** Re-pin + tag C8 töreninde; bu tur
> `CONTRACTS_VERSION.md → **Checksum State:** PENDING_REPIN` ile beyanlı.

### ÖLÇÜLEN SORUN (davranışsal kanıt, iddia değil)

`tools/validate.py` `unevaluatedProperties` kuralını yalnız **kök şemada** ve
**`$defs` birinci seviyesinde** zorluyordu. `schemas/` ağacındaki **310 object
düğümünün 79'u** o iki konumun dışındaydı ve **28'i hiçbir koruma taşımıyordu** —
yani dizi öğeleri (`items`) ve iç içe nesneler sözleşmede **tanımsız alanları
sessizce kabul ediyordu**. KR-073 AV tarama raporunda ölçüldü
(`datasets/scan_report.v1`, gerçek `Draft202012Validator` ile):

```
temiz belge                       -> 0 hata
kök'e tanımsız alan               -> 1 hata   (kapı çalışıyordu)
findings[]'e AYNI alan            -> 0 hata   (SESSİZCE GEÇİYORDU)
scanned_files[]'e AYNI alan       -> 0 hata   (SESSİZCE GEÇİYORDU)
```

Etkilenen düğümlerin çoğu **gözetim zinciri** (chain of custody, KR-072/073)
belgelerindeydi: `dataset_manifest.files[]` · `scan_report.scanned_files[]` /
`findings[]` · `verification_report.computed_hashes[]` / `mismatches[]` ·
`transfer_batch.datasets[]` · `qc_report.checks[]` · `evidence_bundle_ref.evidence_chain`.

İlk tarayıcı ayrıca `"type": ["object", "null"]` **birleşik tiplerini** kaçırmıştı
(7 düğüm daha) — ölçüm aracının kendi kusuru, düzeltildi.

### Changed — şemalar (19 dosya, 27 düğüm)

Sayım `origin/master` ile karşılaştırılarak ölçüldü (elle sayılmadı):
**beyansız düğüm 28 → 1** (kalan tek düğüm aşağıdaki parite-kilitli istisnadır).

- **23 düğüm KAPATILDI** (`unevaluatedProperties: false`).
- **4 düğüm BİLİNÇLİ AÇIK BEYAN EDİLDİ** (`additionalProperties: true` + gerekçe):
  `analysis_result.affected_zone` · `analysis_result.$defs.Detection.geometry` ·
  `dataset_analyzed.payload.results_summary` · `training_feedback.correction_geometry` —
  hepsi keyfi GeoJSON/serbest özet; kapatmak sözleşmeyi yanlış yerden daraltırdı.
  Doğru çözüm `shared/geojson.v1`'e bağlamaktır (üretici çıkınca).
- **`events/field_created.v1`**: `field.boundary` / `field.season` / `field.location`
  alan adları `core/field.v1`'in `$defs.GeoRef` / `SeasonRef` / `LocationInfo`
  tanımlarından **aynalandı** (12 opsiyonel alan beyanı). **DEĞER kısıtları
  (`minLength`, `required`, `const`, enum) BİLEREK aynalanmadı** — üretici ölçüldü:
  `tarlaanaliz-platform/src/core/domain/events/field_events.py:59-66,129` boş dize ve
  savunmacı `{}` üretebiliyor; kısıtları aynalamak canlı olayları kırardı.
  Bu tur **yalnız alan sızmasını** kapatır, kabulü daraltmaz.

### KIRICILIK — ölçüldü, dedektöre GÜVENİLMEDİ

`tools/breaking_change_detector.py --old origin/master --new . --json` →
`has_breaking = false`, 0 breaking, 12 non-breaking. **Ama bu yeşil, kırıcı-değilliğin
KANITI DEĞİLDİR:** dedektör `unevaluatedProperties`/`additionalProperties`'i yalnız
*alt-şema taşıyıcısı* olarak tanıyor (`SUBSCHEMA_SINGLE`, satır 116-120); bir düğümün
**açıktan kapalıya geçmesi** için sınıflandırma kuralı YOK — 27 kapatma **sıfır
değişiklik kaydı** üretti. Bu kör nokta ayrıca kayda geçirildi.

Kırıcılık bu yüzden **elle ölçüldü**:
- Dört depodaki **5385 JSON** dosyası tarandı; etkilenen düğümlerde **fazladan alan
  taşıyan tek bir yük bulunamadı** (pozitif kontrol: tarayıcı dikilmiş fazla alanı
  görüyor). Uyarı: 12 şema için hiç eşleşen yük yok — o düğümler için bu "kanıt yok",
  "temiz" değil.
- Canlı üreticiler kaynaktan okundu: `field.created` (platform) · `drone_metadata`
  (platform → worker) · `expert_feedback.tile_coordinates` (worker). Üçü de yalnız
  beyan edilen alanları yazıyor.

### GERİ ALINAN DEĞİŞİKLİK (kanıt öneriyi çürüttü)

`analysis_result.$defs.Detection.bbox` kapatılmak istendi, **geri alındı**: tüketicide
alan opak taşınıyor (`tarlaanaliz-worker/src/core/domain/analysis_result.py:29,249` →
`dict[str, float] | None`) ve anahtar kümesini kısıtlayan tek satır yok. Ayrıca
kapatma **I-4 parite çelişkisi** üretti (`test_vendored_parity` kırmızı döndü:
`_strip_annotations` iki idiomu tek anahtara indirgediği için kanonikte **herhangi bir**
politika anahtarı, vendored kopyada karşılığı yokken fark sayılıyor). Düğüm
`tools/validate.py → _PARITY_LOCKED_OPEN` içinde **tek girişlik, çıkış koşulu yazılı**
bir istisna olarak beyan edildi; `tests/test_object_drift_gate.py` listenin büyümesini
yasaklıyor.

### Added — kapı ve testler

- **`tools/validate.py`**: `_check_unevaluated_in_defs` → **`_check_object_policy`**.
  Kural: **her object düğümü politikasını BEYAN ETMELİ** — `unevaluatedProperties: false`
  (kapalı) ya da `additionalProperties` (bilinçli açık). Yasak olan **sessizlik**.
  Birleşik tipleri (`["object","null"]`) tanır; `examples`/`notes`/`x-` bloklarını
  taramaz (oralar şema değil veri). Kök daha SIKI kalır (kökte "açık" seçeneği yok).
- **`tests/test_object_drift_gate.py`** (14 test): kapsam · mutasyon (dizi öğesi ve
  birleşik tip körlüğü) · **pozitif kontrol** (meşru serbest düğümler açık kalmalı;
  annotation blokları taranmamalı) · istisna listesi ratchet'i · **davranışsal kanıt**
  (dizi öğesine sızma gerçek doğrulayıcıda REDDEDİLİR).
- Mutasyonla sınandı: gerçek şemadan (`scan_report.findings[]`) koruma kaldırılınca
  `validate.py` 1 hata verdi ve süitte 2 test kırmızıya döndü; desen tutmazsa betik
  durur (sahte yeşil yok).

### Changed — yayın ağacı

`dist/schemas/` yeniden üretildi (`python tools/inline_refs.py --write`, 68 dosya).
Kapı yayın ağacını da denetliyor: bayat `dist` ile `validate.py` **28 hata** verdi,
yeniden üretimden sonra **0**.

---

## `threat_type` kanonik sözlüğe BAĞLANDI + bağlama ratchet'i (KR-073)

### ÖLÇÜLEN SORUN

`enums/threat_type.enum.v1.json` 15 değerlik kanonik bir tehdit türü sözlüğü tanımlıyor;
`datasets/scan_report.v1` (KR-073 AV tarama raporu) ise aynı alanı `{"type": "string"}`
diye tanımlıyordu. Gerçek doğrulayıcıyla ölçüldü:
`findings[0].threat_type = "UYDURMA_TEHDIT_TURU"` → **0 hata**.

`edge/quarantine_event.v1` aynı alanda daha da inceydi: açıklaması kanonik enum'a
**atıf yapıyordu** ama şema hiçbir şeyi zorlamıyordu — deponun 2026-07-31'de `crop_type`
için adını koyduğu *"prose var, zorlanabilirlik yok"* sınıfının aynısı.

Sınıf ölçüldü (ad tabanlı tarama, `schemas/`): **21 bağlı · 22 inline · 12 serbest**.
Pozitif kontrol: aynı tarayıcı `crop_type`'ın bağlı olduğunu görüyor.

### Changed

- **`datasets/scan_report.v1` `findings[].threat_type`** → `$ref` kanonik enum.
  Ayrıca `threat_name`'e *"bilerek kısıtsız"* gerekçesi yazıldı (AV motorunun serbest
  imza adıdır; kanonik sözlüğü YOKTUR — ikisi karıştırılmasın).
- **`edge/quarantine_event.v1` `threat_type`** → `$ref` kanonik enum.

İkisine de `x-compat-accepted` beyanı yazıldı. ⚠️ **Bu beyan burada dedektörü
ETKİLEMEZ — düzeltme:** mekanizma yalnız `ACCEPTABLE_TYPES` içindeki 5 tipe uygulanır
(`MIN_MAX_TIGHTENED`, `PATTERN_TIGHTENED`, `ENUM_CONSTRAINT_ADDED`,
`COMPOSITION_BRANCH_CHANGED`, `FIELD_MADE_REQUIRED`) ve bu değişiklik `REF_CHANGED`
olarak sınıflanıyor. Dedektör `$ref`'i **çözmediğini** kendi belgeliyor (satır 53-55) ve
raporda *"NOT resolved by this tool — manual review required"* yazıyor; yani bu bir
**beyanlı sınır**, gizli bir kör nokta değil. İnsan kapısı SDLC_GATES §3E'dir.
Beyan yine de duruyor: üretici ölçümünü değişikliğin **yanında** tutar.

> Alternatif olarak enum'u satır içi yazmak dedektörü `ENUM_CONSTRAINT_ADDED`'a
> döndürürdü, ama bu deponun DRY kuralını çiğnerdi
> (`tests/test_inline_refs.py::test_source_still_uses_refs`) — `$ref` doğru seçim.

**Kırıcılık ölçümü:** kanonik 15 değerin **hiçbiri** platform/worker/edge Python kodunda
geçmiyor (pozitif kontrol: aynı tarayıcı `QUARANTINED` için edge'de 34 isabet buluyor);
edge'in `QuarantineEvent` modelinde `threat_type` alanı **hiç yok**; dört depodaki
5385 JSON içinde `scan_report.v1`'e uyan tek yük bulunamadı. Her iki şema da vendored
**parite çiftinde değil** → I-4 sonucu yok.

### 🔴 BAĞLANMADI — ölçüm bağlamayı ÇÜRÜTTÜ

**`edge/quarantine_event.v1` `decision`**: edge'in ürettiği sözlük kanonikle **SIFIR
KESİŞİMLİ**. Ölçüldü:

```
edge  (src/core/domain/quarantine_event.py:12-15) : PASS · QUARANTINE · REJECT
kanonik (enums/quarantine_decision.enum.v1.json)  : QUARANTINED · RELEASED · DELETED ·
    MANUAL_REVIEW_REQUIRED · PENDING_SCAN · SCAN_IN_PROGRESS · REJECTED ·
    CONDITIONALLY_RELEASED · ESCALATED
kesişim: ∅
```

Bağlamak edge çıktısının **%100'ünü** reddederdi. Bu bir araç değil **KARAR** sorunudur:
hangi sözlük kazanacak? (`crop_type`'ta 2026-07-31'de verilen *"dört depo AYNI standardı
kullanır"* kararının karantina eksenindeki karşılığı henüz verilmedi.) Gerekçe şemaya ve
ratchet baseline'ına yazıldı; **karar kullanıcıya bırakıldı**.

### Added — ratchet kapısı

**`tests/test_enum_binding_ratchet.py`** (8 test): adı kanonik bir enum ile eşleşen her
alanı tarar ve BAĞLI / INLINE / **SERBEST** diye ayırır. SERBEST kova yalnız **küçülür**:
baseline'da olmayan yeni serbest alan → kırmızı; baseline'da olup artık serbest olmayan
satır → kırmızı (bayat mazeret yasak). Baseline bugün **12 satır**, her biri
*"ölçülmemiş ya da bilinçli ertelenmiş"* demektir.

İki yönde mutasyonla sınandı:
- bağlı alanı serbest bırak → **3 test** kırmızı (tarayıcı · ratchet · davranışsal kanıt)
- baseline'daki alanı bağla → **1 test** kırmızı (bayat baseline)
- desen tutmazsa betik durur (`assert`) — sahte yeşil yok.

Ayrıca **pozitif kontrol**: `threat_name` serbest metin OLARAK KALMALI (bir sonraki tur
onu da enum'a bağlamaya kalkmasın diye kilitlendi).

⚠️ Bu kapı *"hepsini bağla"* demez — **görünür ve sayılabilir** kılar. Bağlamak
daraltmadır; her satır kendi üretici ölçümünü gerektirir.

---

## CI kapısının kendi dürüstlüğü: `paths:` filtresi + `summary.needs`

### ÖLÇÜLEN İKİ KUSUR — ikisi de daha önce bir kez kapatılmış sınıfın GERİ DÖNÜŞÜ

**① `summary.needs` listesinde `lint-openapi` YOKTU.** Bu, SD5'te `verify-checksums`
için kapatılan hatanın aynısı: iş kırmızı olsa bile özet kapısı onu görmüyordu, yani
OpenAPI lint'i düşen bir PR *"Validation Summary: pass"* gösteriyordu.

**② `paths:` filtresi 9 kök eksikti.** Q7'de *"filtre testlerin GERÇEKTEN okuduğu
yollardan türetildi"* denmişti; ama `tools/check_doc_links.py` (AL-K20, bir gün önce
eklendi) `git ls-files` üzerinden **tüm izli** `.md/.txt/.py/.yaml/.yml` dosyalarını
tarıyor ve filtre onunla birlikte genişletilmemişti. Ölçüm:

```
doc-link kapısının tarayacağı ama filtrede OLMAYAN kökler:
  .github/**  ·  .redocly.yaml  ·  .redocly.lint-ignore.yaml
  CLAUDE.md   ·  PATCH_NOTES.md ·  README.md
  denetim/**  ·  drone_registry.yaml
```

Yani bu köklerden birini değiştiren bir PR'da **workflow hiç koşmuyordu**.
Ayrıca `dist/**` de yoktu: yayın ağacı tüketicilerin vendor'ladığı biçimdir,
`validate.py` + `test_inline_refs` + `test_object_drift_gate` onu okur ve **yalnız
`dist/` dokunan gerçek bir commit var** (`d6de514`, 2026-08-07).

### Changed — `.github/workflows/contract_validation.yml`

- `paths:` **13 → 21 kök** (PR ve push blokları birebir aynı).
- `summary.needs`'e `lint-openapi` eklendi; özet çıktısına *"OpenAPI Lint"* satırı ve
  **düşürme koşuluna** `needs.lint-openapi.result == 'failure'` eklendi.
  (`needs`'e eklemek işi *bekletir*; koşula eklemek onu *zorunlu* kılar — ikisi ayrı
  şeydir ve yalnız ilkini yapmak kapıyı yine kör bırakırdı.)

### Added — `tests/test_ci_gate_honesty.py` (11 test)

Liste artık **ezberlenmiyor, TÜRETİLİYOR**: gereken kök kümesi her koşumda
`git ls-files` + `check_doc_links.SCANNED_SUFFIXES` (**tek kaynak** — ikinci kopya
tutulmuyor) + şema kapılarının ağaçlarından hesaplanıp filtreyle karşılaştırılıyor.
Yeni bir kapı eklenip filtre genişletilmezse test kırmızı döner.

Kapsanan değişmezler: her iş `summary.needs`'te · `needs`'teki her iş düşürme
koşulunda · **koşul `needs`'te olmayan işe atıf yapmıyor** · `needs` hayalet işe bağlı
değil · PR ve push filtreleri birebir aynı · filtre türetilen her kökü kapsıyor.

Dört yönde mutasyonla sınandı (desen tutmazsa betik durur):

| Mutasyon | Kırılan test |
|---|---|
| `lint-openapi`'yi `needs`'ten çıkar | **2** (kapsam + hayalet atıf) |
| yalnız düşürme koşulundan çıkar | 1 |
| filtreden `denetim/**` çıkar | 3 |
| PR/push filtrelerini ayrıştır | 2 |

**Kapının ilk getirisi:** `.github/workflows/**` yazmıştım, türetme `.github/**` istedi
ve testi kırmızıya çevirdi — kapı daha yazıldığı turda kendi yazarını denetledi.

---

## Vendored parite kapısı: kör nokta görünür kılındı + **hataya yol açan tavsiye** düzeltildi

Worker oturumu kapımın pointer-tabanlı karşılaştırmasında bir kör nokta bildirdi;
**ölçtüm ve haklı çıktılar** — üstelik daha ağır bir sorun ortaya çıktı.

**① Kör nokta (ölçüldü, tam 1 düğüm):** bir tarafta `$ref`, diğerinde INLINE olan aynı
mantıksal düğüm iki farklı pointer'da durur ve kesişime girmez:

```
schemas/worker/analysis_result.v1.schema.json → $.properties.summary
  kanonik : $ref → $defs.ResultSummary   (9 alan, KAPALI)
  vendored: INLINE                        (1 alan, BEYANSIZ)
```

**② Asıl sorun — kapının TAVSİYESİ hatalıydı.** Sapma raporu *"hizalayın: vendored'a
`additionalProperties` ekleyin"* diyordu. Bu düğümde o tavsiye **bug üretirdi**:
alan kümeleri ayrışık olduğu için kapatmak **8 meşru kanonik alanı** reddettirirdi
(`health_score`, `overall_health`, `index_averages`, …). Yani karşılaştırmaya
sokmamak **doğru davranış**tı — ama sessiz kalması değil.

### Changed

- Sapma mesajı artık alan kümelerini karşılaştırıyor; ayrışıksa
  **"🔴 KAPATMAYIN — aşırı kısıtlama olur, N meşru kanonik alan reddedilirdi"** diyor.
  (Worker'ın ölçtüğü kural: *vendored kopya dar alt kümeyse `additionalProperties:
  false` hizalama değil bug'dır.*)
- `_narrowing_warnings` yerel `$ref`'i **çözüyor**. Öz-denetim notu: ilk yazımda
  çözmüyordu ve uyarı *"kanonik 0 alan"* diyordu — gerçek **9**. Yanlış sayı taşıyan
  uyarı, uyarı değildir.

### Added — `TestRefInlineAsymmetryIsVisible` (2 test)

Asimetrik düğüm sayısı **kilitli** (ölçülen taban: 1) ve bilinen tek asimetrinin
**hâlâ dar alt küme** olduğu doğrulanıyor — alt küme olmaktan çıkarsa "kapatma"
kararının dayanağı düşer ve kapı kırmızıya döner.

**Mutasyon (iki yön):** kanonikte ikinci bir asimetri yarat → **3 kırmızı** ·
uyarı fonksiyonunu kör et → uyarı üretilmiyor. Pozitif kontrol: alan kümeleri eşit
olan düğümde uyarı **çıkmıyor**.

---

## ÖD-13 kapısı **AYNAYI** ölçüyordu — `main()` artık tek kaynağı kullanıyor

### ÖLÇÜLEN SORUN

`tools/validate.py → validation_targets()` docstring'i *"`main()` bu listeyi kullanır"*
diyordu. **Kullanmıyordu:** `main()` aynı dört ağacı kendi `rglob` döngüleriyle yeniden
geziyordu ve `tests/test_publication_tree_gates.py` yalnız `validation_targets()`'ı
okuyordu. Yani kapı, aracın **kopyasını** ölçüyordu.

Mutasyonla kanıtlandı (taze klon, `master`):

```
main()'den dist bloğu silindi
  ->  Total files validated: 165 -> 97      (68 yayın şeması denetlenmiyor)
  ->  ÖD-13 kapısı: 17 passed               ← YEŞİL KALDI
  ->  tüm süit    : yeşil
```

Kapı, koruduğunu iddia ettiği davranışı **hiç ölçmüyordu**.

### Changed — tek kaynak

- `validation_targets()` artık `List[Target]` döndürüyor: `(path, kind, label)`.
  `kind` → `_VALIDATORS` tablosuyla doğrulayıcıya eşlenir (`schema`/`enum`/`openapi`).
- `main()`'in dört `rglob` döngüsü **silindi**; yalnız `validation_targets()`'ı dolaşıyor.
- Davranış eşdeğerliği ölçüldü: **165 dosya**, dosya kümesi iki yönde de **sıfır fark**,
  çıktı etiketleri korundu (`(yayın ağacı)` 68 · `(PII scope)` 7).
- Bonus: `main()`'e eksik `-> None` anotasyonu eklendi (mypy'ın kendi önerisi).

### Added — ayna karşıtı testler

`TestMainActuallyUsesTheTargetList` (2 test): `validation_targets` monkeypatch'lenerek
`main()`'in **gerçekten** o listeyi dolaştığı ölçülür — tek hedef verilince
*"Total files validated: 1"*, boş liste verilince *"0"*.

`TestPublicationTreeIsValidated`'e 2 test daha: her hedefin `kind`'ı `_VALIDATORS`'ta
tanımlı · her ağaç **doğru** doğrulayıcıya yönleniyor (enum dosyası şema doğrulayıcısına
gitmemeli).

**Mutasyon (iki yön):**

| Mutasyon | Önce | Sonra |
|---|---|---|
| `validation_targets`'tan `dist` çıkar | — | **2 kırmızı** (165→97) |
| `main()`'i kendi döngüsüne döndür (ayna hatasını yeniden üret) | **yeşil kalıyordu** | **2 kırmızı** (165→68) |

### Öz-denetim: ayna karşıtı testin KENDİ kör noktası (aynı turda bulundu ve kapatıldı)

İlk yazımda `test_main_validates_exactly_the_declared_targets` monkeypatch'e **tek**
hedef veriyordu. Yayımlanan halde ölçtüm: `main()` listeyi `[:1]` diye **dilimlese bile
test yeşil kalıyordu** (21 passed). Yani "listeyi okuyor mu"yu ölçüyordum, **"hepsini
işliyor mu"yu değil** — ayna hatasının bir gömlek incelmiş hâli.

Düzeltildi: üç hedefle ölçülüyor, hem **sayı** (`Total files validated: 3`) hem
**kimlik** (üç dosya adı da çıktıda) doğrulanıyor. Üç daraltma mutasyonu da artık
kırmızı: `[:1]` · `[1:]` · `[::2]`; daraltma yokken yeşil (pozitif kontrol).

### Ölçüldü ama değiştirilmedi (dürüstlük)

`mypy tools/validate.py` → master'da **2**, şimdi **1**: eksik `-> None` düzeltildi,
geriye önceden de var olan tek kalem kaldı (`:104 unused "type: ignore"`).
`ruff` → dokunduğum iki dosyada **0/0**. CI ikisini de koşturmuyor (workflow'da 0 isabet),
yani bu iki araç burada tavsiye niteliğinde — **ölçüldü, kapı değil**.

> Öz-denetim notu: bu paragrafı önce *"master'da 2, şimdi 2"* diye yazmıştım; `-> None`
> eklendikten sonra yeniden ölçünce **1** çıktı. Sayıyı değil onu üreten komutu yazma
> kuralı burada da işe yaradı.

---

## Node/TS zinciri kaldırıldı — ölü değil **ZARARLI** bir komut vardı

### ÖLÇÜLEN SORUN

**① Hiç var olmamış bir TypeScript zinciri belgeleniyordu.** `package.json` 30 script
taşıyordu; 6'sı doğrudan var olmayan bir dosyaya işaret ediyordu
(`tools/validate.ts` · `generate-types.ts` · `generate-schema-index.ts` ·
`breaking-change-detector.ts` · `pin-version.ts` · `sync-to-repos.sh`).
**O dosyalar depoda HİÇ VAR OLMADI** — `git log --all -- <yol>` dördü için de **0 commit**;
`package.json` ilk commit'ten (2026-01-30) beri iskeleydi.

Geri kalanı ya bunlara zincirleniyordu (`ci:gate`, `build`, `prebuild`, `validate:*`)
ya da çalışacağı dosya yoktu: jest `tests/**/*.ts` arıyordu ama `tests/` **42 `.py` +
0 `.ts`**; eslint 0 `.ts/.js`; `prepare: husky install` ama `.husky/` yok.
`CLAUDE.md` bunları *"Full CI Gate (what runs in CI)"* başlığıyla belgeliyordu —
**CI `npm run ci:gate`'i hiç çağırmıyordu.**

**② `format` script'i ölü değil ZARARLIYDI.**

```
"format": "prettier --write \"**/*.{ts,js,json,yaml,yml,md}\""   +   .prettierignore YOK

npx prettier@3 --check "schemas/**/*.json" "enums/**/*.json" "api/**/*.yaml"
  -> "Code style issues found in 94 files"      (checksum kapsamındaki 97 dosyanın 94'ü)
```

Koşsaydı **üç değişmez aynı anda** kırılırdı: agrega checksum (`pin_version`;
kapsam `schemas/`+`enums/`+`api/`) · vendored bayt-paritesi · `dist/` tazeliği.

### Changed — `package.json` gerçeğe indirgendi

| | önce | sonra |
|---|---|---|
| script | 30 | **6** (`validate:brand` + `openapi:*`) |
| `dependencies` | `ajv`, `ajv-formats` | **0** |
| `devDependencies` | 16 | **1** (`@redocly/cli`) |
| lockfile paketi | 677 | **263** |
| `npm audit` | **38** açık (2 kritik · 21 yüksek) | **30** (2 kritik · 14 yüksek) |
| yapılandırma bloğu | `jest`, `prettier`, `eslintConfig`, `lint-staged` | **hiçbiri** |
| `repository`/`bugs`/`homepage` | `tarlaanaliz/tarlaanaliz-contracts` (yanlış hesap+ad) | `physiscs-zana/tarlaanaliz-contract` |

Kaldırılan paketlerin **hiçbirinin tüketicisi yoktu** (ölçüldü). `json-schema-to-typescript`
ve `typescript` yalnız `tools/generate_types.sh`'te geçiyor — o da **`npm install -g`**
ile global kuruyor, yani devDependency'ye bağlı değil (ve betiğin de çağıranı yok).
Kalan 30 açık `@redocly/cli` ağacından geliyor: **azaltıldı, sıfırlanmadı.**

### Added — `.prettierignore`

Script kaldırıldı ama **elle** `npx prettier --write .` koşan bir geliştiriciye karşı da
koruma gerekiyordu. Kanıt (geçici kaldırıp ölçüldü):

```
korumasız : 228 dosya değişirdi — bunlardan 162'si schemas/enums/api/dist
korumalı  :  64 dosya           — bunlardan   0'ı schemas/enums/api/dist
```

### Added — `tests/test_node_toolchain_honesty.py` (13 test)

Zorlananlar: her script'in dosya hedefi **var** · `npm run X` zinciri tanımlı bir
script'e gidiyor · hiçbir script depo genelinde biçimlendirme yapmıyor ·
`.prettierignore` dört sözleşme ağacını da kapsıyor · beyan edilen her bağımlılığın
**tüketicisi var** · çalışacağı dosyası olmayan araç yapılandırması (jest/eslint/
lint-staged) geri gelemiyor.

Beş yönde mutasyonla sınandı — **her biri tam 1 kırmızı**, taban 0:
ölü script ekle · zararlı `format`'ı geri getir · tüketicisiz bağımlılık ekle ·
jest yapılandırmasını geri getir · `.prettierignore`'dan `schemas/` çıkar.

### Changed — `CLAUDE.md` gerçeğe hizalandı

*Tech Stack* Node bölümü, *Development Commands*'ın 9 ölü `npm run …` satırı ve
*"Full CI Gate"* başlığı düzeltildi; yerine **CI'da gerçekten koşan 8 iş** yazıldı.
Dedektörün iki bilinen sınırı (`$ref` çözülmez · object politikası daralması
sınıflandırılmaz) komutun yanına not düşüldü.

⛔ **"Coverage threshold: 80%" iddiası da kaldırıldı:** o eşik jest'in `tools/**/*.ts`
yapılandırmasındaydı — depoda **0 `.ts`** var, yani eşik **hiç uygulanmadı**. Python
tarafında `--cov-fail-under` hiçbir yerde tanımlı değil (ölçüldü); gerçek kapsam `tools/`
için **%51**. Test tablosunun *"tam liste"* olmadığı da yazıldı (43 dosya).

---

## Vendored politika paritesi — **kendi öz-denetimimin bulduğu boşluk kapatıldı**

### NEDEN — bir kör noktayı kapatırken yerine ikincisini bırakmışım

Yukarıdaki tur kanonikte 27 düğüme sızma politikası ekledi. Öz-denetimde şunu ölçtüm:

```
tools/propagate_vendored.py --check  ->  "Bekleyen yayılım YOK" (exit 0)
tests/test_vendored_parity.py        ->  185 passed
elle ölçüm                           ->  5 SAPMA (kanonik kapalı, vendored beyansız)
```

Sebep ikisinin de kapsamı: `propagate_vendored` yalnız **enum değeri** ve **opsiyonel
alan** yayılımını ölçer; parite süiti ise ortak `$defs` **alanlarının** alt şemalarını
karşılaştırır, `$.properties.*` altındaki iç içe düğümlerin **politika anahtarına**
bakmaz. Sapmayı bulup **plana yazmıştım** — ama plan kalemi kapı değildir; kendi
standardımla *"belgelenmiş ama uygulanmayan kural bir dilektir."*

Bu, worker için kozmetik değil: worker'ın **gelen doğrulaması bloklayıcıdır** (şema
tutmazsa `REJECTED`), yani iki taraf farklı şeyi kabul ediyordu.

### Added — `tests/test_vendored_policy_parity.py` (8 test)

Parite çiftlerinde (**tek kaynak:** `test_vendored_parity.MIRROR_PAIRS`/`SUBSET_PAIRS`)
**iki tarafta da var olan** her object düğümünün politikasını karşılaştırır.
I-4 idiomu normalize edilir: `unevaluatedProperties: false` ≡ `additionalProperties:
false` → KAPALI. **`DÜĞÜM YOK` sapma değildir** — vendored kopyanın alt küme hakkı.

Ratchet iki yönde: yeni sapma → kırmızı · bayat baseline satırı → kırmızı.

**Baseline 3 satır** — üçü de `analysis_result.v1`'de (`index_maps`, `model_metadata`,
`thermal_results`) ve **bu turdan ÖNCE de vardı**; benim değişikliğim üretmedi.
İlk ölçtüğüm 5 sapma **worker oturumu tarafından bu tur içinde hizalandı** (ölçüldü),
o yüzden baseline'a girmedi.

Üç yönde mutasyonla sınandı: vendored'da hizalı düğümü gevşet → *yeni sapma* kırmızı ·
baseline'dakini hizala → *bayat baseline* kırmızı · karşılaştırma mantığını boz →
*sayaç kilidi* kırmızı.

⚠️ **Kapı kardeş depo checkout'u ister** (D4-b): kardeş yoksa 3 test **beyanlı** atlanır
(`tests/conftest.py::ALLOWED_SKIP_REASONS` kapsamı bilinçli olarak genişletildi),
5 saf test yine koşar. Ölçüldü: kardeşli 1345 passed · kardeşsiz 1176 passed +
169 beyanlı atlama, **beyansız atlama YOK**.

> Öz-denetim notu: pozitif kontrolün eşiğini önce **ölçmeden 50 diye yazdım**, test
> kırmızı döndü ve gerçek sayının 48 olduğunu gösterdi. Sayı artık ölçülen değere
> sabit (`MEASURED_PAIRS=18`, `MEASURED_NODES=48`) ve ratchet olarak korunuyor.

---

> ⚠️ Bu tur `paths:` filtresi **kaldırılmadı**. Kaldırmak en dürüst seçenek olurdu
> (her filtre bir fail-open yüzeyidir) ama bu deponun CI geçmişinde **fatura limiti**
> kaynaklı kırmızılar var; filtreyi silmek koşum sayısını artırır. Bunun yerine filtre
> **ölçülen kümeye** genişletildi ve **kapıya bağlandı**. Kaldırma kararı sahibinindir.

---

## [7.6.1] - 2026-08-11 — D12: `stress_ratio` TANIMLANDI + ön faz kapalı listesi KAPIYA bağlandı

> ⛔ **Bu sürüm kendi önceki iddiasını çürütüyor.** v1.4.2–v1.4.3 `analysis_type.enum`
> içinde *"`stress_ratio`: ad var, üretim yok — hiçbir üretici bu adı emit ETMEMELİDİR"*
> yazıyordu. Ölçüm (2026-08-11) bunun **yanlış** olduğunu gösterdi: iddia tek bir dosyaya
> (`feature_extraction.compute_indices_v2`) bakıp "yok" demişti; üretici worker'ın çıkarım
> hattındadır ve çıktı nesne deposuna yüklenip `manifest.json`'da listelenir.

### Changed (PATCH — metadata/açıklama; enum değerleri ve `byLayer` DEĞİŞMEDİ)

- **`enums/analysis_type.enum.v1.json` (metadata v1.4.3 → v1.4.4)** —
  `indexDefinitions.stress_ratio`: `UNDEFINED_PENDING_DECISION` → **`DEFINED`**.
  - `formula`: **`stress_ratio = NDRE / NDVI`** (uygulama okunarak ölçüldü, tahmin değil).
  - `domain_guard` artık **makine-okunur**: `valid_where = "NDVI > 0"`,
    `outside_value = 1.0` (bitki örtüsü olmayan piksellerde nötr — bir ölçüm değil,
    ölçüm YOKLUĞU işareti).
  - `measured_producers`: 7 üretici yol `dosya:satır` ile yazıldı.
  - `delivery_rule` **yeni ve makine-okunur**: `preliminary = false`,
    `feeds_layer = "WATER_STRESS"`. **Teslimat kuralı DEĞİŞMEDİ** — katman `proxy_only`
    olduğu için uzman kapısı öncesinde çiftçiye sunulmaz. *Tanımlılık ≠ geçerlilik:*
    formülün yazılı olması onu doğrulanmış bir su-stresi ölçümü yapmaz.
  - `superseded_claim`: çürütülen metin, neden yanlış olduğu ve dersi kayıtta tutulur.
- **`enums/report_phase.enum.v1.json`** — `PRELIMINARY` açıklamasındaki *"kaynağı
  `stress_ratio` TANIMSIZDIR"* ifadesi düzeltildi; `x-removed-2026-07-31` bloğuna
  `x-enforcement-2026-08-11` eklendi. `stage_b_post_analysis.fields` **DEĞİŞMEDİ**.
- **`docs/TARLAANALIZ_SSOT_v1_2_0.txt`** (KR-093 Aşama B satırı) — aynı düzeltme; metin
  ile makine-okunur liste aynı commit'te hizalandı (AR1 dersi).

### Gate (yeni — belgelenen kural artık uygulanıyor)

- `tests/test_single_normative_body.py` → `TestDerivedQuantitiesAreDefined`:
  `delivery_rule.preliminary` ile `report_phase` → `x-preliminary-content.
  stage_b_post_analysis.fields` **makine düzeyinde anlaşmak zorunda**; `proxy_only` bir
  katmanı besleyen indeks ön fazda teslim edilemez. Eski kapı yalnız "beyan alanı dolu mu"
  diye bakıyordu ve **içeriği yanlış** bir beyanı sorunsuz geçirmişti — D12'nin kök nedeni
  buydu. Yeni kapı 9 mutasyonla sınandı (bayrağı çevirmek, katmanı listeye eklemek,
  formülü ters çevirmek, nötr değeri 0.0 yapmak, satır numarasını silmek → hepsi kırmızı).
  ⚠️ Kapının sınırı: contract deposu worker **KODUNA** bakamaz — `outside_value = 1.0`
  literali kanonik metni sessiz düzenlemeye karşı korur, worker'ın Python sabiti
  değişirse fark etmez. Bu yüzden `stress_ratio.py` başına "kanonik girdiyi aynı turda
  güncelle" uyarısı yazıldı.
- **`tests/test_vendored_parity.py` → `TestVendoredMetadataDoesNotContradict` (YENİ).**
  ⛔ Bu turun ilk yazımında *"çapraz-repo kapı YOK"* demiştim — **ifade fazla genişti ve
  öz-denetimde düzeltildi.** Ölçüm: kardeş-CI parite kapısı VARDI ama `metadata`
  değerlerine **kördü**. Üç mutasyon (worker'da `proxy_only`→`available`,
  `NDRE/NDVI`→`NDVI/NDRE`, `1.4.4`→`1.4.1`) **169 passed** ile hayatta kaldı; yani
  D12'de elle kapattığım ayrışmanın geri kaymasını engelleyen hiçbir şey yoktu.
  Yeni kapı: vendored `metadata`, iki tarafta da bulunan bir yolda kanonikle
  **ÇELİŞEMEZ** (I-4 gereği EKSİK tutabilir). 142 paylaşılan yaprak denetleniyor;
  serbest-metin anahtarları ölçülerek dışlandı (6 ad + `availabilityValues` alt ağacı)
  ve `availability`/`formula`/`preliminary` gibi anlamsal alanların istisnaya kaçmasını
  yasaklayan ayrı bir pozitif kontrol var. 6 mutasyonla sınandı; ayrıca kapının kendi
  sayaç kilidi de mutasyonla sınandı — ilk hâli körlüğü `skip` ile örtüyordu, düzeltildi.
- **Tüketici tarafı:** `tarlaanaliz-platform/src/application/services/
  preliminary_content_gate.py` bu kapalı listeyi **okur** (kopyalamaz) ve çiftçi yolunda
  hem katman/indeks listesini hem raster tile ucunu kısıtlar. Ölçüldü: bu kapıdan önce
  `WATER_STRESS` ön fazda fiilen sunulabiliyordu.

---

## [7.6.0] - 2026-08-07 — INGEST UCU: kalibre manifest kabulü (DK-28/DK-29 son halka)

### Added

- **`api/platform_internal.v1.yaml`** → yeni uç
  **`POST /intake/datasets/{dataset_id}/calibrated-manifest`**.
  Edge (M2) kalibrasyon tamamlandıktan sonra kalibre paket manifestini gönderir;
  platform `outputs[]` içinden adresleri çıkarır:
  - `layer_type == "ORTHO"` → **`datasets.rgb_ortho_uri`** (KR-017 "Gerçek Görünüm"
    taban görüntüsü — **DK-28**'in son halkası),
  - aynı giriş, manifest **ayrı bant rasteri beyan etmiyorsa**
    **`datasets.calibrated_ortho_uri`** (**DK-29**: worker'ın analiz edeceği çok-bantlı
    yığın). Bant girişi varsa (ör. DJI Terra `result_*.tif`) ORTHO **RGB-only**'dir ve
    analiz kaynağı olarak yazılmaz — fail-closed, sessiz-yanlış yerine boş bırakılır.
- **`api/components/schemas.yaml`** → `CalibratedDatasetManifest` (kanonik şemaya `$ref`,
  kopya değil).

### Neden MINOR

`docs/versioning_policy.md:153,163` — *"Yeni endpoint ekleme → Breaking? ❌ Hayır"*,
*"✅ Yeni OpenAPI endpoint ekleme"* MINOR listesinde. Mevcut hiçbir uç/şema değişmedi.

### Fail-closed kuralı (uçta zorunlu)

`uri` **adreslenebilir** olmalıdır (`s3://` | `https://`). **Yerel dosya yolu REDDEDİLİR** —
platform M1'in `C:/…` yolunu okuyamaz. Bu kural 2026-08-07 öz-denetiminde ölçülen gerçek
boşluktan doğdu: edge yazıcısı manifeste yerel yol yazıyordu.

---

## [7.5.0] - 2026-08-07 — CONTRACT TUR 3 (motor-agnostik kalibrasyon KAPANDI)

> ✅ **TUR 3 KAPANDI.** `7.4.0`'ın `PENDING_REPIN` beyanı tam olarak bu turu bekliyordu
> (*"TUR 3 açık — motor-agnostik kalibrasyon"*); `tools/pin_version.py --minor` dosyayı
> baştan üretince beyan kendini sildi ve üç kapı birden sertleşti.
>
> **Kapsam DAR ve ÖLÇÜLDÜ:** `v7.4.0..master` arasında 59 commit var ama **sözleşme
> artefaktı olarak yalnız 3 dosya** değişti (`git diff --stat v7.4.0..master -- schemas/
> enums/ api/`). Üçü de **additive** → MINOR, `Breaking Change: NO`.

### Added

- **`enums/radiometric_mode.enum.v1.json`** → yeni değer **`SENSOR_CORRECTED`**
  (sensör/kamera modeli düzeltmeleri uygulandı, ışınım normalizasyonu YOK).
  `tools/breaking_change_detector.py` doğruladı: *"Non-Breaking Changes — Enum value
  added"*.
- **`enums/radiometric_mode.enum.v1.json`** → **`x-ladder`**: eksen bayrak KÜMESİ değil
  **monoton merdiven** (`RAW_DN < SENSOR_CORRECTED < SUN_IRRADIANCE < PANEL`). Yeni
  düzeltme aşaması çıkarsa kendi basamağı eklenir; kombinasyon başına değer eklenmez
  (n aşama → n değer, 2ⁿ değil). Tüketici kuralı: değer ADINA göre `if/elif` değil,
  `order` içindeki İNDEKS ile karşılaştır.
- **`enums/radiometric_mode.enum.v1.json`** → **`x-provenance-axis`**: bu eksen "NE
  yapıldı"yı söyler, "KİM yaptı"yı DEĞİL. Kim bilgisi `calibration_method` ekseninde
  (`FACTORY_RADIOMETRIC` / `FACTORY_RADIOMETRIC_ILS` dahil). **Gerekçe:** kameralar
  radyometrik düzeltmeyi kendi yapmaya başlarsa motor bayrağı `none` olsa bile veri ham
  DN DEĞİLDİR; bu ayrım olmadan otomatik kalibre eden bir kamera
  `RAW_DN → NONE → KR-018 sert red` ile GERÇEKTEN KALİBRE veriyi reddettirirdi.
- **`enums/calibration_type.enum.v1.json`** → türetme tablosuna iki göz
  (`relative|SENSOR_CORRECTED` ve `absolute|SENSOR_CORRECTED` → **`RELATIVE`**) +
  **`x-never-upgrade-rule`**: `radiometric_mode` sensör sınıfını ASLA YÜKSELTMEZ,
  gerekirse DÜŞÜRÜR. Kural yeni değil — `absolute|RAW_DN → NONE` tabloda zaten vardı.
  E13-R'nin `map.absolute.allowed` kümesi `RELATIVE` ile **tamamlandı** (değiştirilmedi):
  o küme yazıldığında merdivende `SUN_IRRADIANCE`'ın altında basamak YOKTU.
- **`schemas/edge/calibrated_dataset_manifest.v1.schema.json`** → **opsiyonel `outputs[]`**
  (`$defs.file_artifact` + bağımlı `$defs.uri` / `$defs.sha256`). **DK-28:** RGB
  ortomozaiğin adresi edge'den platforma HİÇBİR YOLDAN geçmiyordu; taban görüntü girişi
  `layer_type: "ORTHO"` taşır ve platform onu `datasets.rgb_ortho_uri`'ye yazar.
  Edge'de **opsiyonel**, platform formunda **zorunlu** — fark bilerektir ve
  `tests/test_file_artifact_parity.py` ile kilitlidir.

### Changed (normatif metin)

- **`docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `[KR-034]`**: desteklenen motorlar
  Pix4Dfields + DJI Terra + **OpenDroneMap (ODM)**. *"İkisinin de yerel CLI'ı yoktur"*
  mutlağı olguyla çeliştiği için daraltıldı — **ODM'nin CLI'ı VARDIR** (2026-08-06'da
  ölçüldü: ODM 3.6.1, aynı 670 fotoğrafla üç kol, kol başına ~14 dk, panelsiz, GPU
  gerekmedi). Edge'in okuma sözleşmesi DEĞİŞMEDİ: her motor için tek yol yine
  `engine_adapter` ile çıktı dizinini okumak.

### Consumer etkisi

| Depo | Etki |
|---|---|
| **edge** | `outputs[]` vendor'landı → edge SemVer `1.5.0` → `1.6.0` (MINOR) + hash bloğu yeniden üretilir. `OpenDroneMapAdapter` + `CalibratedManifestWriter` bu sürüme dayanır. |
| **platform** | Submodule pini `v7.5.0`'a alınır (I-3). `datasets.rgb_ortho_uri` kolonu hazır (PR #394). |
| **worker** | Bu turda değişen 3 dosyanın hiçbiri worker'ın 8 izli dosyasında DEĞİL → etki yok. |

---

## [7.4.0] - 2026-08-01 — CONTRACT TUR 2 (C8 ile kapatıldı)

> ✅ **TUR 2 KAPANDI.** `PENDING_REPIN` beyanı kalktı, agrega checksum yeniden pinlendi
> (`c7b8d46e…`), `PENDING_PROPAGATION` **boşaltıldı** (edge + worker vendored kopyalar
> senkronlandı) ve üç OpenAPI spec'inin `info.version`'ı **7.4.0**'a hizalandı (SD9).
>
> 🔴 **Tören sırasında release aracının kendisinde bir hata bulundu ve düzeltildi:**
> `pin_version.py` agrega checksum'ı yazdıktan **sonra** `api/*.yaml`'ı senkronluyordu;
> o dosyalar checksum kümesinin **içinde** olduğu için pin doğduğu anda bayat oluyordu
> (`--verify` hemen kırmızı verdi). v7.3.0 turunda görünmemişti çünkü `info.version` o tur
> `1.0.0`'da kalmış, senkron hiçbir baytı değiştirmemişti. Sıra düzeltildi
> (senkron → hash → yaz) ve regresyon kapısı yazıldı
> (`test_pin_version_selfverifies_when_openapi_sync_changes_bytes`, mutasyonla doğrulandı).

### C6b/S2 · S4 · S6 · S7 — E13 ile engeli kalkan dört kalem (hepsi MINOR)

**C6b/S2 — kalibrasyon alt-küme bileşimi.** `edge/calibrated_dataset_manifest` alt-kümesi
`[ABSOLUTE, RELATIVE]` idi; `edge/intake_manifest` ise dört değer kabul ediyordu. Yani bir
paket intake'te `PANEL_ABSOLUTE` bildirip **aynı istasyonun ikinci belgesinde** aynı değeri
yazamıyordu. `PANEL_ABSOLUTE` eklendi (üretici yok — ölçüldü: edge/src'de yalnız yorumlarda
geçiyor). **İki değer bilerek dışarıda, gerekçeleri farklı:** `NONE` (edge kalibrasyon
başarısızsa manifest hiç üretmez — D8) · `DLS2_RELATIVE` (**E13 kararı** onu kalibre paket
yüzeyinden reddetti).

> 🔴 İlk denemede alt-küme intake ile **tam** hizalandı ve `tests/test_calibration_type_axis.py`
> bunu kırmızıya çevirdi — aynı gün verilen iki kararın (C6b ve E13) çelişmesini kapı
> engelledi. Hizalama kısmi yapıldı; kalan tutarsızlık **S3**'e (MAJOR) bağlı ve yazılı.

**S4 — kalibrasyon mekanizması worker'ın gördüğü yola.** `calibration_method` alanı
platform/edge/datasets/events şemalarında **vardı** ama worker'ın yüzeyinde **yoktu** — S5 ile
birebir aynı desen. `worker/calibration_metadata.v1`'e eklendi; sözlük
`datasets/calibration_certificate.v1` ve `edge/calibration_result.v1` ile aynı
(`REFLECTANCE_PANEL` / `DLS_IRRADIANCE` / `EMPIRICAL_LINE`). Worker artık `ABSOLUTE` ile
`PANEL_ABSOLUTE`'u ayırt etmenin ötesinde *hangi mekanizmayla* kalibre edildiğini de görebilir
(K-3 fine-tuning uygunluğunu **doğrulanabilir** kılar).

**S6 — çıktı başına reflektans ölçeği.** `outputs[]` heterojendir (DSM metre · CWSI birimsiz ·
8-bit ORTHO) ve tek bir paket-düzeyi ölçek hepsini tarif edemez. `$defs.file_artifact`'a
opsiyonel `reflectance_scale` eklendi; paket düzeyindeki alan artık **varsayılan** olarak
tanımlı ve çıktı-düzeyi onu ezer.

**S7 — RGB kompozit kare (YARIM çözüldü, kalanı MAJOR).** `raw_frames[].band` enum'una `RGB`
eklendi: kompozit kare artık **açıkça** işaretlenebilir. Önceden bunu ifade etmenin tek yolu
alanı boş bırakmaktı ve bu, yokluğun **iki ayrı şeyi** kodlaması demekti (RGB kompozit /
bant bilinmiyor).

> 🔴 **Kalan yarım — S7-b:** alan hâlâ opsiyonel, yani yokluk hâlâ belirsiz. Zorunlu kılmak
> `FIELD_MADE_REQUIRED` = **MAJOR** ve bu tur MINOR. Üstelik **ölçüldü**:
> `tools/breaking_change_detector.py` `x-compat-accepted` beyanını kısıt daraltmalarında
> (pattern/maxLength/enum) tanıyor ama `FIELD_MADE_REQUIRED` yolunda **hiç kontrol etmiyor**
> (satır 615-630) — "üretici yok, ölçüldü" gerekçesi bu tipte beyanla geçirilemiyor. Dedektör
> tutarsızlığı **AK-11** olarak plana yazıldı.

⚠️ `RGB` kanonik `available_bands` sözlüğüne **sızdırılmadı**: bir kare TÜRÜDÜR, spektral bant
değildir. Oraya girseydi KR-018 bant kapısı 4-bant minimumunu RGB ile sağlanmış sanabilirdi.
Kapı: `test_calibrated_manifest_fields.py::test_raw_frame_band_matches_canonical`.

### S5 — reflektans ölçeği worker sözleşmesine eklendi (`worker/calibration_metadata.v1`)

**Tip:** MINOR (opsiyonel `scale` bloğu; `required` değişmedi).

**Sorun (ölçüldü):** reflektans ölçeği bugüne kadar **yalnız platform** şemalarındaydı
(`platform/calibration_result.v1` → `scale`, `platform/calibrated_dataset_manifest.v1`).
Worker'ın vendor'ladığı **8 sözleşmenin** ve kanonik `schemas/worker/*` şemalarının
**hiçbirinde** yoktu. Sonuç: worker ölçeği **tüm filo için tek bir global ortam
değişkeninden** okuyor (`src/shared/config.py:236` → `reflectance_scale = 10000.0`).
Worker kodu bunu zaten biliyor ve düzeltmeyi kendisi tarif ediyor: *"The canonical fix is a
per-job scale field in the calibration contract"* (`config.py:230-234`) ·
*"Kalıcı çözüm: per-job reflectance_scale'i calibration_metadata sözleşmesine ekleyip
okumak"* (`pipeline.py:2358`).

**Neden sessiz bir hata sınıfı:** NDVI = (NIR−Red)/(NIR+Red) bir **orandır** → ölçekten
bağımsızdır ve yanlış ölçekte bile makul görünür. EVI'nin `− 7.5·Blue + 1.0` ve SAVI'nin
`+ L` **toplama sabitleri** ise reflektansın 0–1 aralığında olduğunu varsayar. Ölçek
uyuşmazsa bu iki indeks sessizce bozulur **ve NDVI'nin doğru görünmesi hatayı maskeler.**

### Added

- **`schemas/worker/calibration_metadata.v1.schema.json`:** opsiyonel `scale` bloğu —
  `reflectance_scale` (enum: `reflectance_0_1|reflectance_0_100|scaled_int|unknown`) +
  `scale_factor` (number, `exclusiveMinimum: 0`). Alan adları ve enum değerleri
  `platform/calibration_result.v1` → `scale` ile **birebir aynıdır** (dört depo tek standart;
  yeni ad icat edilmedi). Blok içinde `reflectance_scale` zorunlu; `scaled_int` seçilmişse
  `allOf`/`if-then` ile **`scale_factor` de zorunlu** — "ölçekli tamsayı" deyip neye
  böleceğini söylememek S5'in doğduğu boşluğun ta kendisiydi.
- **`x-normalization.scale.missing`:** eksik ölçek davranışı **yazılı** — `DECLARED_FALLBACK`.
  Burada bilerek FAIL-CLOSED yapılmadı (`calibration_type`'ın aksine): `scale` bugün hiçbir
  üretici tarafından yazılmıyor, sert kapı tüm filoyu anında durdururdu. Sapma **geçicidir**
  (I-5) — üretici (E14 `calibration_result_writer`) alanı yazmaya başladığında politika
  `FAIL_CLOSED`'a çevrilir. Bugünkü tek savunma worker'ın doyum alarmıdır
  (`pipeline.py:2364`, `event_type=radiometric_scale_mismatch`) — bir kapı değil, alarmdır.

### Gates

- **YENİ:** `tests/test_reflectance_scale_contract.py` (11 test) — ölçek sözlüğünün platform
  ↔ worker ↔ manifest arasında ayrışmasını yasaklar, `scaled_int`'in bölensiz kalmasını
  reddeder, eksik-ölçek beyanının silinmesini ve "NDVI maskeler" notunun kaybolmasını
  kırmızıya çevirir. **5/5 mutasyon** doğrulandı.
- `PENDING_PROPAGATION`'a `calibration_metadata.v1` beyanı eklendi: kanonik ileri gitti,
  worker vendored kopyası henüz almadı. ⚠️ Yayılım worker'ın **okuma kodu** hazır olmadan
  yapılırsa alan ölü taşınır → bir sonraki C8'e bırakıldı, sessizce değil **beyanla**.
  Worker'ın okuma yarısı ayrı kalem: **W12**.

### SD9 + SD10 — OpenAPI yüzeyi: donmuş sürüm dizesi + **hiçbir kural koşmayan** lint kapısı

**SD9 (karar, koordinatör onaylı):** üç spec'in `info.version`'ı **set sürümünü izliyor**
(`1.0.0` → `7.3.0`). Dayanak ölçüldü: OpenAPI 3.1 alanı *"the version of the OpenAPI
**Document**"* diye tanımlıyor ve bu depoda belge **set** olarak yayımlanıyor (I-1);
"API MAJOR hattı" savunması düştü (hat zaten `servers.url` `…/v1` + dosya adında);
alanı okuyan tüketici **yok** (dört depoda 0 eşleşme). Alan **elle yazılmaz** —
`tools/pin_version.py → sync_openapi_versions()` C8'de yazar, kapı ölçer.

**SD10 (kapı yalanı):** `Lint OpenAPI Specs` adımı **hiçbir kural koşmuyordu** ve daima
"pass" gösteriyordu — `spectral lint` **ruleset'siz** çağrılıyordu (*"No ruleset has been
found"*), üstüne `|| echo` ve `continue-on-error: true`. Kurallar koşturulunca **25 hata +
63 uyarı** çıktı ve **üçü gerçek kusurdu**:

| Kusur | Etkisi |
|---|---|
| `api/components/responses.yaml` → `nullable: true` | **OAS 3.0** anahtarı; 3.1'de kaldırıldı → sessizce yok sayılıyordu, istemci `next_cursor`'ı **zorunlu string** sanıyordu |
| `api/edge_local.v1.yaml` → `/batches/{batch_id}/scan` | yol parametresi **hiç tanımlı değildi** → üretilen istemci imzası parametresiz kalır |
| `api/platform_public.v1.yaml` ödeme uçları | **var olmayan** `PaymentIntent` bileşenine iki **sarkan `$ref`** (KR-033) |

#### Changed
- CI adımı **redocly**'ye çevrildi (spectral bu ağaçta `spectral:oas` ile **çöküyor**:
  *"Cannot read properties of null (reading 'enum')"* — kanonik JSON Şemalara giden göreli
  `$ref` zincirini çözemiyor). Susturucular **kaldırıldı**.
- `.redocly.yaml` — yapısal kurallar `error`; `operationId` (39) ve `4XX` (19) eksikleri
  **görünür `warn`** olarak bırakıldı (ratchet sırası yazılı).
- `.redocly.lint-ignore.yaml` — **elle** yazıldı, yalnız tek sınıf: kanonik şemaların
  `notes`/`metadata` anahtarları (23 ihlal / 12 dosya) → **SD11**. `--generate-ignore-file`
  toptan 85 bulguyu susturacaktı; kapıyı yeniden kör edeceği için kullanılmadı.

#### Added
- `tests/test_publication_tree_gates.py` → **araçtan bağımsız `$ref` kapısı** (npm/ağ
  gerekmez) + SD9 sürüm kapısı. **4/4 mutasyon** kırmızı.

### ÖD-9 … ÖD-16 — kapılar gördüğünü iddia ettikleri yüzeyi ölçsün (şema değişikliği YOK)

**ÖD-9 (dört depo tarandı, AST):** kodlamasız dosya okuma sınıfı **worker'a özgü** —
contract/edge/platform **0**, worker 12. W11 listesi düzeltildi (`map_renderer` rasterio
`MemoryFile.open()` → yanlış pozitif; `safe_path.py:19` docstring örneği). ⚠️ Ölçüm
aracının kendi hatası da bulundu: `open(dosya, mod)` ↔ `Path.open(mod)` imza farkı.

**ÖD-10 (varsayım çürüdü):** 16 vendored dosyanın **0'ı** kanoniğinden fazla prose
taşıyor (37.336 ↔ 71.490 karakter). Kalan risk yükte değil **okuyucuda** (W11). Yine de
yeni kapı olayın şeklini yasaklıyor: `test_vendored_prose_does_not_exceed_canonical`.

**ÖD-11:** `TÜRETİLMİŞ İŞARETÇİ` damgası bir **muafiyet değildir** — damgalı bölüme
1500 karakter tavanı (ölçüm: işaretçiler ≤1366, gövdeler ≥1483) + "işaretçi bir hedef
göstermeli".

**ÖD-12:** "göç taşımadır" kapısı **başlık** sayıyordu → artık **içerik** ölçüyor (her
gövdeye asgari uzunluk + toplam hacim tabanı; 4 bölüm başlığı beyanlı).

**ÖD-13:** yayın ağacı ilk kez kapı altında — `validate.py` **96 → 164 dosya**; yayın
kopyası kaynağının PII kapsamını devralır; `inline_refs --check` artık **yetim** dosya arar.

**ÖD-15:** `SDLC_GATES.md` SD8'i iki yerde iki farklı hâlde anlatıyordu → tek gövde §3G.

**ÖD-16:** CHANGELOG'da yayımlanan `--old v7.2.0` komutu **düşüyordu**; dedektör artık
git ref kabul ediyor ve bir test yayımlanan her `--old` argümanının çözülebilirliğini
zorluyor. CI checkout'u `fetch-depth: 0` + `fetch-tags: true` yapıldı (sığ checkout etiket
getirmiyordu → kapı CI'da yanlış gerekçeyle kırmızıydı).

### 🔄 E13-R — kalibrasyon tipi **drone başına türetilir** (E13'ün filo-geneli `ABSOLUTE` kararı GERİ ALINDI)

**Tip:** şema değişikliği YOK (yalnız enum'a normatif `x-derivation` bloğu + kapı) → MINOR.

**Karar (koordinatör onaylı, 2026-08-01 ikinci oturum):** kalibre pakete yazılacak
`calibration_type` **sabit değildir**; `drone_capability_matrix.yaml →
capabilities[drone_type].calibration_class`'tan türetilir:
`relative → RELATIVE` · `absolute → ABSOLUTE | PANEL_ABSOLUTE`.

**Neden geri alındı (ÖD-5 ölçümü — üç kanonik kaynak da E13'ün tersini söylüyordu):**

| Kaynak | Hüküm |
|---|---|
| `drone_capability_matrix.yaml:18` | `DJI_MAVIC_3M → calibration_class: relative` · *"Pix4Dfields göreli kalibrasyon sağlar"* |
| `docs/TARLAANALIZ_SSOT_v1_2_0.txt:79` ve `:1014` | *"Pix4Dfields, M3M için tam radyometrik kalibrasyon **değil**, göreli (relative) kalibrasyon sağlar"* |
| platform `src/core/domain/value_objects/calibration_class.py:41` | `DJI_MAVIC_3M: RELATIVE` — 2.0× tolerans gevşemesi bu sınıfa bağlı |

E13'ün gerekçesi (panel zorunlu · motor Pix4Dfields · enum `ABSOLUTE`'u *"Pix4D
panel-tabanlı"* diye tanımlıyor) kendi içinde tutarlıydı ama **bu üç kaynağı hiç
ölçmemişti**. Panel zorunluluğu ayırt edici değildir: SOP gereği panel **her** sınıfta
kullanılır (KR-018/KR-092), ayırt edici olan **sensör sınıfıdır**.

🔴 **Ölçülen sonuç:** sabit `ABSOLUTE` yazılsaydı worker'ın
`FINETUNE_ALLOWED_CALIBRATIONS` kümesi (`src/core/domain/enums.py:73`) M3M verisini **ince
ayara uygun** sayacaktı → K-3'ün *"fine-tuning: SADECE PANEL+DLS2"* kuralı sessizce
delinir, platformun 2.0× tolerans gevşemesi devreye girmez, zaman serisi karşılaştırmaları
SSOT `:1014`'ün açıkça reddettiği bir varsayıma oturur.

💰 **Kabul edilen bedel (yazılı, `x-superseded-e13-2026-08-01.cost_accepted`):** demo/pilot
filosu M3M olduğu için M3M verisi **ince ayara girmez**, yalnız SSL ön-eğitimine girer.
Alternatifi göreli veriyi mutlak etiketle eğitime sokmaktı.

✅ **E13'ün ayakta kalan yarısı:** `DLS2_RELATIVE` kalibre paket yüzeyinden **reddedilmeye
devam ediyor** (satıcıya özgü donanım adı + irradyans ayrı eksen). Yeniden adlandırma **S3**.

#### Added
- **`enums/calibration_type.enum.v1.json` → `x-derivation`:** makine-okunur türetme tablosu
  (`source` · `map` · `forbidden` · `consumer_obligation` · geri alma kaydı). Kural yalnız
  prose'da yaşasaydı bir sonraki tur onu görmezdi — E13'ün ilk hâlinin düştüğü hata buydu.
- **YENİ kapı** `tests/test_calibration_type_derivation.py` (14 test): türetme matrise
  **bağlı** mı · her sınıf eşlenmiş mi · türetilen değer kalibre yüzeyde **yazılabilir** mi
  (yoksa kural kâğıt üzerinde kalır — ÖD-1'in aynısı) · **göreli sınıf mutlak etiket
  üretemez** (regresyon) · kararın üç dayanağı yerinde mi · geri alma kaydı bedeliyle
  birlikte duruyor mu. **8/8 mutasyon** kırmızı.

#### Changed
- `tests/test_calibration_type_axis.py`: docstring'i E13-R'yi yansıtıyor; panel
  gerekçesinin *ayırt edici olmadığı* açıkça yazıldı (o dosya artık eksenin temizliğini
  korur, türetme mantığını değil).

#### Consumer obligations (bu depodan zorlanamaz — kalibre manifest `drone_type` taşımaz)
- **edge (E14):** değeri intake'teki drone modelinden + matristen **türetir**; matriste
  olmayan drone için değer uydurmaz → kalibrasyon reddedilir (fail-closed).
- **platform (P14 — ACİLLEŞTİ):** `worker_job_publisher.py:80-84` fail-open
  `CALIBRATED → PANEL_ABSOLUTE` adımı **kaldırılmalı**. Ölçüldü: canlı. E13-R sonrası bu
  adım göreli veriyi mutlak etiketle worker'a gönderen tek yol hâline geliyor.
- **worker:** tipi olduğu gibi tüketir; `RELATIVE` ince ayara girmez (K-3).

### ÖD-1 · ÖD-2 · ÖD-3 · ÖD-8 — *"aynı kavramın iki tanımı, ikisini bağlayan kapı yok"* (hepsi MINOR)

**Tip:** MINOR — dedektör ölçümü: **3 değişiklik / 0 breaking** (enum değeri eklendi ×1,
opsiyonel alan eklendi ×2; `required` değişmedi). Öz-denetimin üç KRİTİK bulgusu da aynı
kök nedene bakıyordu: *bir karar bir yere yazıldı, belgeyi doğrulayan yüzeye yazılmadı ve
hiçbir kapı ikisini karşılaştırmıyordu.*

**ÖD-1 — C6b/S2 kararı kâğıt üzerindeydi.** Kayıt defteri
(`calibration_type.enum.v1 → x-context-subsets['edge/calibrated_dataset_manifest']`)
`PANEL_ABSOLUTE` diyordu; **şemanın inline enum'u** hâlâ `[ABSOLUTE, RELATIVE]` idi. Yani
karar "yapıldı" diye kayıtlıyken `PANEL_ABSOLUTE` taşıyan bir kalibre manifest o gün de
**reddediliyordu.** Şema deftere hizalandı.

**ÖD-2 — S5+W12 tel üstünde ÖLÜYDÜ.** `analysis_job.v1 → $defs/CalibrationMetadata`
kanonik `calibration_metadata.v1`'den ayrışmıştı (4 alan ↔ 8 alan) ve
`unevaluatedProperties: false` taşıyordu. Ölçüldü (jsonschema): `scale` bloğu taşıyan bir iş
belgesi *"Unevaluated properties are not allowed ('scale' was unexpected)"* ile **reddediliyordu**
— W12'de worker'a yazılan `resolve_reflectance_divisor` okuma kodu veriyi asla göremezdi.
S4'ün `calibration_method` alanı da aynı delikten düşüyordu. İkisi de gömülü tanıma eklendi;
`sensor_model`/`red_edge_center_nm` **bilerek** taşınmadı (iş belgesinde onları
`drone_metadata` taşır — ADR-002) ve bu beyan **ölçülüyor**.

**ÖD-3 — E13/C6b kapıları yalan yeşildi.** `test_calibration_type_axis.py` ve
`test_calibrated_manifest_fields.py` kararı yalnız **kayıt defterinden** okuyordu; kararın
değeri şemadan silinse kapılar yeşil kalırdı. Her iki dosya artık **iki yüzeyi birden** ölçüyor.

**ÖD-8 — parite kapısı iki yönden dardı.** Ölçüldü: **16 vendored dosyanın 9'u** izleniyordu
(ÖD-2 tam da izlenmeyen `analysis_job`'dan geçti) ve karşılaştırma yalnız üst düzey
`properties`/`required` idi — `$defs` ve **enum değerleri** hiç ölçülmüyordu. Kapsam 16'ya
çıkarıldı, iki karşılaştırma kipi (MIRROR / SUBSET) tanımlandı ve enum ekseni eklendi.

### Added

- **`schemas/edge/calibrated_dataset_manifest.v1`:** `calibration_result.calibration_type`
  enum'una **`PANEL_ABSOLUTE`** (C6b/S2'nin fiilen uygulanması; additive → MINOR).
- **`schemas/worker/analysis_job.v1 → $defs/CalibrationMetadata`:** opsiyonel **`scale`**
  bloğu (`scaled_int` için `if/then` bölen zorunluluğuyla birlikte) + opsiyonel
  **`calibration_method`**. Doğrulama anlamı kanonik `calibration_metadata.v1` ile birebir;
  normatif gövde orada, burada **işaretçi** (D16 idiomu).

### Gates

- **YENİ:** `tests/test_context_subset_binding.py` (31 test) — defterdeki **her** bağlam
  gerçek bir şema yüzeyine çözülmeli, inline enum ile defter **küme olarak eşit** olmalı ve
  defterde kaydı olmayan bir kalibrasyon yüzeyi kalmamalı. Yüzey keşfi ad listesiyle değil
  **ölçümle** yapılır (8 yüzey bulunuyor). **7/7 mutasyon** kırmızı.
- **YENİ:** `tests/test_calibration_metadata_single_definition.py` (18 test) — iki tanımın
  ayrışmasını yasaklar; beyan edilen eksikliğin **taşıyıcısı ölçülür** (gerekçe doğrulanabilir
  olmalı, yazılı olması yetmez); ve asıl iddia **belge düzeyinde** sınanır: `scale` taşıyan iş
  geçmeli, bölensiz `scaled_int` düşmeli. **9/9 mutasyon** kırmızı.
- **GENİŞLETİLDİ:** `tests/test_vendored_parity.py` — 9 → **16 dosya**, MIRROR/SUBSET kipleri,
  enum yüzeyi karşılaştırması, "kapalı vendored form kanonik alanı atlayamaz" kuralı (ÖD-2'nin
  tam kuralı) ve `test_every_vendored_file_is_tracked` (kapsamı ölçülmeyen kapı = olmayan kapı).
  **7/7 mutasyon** kırmızı.
- **Yeni beyanlar (`PENDING_PROPAGATION`, enum ekseni ilk kez):** edge kalibre manifestte
  `calibration_type` (+`PANEL_ABSOLUTE`) · `raw_frames[].band` (+`RGB`, **S7 yayılmamıştı**) ·
  `qc_report.flags` (D7 sözlüğü — vendored tarafta alan hâlâ **kısıtsız string**) · worker
  `calibration_metadata.v1` → `calibration_method` (S4; okuyan kod yok, C8'e bırakıldı).
  ⚠️ Dördüncü bir beyan (worker `analysis_job` `$defs/CalibrationMetadata`) tur ortasında
  açıldı ve **aynı tur içinde kapandı** (W13) → beyan `527c174`'te silindi. Tur kapanışında
  açık beyan sayısı **2**.
- **Borç kaydı (`KNOWN_VENDORED_AHEAD`) — tur boyunca 16 → 6 değere DÜŞTÜ:** ÖD-8 ile
  **ilk kez ölçülen** ters yön sapmaları dört dosyada / 5 pointer'da / 16 değerdeydi.
  E16 kapanınca (edge sınırda `strip().upper()` normalize ediyor, edge PR #50) edge
  `worker_result` ve `intake_manifest.sorties[]` küçük-harf girişleri **silindi** → bugün
  **2 dosya / 3 pointer / 6 değer**. Kalan altısı worker `expert_labeling_card` (`EGE`) ve
  `expert_review_queue` (APPLE/CHERRY/FIG/PEACH); bunlar **W14 kararıyla borç olmaktan
  çıkıp beyan edilmiş EKSEN FARKI oldu** (worker-içi 12 ürün/7 bölge araştırma ekseni ↔
  tel-üstü GAP 8/9 ekseni bilerek ayrı; yeniden açılma koşulu makine-okunur:
  ürün siparişe açılırsa **tel önce genişletilir**). Liste yalnız **küçülür**.
- **SD11 kararı:** kanonik şemalardaki üst düzey `notes` / `metadata` anahtarları
  **kanonikte KALIR**; `x-notes`/`x-metadata` göçü YAPILMAZ (dört ölçümlü gerekçe: bu
  dosyalar önce JSON Schema belgesidir · göç her okuyucuyu kırar — `metadata.bandRequirements`
  KR-018 bant kapısının kaynağı · sıfır davranış kazancı · istisna dar). 23 redocly `struct`
  bulgusu **beyanlı** susturuldu ve istisna listesi **kapıya bağlandı**: `struct` dışında
  kural, `notes`/`metadata` dışında pointer eklenemez, liste büyüyemez.
- **Yayın kapısı (ÖD-0, 2026-08-01 gece):** `tests/test_pin_version.py` artık
  `CONTRACTS_VERSION.md` sürümünün **CHANGELOG'da bir bölümü** olduğunu ve o bölümün
  **gövdeli** olduğunu zorluyor (`release_gate`). Ölçülen boşluk: `pin_version.py` sürümü
  yazar ama `## [Unreleased]` başlığını çevirmez; unutulursa tüm kapılar yeşil kalır ve
  sürüm notları "Unreleased" etiketiyle yayımlanırdı. **2/2 mutasyon** kırmızı.

---

## [7.3.0] - 2026-08-01 — CONTRACT TUR 1 (C8 ile kapatıldı)

**Breaking-change:** HAYIR (MINOR) — **iki bağımsız ölçümle** doğrulandı:
`tools/breaking_change_detector.py --old v7.2.0 --new .` → *45 değişiklik, **0 breaking***;
ve dedektörden bağımsız bir tarama (157 dosya; `$defs`/`items`/`oneOf` dahil **her derinlikte**
enum-değeri silme · `required` ekleme · tip değişimi · dosya silme) → **dördü de 0**.
İkinci ölçüm bilerek yapıldı: dedektörün iç içe yapılara körlüğü 2026-07-31'de ölçülmüştü,
dolayısıyla tek başına "0 breaking" çıktısı sürüm kararına dayanak sayılmadı.

> ✅ **Tur kapandı.** `PENDING_REPIN` beyanı `pin_version.py` tarafından silindi;
> `PENDING_PROPAGATION` **boşaltıldı** (yayılım yapıldı — aşağıya bakın).
> Tur tanımı: `docs/TARLAANALIZ_EYLEM_PLANI_2026-07-30.md` §3.1 → "🔒 TUR TANIMI";
> tören: `docs/checklists/SDLC_GATES.md` §3G.

### C8 töreninde yapılan yayılım (SD7 — `PENDING_PROPAGATION` boşaltıldı)

Vendored kopyalar kanoniğin **dar runtime alt-kümesidir** (I-4), bu yüzden dosya
kopyalanmadı — yalnız beyanda adı geçen alanlar taşındı, vendored idiom
(`additionalProperties: false`) korundu:

- **edge** `interface/contracts/schemas/edge/calibrated_dataset_manifest.v1.schema.json`
  ← `raw_frames` (C3′ / KG-0.c seçilmiş ham kareler)
- **worker** `interface/contracts/expert_review_queue.v1.schema.json`
  ← 8 denetim alanı (`audit_sample`, `audit_stratum`, `audit_selection_rate`,
  `audit_rotation_key`, `audit_bucket`, `tile_id`, `consensus_participation`,
  `spot_check_suppressed`) + `escalation_reason` enum'una additive `AUDIT_SAMPLE`
  + 5 dallı `allOf` ölçüm-bütünlüğü bloğu (D12–D15: anti-anchoring · i.i.d. bağımsızlık ·
  denetim satırı bütünlüğü)

### Bu turda kapanan kararlar (eylem planı §14.7)

- **D16-b2** — ikili normatif gövde **49 → 0**; kanonik metin `docs/TARLAANALIZ_SSOT_v1_2_0.txt`,
  `ssot/kr_registry.md` navigasyon + kapsam dizinine indirildi (gövdesi orada kalan tek istisna:
  KR-088/089/090/091). Üç gövde fiilen yanlıştı (KR-083 kaldırılmış rol adı · KR-027 donmuş başlık ·
  KR-000 "DJI" ifadesi) — ikinci gövdenin sessizce çürüdüğünün kanıtı.
- **D4-b** — vendored parite kapısı **karşı tarafta** koşar (PAT yok; bu depo PUBLIC, kardeşler PRIVATE).
- **SD8** — 14 geriye dönük annotated tag + `2.0.2` için kayıt notu (release commit'i belirlenemiyor).
  I-2 artık tarihsel olarak da tutuyor.
- **0.h / K3** — veri yönetişimi: üç veri kategorisi KR-090 saklama tablosuna süre + silme yolu +
  gerekçe ile yazıldı; kural `tests/test_data_governance.py` ile zorlanıyor.
- **E13 → C6** — kalibre paket manifestine yazılacak değer **`ABSOLUTE`** (panel zorunlu + motor
  Pix4Dfields). `DLS2_RELATIVE` reddedildi: DLS2 bir MicaSense donanımıdır ve irradyans **yöntemi**
  ayrı eksendir. ⇒ C6'nın koşullu MINOR bump'ı **iptal**, contract değişikliği gerekmedi.

### C0 — `calibrated_dataset_manifest.v1` iki-form ayrımı makine-okunur hâle getirildi

**Tip:** PATCH-düzeyi (metadata/açıklama; hiçbir alan, `required` veya enum değeri değişmedi —
`breaking_change_detector`: **0 değişiklik, 0 breaking**).

**Sorun:** `calibrated_dataset_manifest.v1.schema.json` **iki ayrı dosyadır** ve yalnız dizinle
ayrılır (`schemas/edge/` = kalibrasyon kanıtı · `schemas/platform/` = paket agregası). Her ikisinin
description'ında karşılıklı **prose** atıf zaten vardı, ama bu bir plan turunun üç iş kalemini
(C1/C2/C3) yanlış dosyaya yazmasını **engelleyemedi** — `patches[].object_key` "calibrated
manifest'e eklensin" diye planlandı, oysa `patches` alanı **hiçbir** calibrated formda yok
(gerçek yeri: `intake_manifest.v1 → EdgeForm.priority_zones[].visualizations`).

### Added

- **`schemas/edge/calibrated_dataset_manifest.v1.schema.json`** + **`schemas/platform/…`:**
  makine-okunur **`x-form-role`** bloğu — `role`, `emitter`, `purpose`, `counterpart` (karşı
  formun `$id`'si), `owns[]` (o formun sahiplendiği alanlar), `not_owned_here` (nereye ait
  olduğu), `field_placement_rule` (yeni alan eklemeden önce sahiplik yazılı belirlenir).
  `x-updated: 2026-07-31` eklendi. `properties`/`required`/`$defs` **DEĞİŞMEDİ**.
- **`tests/test_manifest_form_roles.py`** (12 test): `x-form-role` varlığı ve zorunlu anahtarları ·
  rollerin farklı olması · `counterpart` ↔ `$id` **birebir** eşleşmesi (yeniden adlandırma kırar) ·
  `owns[]`'ın hayalî alan saymaması · iki formun **aynı alanı sahiplenmemesi** · **C2 regresyon
  kapısı** (`patches`/`priority_zones`/`visualizations` calibrated manifest'e sızmaz) ·
  `priority_zones`'un `intake_manifest EdgeForm`'da kalması · **C5/KG-0.f kapısı** (BENEFICIAL ve
  THERMAL_STRESS "üretilemez" işaretli kalır ve enum'dan silinmez).

### Changed

- **`ssot/contracts_ssot.md` (KR-072):** iki formun rol/alan-sahipliği tablosu eklendi; yama
  görsellerinin **hiçbirine ait olmadığı**, `intake_manifest.v1` altında olduğu yazıldı.
- **`enums/analysis_type.enum.v1.json` v1.4.1 → v1.4.2** *(C5 kalan deltası)*: `metadata.changeNote`'a
  **KG-0.f karar kaydı çapraz atfı** — izlenebilirlik notu, **davranış değişikliği yok.** KG-0.f'in
  istediği "üretilemez" işaretleri (`BENEFICIAL → enum_valid_not_yet_emittable`,
  `THERMAL_STRESS → requires_thermal_payload`) **zaten v1.4.0/v1.4.1'de mevcuttu**; C5 bu nedenle
  Tur 1 kapsamından düştü. `enum` dizisi, `requires_bands` ve `availability` değerleri DEĞİŞMEDİ.

### Notes

- **Doğrulama:** `validate.py` 89 dosya / 0 hata · `pytest` **560 geçti + 12 yeni** ·
  `breaking_change_detector` **0 breaking**. Tek kırmızı `test_pin_version::test_real_repo_checksum_verifies`
  → **beklenen**, C8'de kapanır (yukarıdaki uyarıya bakın).
- **Gerekçe arşivi:** `denetim/denetim_raporu_2026-07-31_plan_devir_ozdenetim.md` (D-1, D-4).

### C9 + C10 — ÖN RAPOR (`report_phase`) kanonik tanımı: içerik listesi + statü eşlemesi

**Tip:** MINOR (yalnız eklemeli metadata + açıklama; `enum` dizisi `{PRELIMINARY, FULL}` DEĞİŞMEDİ,
hiçbir alan/`required` değişmedi — `breaking_change_detector`: 2 değişiklik, **0 breaking**).

**Sorun (2026-07-31 denetimi, D-6/D-7/D-15):** KG-0.b-R (Y-D) kararı *"yeni faz/şema gerekmiyor"*
diyordu. **Faz kısmı doğruydu, şema kısmı değildi** — üç ayrı eksende:

1. **İçerik:** `analysis_preliminary_ready.v1` (*"carries **ONLY** deterministic index layers…"*) ve
   `report_phase.enum.v1` (*"**Yalnız** deterministik indeks katmanları… sunulur"*) PRELIMINARY
   içeriğini dört kaleme **kapatıyordu**; Y-D'nin göstereceği öncelik bölgesi (poligon +
   `ndvi_value` + `ndvi_overlay`) o listede **yoktu**.
2. **Zamanlama:** `x-derived-from.mapping` yalnız analiz-ve-sonrası statüleri sayıyordu. Y-D raporu
   **kalibrasyondan hemen sonra** (mission `UPLOADED`) gösterilir → haritada **karşılığı yoktu.**
   "Çalışıyor" görünmesinin tek sebebi platformun catch-all'uydu
   (`results_service_impl.py:227` → `"FULL" if DONE else "PRELIMINARY"`), yani platform **kanonik
   haritadan geniş** davranıyordu — contract-first (KR-081) projede demo bunun üstüne kuruluyordu.
3. **Kanonik olmayan adlar:** mapping `ANALYZING` ve `DONE` kullanıyordu; `mission_status.enum.v1`
   bunları **tanımıyor** (kanonik karşılıkları `IN_ANALYSIS` ve `DELIVERED`). **Dört girişin ikisi.**

**Ön koşul (D-7):** `ssot/kr_registry.md` **KR-092'de bitiyordu**, ama contract'ın kendi artefaktları
KR-093'e **normatif atıf** yapıyordu → sarkan kanonik atıf. Ek olarak contract'ın
`docs/TARLAANALIZ_SSOT_v1_2_0.txt` kopyası **KR-084'te bitiyor**, platform kopyası KR-093'e kadar
gidiyor — aynı adlı iki SSOT metni **ayrışmış** (hizalama ayrı kalem).

### Added

- **`ssot/kr_registry.md` → KR-093** *(Çiftçi Ön Raporu — İki-Fazlı Teslimat)*: kanonik registry'ye
  taşındı; 8 bölümlü contract formatında, platform normatif metni (`docs/TARLAANALIZ_SSOT_v1_2_0.txt`
  [KR-093] + `docs/kr/kr_registry.md`) esas alınarak. **KG-0.b-R (Y-D) eklentisi** açıkça işaretli;
  AK-4 çapraz-repo notu eklendi (platform kopyalarının aynalaması ayrı kalem, sapma **geçici**).
- **`enums/report_phase.enum.v1.json` → `x-preliminary-content`:** sunulabilir içeriğin **KAPALI**
  listesi — `stage_a_post_calibration` (öncelik bölgeleri: `geom`/`ndvi_value`/`priority_level`/
  `ndvi_overlay`; kaynak `analysis_priority_zones`) · `stage_b_post_analysis` (ortho + `HEALTH`/
  `NITROGEN_STRESS`/`WATER_STRESS` + `overall_health_index`; **KR-093'ün özgün tanımı, değişmedi**) ·
  **`never`** (`findings`, `detections`, `expert_corrections`, `prescription`,
  `treatment_recommendation`). Gerekçe alanı: Aşama A **gözlemsel indeks türevidir, tespit değildir**
  → KR-019 zayıflamaz, KR-025 korunur.
- **`x-derived-from.unlisted_status_behavior`:** **FAIL-CLOSED** — haritada olmayan statü için faz
  türetilmez ve sonuç sunulmaz. *"Listelenmeyen = PRELIMINARY"* varsayımı **yasaklandı** (aksi hâlde
  `DRAFT`/`PLANNED` ön rapor üretirdi).
- **`x-derived-from.platform_internal_aliases`:** platform 13'lük alias alt-kümesinin kanoniğe
  çevrimi belgelendi (`ANALYZING→IN_ANALYSIS`, `DONE→DELIVERED`, `ACKED→ACCEPTED`,
  `FLOWN→IN_PROGRESS`; kaynak platform `mission.py::_STATUS_TO_CONTRACT`).
- **`tests/test_report_phase_contract.py` (19 test):** mapping anahtarlarının **tamamı**
  `mission_status.enum.v1` üyesi olmalı *(bu kapı eski `ANALYZING`/`DONE` ile **düşüyor** — kanıtlandı)* ·
  `UPLOADED → PRELIMINARY` (Y-D anı) · `FULL` yalnız `DELIVERED`'dan · `EXPERT_REJECTED` → WITHDRAWN ·
  uçuş öncesi statüler haritada olmamalı · fail-closed kuralı yazılı olmalı · Aşama A/B alan kapıları ·
  **hiçbir aşamada tespit içeriği olmamalı** · olay açıklaması faz-düzeyi "ONLY" iddiasında
  bulunmamalı · `x-kr-ref`'teki her KR registry'de **tanımlı** olmalı (genel sarkan-atıf kapısı).

### Changed

- **`enums/report_phase.enum.v1.json`:** `x-derived-from.mapping` **kanonik adlarla** yeniden yazıldı
  ve Y-D anı eklendi → `UPLOADED`/`IN_ANALYSIS`/`PENDING_REVIEW` → `PRELIMINARY`; `DELIVERED` → `FULL`;
  `EXPERT_REJECTED` → WITHDRAWN (409). `x-enum-descriptions.PRELIMINARY` iki aşamalı içeriği anlatacak
  biçimde güncellendi. `x-updated` → 2026-07-31.
- **`schemas/events/analysis_preliminary_ready.v1.schema.json`:** açıklamadaki *"the preliminary phase
  carries ONLY…"* **faz-düzeyi** iddiası, **olayın kendi payload'ına** daraltıldı; faz içeriğinin
  kanonik kaynağı olarak `report_phase.enum.v1 :: x-preliminary-content` gösterildi. Olayın **yalnız
  Aşama B'yi** haber verdiği, Aşama A'nın okuma yoluyla sunulduğu ve **yeni wire olayı eklenmediği**
  yazıldı. KR-019 ifadesi (*"NO expert-dependent detections"*) **korundu**.

### Notes

- **Y-D kararı değişmedi** — kanonik tanım onu **kapsayacak** biçimde genişletildi. ADR-007 §2
  (yeni mission state yok) ve §5 (Aşama B bildirimi) korunur; `report_phase` kümesi `{PRELIMINARY, FULL}`.
- **Platform tarafı borç:** `docs/kr/kr_registry.md` + `docs/TARLAANALIZ_SSOT_v1_2_0.txt` bu metni
  aynalamalı; `results_service_impl.py:227` catch-all'u kanonik mapping'e daraltılmalı (P12 kabul
  kriteri). AK-4: sapma **geçicidir**.
- **Doğrulama:** `validate.py` 89 dosya / 0 hata · `pytest` **579 geçti (+19 yeni)** ·
  `breaking_change_detector` **0 breaking**. Beklenen tek kırmızı: checksum (C8'de kapanır).
- **Gerekçe arşivi:** `denetim/denetim_raporu_2026-07-31_plan_devir_ozdenetim.md` (D-6, D-7, D-15).

### AL-C1 + AL-C2 — i.i.d. denetim örneklemi kanalı (ölçüm temeli [0]'ın kontrat ayağı)

**Tip:** MINOR (additive enum değeri + iki opsiyonel alan + koşullu kısıtlar;
`breaking_change_detector`: **0 breaking**).

**Kaynak:** worker `denetim/birlesik_devir_spec_arsivi_2026.md` §9 — karar-hazır devir
(2026-08-11'e kadar ayrı dosya: `audit_escalation_reason_devir_spec_2026_07_19`).
Worker'ın `audit_set_sampler` + `propagation_metrics` kodu **landed ama uykuda**; canlıya bağlanması
platform kararı bekliyordu (§2.1: worker enum'a değer **uyduramaz**).

### Added

- **AL-C1 — `escalation_reason` += `AUDIT_SAMPLE`** (additive 7. değer). Diğer 6 neden **model
  davranışından** türetilir; `AUDIT_SAMPLE` model çıktısından **bağımsız** stratifiye Bernoulli
  seçimle üretilir. Denetim tile'ını güven-temelli bir neden altında yollamak hem yansızlığı bozar
  hem `escalation_total{reason}` metriğini kirletir.
- **AL-C2 — `audit_sample: boolean` (default false) + `audit_stratum`**. `audit_stratum`
  **yapısal objedir, serbest metin DEĞİLDİR** (§2.1 eksen karışımı = şema hatası):
  `{crop_type, analysis_type, phenology_stage?}`, değer kümeleri kanonik enum'lardan vendor'landı.
  `phenology_stage` **opsiyonel** — kanonik enum bugün **8 mahsulün yalnız 3'ünü** kapsıyor
  (GRAPE/CORN/OLIVE); zorunlu olsa COTTON örneklenemezdi.

### Added — bağlayıcı kurallar (`allOf` / if-then)

| Kural | Neden |
|---|---|
| `audit_sample` ⟺ `escalation_reason == AUDIT_SAMPLE` | A tek başına anchoring'i çözmez, B tek başına metriği kirletir → **birlikte hareket ederler** |
| `audit_sample` → `audit_stratum` **zorunlu** | Stratum'suz örneklem `propagation_precision(crop)`'u stratifiye edemez |
| `audit_sample` → `spot_check == false` | ⚠️ **Devir spesinde YOKTU, bu turda bulundu:** `spot_check` zaten şemada var ve **GÜVEN-KOŞULLU** (HIGH tile'ların ~%5'i). İkisi aynı anda seçilirse seçim güvene koşullanır ve **i.i.d. bağımsızlık ölür** |
| `audit_sample` → `predicted_class`/`detection_type`/`sub_specialty` **null** | **ANTI-ANCHORING sözleşme düzeyinde fail-closed** — Portal'ın gizlemesine güvenilmez. Üçü de zaten nullable → geriye uyumlu |

### Notes — bilinçli sınır: `confidence_score`

Devir spesi anti-anchoring'i **Portal davranış şartı** olarak tanımlıyordu. Sınıf etiketlerini
**tel üzerinden tamamen kaldırarak** bundan daha ileri gidildi (fail-closed). Ancak
`confidence_score` bu turda tel üzerinde **kaldı**: alan `required` + `type: number` ve nullable'a
genişletmek `breaking_change_detector`'a göre **MAJOR** olurdu (ölçüldü) — bu tur MINOR.
→ Yükümlülük `x-anti-anchoring.residual_portal_obligation`'da **yazılı** (AL-P1) ve tam
fail-closed için **AL-C3** kalemi açıldı. Metrikler tahmini `job_id` ile `analysis_result`'tan
JOIN eder; uzman-facing pakette taşınmasına gerek yoktur.

### Added — test

- **`tests/test_audit_sample_contract.py` (25 test):** additive'lik (6 pazarlık-dışı değer
  korunur) · geriye uyumluluk · `audit_stratum`'un **serbest metin kabul etmemesi** · eksen
  kümelerinin kanonik enum'ları **aynalaması** · fenoloji kapsam gerekçesi · bayrak↔neden
  bağının **iki yönde** zorlanması · **spot_check karşılıklı dışlaması** · anti-anchoring'in
  üç sınıf etiketinde de zorlanması (olağan eskalasyonda **serbest kalması**) · KR-071 (field_id
  yok, stratum tanımlayıcı taşımaz, kök kapalı).

### Notes — çapraz-repo sonucu (C8'e devredildi)

- `PENDING_PROPAGATION`'a `expert_review_queue` beyanı eklendi.
- ⚠️ Worker tarafında `tests/contract/test_expert_review_queue_schema.py::TestReasonEnumParity`
  worker `EscalationReason` enum'unu kanonikle **birebir** bağlar → worker vendor edene kadar
  **o test kırmızı kalır**. Beklenen; C8'de kapanır.
- **AL-P1 / AL-P2 / AL-P3** platform kalemleridir (portal anti-anchoring · `escalation_total`
  ayrımı · `test_pii_isolation` denetim kanalını kapsasın) — kontrat tarafı hazır.

### Notes

- **Doğrulama:** `validate.py` 89 dosya / 0 hata · `pytest` **704 geçti (+25 yeni)** ·
  `breaking_change_detector` **0 breaking**.
- **Contract Tur 1 şema kalemleri TAMAM** *(C6 hariç — E13 kararına bağlı)*.

---

### C1′ + C3′ — kalibre manifest alanları (kelime dağarcığı KANONİK kaynaktan türetildi)

**Tip:** MINOR (yalnız **opsiyonel** alanlar; `required` ve mevcut `enum`'lar değişmedi —
`breaking_change_detector`: **0 breaking**).

**Tekrar eden hata sınıfı, üçüncü kez:** plan C1′ için `layer_type(ortho/ndvi/ndre/**ndwi**)`
öneriyordu. Ölçüldü — kanonik indeks kümesi **`drone_capability_matrix.yaml → available_indices`**
altında yaşıyor (`core: NDVI, NDRE, GNDVI, CIR` · `extended: EVI, SAVI, CHLOROPHYLL_A` ·
`thermal: CWSI, CANOPY_TEMP, CANOPY_SOIL_DELTA` + `IRRIGATION_EFFICIENCY`) ve **NDWI orada YOK.**
Aynı biçimde plan `calibration_tier` diyordu; contract'ta öyle bir ad **yok** — kanonik ad
`calibration_type`, alt-kümeleri `calibration_type.enum.v1 → x-context-subsets`'te.
⇒ İkisi de **uydurulmadı, türetildi.**

### Added — C1′ (`schemas/platform/calibrated_dataset_manifest.v1`)

- **`$defs.file_artifact.layer_type`** (opsiyonel): `ORTHO`, `DSM` + **11 kanonik indeks**
  (matristen türetildi). `type` alanıyla karışmaz — `type` tüketici-tanımlı serbest etiket.
- **`$defs.file_artifact.band`** (opsiyonel): vocabulary `intake_manifest.available_bands` ile
  **aynı** (`BLUE/GREEN/RED/RED_EDGE/NIR/LWIR`); ayrı liste açılmadı.
- **top-level `calibration_type`** (opsiyonel): alt-küme `[ABSOLUTE, PANEL_ABSOLUTE,
  DLS2_RELATIVE, RELATIVE]`. **Paket başına tekil**. `NONE` **dışarıda** (KR-018 hard reject).
- **`x-registry-sync`**: türetim kaynağı şemada yazılı.
- **`enums/calibration_type.enum.v1` → `x-context-subsets['platform/calibrated_dataset_manifest']`**
  kaydedildi. *(C6'da bu kaydın okunmaması "iş yok" yanılgısını doğurmuştu.)*
- ⚠️ **Yeni `index_layers[]` dizisi AÇILMADI** — `outputs[]`/`reflectance_scale`/`producer_tool`
  zaten vardı; alan tekrarı üretilmedi.

### Added — C3′ (`schemas/edge/calibrated_dataset_manifest.v1`)

- **`raw_frames[]`** (opsiyonel, `maxItems: 5000`): `{frame_id, relative_path, footprint_wkt?,
  band?}`, `required: [frame_id, relative_path]`.
- ⚠️ **`object_key` YOK** — plan istiyordu, ama bu form **kiosk-emitted**'dır ve KG-0.a-EK
  kural 1 gereği anahtarı **platform üretir**. C2′ kararıyla tutarlı.
- `relative_path` deseni **dizin düzenini dondurmaz** (E11 belirleyecek) ama traversal'ı
  engeller: mutlak yol **RED** · `..` **RED**.

### Changed

- Her iki formun `x-form-role`'ü güncellendi (`owns` + `not_owned_here`).
- ⚠️ **C0'da yazdığım `calibration_tier` ifadesi C1′ ile çelişiyordu** → kanonik ada çevrildi.

### Changed — vendored parite kapısı ASİMETRİK hale getirildi

C3′ kanoniği edge vendored kopyanın önüne geçirdi ve **kendi parite kapım bunu yakaladı.**

| Durum | Anlamı | Davranış |
|---|---|---|
| **vendored ileri** | AK-4 sapması (I-5) | **SERT HATA** (`sorties`/C11 emsali) |
| **kanonik ileri** | açık sürüm turu, C8'de yayılır | **BEYAN ZORUNLU** (`PENDING_PROPAGATION`) |
| beyan bayat | C8 bitti, kayıt duruyor | **SERT HATA** — liste yalan söyleyemez |

`required` her iki yönde eşit kalmalı ⇒ beyan edilen ekler **opsiyonel olmak zorunda**.
Kanıtlandı: beyan silinince `test_canonical_ahead_is_declared` **düşüyor**.
⚠️ Kapsam sınırı yazıldı: kapı yalnız **9 şemayı** izler; `intake_manifest.v1`
(`oneOf` ↔ flat) **kapsam dışı** — `sorties` sapması orada, **C11** ile izlenir.

### Added — test

- **`tests/test_calibrated_manifest_fields.py` (18 test):** türetim kapısı · **NDWI regresyon
  kapısı** · bant vocabulary paylaşımı · `calibration_tier`'ın hiçbir şemada tanımlanmaması ·
  alt-küme kaydı/eşleşmesi · `NONE` dışarıda · `raw_frames` **`object_key` taşımaz** ·
  traversal kapısı.

### Notes

- **Doğrulama:** `validate.py` 89 dosya / 0 hata · `pytest` **679 geçti (+36 yeni)** ·
  `breaking_change_detector` **0 breaking**.
- **Contract tarafı Tur 1 tamam** *(C6 hariç — E13 kararına bağlı)*. Sırada **AL-C1 + AL-C2**.

---

### C2′ — `intake_manifest.v1`: `PlatformForm.priority_zones` + `object_key` sahipliği

**Tip:** MINOR (yalnız **opsiyonel** alan eklendi; `required` listeleri ve `enum`'lar değişmedi —
`breaking_change_detector`: **0 breaking**). Demo kritik yolunun **① adımı**.

**Sorun (D-1/D-2):** Eski C2 `calibrated_dataset_manifest`'e `patches[].object_key` eklemeyi
söylüyordu; o şemada `patches` **yok** (contract genelinde 0 eşleşme). Görsel yollarının gerçek
yeri `intake_manifest.v1` → `EdgeForm.priority_zones[].visualizations`. Ayrıca `priority_zones`
**yalnız `EdgeForm`'da** vardı — oysa KG-0.a-EK *"anahtarı **platform üretir**, manifestteki
`object_key` platformun **döndürdüğü** değerdir"* diyor ⇒ alanın yeri **PlatformForm**'dur.

### Added

- **`$defs.PlatformForm.priority_zones`** (opsiyonel dizi, `maxItems: 500`): EdgeForm ile
  **aynı zone verisi** (`patch_id`, `geom`, `priority_level`, `ndvi_value`, `sampling_reason`;
  aynı `required` listesi), ancak `visualizations` **göreli yol değil NESNE ANAHTARI** tutar.
  ÖN RAPOR okuma ucunun (P6) kaynağıdır.
- **`tests/test_intake_manifest_forms.py` (16 test)** — `oneOf` ayrımı gerçek yüklerle
  doğrulanır (C2′'nin ana riski) · `object_key` sahipliği desen düzeyinde bağlanır ·
  EdgeForm'un geriye uyumluluğu · iki formun aynı zone verisini taşıması.
- **`docs/examples/intake_manifest.example.json`** → `priority_zones` + `object_key` örneği.

### Changed

- **`EdgeForm...visualizations.description`** netleştirildi: göreli yollar **M1'deki YEREL DOSYA
  TANIMLAYICILARIDIR, nesne deposu anahtarı DEĞİLDİR**; platform onları S3 anahtarı olarak kabul
  etmez, imzalamaz, kalıcılaştırmaz.

### Notes — plandan bilinçli sapma

Plan *"`EdgeForm`'daki göreli yol `x-deprecated` işaretlenir"* diyordu; **işaretlenmedi.**
Gerekçe: edge hangi dosyaları ürettiğini bildirmek zorunda ve anahtarı **üretemez** (platform
üretir). Alanı deprecate etmek edge'e dosyaları bildirecek bir yol bırakmazdı. Fiilen deprecate
edilen şey **"bu yolu S3 anahtarı olarak kullanmak"**tır ve bu artık açıklamada yazılı.

### Notes — `object_key` deseni (ölçülerek sertleştirildi)

İlk yazımda desen `{tenant}` ve `{dataset_id}` **biçimlerini donduruyordu** (`[a-z0-9-]`,
`[a-f0-9-]{32,36}`) — bu, platformun entity-önekli id'leriyle (`dataset_…`) çakışabilirdi.
Ayrıca segment sınıfı `.` içerdiği için **`a/../b` traversal geçiyordu.** Desen, biçim yerine
**güvenlik-anlamlı yapıyı** zorlayacak biçimde yeniden yazıldı:
`^[A-Za-z0-9][A-Za-z0-9_-]*(/[A-Za-z0-9_-]+)+/patches/[a-f0-9]{32}/<ad>$`
→ mutlak yol **RED** · `..` **RED** (segmentlerde `.` yok) · `patches/<id>/…` edge göreli yolu
**RED** (`/patches/` öncesi ≥2 segment şartı) · `coop_abc/dataset_x9y8/patches/…` **KABUL**.
Yedi vaka ile tek tek doğrulandı.

### Notes — `oneOf` ayrımı ölçüldü (varsayım düzeltildi)

`PlatformForm.required` ⊂ `EdgeForm.required` olduğu için ayrım `required` ile yapılmıyor.
Ayrımın **tek** dayanağının `unevaluatedProperties` olduğunu varsaymıştım; ölçüm **üç bağımsız
katman** gösterdi: ① `unevaluatedProperties` (`schema_version`/`drone_make`/`correlation_id`)
② **kimlik biçimleri** (PlatformForm `^batch_[a-z0-9]{24}$`/`^field_…`/`^mission_…` ister)
③ **`files[]` şekli** (`sha256_hash` ↔ `sha256`). Ayrım beklenenden sağlam; test yine de
her iki örneğin **tam olarak bir** dala uyduğunu doğruluyor.

### Notes

- **Doğrulama:** `validate.py` 89 dosya / 0 hata · `pytest` **643 geçti (+16 yeni)** ·
  `breaking_change_detector` **0 breaking**. Beklenen tek kırmızı: checksum (C8).
- **Sırada:** `C2″` (edge `priority_zone.py` aynası) · `C1′` · `C3′`.

---

### C-PARITE + C4-düzeltme — vendored parite iddiaları ve `sorties` sapması

**Tip:** PATCH-düzeyi (yalnız `description` metinleri + yeni test; hiçbir alan/`required`/enum
değişmedi — `breaking_change_detector`: 9 değişiklik, **0 breaking**).

**Sorun:** Dokuz kanonik şema açıklamasında *"... `interface/contracts/...` ile **birebir
uyumludur**"* yazıyordu. Ölçüldü: **9/9'u bayt düzeyinde YANLIŞ.** Ama aynı ölçümde
**9/9'unun `properties` + `required` kümeleri birebir aynı**; tek fark tutarlı bir idiom:

| | kanonik | vendored |
|---|---|---|
| kapatma anahtarı | `unevaluatedProperties: false` | `additionalProperties: false` |

9/9'da aynı olması bunun **çürüme değil, bilinçli bir konvansiyon** olduğunu gösterir →
**yanlış olan, iddianın ifadesiydi.**

### Changed

- **9 şema açıklaması düzeltildi:** `edge/attestation_record` · `edge/calibrated_dataset_manifest` ·
  `edge/evidence_bundle_ref` · `edge/upload_receipt` · `edge/worker_result` ·
  `worker/calibrated_dataset` · `worker/calibration_metadata` · `worker/expert_feedback` ·
  `worker/expert_review_queue`. Yeni ifade: *"vendored kopyasıyla `properties` + `required`
  düzeyinde EŞDEĞERDİR; bayt-özdeşlik BEKLENMEZ — idiom farkı bilinçlidir."*

### Added

- **`tests/test_vendored_parity.py` (38 test):** 9 çift için `properties` / `required` / `$id`
  paritesi · **sözcük kapısı** — *"birebir uyumludur"* ifadesinin geri gelmesi yasak
  *(kanıtlandı: eski ifade yeniden konunca test düşüyor)* · idiom farkının açıklamada belgeli
  kalması · kanonik tarafın `unevaluatedProperties` idiomunu koruması.
  ⚠️ Kardeş depo yoksa test **atlanır (skip)** — CI'da "geçti" ile karıştırılmamalı.
- ⚠️ **Kapı kendi eksik düzeltmesini yakaladı:** ilk turda 6 şema bulunmuştu; sözcük kapısı
  kalan **3'ünü** (worker `calibration_metadata` / `expert_feedback` / `expert_review_queue`)
  gösterdi. Sınıfın tamamı ancak testle kapandı.

### Notes — `sorties` / `mission_date` (C4 ikinci kez düzeltildi)

Aynı taramada ortaya çıktı: **`sorties` ve `mission_date` edge'in vendored interface
sözleşmesinde VAR, kanonikte YOK** → *"C4 contract kalemi değil"* hükmü de eksikti; bu bir
**AK-4 edge-ileri sapmasıdır** (I-5: yalnız geçici olabilir). Ayrıca planın *"bbox'ı zorunlu
yapmak breaking olur"* önermesi de yanlıştı — `bbox` o şemada **zaten `required`**
(`sorties[].required = [sortie_id, field_id, crop_type, bbox]`); opsiyonel olan **dizinin
kendisi**. → Absorpsiyon eylem planında **C11** kalemidir.

### Notes — C8'e devredilen vendored yayılımı (**C-VENDOR**)

- worker `interface/contracts/analysis_type.enum.v1.json` **v1.4.1** ↔ kanonik **v1.4.2**
  (C0'da bump; `enum` dizisi aynı, yalnız `changeNote`)
- edge vendored `calibrated_dataset_manifest` + `intake_manifest` bu turun değişikliklerini almalı
- **Bugün kırık yok:** worker/edge kendi hash kapılarını kullanır (I-4); sürüm dizesi hizası (I-1)
  C8'in şartıdır.

---

### C-SSOT — `TARLAANALIZ_SSOT_v1_2_0.txt`: iki repo kopyası hizalandı (checksum-nötr)

**Tip:** doküman + test (şema/enum/api ağacına dokunulmadı → **Contracts Checksum etkilenmez**).

**Sorun (D-7'nin kökü):** Aynı adı ve aynı sürüm etiketini (`v1_2_0`) taşıyan iki dosya **ayrışmıştı**:
contract kopyası **1706 satır / KR-084**'te bitiyor, platform kopyası **1895 satır / KR-093**'e
gidiyordu. Kök neden: bu dosya **hiçbir senkron aracının kapsamında değil**
(`tools/sync_to_repos.sh` yalnız `schemas/` + `enums/` + `CONTRACTS_VERSION.md` taşır).

**Ölçüm (kopyalamadan ÖNCE yapıldı):**
- Platform'da fazla: **KR-088, KR-091, KR-092, KR-093** · Contract'ta fazla: **yok**
- 27 contract-only satırın tamamı **bayat**: (a) eski sürüm/tarih başlığı (son güncelleme 2026-03-07,
  "Contract Versiyon Uyum 2.0.1" — bugün 7.2.0), (b) **`[KR-083] İl Operatörü`** metni — oysa
  contract'ın **kendi** `enums/role.enum.v1.json`'ı `DISTRICT_REP`'i kanonik, `IL_OPERATOR`'ı
  **DEPRECATED** ilan ediyor (yani contract kendi enum'uyla çelişiyordu), (c) 2026-06-14 öncesi
  KR-024 tarama periyodu tablosu → **kaybedilecek özgün içerik yok.**
- Her iki blob git'te **LF** → kopya **bayt-özdeş** oldu (Windows checkout'taki CRLF farkı git'in
  `autocrlf` davranışıdır, içerik farkı değil).

### Changed

- **`docs/TARLAANALIZ_SSOT_v1_2_0.txt`:** platform kopyasıyla **bayt-özdeş** hâle getirildi
  (49 → 53 KR anılıyor; KR-088/091/092/093 geldi; KR-083 `İlçe Temsilcisi`/`DISTRICT_REP` oldu).
  Provenans dosyaya **eklenmedi** — bayt-özdeşlik korunsun diye kayıt buraya ve eylem planına yazıldı.
- **`CLAUDE.md` (KR bölümü) — DÜZELTME:** *"The canonical source is `ssot/kr_registry.md`"* ifadesi
  **yanlıştı.** Ölçüldü: `ssot/kr_registry.md` yalnız **6 KR** tutuyor (KR-088…KR-093);
  tam korpus (~49 tanım) `docs/TARLAANALIZ_SSOT_v1_2_0.txt`'tedir. İki kaynak **tamamlayıcıdır,
  iç içe değildir**; bir KR **en az birinde** tanımlı olmalıdır. Başlık biçiminin tek tip olmadığı
  da yazıldı (`## [KR-019]` · birleşik `## [KR-018 / KR-082]` · kaynaktaki yazım hatası `## # [KR-033]`).

### Added

- **`tests/test_kr_reference_integrity.py` (10 test):** sarkan (dangling) kanonik atıf kapısı —
  her `x-kr-ref` KR'si iki kaynağın **birleşiminde** tanımlı olmalı *(hizalama öncesi durumda
  **düşüyor**: KR-093 hiçbir kaynakta yoktu — kanıtlandı)* · çıkarıcının **birleşik ve
  hatalı-biçimli başlıkları** da görmesi (yanlış-alarm kapısı; dar bir regex bu turda 018/082/033
  için yanlış alarm üretmişti) · KR-088/091/092/093'ün SSOT metninde kalması (ayrışma regresyonu) ·
  KR-083'ün `İlçe Temsilcisi` adını koruması · `role.enum.v1` ↔ SSOT metni `DISTRICT_REP` mutabakatı.

### Notes

- ⚠️ **Açık kalem (kök neden):** SSOT metni senkron aracına **eklenmedi** — rsync yolu burada
  test edilemediği için körlemesine tooling değişikliği yapılmadı. Worker'daki gibi **salt-okunur
  drift dedektörü** olarak eklenmesi eylem planında **C-SSOT-2** kalemidir.
- ⚠️ **Yan bulgu (KİRAZ):** platform'un KR-024 tablosu `| Kiraz | 14-21 |` satırını taşıyor; contract
  `crop_type.enum.v1` **CHERRY tanımıyor**. Tablo **sadakatle** alındı, çelişki gizlenmedi →
  KG-0.d-EK kararı artık **üç** kaynağı bağlıyor (`crop_readiness.json` · wire enum · SSOT KR-024).
- ⚠️ Kaynaktaki `## # [KR-033]` yazım hatası **bilerek düzeltilmedi** (bayt-özdeşlik korunsun);
  platform tarafında düzeltilirse contract kopyası aynı turda güncellenir.
- **Doğrulama:** `validate.py` 89 dosya / 0 hata · `pytest` **589 geçti (+10 yeni)** · iki kopya
  `cmp` ile **bayt-özdeş** ✅.

---

## [7.2.0] - 2026-07-14

**Feature:** intake_manifest.v1 — edge/AV1 karantina görünürlüğü (İş Kolu B2)
**Breaking-change:** HAYIR (MINOR — iki opsiyonel top-level alan; `required` değişmedi)

Edge/AV1 istasyonu, CLEAN olmayan dosyaları manifest emit edilmeden ÖNCE yerelde düşürür; bu dosyalar `files[]`'a hiç girmediği için platform bugüne kadar edge-karantinasını **göremiyordu**. İki opsiyonel sayaç bu boşluğu kapatır — platform admin panosunda >0 iken DAİMA uyarı olarak yüzeye çıkarılır. Merkez/AV2 `REJECTED_QUARANTINE` (dataset durumu) sinyalinden ayrıdır.

### Added

- **`schemas/edge/intake_manifest.v1.schema.json` (EdgeForm + PlatformForm):** iki opsiyonel top-level alan — `quarantined_file_count` (integer ≥ 0) + `quarantined_bytes` (integer ≥ 0). `required` listeleri **DEĞİŞMEDİ**; `unevaluatedProperties: false` korunur → additive MINOR. Her iki formda simetrik (edge üretir, platform tüketir; worker etkilenmez).

### Notes

- **Checksum:** şema değiştiği için re-pin → yeni CONTRACTS_VERSION.md checksum (7.1.0 → 7.2.0). Consumer'lar (edge, platform) re-pin etmeli; worker pin'i değişmez.
- **Doğrulama:** `python -X utf8 tools/validate.py && python -X utf8 -m pytest tests/ -q` + `python -X utf8 tools/pin_version.py --verify`.

---

## [7.1.0] - 2026-07-13

**Feature:** analysis_result.v1 — top-level `tile_counts` (KR-088 çiftçi ön-raporu)
**Breaking-change:** HAYIR (MINOR — opsiyonel obje)

`analysis_result.v1`'e top-level `tile_counts {total, healthy, anomaly}` objesi eklendi (KR-088 çiftçi ön-raporu "kaç kare sağlıklı / kaç kare sorunlu" sinyali). Kaynak: worker `PipelineResponse.tile_count_total/healthy/anomaly`. Opsiyonel/geriye-uyumlu (pre-v7.1.0 üreticiler + `NO_RESULT` atlar), `unevaluatedProperties: false`. AK-4 worker→kanonik ayna (worker v7.1.0'da önden landledi). Ayrıca `tools/sync_to_repos.sh` `sync_to_worker()` salt-okunur drift dedektörüne dönüştürüldü (canonical→worker kopya worker'ın ileri formunu ezerdi).

---

## [7.0.1] - 2026-07-12

**Fix:** KR-018 bant-gate iç-tutarlılık düzeltmeleri + breaking migration guide Rollback bölümü
**Breaking-change:** HAYIR (PATCH — yalnız metadata/açıklama/doküman/test/tooling; hiçbir enum değeri eklenmedi/kaldırılmadı/yeniden adlandırılmadı)

18-ajan bağımsız denetiminde (SW/QA/Pentest/SDLC/ML/DL perspektifleri) doğrulanan bulguların çözümü. Odak: bant-gate tek-kaynak modelini iç-tutarlı hale getirmek — kesişim kuralı DJI_M350 termal varyantı türetemiyordu (LWIR `supported_bands`'te değil, `thermal_variant.thermal_bands`'te) ve THERMAL_STRESS yalnız `[LWIR]` isteyerek CWSI/canopy-soil delta'nın vejetasyon bağlamını atlıyordu; ayrıca drone_type Parrot açıklaması matrisle çelişiyordu.

### Changed

- **`enums/analysis_type.enum.v1.json` v1.4.0 → v1.4.1:** `byLayer.THERMAL_STRESS.requires_bands` `["LWIR"]` → `["GREEN","RED","RED_EDGE","NIR","LWIR"]` (tam set — CWSI/canopy-soil delta için vejetasyon bağlamı fiziksel olarak gerekli; üretilebilen drone kümesi değişmez — tüm termal droneler 4 multispektral bandı da taşır). `bandRequirements.description` kesişim kuralı netleştirildi: `requires_bands ⊆ effective_bands`, `effective_bands = supported_bands ∪ (termal payload takılıysa thermal_variant.thermal_bands)` — DJI_M350_RTK_SENTERA_6X termal varyant örneğiyle. `enforcement: advisory` notu eklendi (repo içi CI-gate yok; tüketici tarafında uygulanır). `cross_reference` `thermal_variant.thermal_bands` içerecek şekilde güncellendi. Enum `enum` dizisi (11 kod) **DEĞİŞMEDİ**.
- **`enums/drone_type.enum.v1.json`:** `PARROT_ANAFI_USA_SEQUOIA_PLUS` açıklamasından yanlış "+ termal" ibaresi kaldırıldı — `drone_capability_matrix.yaml` (KR-018 bant-gate SSOT) Parrot'ta LWIR/thermal indeksi tanımlamaz; Sequoia+ multispektral-only. `x-registry-sync.capability_matrix` çapraz-referansı `effective_bands = supported_bands ∪ thermal_variant.thermal_bands` kuralıyla hizalandı (analysis_type ile tutarlı). `x-updated` "2026-02-24" → "2026-07-12" (6.2.0'da içerik değişmişti, tarih güncellenmemişti). Enum `enum` dizisi (5 model) **DEĞİŞMEDİ**.

### Fixed

- **`tools/breaking_change_detector.py`:** dedektör yalnız `schemas/`'ı tarıyordu; `enums/` diff'i eklendi — kaldırılan/yeniden-adlandırılan enum üyeleri artık MAJOR breaking olarak raporlanır (enum breaking değişiklikleri artık görünmez değil).
- **`tools/sync_to_repos.sh`:** worker senkron listesine `phenology_stage.enum.v1.json` eklendi (7.0.0 MAIZE_*→CORN_* hizalaması worker'a gitmeliydi); bayat `schemas/enums/` yolu repo gerçeği `enums/` ile düzeltildi.

### Added

- **`docs/migration_guides/phenology_stage_maize_to_corn.md`:** `## Rollback` bölümü eklendi — breaking migration guide'lar için politika gereği zorunlu (`docs/versioning_policy.md`, `docs/checklists/SDLC_GATES.md`, `docs/migration_guides/README.md`).
- **`tests/test_validate_all_schemas.py`:** `phenology_stage` 14-değer set assertion'ı (residüel MAIZE_* token yok doğrulaması dahil); `analysis_type.bandRequirements.byLayer` bütünlük testi (anahtarlar == enum kümesi; requires_bands ⊆ bant sözlüğü; availability ∈ availabilityValues).

### Notes

- **Checksum:** enum metadata değiştiği için re-pin yapıldı → yeni CONTRACTS_VERSION.md checksum. Consumer'lar 7.0.0 → 7.0.1'e re-pin etmeli (breaking değil; salt doğrulama hash'i güncellenir).
- **Doğrulama:** `python -X utf8 tools/validate.py && python -X utf8 -m pytest tests/ -q` + `python -X utf8 tools/pin_version.py --verify`.

---

## [7.0.0] - 2026-07-12

**Feature:** phenology_stage `MAIZE_* → CORN_*` rename — son kalan MAIZE kalıntısının temizliği
**Breaking-change:** EVET (MAJOR — enum değeri rename)

`crop_type` v3.0.0'da `MAIZE → CORN` yapılmıştı (contract v5.0.0); kanonik mahsul değeri artık tüm repolarda `CORN`. `phenology_stage` **son kalan MAIZE kalıntısıydı** — evre kodları eski mahsul ön ekiyle ad-uzaylıydı (`MAIZE_EMERGENCE_V5`, …). O rename bilinçli ertelenmişti (bkz. `crop_type_maize_to_corn.md`) çünkü `PhenologyStage` ayrı bir enum'dur ve platform fenoloji profillerini **`crop_type` üzerinden alias-normalizasyonuyla** çözer (`_normalize_crop`: `MAIZE → CORN`), yani `CORN` mahsulü hâlâ `MAIZE_*` evrelerini buluyordu — aktif kırık yoktu. Bu sürüm o tutarlılık boşluğunu kapatır: evre-kodu ön eki artık kanonik `crop_type` değeriyle (`CORN_*`) birebir. Saf rename — evre eklenmedi/kaldırılmadı.

### Changed

- **`enums/phenology_stage.enum.v1.json`:** 4 evre kodu yeniden adlandırıldı — `MAIZE_EMERGENCE_V5→CORN_EMERGENCE_V5`, `MAIZE_V6_PRETASSEL→CORN_V6_PRETASSEL`, `MAIZE_TASSEL_SILK→CORN_TASSEL_SILK`, `MAIZE_GRAINFILL→CORN_GRAINFILL`. `x-enum-descriptions` anahtarları + `x-stage-order` `"MAIZE"→"CORN"` anahtarı ve değerleri + top-level `description` ad-uzayı örneği re-key edildi; `x-breaking-change` notu eklendi. Küme boyutu **14** (GRAPE_*/OLIVE_* DEĞİŞMEDİ). Türkçe açıklama metinleri ("Mısır — …") değişmedi.
- **`enums/crop_type.enum.v1.json`:** `metadata.changeNote` içindeki artık yanlış "`phenology_stage.enum.v1.json MAIZE_* stage codes remain unchanged`" ibaresi "subsequently aligned to `CORN_*` in contract v7.0.0" olarak düzeltildi. `enum` dizisi (8 mahsul) + tüm diğer metadata **DEĞİŞMEDİ** — bu yalnız tarihsel-kayıt düzeltmesidir.

### Added

- **`docs/migration_guides/phenology_stage_maize_to_corn.md`:** yeni göç kılavuzu (gerekçe, before/after tablo, etkilenen tüketiciler, gerekli aksiyonlar, doğrulama).

### Notes

- **`schemas/core/phenology_flight_profile.v1.schema.json` düzenlenmedi:** enum'a `$ref` ile bağlanır, `MAIZE_*` string'i sabit-kodlamaz → renamed kodlara otomatik uyumlu.
- **Repo içi örnek JSON yok:** hiçbir örnek `MAIZE_*` değeri taşımıyor (grep ile doğrulandı) → güncellenecek örnek yok.
- **Worker koordinasyonu (KRİTİK):** worker `phenology_stage` tüketiyorsa aynı turda `CORN_*`'a hizalanmalıdır; aksi halde `MAIZE_*` emit/bekleyen worker renamed enum'a karşı validasyonda kırılır. Bu, contract'ın worker'ı etkileyebilecek tek breaking maddesidir.
- **Consumer etkisi:** Platform/Edge/Worker pin 6.2.0 → 7.0.0'a güncellenmelidir; MAJOR olduğundan tüketici koordinasyonu gerekir. Geçiş penceresi gerekiyorsa inbound `MAIZE_*` `CORN_*`'a normalize edilir, outbound asla `MAIZE_*` emit etmez.
- **Doğrulama:** `python -X utf8 tools/validate.py && python -X utf8 -m pytest tests/ -q` + `python -X utf8 tools/pin_version.py --verify`.

---

## [6.2.0] - 2026-07-12

**Feature:** KR-018 bant-gate tek-kaynak (analysis_type ↔ drone bant kesişimi) + payment_status v1 deprecation
**Breaking-change:** HAYIR (MINOR — yalnız metadata eklemeleri; hiçbir enum değeri eklenmedi/kaldırılmadı/yeniden adlandırılmadı)

Platform tarafı contract önerilerinin (Öneri 4/5/7a) güvenli/non-breaking grubu. Amaç: KR-018 bant-kapısı (kalibrasyonsuz/eksik bant → katman üretilemez) mantığını contract-kanonik + tekil kaynaktan türetilir kılmak, ve zaten-tüketilmeyen payment_status v1'i açıkça emekliye ayırmak. Öneri 2 (PENDING_RECEIPT) platform-side (B) karar → contract değişmez. Öneri 3 (drone kısa↔tam anahtar) + Öneri 6 (IL_OPERATOR) yalnız teyit; contract zaten kanonik.

### Added

- **`enums/analysis_type.enum.v1.json` v1.3.0 → v1.4.0:** `metadata.bandRequirements` eklendi — her 11 map-layer için `requires_bands` (minimum bantlar) + `availability` durumu. Kesişim kuralı: `analysis_type.requires_bands ⊆ drone_capability_matrix.yaml[drone].supported_bands` ise katman o drone ile üretilebilir. `THERMAL_STRESS` → `requires_thermal_payload` (LWIR; yalnız DJI_M350 termal varyant + AGEAGLE_EBEE_X_ALTUM_PT; Mavic 3M'de üretilemez). `BENEFICIAL` → `enum_valid_not_yet_emittable` (model olgunlaşınca aktifleşir). Enum `enum` dizisi (11 kod) **DEĞİŞMEDİ**.
- **`enums/drone_type.enum.v1.json` `x-registry-sync`:** `capability_matrix` çapraz-referansı eklendi (`drone_capability_matrix.yaml` → supported_bands/band_class/available_indices/calibration_class). `add_model_flow` capability-matrix adımını içerecek şekilde güncellendi. Not: matris zaten mevcuttu; bu değişiklik yalnız enum'dan matrise keşfedilebilir bağ kurar.

### Changed

- **`enums/payment_status.enum.v1.json`:** `x-deprecated` bloğu eklendi (`since: 6.2.0`, `replaced_by: payment_status.enum.v2.json`). Gerekçe: v2 kanoniktir (REFUNDED + PENDING_ADMIN_REVIEW); v1'in repo içi `$ref` tüketicisi yoktur (payment_intent.v1 — kendisi DEPRECATED — status değerlerini inline yazar). Enum `enum` dizisi **DEĞİŞMEDİ**; kaldırma değil, yalnız deprecation işareti.

### Notes

- **Öneri 5 zaten karşılanmıştı:** `drone_capability_matrix.yaml` bant/kapasite matrisi (supported_bands, band_classes, available_indices) halihazırda contract-kanonik olduğundan yeni matris **oluşturulmadı**; yalnız enum'dan çapraz-link eklendi.
- **Öneri 2 = (B) platform-side:** "dekont bekleniyor" ara durumu contract'ta ayrı modellenmez; platform `PENDING_RECEIPT` yerine `PAYMENT_PENDING` kullanır. Contract enum'u (v2) kanonik/şişmeden kalır.
- **Consumer etkisi:** Platform/Edge/Worker pin 6.1.0 → 6.2.0'a güncellenmelidir; tüm değişiklikler metadata olduğundan hiçbir üretici/tüketici bozulmaz (wire davranışı değişmez).
- **Doğrulama:** `python -X utf8 tools/validate.py && python -X utf8 -m pytest tests/ -q` + `python -X utf8 tools/pin_version.py --verify`.

---

## [6.1.0] - 2026-07-12

**Feature:** BENEFICIAL (faydalı böcek / doğal düşman) zengin alt-uzmanlık yuvası + result-rich-axis (analysis_result.Detection) worker → kanonik AYNA
**Breaking-change:** HAYIR (MINOR — 1 yeni enum değeri + 2 yeni opsiyonel alan, geriye uyumlu)

Worker'ın v6.1.0 (BENEFICIAL + result-rich-axis, PR #147) additive değişikliklerinin kanonik SSOT aynası (AK-4 uzlaşma; devir spec: worker `denetim/beneficial_ve_sonuc_ekseni_devir_spec_2026_07_11.md`). İki parça: (1) `BENEFICIAL` zengin taksonomi değeri (5.1.0'da aynalanan sub_specialty ekseninin 11. kodu), (2) sub_specialty/detection_type zengin ekseninin `analysis_result.Detection`'a landing'i (5.1.0 yalnız escalation/kart hattını — expert_review_queue + expert_labeling_card — aynalamıştı; sonuç/çiftçi hattı bu sürümde tamamlanır).

### Added

- **`enums/analysis_type.enum.v1.json` v1.2.0 → v1.3.0:** `BENEFICIAL` eklendi (enum + `layerMapping` + `analysisCategories.MAP_LAYERS.types` + `analysisDescriptions` + `displayNames.tr`/`en`). KR-002 renk/deseni **Turkuaz (Teal) + doğal düşman ikonu** worker önerisinden benimsendi (kanonik = KR-002 SSOT; worker'ın `[ÖNERİ — pending]` niteleyicisi kanonikte anlamsız olduğu için düşürüldü). Kaba↔zengin ekseni: BENEFICIAL zengin (rich) eksende yaşar; kaba `detection_type` (disease/pest/weed/abiotic) DEĞİŞMEZ.
- **`schemas/worker/analysis_result.v1.schema.json` `$defs.Detection`:** 2 yeni opsiyonel alan — `sub_specialty` (zengin 11-kod enum, null default) + `detection_type` (kaba 4-kod enum, null default). `unevaluatedProperties:false` korunur; `required` (`confidence`) DEĞİŞMEZ. Farmer-facing sonuç, escalation kuyruğunun taşıdığı aynı zengin ekseni kazanır.

### Changed

- **`schemas/worker/expert_labeling_card.v1.schema.json` v2.6.0 → v2.7.0:** `sub_specialty` enum'una `BENEFICIAL` eklendi (10 → 11 kod). additionalProperties/required/allOf DEĞİŞMEZ.
- **`schemas/worker/expert_review_queue.v1.schema.json`:** `sub_specialty` enum'una `BENEFICIAL` eklendi (10 → 11 kod); açıklama "11 codes incl. BENEFICIAL" + BENEFICIAL'in parite-için-geçerli-ama-henüz-emit-edilemez notu.
- **`tests/test_validate_all_schemas.py`:** `test_analysis_type_enum_canonical` beklenen küme 10 → 11 (`BENEFICIAL` eklendi).

### Notes

- **crop_type DOKUNULMADI:** `crop_type` enum'u (8 mahsul, CORN-kanonik) bu bump'ın KAPSAMI DIŞINDA — ayrı/bağımsız bir konudur. Bu sürüm yalnız analysis_type zengin eksenini + result-rich-axis'i taşır.
- **BENEFICIAL henüz emit edilemez:** Hiçbir model faydalı böcek/doğal düşman tespiti üretmez; BENEFICIAL enum'da parite (worker↔kanonik senkron) için vardır, worker `NaturalEnemyService` çıktısı ayrı ekosistem-durum yüzeyindedir (tespit değil). HEALTH gibi, escalation/detection asla BENEFICIAL emit etmez.
- **Consumer etkisi:** Platform/Edge/Worker pin 6.0.1 → 6.1.0'a güncellenmelidir; yeni alanlar opsiyonel olduğundan mevcut üreticiler/tüketiciler bozulmaz (pre-rich producer'lar alanı omit eder = null). **Deploy sırası:** platform şema aynası worker rich-alan emit etmeye başlamadan ÖNCE yayılmalıdır (platform `worker_bridge_consumer` enforce=True ise bilinmeyen alanı nack→DLX yapabilir).
- **Doğrulama:** `python tools/validate.py && pytest tests/ -q` + `python tools/pin_version.py --verify`.

---

## [6.0.1] - 2026-07-11

**Breaking-change:** HAYIR (PATCH — yalnızca metadata/docs)

crop_type enum'undan `metadata.archived` bloğu (HAZELNUT + RED_LENTIL) **tamamen kaldırıldı**. Gerekçe: kullanıcı direktifi — mercimek (LENTIL/RED_LENTIL/KIRMIZI_MERCIMEK) ve fındık (HAZELNUT) için **arşiv dâhil hiçbir yerde kalıntı tutulmaz**. Enum `enum` dizisi **DEĞİŞMEDİ** (8 mahsul: COTTON, PISTACHIO, CORN, WHEAT, SUNFLOWER, GRAPE, OLIVE, RICE); değer kümesi değişmediği için bu bir metadata/docs değişikliğidir = **PATCH**. Kaldırma-kaydı (provenans) enum `changeNote` + `docs/migration_guides/crop_type_red_lentil_removal.md` içinde **KORUNUR** (audit trail).

### Changed

- **`enums/crop_type.enum.v1.json` v4.0.0 → v4.0.1:** `metadata.archived` bloğu silindi (HAZELNUT + RED_LENTIL girdileri); `changeNote`'taki "`RED_LENTIL` moves to `metadata.archived`" ibaresi "no `metadata.archived` entry retained" olacak şekilde uzlaştırıldı. `enum` dizisi, `aliases`, `displayNames`, `categories`, `gapPriorities`, `worker_alignment` DEĞİŞMEDİ.
- **`docs/migration_guides/crop_type_red_lentil_removal.md`:** iki düzeltme — (1) "moves to `metadata.archived`" cümlesi, arşiv tutulmadığını (migration guide + changeNote'un removal-record-of-record olduğunu) yansıtacak şekilde güncellendi; (2) "Required consumer actions" bölümündeki YANLIŞ "immutable Postgres ENUM (`KIRMIZI_MERCIMEK`…) → ileriye dönük enum-değeri düşürme worker-koordineli ayrı DB migration (COORDINATE)" çerçevesi kaldırıldı → gerçek: enum `2026_04_04_align_expert_schema_to_worker.py`'de zaten VARCHAR(50)'e çevrildi + `DROP TYPE crop_type`, canlı ENUM/forward migration YOK, kalan endişe yalnızca veri-seviyesi read-only audit'tir (aşağıdaki Notes ile tutarlı). Bu ikinci düzeltme root docs-inclusive aggregate'i `56bf11f2…`→`005b579e…` değiştirir (submodule aggregate `957e9904…` docs HARİÇ olduğu için etkilenmez).

### Notes

- **6.0.0 notundaki DÜZELTME (KESİN KURAL — latent tutarsızlık bırakılmaz):** 6.0.0 girişinin "Immutable DB residue (COORDINATE) — ileriye dönük enum-değeri düşürme worker ile eşgüdümlü ayrı bir DB migration'ıdır" notu **YANLIŞTI**. Gerçek: platform tarafındaki `alembic/versions/2026_04_04_align_expert_schema_to_worker.py` Postgres `crop_type` ENUM'unu **zaten VARCHAR(50)'e çevirdi** (6 kolon, `_enum_to_varchar`), değerleri remapladı ve `DROP TYPE IF EXISTS crop_type` çalıştırdı → **canlı ENUM yok, ileriye dönük DB migration GEREKMİYOR.** Geriye yalnız uygulanmış/immutable migration'ların tarihsel DDL metni kalır (tarih, canlı kalıntı değil). Durum: **RESOLVED**, COORDINATE değil.
- **Consumer etkisi:** Platform/Edge/Worker pin 6.0.0 → 6.0.1'e güncellenmelidir; runtime davranışı değişmez (enum değer kümesi aynı) — yalnızca sürüm-string + per-dosya hash + aggregate güncellenir.
- **Doğrulama:** `python tools/validate.py && pytest tests/ -v` (`test_crop_type_enum_matches_gap_canonical` 8-kümeyi assert eder, arşiv kaldırma kırmaz) + `python tools/pin_version.py --verify`.

---

## [6.0.0] - 2026-07-11

**Breaking-change:** EVET (MAJOR — enum değeri kaldırma)

crop_type `RED_LENTIL` kaldırıldı. Gerekçe: worker `LENTIL` (Mercimek) değerini kendi crop-sözlüğünden düşürüyor; contract bunu aynalayarak worker'la %100 senkron kalır (latent/uykuda ayrışma bırakılmaz). `RED_LENTIL`, worker/platform `LENTIL` değerine `metadata.aliases` (`RED_LENTIL↔LENTIL`) ile köprülenen GAP-kanonik yazımdı; bu çapraz-repo alias'ı emekli edildi ve `RED_LENTIL` `metadata.archived`'a taşındı. Kaldırma sonrası GAP kümesi **8 mahsul** (COTTON, PISTACHIO, CORN, WHEAT, SUNFLOWER, GRAPE, OLIVE, RICE). Migration: `docs/migration_guides/crop_type_red_lentil_removal.md`.

### Changed (breaking)

- **`enums/crop_type.enum.v1.json` v3.0.0 → v4.0.0:** enum'dan `RED_LENTIL` çıkarıldı; `gapPriorities`, `categories` (LEGUMES bloğu tümüyle kaldırıldı), `displayNames.tr`/`displayNames.en` `RED_LENTIL` girdileri silindi; `metadata.aliases`'ten `"RED_LENTIL": ["LENTIL"]` kaldırıldı; `metadata.archived`'a `RED_LENTIL` girdisi eklendi; `notes.worker_alignment` v4.0.0 kaldırma notuna güncellendi.
- crop_type ayna/inline kopyaları 8-kümeye hizalandı: `schemas/worker/expert_review_queue.v1.schema.json` (inline enum + "GAP 8-crop set" açıklaması), `api/components/schemas.yaml`, `api/components/parameters.yaml`, `api/components/responses.yaml` (örnek hata mesajı), `schemas/worker/analysis_job.v1.schema.json` + `analysis_result.v1.schema.json` (açıklamadan `RED_LENTIL↔LENTIL` alias ibaresi kaldırıldı).
- Dokümanlar: `docs/README.md` ("8 GAP crops"), `docs/examples/README.md` ("8 GAP Crops Only"); testler: `tests/test_validate_all_schemas.py` + `tests/test_examples_match_schemas.py` beklenen küme 9→8.

### Notes

- **Consumer etkisi:** Platform/Edge/Worker pin 5.1.0 → 6.0.0'a güncellenmelidir; `RED_LENTIL` crop dropdown/routing/pricing/model-sözlüğünden kaldırılmalı, gelen `crop_type = RED_LENTIL` payload'ları 422 `allowed_crop_types` ile reddedilmelidir.
- **Immutable DB residue (COORDINATE):** Platform tarafında uygulanmış bir Alembic migration'ının Postgres ENUM DDL'i hâlâ `KIRMIZI_MERCIMEK` değerini taşır; ileriye dönük enum-değeri düşürme worker ile eşgüdümlü ayrı bir DB migration'ıdır (bu contract bump'ının parçası değildir).
- **Doğrulama:** `python tools/validate.py && pytest tests/ -v` (`test_crop_type_enum_matches_gap_canonical` 8-kümeyi assert eder) + `python tools/pin_version.py --verify`.

---

## [5.1.0] - 2026-07-11

**Feature:** Alt-uzmanlık (sub_specialty / detection_type) worker → kanonik AYNA
**Breaking-change:** HAYIR (MINOR — 3 yeni opsiyonel alan, geriye uyumlu)

Worker escalation/kart hattının additive alt-uzmanlık eksenini kanonik şemalara aynalar (AK-4 vendored/override deseninin kanonik-taraf tamamlaması). Worker bu alanları hash-kapılı vendored kopyasına ÖNCEDEN eklemişti (worker kendi bağımsız v5.2.0/v5.3.0 şemasıyla — bkz. worker CONTRACTS_VERSION "version scheme note": worker'ın 5.x'i kanonik SemVer'den bilinçli decoupled, numaralar eşleşmek zorunda DEĞİL, crop-sözlüğü AK-4 köprüsüyle uzlaşılır). Bu sürüm alanları kanonik SSOT'a landler; yeni enum dosyası YAZILMAZ (değer kümesi `enums/analysis_type.enum.v1.json` v1.2.0'da zaten var, 10 kod).

### Added

- **`schemas/worker/expert_review_queue.v1.schema.json`:** iki opsiyonel alan.
  - `detection_type` (C-1, kaba): `["string","null"]`, enum `disease/pest/weed/abiotic/null`. Worker'ın TAHMİN ettiği ham kart kategorisi (lowercase); platform CONFIRMED kayıtları bununla katmanlar. `analysis_type`'tan (İSTENEN, uppercase) AYRIDIR.
  - `sub_specialty` (C-1 RICH, additive): `["string","null"]`, enum = `analysis_type.enum.v1.json`'un 10 kodu + null. Worker'ın TAHMİN ettiği zengin alt-uzmanlık; `detection_type`'ın YANINDA çalışır (kaba eksen korunur).
- **`schemas/worker/expert_labeling_card.v1.schema.json`:** opsiyonel `sub_specialty` (v2.6.0) — kaba `category` ekseninin zengin ADDITIVE tamamlayıcısı. `category`/`required`/`allOf` ve `additionalProperties` mührü DEĞİŞMEZ.

### Notes

- **Non-breaking:** üç alan da opsiyonel, default null; migrasyon-öncesi üreticiler atlar → hiçbir tüketici kırılmaz (`breaking_change_detector`: 0 breaking / 3 optional-field-added).
- **KR-071:** üç alan da enum-kısıtlı sınıflandırma etiketi; PII taşımaz, `unevaluatedProperties/additionalProperties:false` mührünü genişletmez.
- **KR-002 / SSOT:** zengin değer kümesi `analysis_type.enum.v1.json` (v1.2.0, KR-002 harita-katmanı taksonomisi) — kanonikte zaten mevcut, byte-parity korunur.
- **Consumer etkisi:** Platform pin 5.0.0 → 5.1.0'a güncellenmelidir. Worker vendored kopyası kendi bağımsız şemasında kalır (numara-uzlaşımı gerekmez — bilinçli decoupled).
- **training.feedback (`rich_sub_specialty`):** worker C-3 alanı hash-kapılı DEĞİL, KR-032 additive → kanonik şema-bump YOK; yalnız platform tüketicisi okur.

---

## [5.0.0] - 2026-07-06

**Breaking-change:** EVET (MAJOR — enum değeri yeniden adlandırma)

crop_type `MAIZE` → `CORN` olarak yeniden adlandırıldı. Gerekçe: kanonik `CORN` değerini platform CropType VO'su (`src/core/domain/value_objects/crop_type.py`) ve worker CropType enum'u (`src/core/domain/enums.py`) zaten kullanıyordu; contract bunu `MAIZE` tutan **tek** repoydu. Bu rename `CORN`'u tüm repolarda tek kanonik değer yapar ve `MAIZE`'i yalnız-okuma legacy interop alias'ına indirir. Migration: `docs/migration_guides/crop_type_maize_to_corn.md`.

### Changed (breaking)

- **`enums/crop_type.enum.v1.json` v2.1.0 → v3.0.0:** enum değeri MAIZE→CORN; displayNames CORN'a yeniden anahtarlandı (tr "Mısır", en "Corn (Maize)"); `metadata.aliases` ters çevrildi (`"CORN": ["MAIZE"]`).
- crop_type ayna/inline kopyaları CORN'a hizalandı: `schemas/worker/expert_review_queue.v1.schema.json`, `api/components/schemas.yaml`, `api/components/parameters.yaml`, `api/components/responses.yaml` (örnek hata mesajı), `schemas/core/seasonal_flight_calendar.v1.schema.json` (açıklama), `schemas/worker/analysis_job.v1.schema.json` + `analysis_result.v1.schema.json` (açıklama).

### Deferred (bu sürümde YAPILMADI — ayrı breaking görevler)

- `RED_LENTIL` kanonik kaldı (worker/platform sözlüğü LENTIL); `RED_LENTIL↔LENTIL` alias korunur.
- `phenology_stage.enum.v1.json` `MAIZE_*` evre kodları değişmedi (ayrı enum; tüketiciler fenolojiyi crop_type alias-normalizasyonuyla çözer → kırılmaz).

### Notes

- **Consumer etkisi:** kanonik değer değişti → tüm tüketiciler CORN'a hizalanmalı; inbound `MAIZE` normalize edilerek kabul edilmeli, outbound `MAIZE` yayılmamalı. Platform pin 4.4.0 → 5.0.0'a güncellenmelidir.

---

## [4.4.0] - 2026-07-06

**Feature:** KR-093 — Çiftçi Ön Raporu (İki-Fazlı Teslimat: PRELIMINARY → FULL)
**Breaking-change:** HAYIR (MINOR — yeni enum + yeni event şeması, geriye uyumlu)

Çiftçiye uzman onayından ÖNCE (KR-019 kapısıyla PARALEL) yalnız indeks katmanlarını taşıyan bir "ön rapor" fazının sözleşme yüzeyi. Kanonik normatif metin platform SSOT'undadır (`docs/TARLAANALIZ_SSOT_v1_2_0.txt` KR-093 + ADR-007); bu sürüm yalnızca contract yüzeyini ekler. KR-019 tam-rapor konsensüs kapısı DEĞİŞMEZ — ön faz tespit (hastalık/zararlı/ot) taşımaz (fail-closed).

### Added

- **Enums:** `enums/report_phase.enum.v1.json` (ReportPhase) — `["PRELIMINARY","FULL"]`. Teslim onay fazı; `mission.status`'tan TÜRETİLİR (ayrı state değil). `result_mode` (sensör-bandı fail-closed modu) ve `report_tier` (bant kalite sınıfı) ile KARIŞTIRILMAZ — üç bağımsız eksen.
- **Events:** `schemas/events/analysis_preliminary_ready.v1.schema.json` (AnalysisPreliminaryReadyEvent) — nested-envelope wire olayı (`analysis.preliminary_ready`). PII'siz data: `analysis_result_id`, `mission_id`, `field_id`, `dataset_id?`, `report_phase` (const `PRELIMINARY`), `report_tier?`. Platform worker→platform bridge tarafından `analysis.review_requested` ile PARALEL yayınlanır (üretici Faz 1'de eklenecek; şema lifecycle=DRAFT). Telefon/PII wire'a girmez (KR-050/KR-071).
- **Examples:** `docs/examples/analysis_preliminary_ready.example.json` (+ örnek→şema haritası + README girdisi).

### Notes

- **Consumer etkisi:** Yeni enum + yeni event şeması → mevcut tüketiciler için kırıcı değildir; min-contract korunur. Platform pin 4.3.0 → 4.4.0'a güncellenmelidir.
- **Governance:** KR-019 (uzman konsensüs yayın kapısı) mantığı DOKUNULMADI; KR-093 bu kapının ÖNÜNE faz ekler, zayıflatmaz. Bkz. platform `docs/adr/ADR-007-preliminary-farmer-view.md`.

---

## [4.3.0] - 2026-07-05

**Feature:** KR-092 — Fenolojik/Sezonluk Uçuş Parametreleri (İrtifa & Hız)
**Breaking-change:** HAYIR (MINOR — yeni şema + yeni enum değeri, geriye uyumlu)

Bir görevin uçuş yüksekliği (Y) ve hızı (v) değerlerini bitki türü + sezon haftasına göre türeten haftalık sezon takviminin sözleşme yüzeyi. Kanonik normatif metin platform SSOT'undadır (`docs/TARLAANALIZ_SSOT_v1_2_0.txt` KR-092); bu sürüm yalnızca contract yüzeyini ekler.

### Added

- **Core:** `schemas/core/seasonal_flight_calendar.v1.schema.json` (SeasonalFlightCalendar) — bitki × haftalık (week, date_start/date_end MM-DD, bbch, altitude_m ≤120, speed_ms, critical) sezon takvimi şeması. Fiziksel/mevzuat sınırları (H/v ≥ 3,9, ≤120 m AGL) domain katmanında fail-closed doğrulanır. Kaynak: `tarama_protokolu_v1.6` §10.
- **Enums:** `crop_type` enum'una `RICE` (Çeltik) eklendi (enum v2.0.0 → **2.1.0**, MINOR/non-breaking). KR-092'nin 5 aktif GAP ürününden biri (COTTON/MAIZE/RICE/GRAPE/PISTACHIO). Karacadağ/Şanlıurfa çeltiği GAP'ta yetişir; worker Stage-2 modeli kalibre açık veri gelene kadar `blocked_by_data` (KR-018 hard-gate).
- **SSOT:** `ssot/kr_registry.md` KR-092 girdisi (amaç, MUST, kanıt, hata modları, kabul kriterleri, cross-refs).

### Changed

- `crop_type` ayna kopyaları (inline enum'lar) 9-ürün setine hizalandı: `schemas/worker/expert_review_queue.v1.schema.json`, `api/components/schemas.yaml`, `api/components/parameters.yaml`, `api/components/responses.yaml` (örnek hata mesajı).

### Notes

- **Adlandırma:** Contracts kanonik `MAIZE` korunur; SSOT/platform/worker sözlüğündeki `CORN` bunun alias'ıdır (`crop_type.metadata.aliases: MAIZE↔CORN`). `RICE` her iki tarafta da aynı addır.
- **Consumer etkisi:** Yeni şema + yeni enum değeri → mevcut tüketiciler için kırıcı değildir; min-contract korunur. Platform pin 4.2.1 → 4.3.0'a güncellenmelidir.

---

## [4.2.1] - 2026-06-26

**SYNC:** Kardeş contracts reposu (rebrand edilmiş üst-akış, 4.2.1) ile tam eşitleme (back-port)  
**Breaking-change:** EVET — yapısal absorpsiyon (2.1.0 -> 4.2.1). Migration: `docs/migration_guides/contracts_3_0_0_structural_absorption.md`

Bu sürüm, kardeş contracts reposu (TarlaAnaliz'den rebrand edilmiş, daha ileri sürüm) ile özellik eşitlemesidir. Marka (`tarlaanaliz`/GAP), bitki türü adlandırması (MAIZE/RED_LENTIL korundu; Ege'ye özel CHERRY/FIG/APPLE/PEACH **alınmadı**) ve bölge farkları (Tariş/Ege -> GAP) korunarak uygulanmıştır. TarlaAnaliz yalnızca GAP bölgesine hizmet eder; bu nedenle **HAZELNUT (Fındık) kaldırılmıştır** (Karadeniz bitkisi, GAP'ta yetişmez).

### Removed (breaking)

- **`crop_type` enum HAZELNUT kaldırıldı** (enum v2.0.0). Fındık GAP bölgesinde yetişmez; orijinal sette hatalı yer alıyordu. Crop seti 9 → 8'e indi. Migration: `docs/migration_guides/crop_type_hazelnut_removal.md`. Etki: `crop_type` kullanan tüm şemalar (Field, Mission, Pricing, AnalysisJob/Result, expert_review_queue) + api enum'ları.

### Added

- **Worker:** `calibrated_dataset`, `calibration_metadata`, `expert_feedback`, `expert_labeling_card`, `expert_review_queue` şemaları.
- **Edge:** `attestation_record`, `calibrated_dataset_manifest`, `evidence_bundle_ref`, `upload_receipt`, `worker_result` şemaları.
- **Events:** `analysis_review_requested`, `dataset_quarantined`, `dataset_unquarantined`, `expert_review_decided`.
- **Core:** `phenology_flight_profile`; **Enums:** `phenology_stage` (GRAPE/MAIZE/OLIVE), `edge_custody_event`.
- **Tools:** `check_no_egeanaliz.py` marka guard'ı (CI + `npm run validate:brand`); `read_contracts_version`, lifecycle-chain testleri.
- **Docs:** expert-review/worker/yield örnekleri, `contracts_3_0_0_structural_absorption.md`, `subscription_lifecycle.md`.

### Changed

- Tüm şema/enum/api/ssot dosyaları üst-akış 4.2.1 içeriğine hizalandı (marka/$id `api.tarlaanaliz.com` korunarak).
- `phenology_stage`: `CORN_*` kodları `MAIZE_*` olarak ad-uzaylandı (aynı bitki); kiraz (CHERRY) evreleri GAP kapsamı dışı olduğu için çıkarıldı.

### Preserved (kasıtlı farklar)

- `crop_type` enum: GAP 8-bitki seti (COTTON, PISTACHIO, MAIZE, WHEAT, SUNFLOWER, GRAPE, OLIVE, RED_LENTIL); MAIZE/RED_LENTIL adlandırması korundu (worker CORN/LENTIL yerine, aliaslarla eşlenir).
- `payment_method`: `TARIS_DEDUCTION` (Ege kooperatifi) **alınmadı**.
- Hariç tutulan migration rehberleri: `crop_type_v1_to_v2.md`, `crop_type_v2_to_v3.md` (tarlaanaliz bu crop değişikliklerini yapmıyor).

---

## [4.1.1] - 2026-06-23

**PATCH (yıkıcı değil) — KR-019 tam uzman kapısı olay şemaları DRAFT → ACTIVE**

Faz 3'te tarlaanaliz-platform'da uyumlu üreticiler eklendi; bu nedenle iki olay
şemasının `notes.lifecycle` alanı DRAFT'tan ACTIVE'e çekildi. Yalnız metadata/
açıklama değişikliği — şema şekli, alanlar, required listesi ve enum değerleri
değişmedi (geriye uyumlu).

### Changed

- **`schemas/events/analysis_review_requested.v1.schema.json`** (`notes.lifecycle`):
  DRAFT → ACTIVE. Platform worker→platform bridge (`worker_bridge_consumer.py`)
  HER ExpertReview satırı için bu wire olayını yayınlar (AnalysisReviewRequestedV1,
  `expert_gate_events.py` → domain.events exchange, routing
  `event.analysis.review_requested`). In-process ExpertReviewRequested WORM audit
  için korunur.
- **`schemas/events/expert_review_decided.v1.schema.json`** (`notes.lifecycle`):
  DRAFT → ACTIVE. Platform-expert-portal `submit_review` + `bulk_approve`
  (`expert_portal.py`) GERÇEK N-uzman konsensüs kapı kararıyla bu wire olayını
  yayınlar (ExpertReviewDecidedV1 → routing `event.expert.review_decided`).

### Notes

- SYNC-1 hizalandı: contract DRAFT lifecycle'ları, üreticiler bağlandıktan sonra
  ACTIVE'e çekildi (2026-06-23 / Faz 3).

---

## [4.1.0] - 2026-06-21

**MINOR (eklemeli) — KR-019 tam uzman kapısı: iki olay şeması + mission_status durumları**

Çiftçinin her analiz sonucunu görmeden önce zorunlu uzman onayından geçmesini
sağlayan "tam kapı" (full expert gate) iş akışı için sözleşmeye iki yeni domain
olayı ve `mission_status` enum'una iki yeni durum eklendi. Değişiklik tamamen
eklemeli; mevcut şemalar/enum değerleri değişmedi (geriye uyumlu).

### Added

- **`schemas/events/analysis_review_requested.v1.schema.json`:** Worker analizi
  bitince platform her sonuç için bir uzman incelemesi açar; bu olay yayınlanır
  (artık yalnız düşük-güvenli vakalar değil — KR-019 tam kapı). `review_id`,
  `analysis_result_id`, `mission_id`, `field_id` (required) + opsiyonel
  `job_id`/`dataset_id`/`analysis_type`/`crop_type`/`confidence_score`. Kimlikler
  RFC 4122 UUID (çalışan platform/worker tel-gerçeği).
- **`schemas/events/expert_review_decided.v1.schema.json`:** Uzman kararı (`verdict`:
  confirmed/corrected/rejected/needs_more_expert) ve yayın kapısı sonucu
  (`gate_outcome`: APPROVED_PUBLISHED / REJECTED / ESCALATED). Yalnız
  APPROVED_PUBLISHED çiftçiye yayını yetkilendirir; `gate_outcome` GERÇEK N-uzman
  konsensüs kararıdır (naif verdict eşlemesi değil — erken çiftçi yayınını önler).
- **`enums/mission_status.enum.v1.json`** (metadata 1.0.0 → 1.1.0): `PENDING_REVIEW`
  (KR-019 yayın kapısı — uzman onayı bekliyor) ve `EXPERT_REJECTED` (uzman reddi →
  yeniden işleme için `IN_ANALYSIS`'e döner) durumları eklendi. Tam metadata
  (statusDescriptions, statusFlow.alternativeFlows.expertRejection,
  statusCategories, displayNames tr/en, uiColors) güncellendi.
- `docs/examples/analysis_review_requested.example.json`,
  `docs/examples/expert_review_decided.example.json` + test eşlemesi
  (`tests/test_examples_match_schemas.py`) ve README girişleri.
- **`tests/test_lifecycle_chain.py`** + **`tests/fixtures/full_lifecycle_chain.json`:**
  uçtan uca olay zinciri bütünlük testi — her belge kendi şemasına doğrular,
  yayın kapısı (onayda derived.published VAR, redde YOK) ve verdict→gate_outcome
  türetimi assert edilir.

### Notes

- **Lifecycle = DRAFT.** İki olay şeması `notes.lifecycle = DRAFT` ile işaretlidir:
  tarlaanaliz-platform'da uyumlu üretici (worker→platform bridge / expert-portal)
  henüz YOK; Faz 2/3'te eklenecek. Üretici hizalanana kadar bu wire olaylarını
  TÜKETMEYİN. Üretici hazır olunca lifecycle ACTIVE'e çekilecek (planlanan 4.1.1
  PATCH).
- **`notes.platform_alignment`** eklendi — platform kısa-form alias eşlemesi
  belgelendi (kanonik ← platform: `ACCEPTED←ACKED`, `IN_PROGRESS←FLOWN`,
  `IN_ANALYSIS←ANALYZING`, `DELIVERED←DONE`). Alias'ları kanonik uzun forma yeniden
  adlandırmak (platform DB enum migration'ı) ayrı bir MAJOR iştir; bu sürümde sapma
  yalnız belgelendi, birleştirilmedi.

### Migration

- Eklemeli MINOR — consumer'lar mevcut kullanımlarını bozmadan 4.1.0'a pin'leyebilir.
  Yeni olayları tüketmek isteyen platform/worker, UUID kimlik biçimini varsayar.

---

## [4.0.0] - 2026-06-14

**Breaking-change:** EVET — `crop_type` worker-canonical 14 değere hizalandı

### Removed

- **`enums/crop_type.enum.v1.json`:** `BARLEY` ve `POTATO` kaldırıldı (worker portföy kararı 2026-05-18 — yerel pazar/ihracat değeri ve drone WTP düşük, açık kaynak veri yok).

### Added

- **`enums/crop_type.enum.v1.json`:** `CHERRY`, `FIG`, `RICE` eklendi (worker `CropType` ile 1:1, 14 değer).
- **`schemas/worker/expert_review_queue.v1.schema.json`:** inline `crop_type` enum'una `RICE` eklendi (14 değer); açıklama "13-value" → "14-value".

### Migration

- Bkz. `docs/migration_guides/crop_type_v1_to_v2.md`. Persisted `BARLEY`/`POTATO` değerleri artık geçersiz.

---

## [3.0.0] - 2026-06-14

**Breaking-change:** EVET — coğrafi `EGE` bölgesi region enum'larından kaldırıldı

### Removed

- **`schemas/core/field.v1.schema.json`:** `region` enum'undan `EGE` değeri kaldırıldı. tarlaanaliz yalnızca GAP (Güneydoğu Anadolu) bölgesi içindir; Ege coğrafyası desteklenmez (egeanaliz ayrı dağıtım).
- **`schemas/worker/expert_labeling_card.v1.schema.json`:** `endemic_regions` ve `region` enum'larından `EGE` değeri kaldırıldı (aynı gerekçe).

---

## [2.0.2] - 2026-03-15

**KR-025 Compliance Fix**

### Removed

- **`schemas/worker/analysis_result.v1.schema.json`:** `recommendations` property removed — KR-025 prohibits the system from making pesticide, spraying, or fertilization decisions. The `Recommendation` type definition (including categories PEST_CONTROL, FERTILIZATION, IRRIGATION, DISEASE_MANAGEMENT, HARVEST_TIMING, GENERAL) has been removed from `$defs`.
- **`schemas/worker/analysis_result.v1.schema.json`:** `PRESCRIPTION` value removed from `LayerRef.type` enum — prescription layers violate KR-025 observational-only constraint.

### Added

- **`schemas/worker/analysis_result.v1.schema.json`:** `x-kr-025-note` field added at schema root documenting the KR-025 constraint: this schema must not contain recommendation, prescription, or spraying decision fields.

---

## [2.0.0] - 2026-02-24

**SSOT Uyum:** 1.2.0  
**Breaking-change:** EVET — `payment_status` enum değişiklikleri ve IBAN kanal güncellemesi

### Breaking Changes

- **`enums/payment_status.v1.json` + `v2.json`:** `APPROVED` değeri kaldırıldı — kanonik onay durumu `PAID`'dir. `APPROVED` kullanan tüm consumer'lar `PAID`'e geçmelidir.
- **`enums/payment_status.v1.json` + `v2.json`:** `EXPIRED` değeri kaldırıldı — otomatik expire mekanizması kaldırıldı. `PAYMENT_PENDING` intent'ler yalnızca admin kararıyla `CANCELLED` yapılır.
- **`enums/payment_method.v1.json`:** `IBAN_TRANSFER` dekont kanalı güncellendi. E-posta gönderimine dayalı akışlar geçersiz; dekont artık `POST /payments/intents/{id}/upload-receipt` endpoint'i ile uygulama içi yüklenir.
- **`schemas/platform/payment_intent.v2.schema.json`:** `receipt_blob_id`, `admin_user_id`, `rejection_reason`, `admin_note`, `field_id`, `rejected_at`, `refunded_at` alanları eklendi. `mark-paid` ve `reject` admin endpoint'lerinde `admin_note` / `rejection_reason` zorunlu hale geldi.

**Migration:** `docs/migration_guides/payment_intent_v1_to_v2.md`

### Added

- **`enums/drone_type.enum.v1.json`:** Drone-agnostik mimari için yeni enum. Desteklenen modeller: DJI_MAVIC_3M (birincil), DJI_M350_RTK_SENTERA_6X, WINGTRAONE_GEN2_MICASENSE_REDEDGE_P, PARROT_ANAFI_USA_SEQUOIA_PLUS, AGEAGLE_EBEE_X_ALTUM_PT. (KR-015 + KR-030 + KR-034)
- **`schemas/platform/payment_intent.v2.schema.json`:** KR-033 tam uyumlu v2 şeması. `REFUNDED` durumu, `field_id`, `admin_user_id`, `receipt_blob_id` alanları, tam state machine dokümantasyonu, API endpoint listesi.
- **`docs/examples/payment_intent_iban_pending.example.json`:** IBAN_TRANSFER + PAYMENT_PENDING örnek payload.
- **`docs/examples/payment_intent_iban_paid.example.json`:** IBAN_TRANSFER + admin onayı sonrası PAID örnek payload.
- **`docs/examples/payment_intent_creditcard_paid.example.json`:** CREDIT_CARD + webhook PAID örnek payload.
- **`docs/migration_guides/payment_intent_v1_to_v2.md`:** DB migration SQL, uygulama kodu değişiklikleri, rollback planı, doğrulama testleri.
- **`docs/ssot/kr_registry.md`:** KR Registry v8 — drone-agnostik + Sezonluk Paket terminolojisi + KR-081 cross-ref eklendi.
- **`docs/ssot/GOVERNANCE_PACK_v1_0_1.md`:** GOVERNANCE_PACK v1.0.1 — §0 RACI kanonik kayıt notu, §3.3 ödeme senkronizasyon notu, §5 RESULT.SIGNATURE_FAIL eklendi, §9 KR-033 + KR-081 cross-ref eklendi.
- **`docs/ssot/contracts_ssot.md`:** Contracts component SSOT filtrelenmiş görünümü.

### Changed

- **`schemas/edge/intake_manifest.v1.schema.json`:** `drone_model` alanı `drone_type.enum.v1.json`'a bağlandı (drone-agnostik). Önceki DJI-only whitelist kaldırıldı. (KR-015 + KR-030)
- **`schemas/core/mission.v1.schema.json`:** `drone_model` alanı DroneType enum'una bağlandı. `mission_source` alanı eklendi (SINGLE / SUBSCRIPTION — Sezonluk Paket ayrımı). (KR-028)
- **`docs/checklists/PR_GATE_CHECKLIST.md`:** SSOT 1.2.0 kontrolleri eklendi: payment guard, drone registry senkronizasyon.
- **`docs/checklists/CI_GATE_CHECKLIST.md`:** payment_status APPROVED/EXPIRED guard, drone_registry.yaml senkronizasyon kontrolü eklendi.
- **`docs/checklists/RELEASE_GATE_CHECKLIST.md`:** SSOT 1.2.0 özgül kontroller bölümü eklendi.

### Deprecated

- **`schemas/platform/payment_intent.v1.schema.json`:** Deprecated. Yeni geliştirme `v2` ile yapılmalıdır. REFUNDED durumu ve admin zorunlu alanlar eksik. Geriye dönük uyumluluk için tutuldu.

---

## [1.x.x] - 2026-02-02

İlk sürüm. Contract-first repo başlangıcı. Temel şemalar (field, mission, user, edge, worker, events), enums, OpenAPI specs.
