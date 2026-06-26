# Changelog

All notable changes to `tarlaanaliz-contracts` will be documented in this file.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)  
Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

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
