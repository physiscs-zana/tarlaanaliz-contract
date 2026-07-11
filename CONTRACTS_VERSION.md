# TarlaAnaliz Contracts Version Lock

## Version: 6.0.0

**Release Date:** 2026-07-11T12:30:17.879399Z  
**Breaking Change:** YES  
**Contracts Checksum (SHA-256):** `0dd8351a8d845835a1e560e6748f22e1c68637f74decc34ac29287176d581afc`

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
  `030316e8eb64139c019cdcbc2e0def60af85cb5da14b620c2574ab970fad112c`
- `enums/calibration_type.enum.v1.json`  
  `35c85add630b2631ed2f4749a045f258955db11f255ef081822c9654b27c70b8`
- `enums/crop_type.enum.v1.json`  
  `f99265993e9d757ba01a520a13ac10bd2808786b3860d2ed4a7d62fad50534d9`
- `enums/dataset_status.enum.v1.json`  
  `a1af5173853fd0983339075fa550e66847c0d19a8a2411c72a612d866de54b07`
- `enums/drone_type.enum.v1.json`  
  `1aedf3020a675096f1a2188c2c148f5fb028814f41827d22fd0818d956ec4099`
- `enums/edge_custody_event.enum.v1.json`  
  `f5578afc7a31de5c3f7afd1974fc90530bf60a307ee5d7134c98707e1139f389`
- `enums/field_history_event_type.enum.v1.json`  
  `0a8fe27c92fb127d61ccee7740fd8db5765d49551edb493f650e5e01b8b3618c`
- `enums/mission_status.enum.v1.json`  
  `f8623eaef3c959c65c9469cd761430acfd372bd8aba1010855a1e2f0a08b3478`
- `enums/payment_method.enum.v1.json`  
  `14291b81875704058bf6eed4e701ec7a1325b48d08fccd21f6227e4f6659e12c`
- `enums/payment_status.enum.v1.json`  
  `08df313506b10f37da55ee2e07e5175c6a3785c8c89e50420f538d945b92f7ae`
- `enums/payment_status.enum.v2.json`  
  `03cc82adf59a8f04ed7122b806b8796eb8f6c7fd0aaf98a01ffd5f40ff753029`
- `enums/payment_target_type.enum.v1.json`  
  `761b3e420245b1dabce63308572f9aa82da64eaf89381533491f28e1e3258c50`
- `enums/phenology_stage.enum.v1.json`  
  `da82e4621ec668e8fce146a86e3facd446cf164a5741e0c9a13333d50379d4cb`
- `enums/qc_status.enum.v1.json`  
  `889b0f3010678976e7ac351977b5d83391d9d119c91e50e060bc027c32134206`
- `enums/quarantine_decision.enum.v1.json`  
  `641b5a9e766f7e91837695954d1d0b45aeca6bfbe67356f12a0a65f762fa91c0`
- `enums/report_phase.enum.v1.json`  
  `a0f74cd5200ebf9cb7860473b331997e0faca3a404ff932d6cf868ecbdd2b8e8`
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
  `5f3aba49cc653a8679f8d43b09d5788f8378df8f35879755ae36d3f6fe618d94`
- `schemas/datasets/dataset.v1.schema.json`  
  `652b794330b3a087152716091402f962722abbe1038a73b26cfb049545c12b89`
- `schemas/datasets/dataset_manifest.v1.schema.json`  
  `e2a02116b45ed4275dbf02bbc5e5f49281e6a048b33264d923ca6a7634ff7d78`
- `schemas/datasets/evidence_bundle_ref.v1.schema.json`  
  `8897f5873ad9e97083309cb35cf4a8c1ebef213a253c28ac7beb2fe12db51e21`
- `schemas/datasets/qc_report.v1.schema.json`  
  `f3de16e8d4c816a06cc2e9a1dbda6797db3a41d28e27b6df70d372ace8d68e70`
- `schemas/datasets/scan_report.v1.schema.json`  
  `cf1197c4d4c552ce7c3516317bd5224a3c114d067843260bdc294fd4bf14a430`
