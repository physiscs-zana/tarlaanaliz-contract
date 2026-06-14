# TarlaAnaliz Contracts Version Lock

## Version: 4.0.0

**Release Date:** 2026-06-14T17:38:24.311513Z  
**Breaking Change:** YES  
**Contracts Checksum (SHA-256):** `352b3dfb36ee251e04677b0a972ff2042ab25e92b96e1cdac34e4e7f5bd9e6ac`

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

### v4.0.0 (2026-06-14)

**Breaking:** YES

**MAJOR/BREAKING**: crop_type worker-canonical 14 degere hizalandi. BARLEY+POTATO kaldirildi (worker portfoy karari 2026-05-18), CHERRY+FIG+RICE eklendi. expert_review_queue.v1 inline enum + enums/crop_type.enum.v1 guncellendi. Bkz migration_guides/crop_type_v1_to_v2.md.

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

assert verify_contracts("352b3dfb36ee251e04677b0a972ff2042ab25e92b96e1cdac34e4e7f5bd9e6ac"), "Contracts checksum mismatch!"
```

### Node.js
```javascript
const crypto = require('crypto');
const assert = require('assert');

function verifyContracts(expectedChecksum) {
  const actualChecksum = computeContractsChecksum();
  return actualChecksum === expectedChecksum;
}

assert(verifyContracts("352b3dfb36ee251e04677b0a972ff2042ab25e92b96e1cdac34e4e7f5bd9e6ac"), "Contracts checksum mismatch!");
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

**Last Updated:** 2026-06-14T17:38:24.311513Z
