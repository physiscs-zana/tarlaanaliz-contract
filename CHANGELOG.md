# Changelog

All notable changes to `tarlaanaliz-contracts` will be documented in this file.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)  
Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

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
