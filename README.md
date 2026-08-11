# TarlaAnaliz — Contracts Repository

**Tek Doğru Sözleşme Kaynağı** — Contract-first mimari için JSON Schema, OpenAPI ve enum tanımları.

## 📋 Amaç

Bu repository, TarlaAnaliz platformunun tüm servisleri (platform, edge, worker) arasında **tek ve normatif** sözleşme kaynağıdır. Hiçbir servis kendi başına API veya veri yapısı tanımlamaz; tüm tanımlar bu repository'den gelir.

### Contract-First Prensipleri

1. **Tek Doğru Kaynak (Single Source of Truth)**
   - Tüm JSON Schema, enum ve OpenAPI tanımları sadece bu repository'de bulunur
   - Consumer repository'lar bu tanımları kopyalamaz, pin'leyerek referans alır
   - Değişiklikler bu repository'de başlar, ardından consumer'lara yayılır

2. **Versiyon Kilitleme (Version Pinning)**
   - Her consumer repository `CONTRACTS_VERSION.md` dosyasıyla belirli bir contract versiyonunu pin'ler
   - SHA-256 hash kontrolüyle içerik bütünlüğü garanti edilir
   - Breaking change'ler semver MAJOR bump gerektirir

3. **Değişiklik Disiplini**
   - Her PR: schema validation + tests + breaking-change detection
   - Breaking change varsa: migration guide + MAJOR version bump zorunlu
   - Release: changelog + consumer sync + hash doğrulama

## 🎯 JSON Schema Standardı

Bu repository **JSON Schema Draft 2020-12** kullanır.

### İlk Etap Profili (Zorunlu)

Karmaşıklığı kontrol altında tutmak için Draft 2020-12'nin şu iki özelliği zorunludur:

1. **`$defs`** — Tekrar kullanılan tip/alt şema tanımları
   - Ortak ID formatları, timestamp'ler, GeoJSON parçaları tek yerde
   - Refactor maliyetini düşürür, servisler arası tutarlılığı artırır
   - Örnek: `$defs/ObjectId`, `$defs/Timestamp`, `$defs/GeoPoint`

2. **`unevaluatedProperties: false`** — Şema dışı alan sızmasını engeller
   - Tanımlanmayan alanların sessizce sisteme girmesini önler
   - Contract-first mimaride "gizli alan" drift'ini engeller
   - Veri çöplüğü ve uyumsuzluk riskini minimize eder

### İleride Eklenebilir (Kontrollü)

İhtiyaç oldukça şu özellikler kontrollü şekilde eklenebilir:
- `dependentSchemas` — Koşullu şema gereksinimleri
- `if/then/else` — Koşullu validasyon
- `dynamicRef` — Dinamik referanslar
- İleri seviye `patternProperties`

**İlke**: Önce modüler `$defs` mimarisini otur, sonra genişlet.

## 🔒 Kritik Güvenlik Kuralları

### PII Minimizasyonu

**YASAK ALANLAR** — Aşağıdaki alanlar hiçbir şemada bulunamaz:
- ❌ `email` — Email adresi kullanılmaz
- ❌ `tckn` — TC Kimlik No kullanılmaz
- ❌ `otp` — OTP kodları kullanılmaz

**Kimlik Modeli**: Telefon + 6 haneli PIN yaklaşımı (KR-050)

### Otomatik Kontroller

`tools/validate.py` her PR'da şemaları **ve yayın ağacını** tarar:
```python
# tools/validate.py — TEK KAYNAK (pyproject.toml [tool.tarlaanaliz.schema] aynalar)
FORBIDDEN_FIELDS = ['email', 'e_mail', 'tckn', 'tc_kimlik_no', 'otp', 'one_time_password']
```
> ⚠️ Bu blok 2026-08-11'e kadar `FORBIDDEN_FIELD_NAMES` (var olmayan ad) ve **3 değer**
> yazıyordu; gerçek sabit `FORBIDDEN_FIELDS` ve **6 değer**. Aynı sınıf D18'de
> `pyproject` ↔ araç arasında bir kez düzeltilmişti, README'de kalmıştı.
> `tests/test_pii_scope_gate.py` iki kaynağın ayrışmasını yasaklar.

