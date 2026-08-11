# TarlaAnaliz Contracts Version Lock

## Version: 7.7.0

**Release Date:** 2026-08-11T18:33:03.020827Z  
**Breaking Change:** NO  
**Contracts Checksum (SHA-256):** `bf269235da5ba9eabd09d17fa9efe1e9e722dc6802b24abc7a3b74bd447f32a1`

---

## Version Policy

This file locks the contract version for all consumers (platform, edge, worker).
Consumers MUST validate the contracts checksum before use.

**Semantic Versioning:**
- **MAJOR** (breaking): Incompatible schema changes (field removal, type change, enum removal)
- **MINOR** (non-breaking): New optional fields, new enums, new schemas
- **PATCH** (fixes): Documentation updates, examples, metadata

**Breaking Change Rules:**
- Field removal or rename → MAJOR
- Required field addition → MAJOR
- Type change → MAJOR
- Enum value removal → MAJOR
- Schema removal → MAJOR

**Non-Breaking Changes:**
- Optional field addition → MINOR
- New enum value → MINOR
- New schema → MINOR
- Description/example update → PATCH

---

## File Checksums (SHA-256)

Individual file hashes for verification:

### Shared Schemas

- `schemas/shared/address.v1.schema.json`  
  `9edecd639a7a4440f66c887aedeab9f255208d0f9e50723f08905023cf398665`
- `schemas/shared/geojson.v1.schema.json`  
  `2fe6dfa92852ce5cd836448a57d9385ba718bd6821c3e3e27347dc6665e69265`
- `schemas/shared/index.json`  
  `5ffad3815db62e1334ebd8beaf9aef140a5432d2baf622ac490bfebb8397c529`
- `schemas/shared/money.v1.schema.json`  
  `64fc425b2c734fd51c79bf43fa4a3f85572b4c48fcbead8215e506202250ec2e`

### Enums

- `enums/analysis_type.enum.v1.json`  
  `aa68f4ad6d32a2cedb30f3974513a4310cd5e7db2ac9fb953596a4de29588c8c`
- `enums/calibration_type.enum.v1.json`  
  `8c35271314e57a936dd1cf7c6fa62badea272a551b1d172e4456f7fe2d649f29`
- `enums/crop_type.enum.v1.json`  
  `34babfb9245ca3999bfef7f06846c8835592acbf0cd2804c6167df8bd9451194`
- `enums/dataset_status.enum.v1.json`  
  `a1af5173853fd0983339075fa550e66847c0d19a8a2411c72a612d866de54b07`
- `enums/drone_type.enum.v1.json`  
  `baac44459fd505f6a8cea60bc1c71766513333c434c8fbb2aa0363b4884ed5b0`
- `enums/edge_custody_event.enum.v1.json`  
  `f5578afc7a31de5c3f7afd1974fc90530bf60a307ee5d7134c98707e1139f389`
- `enums/field_history_event_type.enum.v1.json`  
  `0a8fe27c92fb127d61ccee7740fd8db5765d49551edb493f650e5e01b8b3618c`
- `enums/mission_status.enum.v1.json`  
  `f8623eaef3c959c65c9469cd761430acfd372bd8aba1010855a1e2f0a08b3478`
- `enums/payment_method.enum.v1.json`  
  `14291b81875704058bf6eed4e701ec7a1325b48d08fccd21f6227e4f6659e12c`
- `enums/payment_status.enum.v1.json`  
  `d2eeb8c6f1e4211b6127120018a88bc29cd52aa8bcdf30ce24f5709ec067e6b4`
- `enums/payment_status.enum.v2.json`  
  `03cc82adf59a8f04ed7122b806b8796eb8f6c7fd0aaf98a01ffd5f40ff753029`
- `enums/payment_target_type.enum.v1.json`  
  `761b3e420245b1dabce63308572f9aa82da64eaf89381533491f28e1e3258c50`
- `enums/phenology_stage.enum.v1.json`  
  `86f6f10ec7951fc3001b0f5f2f3f76720ff1234a6ed37272136bc59f378838de`
- `enums/qc_status.enum.v1.json`  
  `889b0f3010678976e7ac351977b5d83391d9d119c91e50e060bc027c32134206`
