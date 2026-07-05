# TarlaAnaliz Contracts Version Lock

## Version: 5.1.0

**Release Date:** 2026-07-05T00:00:00.000000Z  
**Breaking Change:** NO  
**Contracts Checksum (SHA-256):** `9fe88842483a20f26dee28a235b9829d75bc702f459d3f802f40049f4a63db5c`

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

---

## Changelog

### v5.1.0 (2026-07-05)

**Breaking:** NO

MINOR (non-breaking): KR-092 yeni sema seasonal_flight_calendar.v1.schema.json eklendi. GAP bolgesi 5 urun (COTTON/CORN/RICE/GRAPE/PISTACHIO) icin haftalik sezonluk ucus takvimi (tek skalar irtifa Y / hiz v, bolgesel MM-DD pencereleri). Yeni sema eklemesi = SemVer MINOR; mevcut semalar/enumlar degismedi.

### v5.0.0 (2026-06-30)

**Breaking:** YES

MAJOR (BREAKING): payment_method.enum.v1 TARIS_DEDUCTION kaldirildi. Taris Ege bolgesi kooperatifi; tarlaanaliz yalniz GAP'a hizmet eder. Kalan: CREDIT_CARD, IBAN_TRANSFER. Migration: docs/migration_guides/payment_method_v5_remove_taris.md

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

assert verify_contracts("9fe88842483a20f26dee28a235b9829d75bc702f459d3f802f40049f4a63db5c"), "Contracts checksum mismatch!"
```

### Node.js
```javascript
const crypto = require('crypto');
const assert = require('assert');

function verifyContracts(expectedChecksum) {
  const actualChecksum = computeContractsChecksum();
  return actualChecksum === expectedChecksum;
}

assert(verifyContracts("9fe88842483a20f26dee28a235b9829d75bc702f459d3f802f40049f4a63db5c"), "Contracts checksum mismatch!");
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

**Last Updated:** 2026-07-05T00:00:00.000000Z