- `schemas/datasets/transfer_batch.v1.schema.json`  
  `b72a86ecf37ba3768843a105ac6c0c066124e68e74cd4c8c469f73e552ddd2f9`
- `schemas/datasets/verification_report.v1.schema.json`  
  `c9bb30e2e9d129ea64a7695fc29e95846147a061aa0ab7e56c6f809bc519dd40`

### Edge Schemas

- `schemas/edge/attestation_record.v1.schema.json`  
  `fab5bddcbcedfdac410f9bc9d9ae9714174630db6e24056c3cc95185f0dbd2e3`
- `schemas/edge/calibrated_dataset_manifest.v1.schema.json`  
  `5490dabf9c14bae4b87640636d111f91ff00f58e20e4f1458cc6de8fe484e81f`
- `schemas/edge/calibration_result.v1.schema.json`  
  `cf67bfa0642dc24e0745ed4fd32cf12c1190206e36684a06c7127d3c816c58be`
- `schemas/edge/dataset_manifest.v1.schema.json`  
  `b5a6f03d6aae2dc3e39605e1b2bf80729abcdfe3ebc73c6099747cf44127c5be`
- `schemas/edge/edge_metadata.v1.schema.json`  
  `d081229b4092d67d1a38e61b994a8d4a83010d695c6b0769c3e31ac80312f851`
- `schemas/edge/evidence_bundle_ref.v1.schema.json`  
  `7c2f17fca155d8c37047c165c021b8daa5f725aa8719663d15a6ede62f20f3fd`
- `schemas/edge/intake_manifest.v1.schema.json`  
  `a39dc944a128cf8e7dc84aa758e833041312355790c83189d0dfd855a97b54ae`
- `schemas/edge/qc_report.v1.schema.json`  
  `4193e9c6d73ddd98bf62ba5b2ea034263cb9a86b69f6c549e7d77ed5bc93d219`
- `schemas/edge/quarantine_event.v1.schema.json`  
  `8ea1bf0eea7409b4cbfdc5608cda4689970a24eae7bbbfe251b7d66790e6bc94`
- `schemas/edge/scan_report.v1.schema.json`  
  `d07e24a4c295f54bfc50da7f9e3cfb51ae95c0264d6ea3d02a8798e370ca9d28`
- `schemas/edge/transfer_batch.v1.schema.json`  
  `3dcc72d3097dad67d3216641b1d2bdecb44e6bfacb763c5fe3893cc21beb8472`
- `schemas/edge/upload_receipt.v1.schema.json`  
  `dafd4c505bbc6703b9a400d278635f09f5eb86f2ffacce9606763145108d0eab`
- `schemas/edge/verification_report.v1.schema.json`  
  `aa84f86d4ca03b515af8fc551ab66197f46e6dd532f6b48601f591e2be197d42`
- `schemas/edge/worker_result.v1.schema.json`  
  `8e0b4a7f3c030e19d53dc5064666e16f5f458b501ebd9611e8912b628b95e5a2`

### Worker Schemas

- `schemas/worker/analysis_job.v1.schema.json`  
  `0d235742987d438a7cdc256b7f75bc13a348a6d67f198aae8c25cab8c6d535f8`
- `schemas/worker/analysis_result.v1.schema.json`  
  `3ce26669ee388d46483352b54c416d4351963e52121d8dcc32ef575bb4d3b8c6`
- `schemas/worker/calibrated_dataset.v1.schema.json`  
  `31d201316f59f0c438ebd2018dff5a662441beb072ff148f79f8ce45e7d8de88`
- `schemas/worker/calibration_metadata.v1.schema.json`  
  `fce8bfc0957adc3fc7de86a2e88fb40790b9f05c50a3ed5e2103c8783031aac2`
- `schemas/worker/expert_feedback.v1.schema.json`  
  `c0c2a1103fbec11e10d649d0cc8233f82f32f1caef3fcf51df54d149ba16123f`
- `schemas/worker/expert_labeling_card.v1.schema.json`  
  `a3f9c3b8a37cbc6424fa832a22ceca210910ee08fe3285d7924dd856d9f6f70c`
- `schemas/worker/expert_review_queue.v1.schema.json`  
  `1d5c926e51749eba46689ddb6b9d3af5d41e56cdfee12548b2fc0e68967400b9`
