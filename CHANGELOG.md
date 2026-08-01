# Changelog

All notable changes to `tarlaanaliz-contracts` will be documented in this file.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)  
Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

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

**Kaynak:** worker `denetim/audit_escalation_reason_devir_spec_2026_07_19.md` — karar-hazır devir.
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
