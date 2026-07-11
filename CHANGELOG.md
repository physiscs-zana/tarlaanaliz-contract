# Changelog

All notable changes to `tarlaanaliz-contracts` will be documented in this file.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)  
Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

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