- `enums/quarantine_decision.enum.v1.json`  
  `641b5a9e766f7e91837695954d1d0b45aeca6bfbe67356f12a0a65f762fa91c0`
- `enums/radiometric_mode.enum.v1.json`  
  `da7c319fa30be25fb42db9cc03d777815a9975c48ae46580582da9e861546ae9`
- `enums/report_phase.enum.v1.json`  
  `ed65ed8137545fa984aa9fb7c21082200d82cb0b54657a06c81ce743ee9afdd9`
- `enums/role.enum.v1.json`  
  `c978f07a112deabb74c62ba229599d4946a9fa3e2a9bb14162accc802d490c22`
- `enums/scan_stage.enum.v1.json`  
  `d7f4fd76caeb6d9bfaeb31d8920143d845386a451f5222bcdcca254394c152ff`
- `enums/threat_type.enum.v1.json`  
  `dd210d6016764bcb91c1a69d643ee551f1b3dd37a85e73c6984e922dc6ddf81e`
- `enums/user_role.enum.v1.json`  
  `95d76349772e49365cf178c109acdb9e36a445016a3de79211086713f48a718f`
- `enums/verification_status.enum.v1.json`  
  `f9857891f92f272fbdf12959224dae22a006fafce0382f9c0745538101219ede`

### Core Schemas

- `schemas/core/field.v1.schema.json`  
  `e2000a6f8cfac11dfef0e455813fb87339dbcbfafab5a334d983acf3034bf157`
- `schemas/core/mission.v1.schema.json`  
  `e0055a61a41be6900c15f7445f7fa979564cc5aa0306a3573e717c3c80db4133`
- `schemas/core/phenology_flight_profile.v1.schema.json`  
  `4d1e1f4f7bae6353a646280e4959204c2b4da1a376a96f978435ee64c0121d73`
- `schemas/core/seasonal_flight_calendar.v1.schema.json`  
  `db77a05e47bded7da0f5e958439fab63bf3dd7d91b24a1311c9ceec369476cfe`
- `schemas/core/user.v1.schema.json`  
  `9c2659f56ddc3a826eac8e7799536ab50f0bd7f212708e568657cc396d43f6e3`
- `schemas/core/user_pii.v1.schema.json`  
  `e665ae5ebb0c48f89f23358b2bf88c1766a5ef5a5ecaf74380b631d46457b4f5`

### Datasets

- `schemas/datasets/attestation.v1.schema.json`  
  `a4d906c1a1dadcb3284775f1fd8a97be9b3ec88142fe33f01d14cd5b2e2e1934`
- `schemas/datasets/calibration_certificate.v1.schema.json`  
  `97227191bce218950b423bfbed2bb72c0ec96b1dbf31ff508bf86a9c8dfbe09f`
- `schemas/datasets/dataset.v1.schema.json`  
  `652b794330b3a087152716091402f962722abbe1038a73b26cfb049545c12b89`
- `schemas/datasets/dataset_manifest.v1.schema.json`  
  `4a8b4de900b30603f3bb6c596d17125a3188a7a441f67c29cb657060e7172581`
- `schemas/datasets/evidence_bundle_ref.v1.schema.json`  
  `8897f5873ad9e97083309cb35cf4a8c1ebef213a253c28ac7beb2fe12db51e21`
- `schemas/datasets/qc_report.v1.schema.json`  
  `31f90c30b3fb030458d0b5a7343b3ba914c64546ed0a72826dc4fbdfc4dc5424`
- `schemas/datasets/scan_report.v1.schema.json`  
  `31d4e5ca966fc13274185d6f08274475b72e6a3d3198fa2cff7d7b7e79b341f3`
- `schemas/datasets/transfer_batch.v1.schema.json`  
  `c61d82e8df3bf1a0827fc8c0b6d1f1725e6be7ee659c3589836e342abee8a81f`
- `schemas/datasets/verification_report.v1.schema.json`  
  `80a59cd6f28bf4d48b22be591fce8f8f0794a416c9babce5d967b0756c99ad43`

### Edge Schemas

- `schemas/edge/attestation_record.v1.schema.json`  
  `dfcc65d709746107eceb67f943dcb60a13a900008e959f0f38df197d6cc1b95b`
- `schemas/edge/calibrated_dataset_manifest.v1.schema.json`  
  `766891608ffd6f00ab49d53a3901e076beaa66b684825ee0bcca69356cb59c4c`
