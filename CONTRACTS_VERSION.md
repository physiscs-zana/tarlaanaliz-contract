# TarlaAnaliz Contracts Version Lock

## Version: 3.0.0

**Release Date:** 2026-06-14T17:32:22.122311Z  
**Breaking Change:** YES  
**Contracts Checksum (SHA-256):** `ad485ac4975c8b5242548755c9ee3410488f72a643779ed4b087388c59ef10c8`

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

### v3.0.0 (2026-06-14)

**Breaking:** YES

**MAJOR/BREAKING**: field.v1 + expert_labeling_card.v1 region enum'larindan EGE cografi bolgesi kaldirildi. tarlaanaliz yalnizca GAP bolgesi icindir; Ege cografyasi desteklenmez (egeanaliz ayri dagitim).

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

assert verify_contracts("ad485ac4975c8b5242548755c9ee3410488f72a643779ed4b087388c59ef10c8"), "Contracts checksum mismatch!"
```

### Node.js
```javascript
const crypto = require('crypto');
const assert = require('assert');

function verifyContracts(expectedChecksum) {
  const actualChecksum = computeContractsChecksum();
  return actualChecksum === expectedChecksum;
}

assert(verifyContracts("ad485ac4975c8b5242548755c9ee3410488f72a643779ed4b087388c59ef10c8"), "Contracts checksum mismatch!");
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

**Last Updated:** 2026-06-14T17:32:22.122311Z