Bu alanların varlığı CI'da FAIL'e neden olur.

### Log Maskeleme

Tüm consumer repository'larda loglarda şu alanlar maskelenir:
- `phone_number` → `phone_***5678`
- `pin` → `***`
- `name`, `surname` → İlk harf + `***`

## 📦 Repository Yapısı

```
tarlaanaliz-contracts/
├─ schemas/           # JSON Schema tanımları (Draft 2020-12)
│  ├─ core/          # Field, Mission, User (merkezi modeller)
│  ├─ edge/          # Edge/istasyon intake ve metadata
│  ├─ worker/        # Worker analysis job/result
│  ├─ events/        # Event payloads (field_created, mission_assigned)
│  ├─ shared/        # GeoJSON, Money, Address (paylaşılan tipler)
│  └─ platform/      # Pricing, Payroll, Layer Registry
│
├─ enums/            # Enum tanımları (tek kaynak)
│  ├─ crop_type.enum.v1.json
│  ├─ role.enum.v1.json
│  ├─ mission_status.enum.v1.json
│  └─ ...
│
├─ api/              # OpenAPI 3.1 tanımları
│  ├─ platform_public.v1.yaml
│  ├─ platform_internal.v1.yaml
│  ├─ edge_local.v1.yaml
│  └─ components/
│
├─ docs/             # Politika, örnekler, migration guides
│  ├─ versioning_policy.md
│  ├─ canonical/     # v2.4 normatif dokümanlar (KR sistemi)
│  ├─ examples/      # Schema'ya uygun örnek JSON'lar
│  ├─ migration_guides/
│  └─ checklists/    # PR/CI/Release gate kontrolleri
│
├─ tools/            # Validation, type generation, sync
│  ├─ validate.py
│  ├─ breaking_change_detector.py
│  ├─ generate_types.sh
│  └─ sync_to_repos.sh
│
├─ tests/            # Contract testleri
│  ├─ test_validate_all_schemas.py
│  ├─ test_examples_match_schemas.py
│  └─ test_no_breaking_changes.py
│
├─ generated/        # Otomatik üretilen tipler (commit edilmez)
│  ├─ typescript/
│  └─ python/
│
├─ README.md         # Bu dosya
├─ CONTRACTS_VERSION.md  # Sürüm kilitleme dosyası
├─ CHANGELOG.md
├─ package.json      # Node/TS toolchain
└─ pyproject.toml    # Python toolchain
```

## 🚀 Kullanım (Consumer Repository)

### 1. Contract Versiyonunu Pin'leme

Consumer repository'de `CONTRACTS_VERSION.md` oluştur:

```markdown
# Contracts Version Lock

version: 1.0.0
sha256: a3f2b8c9d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1
created_at: 2026-01-26T10:30:00Z
breaking_change: false
```

### 2. CI'da Doğrulama

```yaml
# .github/workflows/contract_check.yml
- name: Verify contracts hash
  run: python3 contracts/tools/pin_version.py --verify
```
> `CONTRACTS_VERSION.md` `sha256sum -c` biçiminde **değildir** (Markdown tablo/liste);
> doğrulamayı `pin_version.py --verify` yapar.

### 3. Type Generation

```bash
# TypeScript (araçları `npm install -g` ile GLOBAL kurar; package.json'a bağlı değildir)
bash tools/generate_types.sh --typescript

# Python
bash tools/generate_types.sh --python     # datamodel-code-generator
```

## 🔄 Geliştirme Akışı

### PR Gate (Zorunlu Kontroller)

```bash
# Schema validation (Draft 2020-12)
python tools/validate.py

# (Yasak alan taraması ayrı komut DEĞİL — yukarıdaki koşum içinde yapılır.
#  `--check-forbidden` diye bir bayrak YOK: validate.py argüman almaz.)

# Tests
pytest tests/

# Breaking change detection
python tools/breaking_change_detector.py
```

