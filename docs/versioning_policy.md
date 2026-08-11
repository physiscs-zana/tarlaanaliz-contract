# Versioning Policy

Bu dokümant **tarlaanaliz-contracts** repository'si için versiyon yönetimi, breaking change kuralları, deprecation süreci ve release prosedürlerini tanımlar.

## 📋 İçindekiler

- [JSON Schema Standardı](#json-schema-standardı)
- [Semantic Versioning (SemVer)](#semantic-versioning-semver)
- [Breaking Change Kuralları](#breaking-change-kuralları)
- [Deprecation Süreci](#deprecation-süreci)
- [Release Prosedürü](#release-prosedürü)
- [Migration Guide Gereksinimleri](#migration-guide-gereksinimleri)
- [Consumer Koordinasyonu](#consumer-koordinasyonu)

---

## JSON Schema Standardı

### Normatif Standart

**tarlaanaliz-contracts** repository'si **JSON Schema Draft 2020-12** standardını kullanır.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema"
}
```

### İlk Etap Profili

Karmaşıklığı kontrol altında tutmak için Draft 2020-12'nin şu iki özelliği zorunludur:

#### 1. `$defs` — Tekrar Kullanılan Tipler

Ortak tip tanımları `$defs` altında toplanır:

```json
{
  "$defs": {
    "ObjectId": {
      "type": "string",
      "pattern": "^[a-f0-9]{24}$",
      "description": "MongoDB ObjectId format"
    },
    "Timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp (UTC)"
    },
    "GeoPoint": {
      "type": "object",
      "properties": {
        "type": { "const": "Point" },
        "coordinates": {
          "type": "array",
          "items": { "type": "number" },
          "minItems": 2,
          "maxItems": 2
        }
      },
      "required": ["type", "coordinates"]
    }
  }
}
```

**Amaç**:
- Tekrar azaltma
- Refactor maliyetini düşürme
- Servisler arası tutarlılık

#### 2. `unevaluatedProperties: false` — Şema Dışı Alan Engelleme

Her şemada `unevaluatedProperties: false` zorunludur:

```json
{
  "type": "object",
  "properties": {
    "id": { "type": "string" },
    "name": { "type": "string" }
  },
  "required": ["id", "name"],
  "unevaluatedProperties": false  // ← ZORUNLU
}
```

**Amaç**:
- Tanımlanmayan alanların sisteme sızmasını engelleme
- "Gizli alan" drift'ini önleme
- Veri çöplüğü riskini minimize etme

**Kontrol**: `tools/validate.py    # (bayrak YOK — tüm kurallar tek koşumda)

### İleride Eklenebilir Özellikler

İhtiyaç oldukça kontrollü şekilde eklenebilir:

| Özellik | Amaç | Eklenme Koşulu |
|---------|------|----------------|
| `dependentSchemas` | Koşullu şema gereksinimleri | Karmaşık veri modeli |
| `if/then/else` | Koşullu validasyon | Durum bazlı kurallar |
| `dynamicRef` | Dinamik referanslar | Polimorfik yapılar |
| `patternProperties` | Pattern bazlı alanlar | Serbest key'li map'ler |

**Ekleme Prosedürü**:
1. RFC dokümantı oluştur (`docs/rfc/`)
2. Proof-of-concept şema
3. Test coverage
4. Team review + onay
5. Dokümantasyon güncelleme

---

## Semantic Versioning (SemVer)

### Format

```
MAJOR.MINOR.PATCH
```

Örnek: `2.4.1`

### MAJOR (X.0.0)

**Breaking change'ler** MAJOR bump gerektirir.

#### JSON Schema Breaking Changes

| Değişiklik | Örnek | Breaking? |
|------------|-------|-----------|
| Zorunlu alan ekleme | `required: ["id"]` → `required: ["id", "email"]` | ✅ Evet |
| Alan tipini değiştirme | `type: "string"` → `type: "number"` | ✅ Evet |
| Enum değeri silme | `enum: ["A", "B", "C"]` → `enum: ["A", "B"]` | ✅ Evet |
| Constraint sıkılaştırma | `minLength: 1` → `minLength: 5` | ✅ Evet |
| Alan adı değiştirme | `user_id` → `userId` | ✅ Evet |
| Alan silme | `properties: {email}` → `properties: {}` | ✅ Evet |
| Opsiyonel alan ekleme | `required: ["id"]` → `properties: {email}` | ❌ Hayır |
| Enum değeri ekleme | `enum: ["A"]` → `enum: ["A", "B"]` | ❌ Hayır |
| Constraint gevşetme | `minLength: 5` → `minLength: 1` | ❌ Hayır |

#### OpenAPI Breaking Changes

| Değişiklik | Örnek | Breaking? |
|------------|-------|-----------|
| Endpoint silme | `DELETE /api/users/{id}` | ✅ Evet |
| HTTP metodu değiştirme | `POST` → `PUT` | ✅ Evet |
| Path parametresi değiştirme | `/users/{id}` → `/users/{userId}` | ✅ Evet |
| Zorunlu query param ekleme | `?filter` (optional) → `?filter` (required) | ✅ Evet |
| Response yapısı değiştirme | `{id, name}` → `{userId, fullName}` | ✅ Evet |
| Status code değiştirme | `200 OK` → `201 Created` | ✅ Evet |
| Yeni endpoint ekleme | `POST /api/v1/reports` | ❌ Hayır |
| Opsiyonel param ekleme | `?sort` (optional) | ❌ Hayır |
| Response alan ekleme | `{id, name}` → `{id, name, email}` | ❌ Hayır |

### MINOR (x.Y.0)

**Geriye dönük uyumlu** yeni özellikler:

- ✅ Opsiyonel JSON Schema alanı ekleme
- ✅ Enum'a yeni değer ekleme
- ✅ Yeni OpenAPI endpoint ekleme
- ✅ Response'a opsiyonel alan ekleme
- ✅ Yeni şema dosyası ekleme

**Örnek**:

```diff
// v1.2.0 → v1.3.0
{
  "properties": {
    "id": { "type": "string" },
    "name": { "type": "string" },
+   "email": { "type": "string" }  // ← Opsiyonel (required listesinde değil)
  },
  "required": ["id", "name"]
}
```

### PATCH (x.y.Z)

**Geriye dönük uyumlu** düzeltmeler:

- ✅ Dokümantasyon düzeltmesi
- ✅ Örnek (examples/) güncelleme
- ✅ `description` alanı değişikliği
- ✅ Validasyon constraint'i gevşetme
- ✅ Typo düzeltmeleri

**Örnek**:

```diff
// v1.2.1 → v1.2.2
{
  "properties": {
    "name": {
      "type": "string",
-     "minLength": 5
+     "minLength": 1  // ← Constraint gevşetme (non-breaking)
    }
  }
}
```

---

## Breaking Change Kuralları

### Tespit

Breaking change'ler otomatik tespit edilir:

```bash
python tools/breaking_change_detector.py --from v1.2.0 --to HEAD
```

**Çıktı**:

```
⚠ BREAKING CHANGES DETECTED:

File: schemas/core/field.v1.schema.json
- Added required field: 'crop_type'
- Changed type of 'area': number → string

File: enums/mission_status.enum.v1.json
- Removed enum value: 'DEPRECATED_STATUS'

File: api/platform_public.v1.yaml
- Removed endpoint: DELETE /api/v1/fields/{id}
- Changed response schema: POST /api/v1/missions

ACTION REQUIRED:
1. Bump MAJOR version (2.0.0)
2. Create migration guide (docs/migration_guides/field_v1_to_v2.md)
3. Set breaking_change: true in CONTRACTS_VERSION.md
4. Update CHANGELOG.md
```

### SDLC Gate

Breaking change varsa:

1. **PR Gate**: `breaking_change_detector.py` FAIL
2. **Developer Action**: Migration guide yaz
3. **Code Review**: Migration guide + breaking change gerekçesi
4. **CI Gate**: Version bump kontrolü (MAJOR mı?)
5. **Release Gate**: Consumer koordinasyonu

### Migration Guide Zorunluluğu

Breaking change varsa migration guide **zorunludur**:

```
docs/migration_guides/
├─ MIGRATION_GUIDE_TEMPLATE.md
├─ field_v1_to_v2.md
└─ mission_v2_to_v3.md
```

Detaylar için [Migration Guide Gereksinimleri](#migration-guide-gereksinimleri) bölümüne bakın.

---

## Deprecation Süreci

Deprecation, breaking change'i iki aşamaya yayar.

### Adımlar

#### 1. MINOR Version: Deprecation Warning

```json
{
  "properties": {
    "user_id": {
      "type": "string",
      "deprecated": true,
      "description": "DEPRECATED: Use 'userId' instead. Will be removed in v2.0.0"
    },
    "userId": {
      "type": "string",
      "description": "User identifier (replaces deprecated 'user_id')"
    }
  }
}
```

**Changelog**:

```markdown
## [1.5.0] - 2026-02-01

### Deprecated
- `user_id` field in `schemas/core/user.v1.schema.json` (use `userId` instead)
  - Removal planned for v2.0.0
```

**Consumer Action**: Uyarı logları; kod güncellemesi için zaman var

#### 2. MAJOR Version: Removal

```json
{
  "properties": {
    "userId": {
      "type": "string",
      "description": "User identifier"
    }
  }
}
```

**Changelog**:

```markdown
## [2.0.0] - 2026-03-01

### Removed (Breaking)
- `user_id` field (deprecated in v1.5.0) — use `userId` instead

### Migration Guide
- See: docs/migration_guides/user_v1_to_v2.md
```

### Deprecation Timeline

| Değişiklik Tipi | Minimum Deprecation Süresi |
|-----------------|---------------------------|
| JSON Schema alan | 2 MINOR version (min 1 ay) |
| Enum değer | 2 MINOR version (min 1 ay) |
| OpenAPI endpoint | 3 MINOR version (min 2 ay) |

**Örnek Timeline**:

```
v1.3.0 (2026-01-15): user_id deprecated
v1.4.0 (2026-02-01): still supported
v1.5.0 (2026-02-15): still supported (warning logs)
v2.0.0 (2026-03-15): user_id removed (breaking)
```

---

## Release Prosedürü

### Öncesi Hazırlık

#### 1. Version Bump

```bash
# Breaking change varsa
python tools/pin_version.py --bump major

# Yeni feature varsa
python tools/pin_version.py --bump minor

# Bug fix varsa
python tools/pin_version.py --bump patch
```

**Output**:

```
Current version: 1.2.3
New version: 2.0.0
Breaking change: true

✓ CONTRACTS_VERSION.md updated
✓ SHA-256 hash calculated
✓ Timestamp set
```

#### 2. Changelog Güncelleme

```markdown
## [2.0.0] - 2026-01-26

### Breaking Changes
- **schemas/core/field.v1.schema.json**: Added required field `crop_type`
- **enums/mission_status.enum.v1.json**: Removed deprecated value `OLD_STATUS`

### Migration Guide
- See: [docs/migration_guides/field_v1_to_v2.md](docs/migration_guides/field_v1_to_v2.md)

### Added
- New schema: `schemas/platform/pricing.v1.schema.json`

### Fixed
- Corrected `minLength` constraint in `user.name` field
```

#### 3. Migration Guide (Breaking Change Varsa)

Template'e göre yaz: `docs/migration_guides/MIGRATION_GUIDE_TEMPLATE.md`

Minimum içerik:
- **Scope**: Hangi değişiklikler?
- **Impact**: Hangi consumer'lar etkilenir?
- **Migration Steps**: Adım adım rehber
- **Code Examples**: Önce/sonra örnekleri
- **Rollback**: Geri dönüş prosedürü

#### 4. PR Review

Checklist: `docs/checklists/PR_GATE_CHECKLIST.md`

- [ ] Schema validation geçiyor (`python tools/validate.py`)
- [ ] Tests geçiyor (`pytest tests/`)
- [ ] Breaking change tespit edildi
- [ ] Version bump yapıldı (MAJOR)
- [ ] Migration guide yazıldı
- [ ] Changelog güncellendi
- [ ] Code review onayı

### Release

#### 1. Tag ve GitHub Release

```bash
git tag -a v2.0.0 -m "Release v2.0.0 - Breaking changes"
git push origin v2.0.0
```

> #### 📌 Tarihsel kayıt — SD8 (2026-08-01): 14 geriye dönük tag + 1 istisna
>
> **Sorun:** I-2 değişmezi (*"her contract sürümü annotated tag alır"*) tarihsel olarak
> **tutmuyordu.** Ölçüm: CHANGELOG'da **19 sürüm**, depoda yalnız **4 tag**
> (`v6.1.0`, `v7.0.1`, `v7.1.0`, `v7.2.0`) → **15 sürüm etiketsiz**. Etiketsiz sürüm,
> tüketicinin tag ile pinlenmesini engeller ve `git describe` çıktısını bulanıklaştırır
> (`vA.B.C-N-g…`).
>
> **Karar: geriye dönük tag AT — ama yalnız ölçülebilenlere.** 14 sürüme annotated
> retro-tag atıldı; her tag mesajında *retro olduğu*, *gerçek yayın tarihi* ve
> *release commit'inin nasıl bulunduğu* yazılıdır. Tag'lerin oluşturma tarihi
> 2026-08-01'dir, sürümlerin yayın tarihi değil — bu ayrım gizlenmez.
>
> **Yöntem (tahmin değil ölçüm):** release commit'i, `CONTRACTS_VERSION.md`'ye
> `## Version: X.Y.Z` satırının eklendiği commit'tir (`git log -S`). Yöntem, halihazırda
> etiketli **dört** sürümde **4/4 doğrulandı** — dördünde de mevcut tag ile ölçümün
> bulduğu commit aynı çıktı. Doğrulanmamış bir yöntemle tag atmak, doğrulanamaz kanıt
> üretirdi.
>
> **🔴 İSTİSNA — `2.0.2` etiketlenmedi ve etiketlenmeyecek.** CHANGELOG'da bir girdisi
> var (`## [2.0.2] - 2026-03-15`) ama `CONTRACTS_VERSION.md`'ye **hiçbir zaman**
> `## Version: 2.0.2` yazılmamış → release commit'i belirlenemiyor. Bu sürüm ya fiilen
> yayımlanmadı ya da sürüm kilidi güncellenmeden yayımlandı. **Uydurulmuş bir commit'e
> tag atmak, kilidi olmayan bir sürümü varmış gibi göstermek olurdu.** Kayıt buraya
> düşülür; tag atılmaz.
>
> **Doğrulama (bu turda koşuldu):** 14 sürüm commit'inin tamamında `git describe --tags`
> **temiz** `vX.Y.Z` döndü (0 bulanık); 18 tag'in tamamı annotated (`git cat-file -t` →
> `tag`). Tag push'u hiçbir workflow tetiklemez — `contract_validation.yml` yalnız
> `branches: [master]` push + `pull_request` dinler, `on: push: tags:` yok ve depoda
> release oluşturan bir adım bulunmuyor (ölçüldü). Yani retro-tag **yan etkisizdir**.

GitHub Release oluştur:

```markdown
## TarlaAnaliz Contracts v2.0.0

### ⚠️ Breaking Changes

This release contains breaking changes. See the [Migration Guide](docs/migration_guides/field_v1_to_v2.md) for upgrade instructions.

**Changed:**
- `schemas/core/field.v1.schema.json`: Added required field `crop_type`
- `enums/mission_status.enum.v1.json`: Removed deprecated `OLD_STATUS`

### Migration Guide

[Full migration guide](docs/migration_guides/field_v1_to_v2.md)

**Quick Steps:**
1. Update your Field model to include `crop_type` (required)
2. Remove references to `OLD_STATUS` enum value
3. Run type generation: `npm run types:gen`
4. Update tests

### Changelog

[View full changelog](CHANGELOG.md#200---2026-01-26)

---

**Contracts Version Lock:**
```yaml
version: 2.0.0
sha256: a3f2b8c9d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1
created_at: 2026-01-26T12:00:00Z
breaking_change: true
```
```

#### 2. Consumer Sync

```bash
./tools/sync_to_repos.sh --target platform   # (--version/--notify diye bayrak YOK)
```

Bu script:
1. Consumer repository'lere PR açar
2. `CONTRACTS_VERSION.md` günceller
3. Migration guide link'i ekler
4. Slack/email notification gönderir

#### 3. Consumer Koordinasyonu

Breaking change varsa:

1. **Notification**: Slack + Email
2. **Migration Window**: 2 hafta (önerilen)
3. **Support**: Consumer'lara migration desteği
4. **Rollback Plan**: Acil durumda geri dönüş

---

## Migration Guide Gereksinimleri

### Template

`docs/migration_guides/MIGRATION_GUIDE_TEMPLATE.md` kullanın.

### Zorunlu Bölümler

#### 1. Overview

```markdown
# Migration Guide: Field v1 → v2

**Version**: v1.5.0 → v2.0.0  
**Date**: 2026-01-26  
**Type**: Breaking Change

## Summary

This guide covers migration from Field schema v1 to v2.

**Key Changes:**
- Added required field: `crop_type`
- Renamed field: `user_id` → `userId`
- Removed deprecated field: `legacy_status`
```

#### 2. Impact Analysis

```markdown
## Impact Analysis

### Affected Components
- ✅ Platform API (`POST /api/v1/fields`)
- ✅ Edge intake (`intake_manifest.v1.schema.json`)
- ✅ Worker processing (`analysis_job.v1.schema.json`)

### Affected Repositories
- tarlaanaliz-platform
- tarlaanaliz-edge
- tarlaanaliz-worker

### Estimated Effort
- Small repo: 2 hours
- Medium repo: 4-6 hours
- Large repo: 1-2 days
```

#### 3. Migration Steps

```markdown
## Migration Steps

### Step 1: Update Schema

**Before (v1.5.0):**
```json
{
  "id": "field_123",
  "name": "North Field",
  "user_id": "user_456"  // deprecated
}
```

**After (v2.0.0):**
```json
{
  "id": "field_123",
  "name": "North Field",
  "userId": "user_456",  // renamed
  "crop_type": "COTTON"  // required
}
```

### Step 2: Update Code

**TypeScript:**
```typescript
// Before
interface Field {
  id: string;
  name: string;
  user_id: string;
}

// After
interface Field {
  id: string;
  name: string;
  userId: string;
  crop_type: CropType;  // required enum
}
```

**Python:**
```python
# Before
class Field(BaseModel):
    id: str
    name: str
    user_id: str

# After
class Field(BaseModel):
    id: str
    name: str
    user_id: str = Field(..., alias="userId")  # renamed
    crop_type: CropType  # required
```

### Step 3: Update Tests

```typescript
// Update test fixtures
const mockField: Field = {
  id: "field_123",
  name: "Test Field",
  userId: "user_456",  // renamed
  crop_type: CropType.COTTON  // added
};
```

### Step 4: Data Migration

```sql
-- If you have existing data
UPDATE fields
SET 
  user_id_new = user_id,
  crop_type = 'UNKNOWN'  -- default value
WHERE crop_type IS NULL;

ALTER TABLE fields
  RENAME COLUMN user_id TO user_id_old,
  RENAME COLUMN user_id_new TO user_id,
  ALTER COLUMN crop_type SET NOT NULL;
```
```

#### 4. Validation

```markdown
## Validation

### Checklist
- [ ] Schema validation passes (`python tools/validate.py`)
- [ ] Type generation works (`npm run types:gen`)
- [ ] All tests pass (`npm test`)
- [ ] API integration tests pass
- [ ] End-to-end tests pass

### Smoke Tests
```bash
# Test new field creation
curl -X POST https://api.tarlaanaliz.com/api/v1/fields \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Field",
    "userId": "user_123",
    "crop_type": "COTTON"
  }'

# Expected: 201 Created
```
```

#### 5. Rollback

```markdown
## Rollback

If migration fails:

### Option 1: Revert Contracts Pin

```bash
cd contracts/
git checkout v1.5.0
cd ..
cp contracts/CONTRACTS_VERSION.md .
npm run types:gen
```

### Option 2: Backward Compatibility Shim

```typescript
// Temporary shim (remove after migration)
interface FieldV1 {
  user_id: string;
}

interface FieldV2 {
  userId: string;
  crop_type: CropType;
}

function migrateField(v1: FieldV1): FieldV2 {
  return {
    ...v1,
    userId: v1.user_id,
    crop_type: CropType.UNKNOWN
  };
}
```

### Emergency Contacts
- Platform Lead: @platform-lead
- Contracts Owner: @contracts-owner
```

---

## Consumer Koordinasyonu

### Notification

Breaking change release öncesi:

#### 1 Hafta Önce

**Slack (#tarlaanaliz-dev)**:

```
🚨 Breaking Change Alert - Contracts v2.0.0

**Release Date**: 2026-03-01  
**Migration Window**: 2 weeks

**Changes:**
- Field schema: Added required `crop_type` field
- Mission enum: Removed deprecated `OLD_STATUS`

**Action Required:**
1. Read migration guide: [link]
2. Plan migration timeline
3. Notify your team

**Support:** #tarlaanaliz-contracts-support
```

**Email** (Engineering Leads):

```
Subject: [ACTION REQUIRED] Contracts v2.0.0 Breaking Changes

Hi Team,

We're releasing Contracts v2.0.0 on March 1st with breaking changes.

Migration Guide: [link]
Release Notes: [link]

Please plan your migration within 2 weeks.

Support available in #tarlaanaliz-contracts-support.

Thanks,
Contracts Team
```

#### Release Günü

**GitHub Release**: Detaylı release notes + migration guide link

**Slack**: Release announcement + migration başladı

#### Release Sonrası

**Weekly Status Updates**:

```
📊 Contracts v2.0.0 Migration Status (Week 1)

✅ Completed: tarlaanaliz-platform
🔄 In Progress: tarlaanaliz-edge (Est: 3 days)
⏰ Planned: tarlaanaliz-worker (Start: Mar 5)

Blockers: None
Support Requests: 2 (resolved)
```

### Migration Tracking

Google Sheet veya GitHub Project:

| Repository | Owner | Status | Started | Completed | Blocker |
|------------|-------|--------|---------|-----------|---------|
| platform | @alice | ✅ Done | 2026-03-01 | 2026-03-03 | - |
| edge | @bob | 🔄 In Progress | 2026-03-02 | - | DB schema |
| worker | @charlie | ⏰ Planned | - | - | - |

---

## Örnekler

### Örnek 1: MAJOR Bump (Breaking Change)

**Senaryo**: Field şemasına zorunlu `crop_type` alanı ekleniyor.

```bash
# 1. Breaking change tespit
$ python tools/breaking_change_detector.py --from v1.5.0 --to HEAD
⚠ BREAKING: Added required field 'crop_type' in schemas/core/field.v1.schema.json

# 2. Migration guide yaz
$ cat docs/migration_guides/field_v1_to_v2.md
# [Guide content]

# 3. Version bump
$ python tools/pin_version.py --bump major
Current: 1.5.0 → New: 2.0.0
Breaking change: true

# 4. Changelog güncelle
$ cat CHANGELOG.md
## [2.0.0] - 2026-03-01
### Breaking Changes
- Added required field `crop_type` to Field schema
...

# 5. Release
$ git tag v2.0.0
$ git push origin v2.0.0
$ ./tools/sync_to_repos.sh --target platform   # (--version/--notify diye bayrak YOK)
```

### Örnek 2: MINOR Bump (Yeni Feature)

**Senaryo**: Field şemasına opsiyonel `notes` alanı ekleniyor.

```bash
# 1. Değişiklik yap
$ cat schemas/core/field.v1.schema.json
{
  "properties": {
    ...
    "notes": { "type": "string" }  // ← opsiyonel (required'da değil)
  }
}

# 2. Breaking change kontrolü
$ python tools/breaking_change_detector.py --from v1.5.0 --to HEAD
✓ No breaking changes detected

# 3. Version bump
$ python tools/pin_version.py --bump minor
Current: 1.5.0 → New: 1.6.0
Breaking change: false

# 4. Changelog güncelle
$ cat CHANGELOG.md
## [1.6.0] - 2026-02-15
### Added
- Optional `notes` field in Field schema

# 5. Release
$ git tag v1.6.0
$ git push origin v1.6.0
```

### Örnek 3: PATCH Bump (Düzeltme)

**Senaryo**: User şemasında `name` field'ın description'ı düzeltiliyor.

```bash
# 1. Değişiklik yap
$ cat schemas/core/user.v1.schema.json
{
  "properties": {
    "name": {
      "type": "string",
-     "description": "User name"
+     "description": "Full name of the user (first + last)"
    }
  }
}

# 2. Version bump
$ python tools/pin_version.py --bump patch
Current: 1.6.0 → New: 1.6.1
Breaking change: false

# 3. Changelog
$ cat CHANGELOG.md
## [1.6.1] - 2026-02-20
### Fixed
- Clarified description of User `name` field

# 4. Release (lightweight tag)
$ git tag v1.6.1
$ git push origin v1.6.1
```

---

## Araçlar

### `tools/pin_version.py`

Version bump ve hash hesaplama:

```bash
# Breaking change
python tools/pin_version.py --bump major

# New feature
python tools/pin_version.py --bump minor

# Bug fix
python tools/pin_version.py --bump patch

# Manuel version
python tools/pin_version.py --set 3.0.0
```

### `tools/breaking_change_detector.py`

Breaking change tespit:

```bash
# PR'da (current branch vs main)
python tools/breaking_change_detector.py

# İki versiyon arası
python tools/breaking_change_detector.py --from v1.5.0 --to v2.0.0

# JSON output (CI için)
python tools/breaking_change_detector.py --format json
```

### `tools/sync_to_repos.sh`

Consumer'lara sync:

```bash
# PR aç (review için)
./tools/sync_to_repos.sh --target platform

# Notify gönder
./tools/sync_to_repos.sh --target platform   # (--version/--notify diye bayrak YOK)

# Specific repos
./tools/sync_to_repos.sh --all               # (--repos diye bayrak YOK)
```

---

## FAQ

### Q: Breaking change varsa ne yapmalıyım?

A:
1. Migration guide yaz (`docs/migration_guides/`)
2. MAJOR version bump yap
3. `CONTRACTS_VERSION.md` içinde `breaking_change: true` set et
4. Consumer'ları bilgilendir (1 hafta önceden)
5. Migration desteği sağla

### Q: Deprecation ne kadar sürmeli?

A: Minimum:
- JSON Schema alan: 2 MINOR (1 ay)
- OpenAPI endpoint: 3 MINOR (2 ay)

### Q: Migration guide zorunlu mu?

A: Evet, her breaking change için zorunludur. Template: `docs/migration_guides/MIGRATION_GUIDE_TEMPLATE.md`

### Q: Consumer'lar ne zaman güncellemeli?

A: Breaking change varsa 2 hafta içinde (önerilen). Kritik güvenlik fix'leri için daha kısa olabilir.

### Q: Rollback nasıl yapılır?

A: Consumer kendi `CONTRACTS_VERSION.md` dosyasında önceki versiyona dönebilir. Migration guide'da rollback adımları olmalı.

---

## İletişim

- **Slack**: #tarlaanaliz-contracts
- **Support**: #tarlaanaliz-contracts-support
- **Issues**: GitHub Issues

---

**Son Güncelleme**: 2026-01-26  
**Standart**: JSON Schema Draft 2020-12  
**Versioning**: Semantic Versioning 2.0.0