- `schemas/edge/calibration_result.v1.schema.json`  
  `1518bdfa2d99f03c1873483c04de71363ea11fb7e5fc9775717fd331e499e28a`
- `schemas/edge/dataset_manifest.v1.schema.json`  
  `0c30a9e1c7b6b13a78908686f11fbdbd677b081d560f7c9b2af57a7f9df4307e`
- `schemas/edge/edge_metadata.v1.schema.json`  
  `d081229b4092d67d1a38e61b994a8d4a83010d695c6b0769c3e31ac80312f851`
- `schemas/edge/evidence_bundle_ref.v1.schema.json`  
  `d83cf9d60e935955dc9dd5d2f2cd97b42c4b84954c2602a0be50f270e972f751`
- `schemas/edge/intake_manifest.v1.schema.json`  
  `e484bf6e4570c1d818b09e0d60588dfa003de778c3e8c076ef1d29101a055838`
- `schemas/edge/qc_report.v1.schema.json`  
  `d052550ac7d561242c617f1d315eca9e1582f2f63d12dd8018da7eb28f33601e`
- `schemas/edge/quarantine_event.v1.schema.json`  
  `3e2820232e39f84e39458a084e86e3a62aefee06f744e2f88fca3bfdbf4cd523`
- `schemas/edge/scan_report.v1.schema.json`  
  `bc1d7fb333604eac47d7c03f95ffc559acee79a3519587f564e8905a7933c98b`
- `schemas/edge/transfer_batch.v1.schema.json`  
  `3dcc72d3097dad67d3216641b1d2bdecb44e6bfacb763c5fe3893cc21beb8472`
- `schemas/edge/upload_receipt.v1.schema.json`  
  `93823aeb5abd686f9c751f57767f7524a7e295bcdf0f5de3aa49e54a69146fb1`
- `schemas/edge/verification_report.v1.schema.json`  
  `5211c16f22fc76e7c9dc50f290cd16c533ccca9da1f6b33b367eaa1b19724967`
- `schemas/edge/worker_result.v1.schema.json`  
  `08cf7cd62cbc037cf93c43a078ce1a97e12be44a946afd87b12aa8eb6a5cce67`

### Worker Schemas

- `schemas/worker/analysis_job.v1.schema.json`  
  `dd83bb7537447c204001655e1a552198f3610eab2116bb262be1a5b241487702`
- `schemas/worker/analysis_result.v1.schema.json`  
  `42cc6686b2bdbcdf35f107b1614fd24d4376f98e3d114bd58fed08ea8c4fccc6`
- `schemas/worker/calibrated_dataset.v1.schema.json`  
  `a2e628b8ef996d8bdb828ef623a378aba9c43337b083351e0b137a312092618a`
- `schemas/worker/calibration_metadata.v1.schema.json`  
  `7fbe7303c237bb11302a9c879d091d4da788b4a893ee8c1bebcfb8edf6b90d0c`
- `schemas/worker/expert_feedback.v1.schema.json`  
  `f68361bec55ee84c49682779f078f695baadf5a811733a2a5873c1a9d9dd5475`
- `schemas/worker/expert_labeling_card.v1.schema.json`  
  `8c320cb4c34fdfcf14c9c33be39d91445735251e347bc16cf9671ce8dba43c51`
- `schemas/worker/expert_review_queue.v1.schema.json`  
  `4e0c3fa64109b062576fd1071dda57d7aac465ea51976f64acd1f57972815c1b`
- `schemas/worker/thermal_analysis_result.v1.schema.json`  
  `c7b013adce00fa5618214865d869f1f85d68dad83786b21d27f9ea019c8de212`

### Events

- `schemas/events/analysis_completed.v1.schema.json`  
  `a17eaa5f0b3fbb63deb4381b8f0c7edbb77c6e835c21b3a8bdeeb11c56282825`
- `schemas/events/analysis_preliminary_ready.v1.schema.json`  
  `5b7f108edbfea216b8c08d0c41ab63d41a9fbbdc3399d53a9de76fb9eac5200b`
- `schemas/events/analysis_review_requested.v1.schema.json`  
  `8e08b503e0b25c866f2e8cbede96b39f3beb77490d82c6d78410db443706c687`
