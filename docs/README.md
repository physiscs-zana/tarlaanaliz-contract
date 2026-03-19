# TarlaAnaliz Contracts Documentation

> **Single source of truth** for all TarlaAnaliz API contracts, schemas, and integration specifications.

## 📚 Documentation Map

### Quick Start

| Question | Document |
|----------|----------|
| "How do I integrate my service?" | [Integration Guide](#integration-guide) |
| "What changed in this version?" | `GUNCELLEMELER.md`, `CONTRACTS_VERSION.md` |
| "How do I validate my payloads?" | [Validation Guide](#validation-guide) |
| "What are the breaking change rules?" | `versioning_policy.md` |
| "How do I contribute a schema change?" | [Contributing](#contributing) |

---

## 📖 Documentation Structure

```
tarlaanaliz-contracts/
│
├── README.md                         # 👈 Repository overview
├── CONTRACTS_VERSION.md              # Version lock + checksums
├── versioning_policy.md              # Semantic versioning rules
├── GUNCELLEMELER.md                  # KR-002 update summary
│
├── docs/                             # 👈 YOU ARE HERE
│   ├── README.md                     # 👈 This file (documentation map)
│   ├── examples/                     # Example payloads
│   │   ├── README.md                 # Example validation guide
│   │   ├── field.example.json
│   │   ├── mission.example.json
│   │   └── ...
│   ├── canonical/                    # Kanonik iş dokümanları (v2.4 .docx)
│   ├── checklists/                   # SDLC gate kontrol listeleri
│   │
│   └── migration_guides/             # Kırıcı değişiklik geçiş rehberleri
│
├── schemas/                          # JSON Schema definitions
│   ├── shared/                       # Shared types (GeoJSON, Address, Money)
│   ├── enums/                        # Enums (Crop, Role, Status, etc.)
│   ├── core/                         # Core entities (Field, Mission, User)
│   ├── edge/                         # Edge schemas (Intake, Quarantine)
│   ├── worker/                       # Worker schemas (Job, Result)
│   ├── events/                       # Domain events
│   └── platform/                     # Platform schemas (Pricing, Payroll)
│
├── api/                              # OpenAPI specifications
│   ├── components/                   # Reusable components
│   ├── platform_public.v1.yaml       # Public API (web/mobile)
│   ├── platform_internal.v1.yaml     # Internal API (services)
│   └── edge_local.v1.yaml            # Edge local API (kiosk)
│
└── tools/                            # Automation tools
    ├── validate.py                   # Schema validator
    ├── pin_version.py                # Version pinner
    ├── breaking_change_detector.py   # Breaking change detector
    ├── generate_types.sh             # Type generator
    └── sync_to_repos.sh              # Repo sync tool
```

---

## 🎯 Core Concepts

### Contract-First Development

TarlaAnaliz follows **contract-first** development:

1. **Contracts define interfaces** - Schemas are the single source of truth
2. **Code is generated** - TypeScript/Python types generated from schemas
3. **Validation is automated** - All payloads validated against schemas
4. **Versioning is strict** - Semantic versioning with breaking change detection

### Key Principles

#### 1. PII Minimization (KR-050)
- **NO email** in any schema
- **NO TCKN** (Turkish ID number)
- **NO OTP** (one-time passwords)
- Authentication: **Phone + PIN only**
- Separate PII vault: `user_pii.v1.schema.json`

#### 2. KR-002 Compliance
- **8 GAP crops only**: COTTON, PISTACHIO, MAIZE, WHEAT, SUNFLOWER, GRAPE, OLIVE, RED_LENTIL
- **7 map layers only**: HEALTH, DISEASE, PEST, FUNGUS, WEED, WATER_STRESS, NITROGEN_STRESS
- **No prescriptions** - AI provides map layers, NOT action recommendations

#### 3. Chain-of-Custody
- Every file tracked with SHA-256 hash
- Intake → Quarantine → Analysis → Result
- Full audit trail from edge to platform

#### 4. Immutability
- Events are immutable once published
- Price books are immutable once approved
- Version pins are immutable

---

## 🔍 Finding the Right Schema

### By Use Case

| Use Case | Schema | Example |
|----------|--------|---------|
| Register a field | `core/field.v1.schema.json` | `examples/field.example.json` |
| Create a mission | `core/mission.v1.schema.json` | `examples/mission.example.json` |
| Submit drone data | `edge/intake_manifest.v1.schema.json` | `examples/intake_manifest.example.json` |
| Queue AI analysis | `worker/analysis_job.v1.schema.json` | `examples/analysis_job.example.json` |
| Retrieve results | `worker/analysis_result.v1.schema.json` | `examples/analysis_result.example.json` |

### By Entity

| Entity | Schema Location |
|--------|----------------|
| Field | `schemas/core/field.v1.schema.json` |
| Mission | `schemas/core/mission.v1.schema.json` |
| User | `schemas/core/user.v1.schema.json` |
| User PII | `schemas/core/user_pii.v1.schema.json` |
| Intake Manifest | `schemas/edge/intake_manifest.v1.schema.json` |
| Analysis Job | `schemas/worker/analysis_job.v1.schema.json` |
| Analysis Result | `schemas/worker/analysis_result.v1.schema.json` |
| Price Book | `schemas/platform/pricing.v1.schema.json` |
| Payroll | `schemas/platform/payroll.v1.schema.json` |

### By Enum

| Enum | Schema Location | Values |
|------|----------------|--------|
| Crop Type | `enums/crop_type.enum.v1.json` | 8 GAP crops |
| Analysis Type | `enums/analysis_type.enum.v1.json` | 7 KR-002 layers |
| Role | `enums/role.enum.v1.json` | 11 roles |
| Mission Status | `enums/mission_status.enum.v1.json` | 17 statuses |

---

## ✅ Validation Guide

### Validate Your Payload

```bash
# Install jsonschema
pip install jsonschema --break-system-packages

# Validate example
python3 -c "
import json
from jsonschema import Draft202012Validator

# Load schema
with open('schemas/core/field.v1.schema.json') as f:
    schema = json.load(f)

# Load your payload
with open('my_field.json') as f:
    payload = json.load(f)

# Validate
validator = Draft202012Validator(schema)
errors = list(validator.iter_errors(payload))

if errors:
    for error in errors:
        print(f'Error: {error.message}')
else:
    print('✅ Valid!')
"
```

### Using the Validator Tool

```bash
# Validate all schemas
python3 tools/validate.py

# This checks:
# ✅ Draft 2020-12 compliance
# ✅ unevaluatedProperties: false
# ✅ No forbidden fields (email/tckn/otp)
# ✅ Enum uniqueness
```

---

## 🚀 Integration Guide

### For Platform Service (TypeScript)

```bash
# Add contracts as submodule
git submodule add https://github.com/tarlaanaliz/contracts contracts
git submodule update --remote

# Sync contracts
export PLATFORM_DIR=$(pwd)
cd contracts
./tools/sync_to_repos.sh --target platform

# Use generated types
import { Field, Mission } from './src/types/contracts';
```

### For Edge Station (Python)

```bash
# Add contracts
git submodule add https://github.com/tarlaanaliz/contracts contracts
git submodule update --remote

# Sync contracts
export EDGE_DIR=$(pwd)
cd contracts
./tools/sync_to_repos.sh --target edge

# Use generated types
from contracts.field_v1 import Field
from contracts.intake_manifest_v1 import IntakeManifest
```

### For Worker Service (Python)

```bash
# Add contracts
git submodule add https://github.com/tarlaanaliz/contracts contracts
git submodule update --remote

# Sync contracts
export WORKER_DIR=$(pwd)
cd contracts
./tools/sync_to_repos.sh --target worker

# Use generated types
from contracts.analysis_job_v1 import AnalysisJob
from contracts.analysis_result_v1 import AnalysisResult
```

---

## 🔄 Version Management

### Checking Current Version

```bash
# Read version
grep "Version:" CONTRACTS_VERSION.md

# Verify checksum
python3 tools/pin_version.py --verify
```

### Updating Version

```bash
# Patch (bug fixes, documentation)
python3 tools/pin_version.py --patch

# Minor (new features, non-breaking)
python3 tools/pin_version.py --minor

# Major (breaking changes)
python3 tools/pin_version.py --major --breaking
```

### Detecting Breaking Changes

```bash
# Compare versions
python3 tools/breaking_change_detector.py --old v1.0.0 --new v2.0.0

# Generate PR comment
python3 tools/breaking_change_detector.py --old v1.0.0 --new . --pr-comment
```

---

## 📊 KR Reference

### Kanonik Requirements

| KR | Title | Affected Schemas |
|----|-------|------------------|
| KR-002 | Map Layer Definitions | `analysis_type.enum`, `layer_registry` |
| KR-013 | Field Management | `field`, `field_created` |
| KR-015 | Pilot Management | `mission`, `mission_assigned` |
| KR-016 | Crop-Model Routing | `mission`, `analysis_job` |
| KR-017 | Analysis Flow | `analysis_job`, `analysis_result` |
| KR-020-022 | Pricing | `pricing` |
| KR-031 | Payroll | `payroll` |
| KR-040 | Security | `intake_manifest`, `quarantine_event` |
| KR-050 | Identity Model | `user_pii` (phone + PIN) |
| KR-063 | RBAC | `user`, `role` |
| KR-064 | Layer Registry | `layer_registry` |
| KR-066 | KVKK/GDPR | `user_pii` |
| KR-070 | AI Isolation | `analysis_job` |
| KR-071 | One-Way Flow | `analysis_completed` |

---

## 🛠️ Tools Reference

### validate.py
Validates all schemas against policies.

```bash
python3 tools/validate.py
```

### pin_version.py
Pins contract version with checksums.

```bash
python3 tools/pin_version.py --major --breaking
```

### breaking_change_detector.py
Detects breaking changes between versions.

```bash
python3 tools/breaking_change_detector.py --old v1.0.0 --new v2.0.0
```

### generate_types.sh
Generates TypeScript and Python types.

```bash
./tools/generate_types.sh
```

### sync_to_repos.sh
Syncs contracts to consumer repositories.

```bash
./tools/sync_to_repos.sh --target platform
```

---

## 📝 Contributing

### Schema Change Workflow

1. **Create feature branch**
   ```bash
   git checkout -b feature/add-new-field
   ```

2. **Update schema**
   - Edit schema file
   - Update example
   - Run validation

3. **Validate changes**
   ```bash
   python3 tools/validate.py
   pytest tests/
   ```

4. **Check for breaking changes**
   ```bash
   python3 tools/breaking_change_detector.py --old main --new .
   ```

5. **Create PR**
   - CI will automatically validate
   - Breaking changes will be flagged
   - Version bump recommendation provided

6. **Merge and release**
   - Merge to main
   - Pin new version
   - Auto-sync to consumer repos

---

## 🔐 Security

- **PII Protection**: Minimal PII, separate vault
- **Hash Verification**: SHA-256 chain-of-custody
- **Forbidden Fields**: No email/TCKN/OTP
- **KVKK Compliance**: Data retention, deletion policies

---

## 📞 Support

- **Documentation Issues**: Open issue in this repo
- **Schema Questions**: Check examples/ first, then ask
- **Integration Help**: See integration guide above

---

**Last Updated:** 2026-03-07
**Current Version:** 2.0.1
**Compliance:** KR-002 ✅ | KR-033 ✅ | KR-050 ✅ | KVKK ✅ | Draft 2020-12 ✅