### Release Prosedürü

1. **Version bump** (`tools/pin_version.py`)
   - Breaking change varsa MAJOR
   - Yeni feature varsa MINOR
   - Bug fix varsa PATCH

2. **Changelog güncelle**

3. **Migration guide** (breaking change varsa zorunlu)

4. **Tag ve release**

5. **Consumer sync** (`tools/sync_to_repos.sh`)

## 📚 Dokümantasyon

- **[Versioning Policy](docs/versioning_policy.md)** — SemVer kuralları, deprecation, breaking change politikası
- **[SDLC Gates](docs/checklists/SDLC_GATES.md)** — PR · CI · C8 release kapılarının **tamamı tek dosyada**
  (Bu üç ayrı checklist dosyası hiç var olmadı; atıflar 2026-08-11'de düzeltildi.)

### Kanonik Dokümanlar (v2.4)

- **[Kanonik Ürün İşleyiş Rehberi](docs/canonical/KANONIK_URUN_ISLEYIS_REHBERI_v2_4_.docx)** — KR referans sistemi, rol/akış, değişmez iş kuralları
- **[Geliştirici Uygulama Paketi](docs/canonical/GELISTIRICI_UYGULAMA_PAKETI_v2_4_.docx)** — MVP API listesi, implementasyon notları
- **[Saha Operasyon SOP](docs/canonical/SAHA_OPERASYON_SOP_v2_4_.docx)** — İstasyon QC/karantina prosedürleri

## 🛠️ Toolchain

### Node.js (TypeScript)

```json
{
  "dependencies": {
    "ajv": "^8.12.0",
    "ajv-formats": "^2.1.1",
    "json-schema-to-typescript": "^13.1.1"
  }
}
```

- **Ajv** — JSON Schema Draft 2020-12 validator
- **json-schema-to-typescript** — TS type generation

### Python

```toml
[tool.poetry.dependencies]
jsonschema = { extras = ["format"], version = "^4.20.0" }

[tool.poetry.group.dev.dependencies]
pytest = "9.0.2"        # AK-4: kapıyı KOŞTURAN araç TAM SÜRÜME sabit
pytest-cov = "7.0.0"    # (requirements-dev.txt + poetry.lock ile BİRLİKTE değişir)
```

- **jsonschema** — Draft202012Validator
- **pytest** — Test runner

## 🎯 Örnekler

### Doğru Şema (Draft 2020-12, unevaluatedProperties:false)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://api.tarlaanaliz.com/schemas/core/field.v1.schema.json",
  "title": "Field",
  "type": "object",
  "properties": {
    "id": { "$ref": "#/$defs/ObjectId" },
    "name": { "type": "string", "minLength": 1 },
    "geometry": { "$ref": "#/$defs/GeoJSON" }
  },
  "required": ["id", "name", "geometry"],
  "unevaluatedProperties": false,
  "$defs": {
    "ObjectId": {
      "type": "string",
      "pattern": "^[a-f0-9]{24}$"
    },
    "GeoJSON": {
      "type": "object",
      "properties": {
        "type": { "const": "Polygon" },
        "coordinates": { "type": "array" }
      },
      "required": ["type", "coordinates"]
    }
  }
}
```

### Yasak Kullanım (❌)

```json
{
  "properties": {
    "email": { "type": "string" },  // ❌ FORBIDDEN
    "tckn": { "type": "string" }    // ❌ FORBIDDEN
  }
}
```

## 📞 Destek

- **Issues**: GitHub Issues kullanın
- **Breaking Changes**: Migration guide zorunludur
- **Dokümantasyon**: `docs/` altında arayın

## 📄 Lisans

`UNLICENSED` — özel (proprietary) depo, dağıtım için değildir. Bkz. `LICENSE`.

---

**Son Güncelleme**: 2026-08-11  
**Kanonik Versiyon**: v2.4  
**JSON Schema Standardı**: Draft 2020-12