- `schemas/events/dataset_analyzed.v1.schema.json`  
  `f1c6f51d9fbee29eafeda4da52be06b52c8664a459129f91d57ecee4ff8ef0e2`
- `schemas/events/dataset_calibrated.v1.schema.json`  
  `f97fefea1da31e85d239a205b5ed69171f148ef21df5c9d74ad1b76f5f474366`
- `schemas/events/dataset_dispatched.v1.schema.json`  
  `4467cbb6467684a7cc4cd9c2099eff13fe56478c64f148ff7c1c5cb7e8423e4d`
- `schemas/events/dataset_ingested.v1.schema.json`  
  `3511acf5c393c98ce2e2b67b49dea4e43b8660cbe262dfd96cbc8af76c0e00b1`
- `schemas/events/dataset_quarantined.v1.schema.json`  
  `ebd91761c1dcf5f239a4b4888805deee57b2bd4e537c22c42b88126bcc78702f`
- `schemas/events/dataset_scanned.v1.schema.json`  
  `62d52566fa778442f92854e0eb63bc1bb5c4d1361bc7e5407bdd4772c5fc89b4`
- `schemas/events/dataset_unquarantined.v1.schema.json`  
  `b71caed490df1a5d5a96b9a52e28b80c813fc35500c2840a7044b3a859a3f287`
- `schemas/events/dataset_verified.v1.schema.json`  
  `c5e351dd077e5eeeca6b98d3062d1e22079225b230a0c2d47971da73b1565b24`
- `schemas/events/derived_published.v1.schema.json`  
  `9c932b7e7e0ef59f54e434793e556cdc2c18dffd012cd2d23dc7a31fc545bc03`
- `schemas/events/expert_review_decided.v1.schema.json`  
  `5496b4abba4d63a9e047551fffba34ff340ec08e07de99668849e2096a39f62b`
- `schemas/events/field_created.v1.schema.json`  
  `655d2ef33d1bd0acce01db481950236eabed3d87682dcef1b7734c5510e5fb93`
- `schemas/events/field_health_changed.v1.schema.json`  
  `48763d4b3b27eecf711d28b78f465032d3042a474e3d04681ddcd72644460c3d`
- `schemas/events/mission_assigned.v1.schema.json`  
  `6a3d4a6cb0b286cfa4f35fa8cab41a8d5fe04c410c90f8bb83a59cdeee77f2c3`

### Platform

- `schemas/platform/calibrated_dataset_manifest.v1.schema.json`  
  `f6e7da93614809e762f982af4dffbf9b0d4ee87c1ecabc9df709d0c00c2912d4`
- `schemas/platform/calibration_result.v1.schema.json`  
  `c51b377e0aa6922d0b86f4cf9076093d66fc4c13a747f44da3f7059c40a73038`
- `schemas/platform/evidence_bundle_ref.v1.schema.json`  
  `258e9e21ca56ea5ceba49f40d8a11d7e42b14894c0ed8992bbc58c056240fd97`
- `schemas/platform/layer_registry.v1.schema.json`  
  `f1a89214a26b14ee97442e0bc64a9689daa163e0b9bc63edbdc5c7552a811f65`
- `schemas/platform/payment_intent.v1.schema.json`  
  `ec1223135e451b17a76dd8fedd8f36b9ecda47cdd2f8688afce32f3e6455069d`
- `schemas/platform/payment_intent.v2.schema.json`  
  `5e03511707e78c82e123b70232c7fb5040c2c0c8a11ccff4c2a41bd6a86e3628`
- `schemas/platform/payroll.v1.schema.json`  
  `f415b8413fa1a6778e41c2e53457c4c310646e09de3fa08bcb37cdc54e2a1a3e`
- `schemas/platform/pricing.v1.schema.json`  
  `25e0c9fa7d5a351ab7763facdf3824007fc5e95adf19fde7425a6780e115f580`
- `schemas/platform/qc_report.v1.schema.json`  
  `0709dd9c98ebaa11c45924bf571b0cfb6291af16711fbb133e1e2e7b3d97a538`
- `schemas/platform/subscription.v1.schema.json`  
  `3467b8c75a94a3558edee94c3c9db7ec7e8db8ea1a59165668073a8a7698adcc`