- `schemas/worker/thermal_analysis_result.v1.schema.json`  
  `c7b013adce00fa5618214865d869f1f85d68dad83786b21d27f9ea019c8de212`

### Events

- `schemas/events/analysis_completed.v1.schema.json`  
  `6f093470ce2644ffff3bb1e05c9148a2650723e7f4420dcddd81f228006a4db6`
- `schemas/events/analysis_preliminary_ready.v1.schema.json`  
  `7d8a8a4b5764c54417c4a32dbf591749a962bb4e3902f22b9997245a6d50c4d0`
- `schemas/events/analysis_review_requested.v1.schema.json`  
  `c1e4d6f2a7866bed9d2fde61b43108892570c4ecb9b5b74033dae1570e46a35b`
- `schemas/events/dataset_analyzed.v1.schema.json`  
  `13be86abb9d3be607d1779a02a42fa34742a37254f23bbf687475560c9410ed2`
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
  `9fb0649f1d2e214553f4afc4148cf3ebf6358e9f9dcb0effd83188f0370e1035`
- `schemas/events/field_health_changed.v1.schema.json`  
  `46e9405d4137f863ce2e1260ccc73a18bf5df77dd29d6222963a7765195ceeaa`
- `schemas/events/mission_assigned.v1.schema.json`  
  `6a3d4a6cb0b286cfa4f35fa8cab41a8d5fe04c410c90f8bb83a59cdeee77f2c3`

### Platform

- `schemas/platform/calibrated_dataset_manifest.v1.schema.json`  
  `40e1656e914b9c420007fd109c128828c0710d3a7a730dfd58f1edec5a77d3fc`
- `schemas/platform/calibration_result.v1.schema.json`  
  `c51b377e0aa6922d0b86f4cf9076093d66fc4c13a747f44da3f7059c40a73038`
- `schemas/platform/evidence_bundle_ref.v1.schema.json`  
  `879e2c3762d92d257c579112c1a741dae78e33997a7c5ec53506dbc6e73bd109`
- `schemas/platform/layer_registry.v1.schema.json`  
  `dcca0ac46ee0105da86a9c6f5dd867874b38bc288418c6807ec270c6e4a8cfeb`
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
  `b2f20d016265619a92019ec7585b1d9573ba6c2639f458b8bfc4637c2ed8a438`

### API Components

- `api/components/parameters.yaml`  
  `ed7e7fd541e74f323606f17329b0bb9cadf993a9be30eb296ecc553cec1ba26f`
- `api/components/responses.yaml`  
  `d7fcd4ce585d77ef9d260ea53c89b3d513d0f9628980ca356aa24b6cc5796308`
- `api/components/schemas.yaml`  
  `2676ba18722b6410ee5865aef2233831047932a0c0dcfcaa98a233d58a1e8782`
- `api/components/security_schemes.yaml`  
  `9d45e3181a4b847b617a0553c72458650aa9c3deacf38cbed67c5c12db3e1c79`

### API Specs

- `api/edge_local.v1.yaml`  
  `510fac0f988752927353a6ec0fe431fe0098fbec2600074a39ca96103f040ccd`
- `api/platform_internal.v1.yaml`  
  `f253f4b68be11f4a1f65416827a6482106017a63c940c39e46eb90e69232cbb7`
- `api/platform_public.v1.yaml`  
  `840e42906cdff3f096bc1f03b004ebd35e538b97c93371f7268fe5741980dca1`

---

## Changelog

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

assert verify_contracts("0dd8351a8d845835a1e560e6748f22e1c68637f74decc34ac29287176d581afc"), "Contracts checksum mismatch!"
```

### Node.js
```javascript
const crypto = require('crypto');
const assert = require('assert');

function verifyContracts(expectedChecksum) {
  const actualChecksum = computeContractsChecksum();
  return actualChecksum === expectedChecksum;
}

assert(verifyContracts("0dd8351a8d845835a1e560e6748f22e1c68637f74decc34ac29287176d581afc"), "Contracts checksum mismatch!");
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

**Last Updated:** 2026-07-11T12:30:17.879399Z