- `schemas/platform/training_feedback.v1.schema.json`  
  `df2388e7a5bf7e6d4d670c772790a937d92d8666ac0bc363c0c9d337273d2051`

### API Components

- `api/components/parameters.yaml`  
  `ed7e7fd541e74f323606f17329b0bb9cadf993a9be30eb296ecc553cec1ba26f`
- `api/components/responses.yaml`  
  `13af6e16c4044592bd6720a642905aa493ccddc73334aa4d7bddace65e1b571f`
- `api/components/schemas.yaml`  
  `c7a0a388eabd3db90507179b632db917f8b367098db33447a7b911fe435992a1`
- `api/components/security_schemes.yaml`  
  `9d45e3181a4b847b617a0553c72458650aa9c3deacf38cbed67c5c12db3e1c79`

### API Specs

- `api/edge_local.v1.yaml`  
  `7eea7b070927df4e5cb64cc099dcf7532fcb59d411b74c1f87f84b9b0493b5c6`
- `api/platform_internal.v1.yaml`  
  `58db12948dc8863323ac747f2dd39a5f064ac8073a853018d497c9e684af2c41`
- `api/platform_public.v1.yaml`  
  `8e2ce6495010af6ce1999c992f9941ad2fb05af0d31d41e4e13525b82d4b1520`

---

## Changelog

### v7.7.0 (2026-08-11)

**Breaking:** NO

Alan sizmasi kapatildi (27 dugum) - threat_type kanonik sozluge baglandi - CI kapi durustlugu - Node/TS zinciri kaldirildi - OD-13 ayna duzeltmesi - vendored politika paritesi kapisi

### v7.6.1 (2026-08-10)

**Breaking:** NO

D12: stress_ratio kanonik olarak TANIMLANDI (NDRE/NDVI, NDVI<=0 -> notr 1.0); yanlis 'uretim yok' iddiasi curutuldu; teslimat kurali makine-okunur (delivery_rule.preliminary=false) ve ON FAZ kapali listesi platformda kapiya baglandi.

### v7.6.0 (2026-08-07)

**Breaking:** NO

Version pinned automatically.

### v7.5.0 (2026-08-07)

**Breaking:** NO

Version pinned automatically.

### v7.4.0 (2026-08-01)

**Breaking:** NO

TUR 2: S5 (reflektans olcegi) · C6b/S2 (PANEL_ABSOLUTE) · S4 (calibration_method) · S6 (cikti basina olcek) · S7 (RGB kompozit kare) · E13-R (kalibrasyon tipi drone basina turetilir) · OD-1/OD-2 (karar yuzeyi ile dogrulama yuzeyi baglandi) · SD9 (info.version set surumunu izler) · SD10 (OpenAPI lint gercekten kosuyor) · SD11 (notes/metadata kanonikte kalir)

### v7.3.0 (2026-08-01)

**Breaking:** NO

Version pinned automatically.

### v7.2.0 (2026-07-14)

**Breaking:** NO

MINOR (non-breaking): intake_manifest.v1 -- EdgeForm + PlatformForm top-level iki opsiyonel alan: quarantined_file_count (integer >=0) + quarantined_bytes (integer >=0). Edge/AV1 manifest emit edilmeden ONCE yerelde karantinaya alip dusurdugu dosya sayisi + toplam boyutu (bu dosyalar files[] icine GIRMEZ -> platform bugune kadar goremiyordu). Platform admin panosunda >0 iken DAIMA uyari. required DEGISMEDI (pre-v7.2.0 ureticiler atlar), unevaluatedProperties:false korunur -> additive MINOR. Is Kolu B2 edge-karantina gorunurlugu. Consumer: edge (uretici) + platform (tuketici); worker etkilenmez.

### v7.1.0 (2026-07-13)

**Breaking:** NO

MINOR (non-breaking): analysis_result.v1 -- top-level tile_counts {total, healthy, anomaly} objesi eklendi (KR-088 ciftci on-raporu 'kac kare saglikli / kac kare sorunlu' sinyali). Kaynak: worker PipelineResponse.tile_count_total/healthy/anomaly. Opsiyonel/geriye-uyumlu (pre-v7.1.0 ureticiler + NO_RESULT atlar), unevaluatedProperties:false. AK-4 worker->kanonik ayna (worker v7.1.0'da onden landledi). Ayrica tools/sync_to_repos.sh sync_to_worker() salt-okunur drift dedektorune donusturuldu (AK-4: canonical->worker kopya worker ileri formunu ezerdi).

### v7.0.1 (2026-07-12)

**Breaking:** NO

PATCH: KR-018 bant-gate ic-tutarlilik duzeltmeleri (18-ajan denetim bulgulari). analysis_type.enum v1.4.1 — THERMAL_STRESS.requires_bands tam set [GREEN,RED,RED_EDGE,NIR,LWIR]; kesisim kurali effective_bands=supported_bands + thermal_variant.thermal_bands; enforcement:advisory. drone_type.enum — PARROT '+termal' kaldirildi (matris kanonik); x-registry-sync capability_matrix effective_bands ile hizalandi; x-updated 2026-07-12. Enum dizileri DEGISMEDI -> non-breaking.

### v7.0.0 (2026-07-12)

**Breaking:** YES

MAJOR/breaking: phenology_stage.enum MAIZE_* -> CORN_* rename (4 deger: EMERGENCE_V5, V6_PRETASSEL, TASSEL_SILK, GRAINFILL + x-enum-descriptions keys + x-stage-order 'CORN' anahtari + top description namespace). Son kalan MAIZE kalintisi; crop_type v3.0.0 CORN rename'ini tamamlar (evre ad-uzayi oneki artik crop_type kanonik degeriyle birebir). Enum kume boyutu 14 (GRAPE_*/OLIVE_* degismedi). crop_type changeNote'taki 'MAIZE_* remain unchanged' notu 'aligned to CORN_* in v7.0.0' olarak duzeltildi. Migration: docs/migration_guides/phenology_stage_maize_to_corn.md. Worker phenology_stage tuketiyorsa ayni turda hizalanmalidir.

### v6.2.0 (2026-07-12)

**Breaking:** NO

MINOR (non-breaking): (1) analysis_type.enum v1.3.0->v1.4.0 — bandRequirements eklendi (requires_bands + availability; KR-018 bant-gate tek-kaynak, drone_capability_matrix.yaml ile kesisim = uretilebilir katman). THERMAL_STRESS->requires_thermal_payload (LWIR), BENEFICIAL->enum_valid_not_yet_emittable. (2) drone_type.enum x-registry-sync — drone_capability_matrix.yaml capraz-referansi + add_model_flow guncellendi. (3) payment_status.enum.v1 x-deprecated isaretlendi (v2 kanonik; repo ici $ref tuketicisi yok, payment_intent.v1 status'u inline yazar). Enum dizileri DEGISMEDI; kaldirma/rename yok. Oneri 2 (PENDING_RECEIPT) = platform-side (B), contract degismez; Oneri 3/6 teyit-only.

### v6.1.0 (2026-07-11)

**Breaking:** NO

BENEFICIAL rich taxonomy value (analysis_type v1.3.0, Teal adopted from worker proposal) + result-rich-axis on analysis_result.Detection (sub_specialty/detection_type); BENEFICIAL added to card+review_queue sub_specialty enums. Worker v6.1.0 AK-4 canonical mirror. crop_type untouched. MINOR/non-breaking.

### v6.0.1 (2026-07-11)

**Breaking:** NO

crop_type enum metadata.archived (HAZELNUT+RED_LENTIL) kaldirildi — kullanici direktifi: mercimek/findik icin arsivde dahil hicbir kalinti tutulmaz. Enum array DEGISMEDI (8 mahsul); bu metadata/docs degisikligi = PATCH. Kaldirma-kaydi enum changeNote + migration guide crop_type_red_lentil_removal.md'de KORUNUR. DUZELTME: 6.0.0 notundaki 'Immutable DB residue (COORDINATE, ileriye-donuk worker-koordineli DB migration)' cercevesi YANLISTI — platform 2026_04_04_align_expert_schema_to_worker.py Postgres crop_type ENUM'unu zaten VARCHAR(50)'e cevirdi + DROP TYPE crop_type calisti; canli ENUM yok, forward migration GEREKMIYOR; yalniz uygulanmis/immutable migration'larin tarihsel DDL metni kalir (RESOLVED, COORDINATE degil).

### v6.0.0 (2026-07-11)

**Breaking:** YES

crop_type RED_LENTIL kaldirildi (MAJOR/breaking); enum v3.0.0->v4.0.0. Worker LENTIL'i crop-sozlugunden dusuruyor; contract aynalar (%100 worker-sync). RED_LENTIL<->LENTIL cross-repo alias emekli. GAP kumesi 8 mahsul (COTTON, PISTACHIO, CORN, WHEAT, SUNFLOWER, GRAPE, OLIVE, RICE). Migration: docs/migration_guides/crop_type_red_lentil_removal.md

### v5.1.0 (2026-07-11)

**Breaking:** NO

Alt-uzmanlik ayna: expert_review_queue detection_type+sub_specialty, expert_labeling_card sub_specialty (3 opsiyonel alan, MINOR non-breaking). Enum kaynagi analysis_type.enum.v1.json v1.2.0 (yeni enum yok). AK-4 worker->kanonik ayna.

### v5.0.0 (2026-07-06)

**Breaking:** YES

crop_type MAIZE->CORN rename (MAJOR/breaking). enum v2.1.0->3.0.0; displayNames re-keyed; aliases flipped to CORN->MAIZE. Deferred (separate breaking tasks): RED_LENTIL canonical + phenology_stage MAIZE_* codes. Migration: docs/migration_guides/crop_type_maize_to_corn.md

### v4.4.0 (2026-07-05)

**Breaking:** NO

KR-093 Ciftci On Raporu: report_phase enum + analysis_preliminary_ready.v1 event (MINOR, non-breaking)

### v4.3.0 (2026-07-05)

**Breaking:** NO

Version pinned automatically.

### v4.2.1 (2026-06-26)

**Breaking:** YES

Merge master (4.1.2) into GAP-only sync. crop_type GAP 8-set korundu (master 14-canonical override edildi; worker tarafinda ayri degisiklik gerekir). Master KR-019 event semalari + CI + EGE bolge temizligi korundu. TARIS ve Ege crop migration rehberi cikarildi.

### v2.0.1 (2026-03-06)

**Breaking:** NO

Version pinned automatically.

---

## Verification

Consumers MUST verify contracts checksum:

### Python
```python
import hashlib
import json

def verify_contracts(expected_checksum: str) -> bool:
    # Compute actual checksum from schemas
    actual_checksum = compute_contracts_checksum()
    return actual_checksum == expected_checksum

assert verify_contracts("bf269235da5ba9eabd09d17fa9efe1e9e722dc6802b24abc7a3b74bd447f32a1"), "Contracts checksum mismatch!"
```

### Node.js
```javascript
const crypto = require('crypto');
const assert = require('assert');

function verifyContracts(expectedChecksum) {
  const actualChecksum = computeContractsChecksum();
  return actualChecksum === expectedChecksum;
}

assert(verifyContracts("bf269235da5ba9eabd09d17fa9efe1e9e722dc6802b24abc7a3b74bd447f32a1"), "Contracts checksum mismatch!");
```

### CI/CD Integration

Add to `.github/workflows/validate.yml`:

```yaml
- name: Verify Contracts Version
  run: |
    python3 tools/pin_version.py --verify
```

---

## Consumer Integration

### Platform Service (platform repo)
```bash
# In platform repo
git submodule add https://github.com/tarlaanaliz/tarlaanaliz-contracts contracts
git submodule update --remote
python3 contracts/tools/pin_version.py --verify
```

### Edge Station (edge repo)
```bash
# In edge repo
git submodule add https://github.com/tarlaanaliz/tarlaanaliz-contracts contracts
git submodule update --remote
./contracts/tools/sync_to_repos.sh --target edge
```

### Worker Service (worker repo)
```bash
# In worker repo
git submodule add https://github.com/tarlaanaliz/tarlaanaliz-contracts contracts
git submodule update --remote
./contracts/tools/sync_to_repos.sh --target worker
```

---

## Notes

- **Immutable:** Once released, versions are immutable. Create new version for changes.
- **CI Enforcement:** All PRs MUST pass `tools/validate.py` and checksum verification.
- **Breaking Changes:** Require major version bump and consumer coordination.
- **Hash Algorithm:** SHA-256 (collision-resistant, FIPS 140-2 compliant)
- **Timestamp:** ISO 8601 UTC format

**Last Updated:** 2026-08-11T18:33:03.020827Z
