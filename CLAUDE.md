# CLAUDE.md — AI Assistant Guide for tarlaanaliz-contracts

## Project Overview

**tarlaanaliz-contracts** is the single source of truth (SSOT) for all data contracts across the TarlaAnaliz agricultural analysis platform. It follows a **contract-first architecture**: no service (platform, edge, worker) defines its own API or data structures — all definitions originate from this repository.

**Domain**: Drone-based agricultural field analysis in Turkey's GAP (Southeastern Anatolia) region. Farmers request aerial analysis missions; drone pilots capture multispectral imagery; workers process it with AI models; results are delivered as map layers.

**Primary language of documentation**: Turkish, with English used in schema descriptions and code.

## Repository Structure

```
tarlaanaliz-contracts/
├── schemas/            # JSON Schema definitions (Draft 2020-12)
│   ├── core/           # Field, Mission, User, UserPII
│   ├── datasets/       # Dataset lifecycle + chain of custody (KR-072/073): dataset, dataset_manifest, calibration_certificate, qc_report, scan_report, verification_report, attestation, transfer_batch, evidence_bundle_ref
│   ├── edge/           # Edge station intake, metadata, quarantine
│   ├── events/         # Event payloads (field_created, mission_assigned, analysis_completed)
│   ├── platform/       # Pricing, Payroll, LayerRegistry, PaymentIntent, QC, Calibration
│   ├── shared/         # GeoJSON, Money, Address (reusable types)
│   └── worker/         # AnalysisJob, AnalysisResult
├── enums/              # Canonical enum definitions (single source)
├── api/                # OpenAPI 3.1 specs
│   ├── platform_public.v1.yaml
│   ├── platform_internal.v1.yaml
│   ├── edge_local.v1.yaml
│   └── components/     # Shared parameters, responses, schemas, security
├── ssot/               # KR registry and component-filtered SSOT views
│   ├── kr_registry.md  # Canonical KR (business rule) definitions
│   └── contracts_ssot.md
├── docs/
│   ├── canonical/      # v2.4 canonical product docs (.docx)
│   ├── checklists/     # PR/CI/Release gate checklists
│   ├── examples/       # Example JSON files matching schemas
│   ├── migration_guides/
│   └── versioning_policy.md
├── tools/              # Validation, type generation, sync, version pinning
├── tests/              # Python pytest-based contract tests
├── .github/workflows/  # CI: contract_validation.yml, auto_sync.yml
├── CONTRACTS_VERSION.md # SemVer + SHA-256 hash lock
├── CHANGELOG.md
├── package.json        # Node.js/TypeScript toolchain
└── pyproject.toml      # Python toolchain
```

## Tech Stack

### Node.js (package.json) — **TEK ARAÇ**
- **Runtime**: Node >= 18, npm >= 9
- **@redocly/cli** — OpenAPI lint + bundle. **Bu deponun tek Node aracıdır.**

> ⛔ **Burada bir TypeScript zinciri YOKTUR ve HİÇ OLMADI.** 2026-08-11'e kadar bu
> bölüm Ajv · json-schema-to-typescript · Jest · ESLint · Prettier · Husky ·
> lint-staged sayıyordu ve `package.json` 30 script taşıyordu. Ölçüldü: depoda **0
> adet `.ts`/`.js`** dosyası var, `tools/*.ts` hedeflerinin **hiçbiri hiç commit
> edilmemiş** (`git log --all` → 0), `tests/` 42 `.py` + 0 `.ts`, `.husky/` yok.
> `package.json` ilk commit'ten (2026-01-30) beri iskeleydi.
>
> En kritiği: `npm run format` = `prettier --write "**/*.{…,json,yaml,…}"` ve
> `.prettierignore` YOKTU → checksum kapsamındaki **97 dosyanın 94'ünü** yeniden
> biçimlendirirdi (ölçüldü). Bu ölü değil **zararlı** bir komuttu.
>
> Zincir kaldırıldı (676 → 263 paket, `npm audit` 38 → 30 açık) ve
> `tests/test_node_toolchain_honesty.py` geri gelmesini yasaklıyor.
> **Doğrulama/test/tip üretimi Python tarafındadır** — aşağıya bakın.

### Python (pyproject.toml)
- **Python**: >= 3.10
- **jsonschema** ^4.20.0 (with format extras) — Draft202012Validator
- **pydantic** ^2.5.3 — Data validation
- **pytest** ^7.4.3 + pytest-cov + pytest-xdist — Testing
- **black** ^23.12.1 — Code formatting (line-length: 100)
- **ruff** ^0.1.9 — Linting
- **mypy** ^1.8.0 — Type checking (strict mode)
- **datamodel-code-generator** — Python model generation from schemas

## Critical Rules — MUST Follow

### 1. JSON Schema Draft 2020-12 — Mandatory

Every schema file MUST:
- Include `"$schema": "https://json-schema.org/draft/2020-12/schema"`
- Include `"$id"` with the canonical URL pattern: `https://api.tarlaanaliz.com/schemas/{domain}/{name}.v{N}.schema.json`
- Include `"title"` and `"type"`
- Use `"unevaluatedProperties": false` on all `object` types (prevents field drift)
- Use `"$defs"` for reusable type definitions (referenced via `"$ref": "#/$defs/TypeName"`)

### 2. PII Minimization (KR-050) — Hard Security Requirement

**FORBIDDEN FIELDS** — These field names must NEVER appear in any schema:
- `email`, `e_mail`
- `tckn`, `tc_kimlik_no`
- `otp`, `one_time_password`

**Identity model**: Phone number + 6-digit PIN only. No email, no Turkish national ID, no OTP.

The validator (`tools/validate.py`) and CI workflow check for these automatically. Violating this fails the build.

### 3. Versioning (SemVer)

- **MAJOR**: Breaking changes (adding required fields, changing types, removing enum values, changing endpoints)
  - Requires migration guide in `docs/migration_guides/`
  - `breaking_change: true` in CONTRACTS_VERSION.md
- **MINOR**: Backwards-compatible additions (optional fields, new enum values, new endpoints)
- **PATCH**: Docs, descriptions, loosening constraints

### 4. Schema File Naming Convention

- Schemas: `{name}.v{version}.schema.json` (e.g., `field.v1.schema.json`)
- Enums: `{name}.enum.v{version}.json` (e.g., `crop_type.enum.v1.json`)
- Some older payment enums use `{name}.v{version}.json` without `.enum.`
- OpenAPI: `{service}_{scope}.v{version}.yaml`

### 5. KR (Business Rule) References

Business rules are referenced as `KR-NNN` throughout the codebase.

**Canonical KR sources — TWO files, but only ONE holds bodies.**

⚠️ **Do not trust a number written here — run the generator.** Counts in this file went
stale twice and caused two real misdiagnoses (see the note below). The authoritative
answer is whatever this command prints *today*:

```bash
python -c "import sys; sys.path.insert(0,'tests'); from test_kr_reference_integrity import _ssot_defined_krs as s, _registry_defined_krs as r, _collect_kr_refs as x; from test_single_normative_body import _registry_body_krs as rb, _dual_body_krs as d; a,b=s(),r(); print(f'SSOT text {len(a)} | registry headings {len(b)} | registry BODIES {len(rb())} | union {len(a|b)} | DUAL BODIES {len(d())} | referenced by schemas {len(x())}')"
```

> 🔴 **Read `DUAL BODIES`, not the heading intersection.** A pointer still carries a
> heading, so "defined in both files" counts ~50 and means nothing. The number that
> matters — how many KRs have a normative *body* in two places — must stay **0**.
> Mixing these two up is what made the D16-b gate green while it was blind (2026-07-31).

| File | Role | Heading forms it uses |
|---|---|---|
| `docs/TARLAANALIZ_SSOT_v1_2_0.txt` | Full KR corpus; **byte-identical with the platform copy** (aligned 2026-07-31) — the cross-repo artifact | `## [KR-019]`, combined `## [KR-018 / KR-082]`, typo `## # [KR-033]`, bracket-less `### KR-017` |
| `ssot/kr_registry.md` | **Navigation + scope index — NOT a body store** (since 2026-08-01/D16-b2). Each KR heading carries a `TÜRETİLMİŞ İŞARETÇİ` stamp pointing at the SSOT text, plus `Applies to` / `Kaynaklar` (which the SSOT text does **not** carry: measured 0 matches). **Exception:** `KR-088/089/090/091` still hold their bodies here — they are undefined in the SSOT text | `### KR-070`, `## KR-088` |

The extractor in `tests/test_kr_reference_integrity.py` recognises **all four heading
forms at any heading level**; use it rather than writing a new regex.

✅ **D16 landed (2026-08-01, D16-b2): a KR body lives in exactly ONE place.** The dual-body
count went **49 → 0**; `docs/TARLAANALIZ_SSOT_v1_2_0.txt` is the single normative text and
**it wins on conflict**. The gate `tests/test_single_normative_body.py` now runs in *forbid*
mode (`KNOWN_DUAL_BODY_COUNT = 0`), not debt-freeze.

The migration was **not** mechanical, and the reason matters: of the 49 registry bodies,
41 were derived summaries, 6 were strict subsets of the SSOT text, and only 2 (`KR-019`,
`KR-092`) plus one clause of `KR-072` carried real content — those were moved by hand.
**Three bodies were actively wrong**, which is exactly the AR1 failure mode: `KR-083` still
named a retired role (*İl Operatörü*, successor `DISTRICT_REP` in live code), `KR-027`'s
title was frozen at "Abonelik Planlayıcı", and `KR-000` said "DJI" under a drone-agnostic
architecture. A second body does not stay in sync — it rots quietly.

Rule going forward: **a KR's rule changes in the SSOT text first**, then the registry
heading (title/scope) follows. Writing a normative body back under a registry heading turns
the gate red.

> ⚠️ Two earlier versions of this section were wrong and both caused real misdiagnoses:
> it first claimed `ssot/kr_registry.md` was *the* canonical source, then that the registry
> holds "only 6 of ~49, complementary". Both were hardcoded numbers that measurement
> contradicted. Hence the rule above: **publish the generator, not the number.**

A KR referenced via `x-kr-ref` must be defined in **at least one** of the two;
`tests/test_kr_reference_integrity.py` enforces this (dangling-reference gate), and the
extractor there recognises **all four heading forms** at any heading level.

Where the data-layer KR bodies actually live (measured, do not guess):
`KR-092`/`KR-093` → **SSOT text only** (registry holds pointers) · `KR-088`/`KR-091` →
**registry only** (the SSOT text mentions them in a single cross-reference line, which is
**not** a definition — so pointerising them would erase the rule).

Key KRs for this repo:
- **KR-050**: PII minimization (no email/TCKN/OTP)
- **KR-081**: Contract-first / Schema gates (CI)
- **KR-072**: Dataset lifecycle + chain of custody
- **KR-073**: Untrusted file handling + malware scanning
- **KR-018/082**: Radiometric calibration hard gate

## Development Commands

> ⚠️ **Aşağıdaki komutların hepsi ÖLÇÜLDÜ (2026-08-11) ve koşuyor.** Bu bölüm daha önce
> 9 adet `npm run …` komutu belgeliyordu; hiçbiri koşmuyordu (bkz. Tech Stack notu).
> Kapı: `tests/test_node_toolchain_honesty.py` — hedefi olmayan script eklenemez.

### Validation
```bash
python tools/validate.py
```
Tek doğrulayıcı budur: `schemas/` + `enums/` + **`dist/schemas/`** (yayın ağacı) +
`api/` (PII kapsamı). Draft 2020-12 zorunlulukları, KR-050 yasak alanları ve
**alan sızması politikası** (her object düğümü `unevaluatedProperties: false` ya da
gerekçeli `additionalProperties` beyan etmeli) burada koşar.

### Testing
```bash
pytest tests/ -q
```
Süit **Python**'dur. Beklenen tek yerel kırmızı, `requirements-dev.txt`'teki pytest
pininden sapmış bir yerel kurulumdur (`test_toolchain_pinning`).

### Type Generation
```bash
bash tools/generate_types.sh --python        # datamodel-code-generator
bash tools/generate_types.sh --typescript    # json-schema-to-typescript (npm -g kurar)
```
⚠️ Bu betiğin **CI'da çağıranı yoktur**; araçlarını **global** kurar, bu deponun
`package.json`'ına bağlı değildir. Tüketiciler tipi kendi depolarında üretir.

### OpenAPI
```bash
npm run openapi:validate      # redocly lint (CI aynı işi `npx @redocly/cli@1 lint` ile yapar)
npm run openapi:bundle        # dist/openapi/ altına bundle
```

### Linting & Formatting
```bash
black .            # Python biçim
ruff check .       # Python lint
mypy tools/        # Python tip
```
⛔ **Depo genelinde `prettier` KOŞTURMAYIN.** `schemas/` · `enums/` · `api/` · `dist/`
`.prettierignore` ile korunuyor: bu ağaçların biçimi elle bakımlıdır ve
checksum + vendored bayt-paritesi + `dist` tazeliği ona bağlıdır.

### CI'da GERÇEKTEN ne koşuyor
`.github/workflows/contract_validation.yml` — 8 iş: `validate-schemas` ·
`test-schemas` · `detect-breaking-changes` · `verify-checksums` · `lint-openapi` ·
`check-forbidden-fields` · `check-draft-2020-12` · `check-brand-guard` (+ doc-link
kapısı **+ I-1 sürüm hizası kapısı** AL-K30 **+ betik ağacı kapısı** AL-K32). Hepsi `summary` işinde toplanır. **Tek bir `npm run ci:gate` komutu yoktur** —
öyle bir script hiç çalışmadı. Kapsam ve `needs` bütünlüğü
`tests/test_ci_gate_honesty.py` ile türetilip zorlanır.

### Betik ağacı kapısı (AL-K32, 2026-08-11) — `tools/check_scripts.py`

```bash
python tools/check_scripts.py
```

Bu deponun betik ağacı **tümden kapısızdı**: 3 dosya / 1021 satır ve workflow'larda onları
ayrıştıran **0 isabet**. Dört yeşil kapı (validate · pytest · redocly · checksum) o
satırların hiçbirini görmüyordu. Ölçüm **dürüst negatif** sonuç verdi — sözdizimi kusuru
yoktu — ama kök dizinde yetim ve **koşarsa zararlı** bir betik bulundu ve kaldırıldı:
`Downloads` içindeki bir ZIP'i çalışma ağacının tamamının üstüne kopyalıyor, bitince de
kök `CLAUDE.md`'nin **yasakladığı** toplu ekleme komutunu kullanıcıya yazdırıyordu.

İki katman: ① **sözdizimi** (`.sh` → `bash -n`, `.ps1` → PowerShell ayrıştırıcısı;
betik **çalıştırılmaz**) ② **yasaklı komut** — toplu ekleme · çalışma ağacını ezen
özyinelemeli kopyalama · çalışma dizini kökünü silme. Ayrıca **indekste CRLF** taşıyan
betik reddedilir (Linux'ta ayrıştırılamaz).

Tasarım kararları — hepsi ölçümle:

- **Desenler dar tutuldu.** `sync_to_repos.sh`'teki 4 `git add` kullanımının hepsi
  yol-sınırlı, `generate_types.sh` yalnız kendi üretim dizinini siliyor → kapı meşru koda
  takılmıyor (pozitif kontrol testte).
- ⚠️ **Yorum satırları taranmaz.** Bu oturumda **dört kez** bir kusuru *yasaklayan* kapı,
  kusuru *anlatan* metne takıldı; bir kuralı betiğin içinde gerekçelendirmek mümkün olmalı.
- 🔴 **Ayrıştırma CR'siz metin üzerinde, stdin'e BAYT olarak yapılır.** İlk hâl çalışma
  ağacını ayrıştırıyordu ve `core.autocrlf=true` olan makinede her betikte **yanlış
  kırmızı** verdi; `git ls-files --eol` indeks tarafını `lf` gösterip iddiayı çürüttü.
  Metin kipinde Python `
`'i boruda geri `
` yapıyor — bayt kipi şart (mutasyon: 4 test).
- **Fail-closed:** hiç betik bulunamazsa hata döner; *"0 bulgu"* ile *"0 dosya taradım"*
  aynı şey değildir. Taranan dosya sayısı her koşumda basılır.

### Breaking Change Detection
```bash
python tools/breaking_change_detector.py --old <dizin|git-ref> --new .
```
⚠️ Bilinen sınırlar (kapı bunları gördüğünü iddia ETMEZ): `$ref` çözülmez
(`REF_CHANGED` → insan incelemesi, SDLC_GATES §3E) · **object politikası daralması
hiç sınıflandırılmaz** (2026-08-11: 27 kapatma → 0 değişiklik kaydı). Sürüm kararı
bu iki sınıfta **elle ölçülür**.

### Version Pinning
```bash
python tools/pin_version.py          # Update CONTRACTS_VERSION.md hash
python tools/pin_version.py --verify # Verify current hash
```

## CI/CD Workflows

### contract_validation.yml (on PR to main/develop + push to main)
1. **validate-schemas** — Runs `python3 tools/validate.py`
2. **test-schemas** — Runs `pytest tests/ -v` with coverage
3. **detect-breaking-changes** — Compares PR branch against base (PR only)
4. **verify-checksums** — Verifies CONTRACTS_VERSION.md hash
5. **lint-openapi** — Spectral lint on OpenAPI specs
6. **check-forbidden-fields** — Grep-based PII field check
7. **check-draft-2020-12** — Ensures all schemas use 2020-12
8. **summary** — Aggregates results; fails if critical checks fail

### auto_sync.yml
Syncs contract changes to consumer repositories.

## Code Style & Conventions

### TypeScript / JavaScript
- Semicolons: yes
- Quotes: double
- Trailing commas: es5
- Print width: 100
- Tab width: 2
- Arrow parens: always
- End of line: LF

### Python
- Line length: 100
- Target: Python 3.10+
- Formatter: black
- Linter: ruff (pycodestyle, pyflakes, isort, pep8-naming, pyupgrade, bugbear, etc.)
- Type checker: mypy (strict mode, `disallow_untyped_defs`)
- Tests: pytest with strict markers and `--showlocals --tb=short`

### Git Commit Messages
Follow conventional commits pattern:
- `feat(scope): description` — New features
- `fix(scope): description` — Bug fixes
- `audit: description` — Compliance/audit changes
- Scopes include: `contracts`, `geojson`, `schemas`, etc.

## Test Structure

All tests are in `tests/` and use Python's pytest:

| Test File | Purpose |
|---|---|
| `test_validate_all_schemas.py` | Draft 2020-12 compliance, unevaluatedProperties, forbidden fields, enum format |
| `test_examples_match_schemas.py` | Example JSON files validate against their schemas |
| `test_no_breaking_changes.py` | Breaking change detection between versions |

> ⚠️ **Bu tablo TAM LİSTE DEĞİLDİR** — süitte bugün **43** test dosyası var. Sayı
> ezberlemeyin; `git ls-files 'tests/*.py' | wc -l` koşun.
>
> ⛔ **"Coverage threshold: 80%" iddiası KALDIRILDI (2026-08-11, ölçüldü).** O eşik
> `package.json`'daki jest yapılandırmasındaydı ve jest `tools/**/*.ts` üzerinde
> koşuyordu — depoda **0 adet `.ts`** var, yani eşik hiç uygulanmadı. Python tarafında
> `--cov-fail-under` **hiçbir yerde tanımlı değil** (`git grep -i fail_under` → yalnız
> eylem planındaki bir cümle). Gerçek ölçülen kapsam: `tools/` için **%51**.
> Bir eşik istenirse `pyproject.toml → addopts`'a eklenmeli ve o zaman GERÇEK bir kapı olur.

## When Modifying Schemas

1. **Read the existing schema** before making changes
2. **Maintain Draft 2020-12 compliance**: `$schema`, `$id`, `title`, `type`, `unevaluatedProperties: false`
3. **Use `$defs`** for reusable types; reference with `$ref`
4. **Never add PII fields** (email, tckn, otp)
5. **Check if the change is breaking** — if adding to `required`, changing types, or removing enum values, it's a MAJOR bump
6. **Update the corresponding example** in `docs/examples/` if one exists
7. **Run validation**: `python tools/validate.py && pytest tests/ -v`

## When Adding New Schemas

1. Place in the appropriate subdirectory under `schemas/`
2. Follow naming: `{name}.v1.schema.json`
3. Include all mandatory fields: `$schema`, `$id`, `title`, `type`, `unevaluatedProperties: false`
4. Add `$defs` for complex sub-types
5. Create an example in `docs/examples/`
6. Run the full validation suite

## When Modifying Enums

1. **Adding values**: Non-breaking (MINOR). Add to the `enum` array.
2. **Removing values**: Breaking (MAJOR). Requires migration guide.
3. **Renaming values**: Breaking (MAJOR). Requires migration guide.
4. Include bilingual display names (`tr` + `en`) in metadata when applicable.

## When Modifying OpenAPI Specs

1. OpenAPI version: 3.1.0
2. Reference JSON Schemas via `$ref` where possible
3. All endpoints follow the authentication model: session token from phone + PIN login
4. Run `npm run openapi:validate` after changes
5. Shared components go in `api/components/`

## Key Domain Concepts

- **Field**: Agricultural parcel with boundary geometry, crop type, season
- **Mission**: Drone flight analysis request tied to a Field
- **Intake Manifest**: Edge station document tracking raw data ingestion with hash chain
- **Quarantine**: Failed QC/AV/hash checks result in quarantine status
- **Analysis Job/Result**: Worker processing pipeline input/output
- **Layer Registry**: Map layer definitions (NDVI, disease detection, etc.)
- **Payroll**: Pilot payment calculations
- **KR (Kural Referansı)**: Business rule identifier system used across all docs

## Consumer Repositories

This contracts repo is consumed by:
- **tarlaanaliz-platform** — Main platform backend
- **tarlaanaliz-edge** — Edge/kiosk station software
- **tarlaanaliz-worker** — AI analysis worker

Consumers pin to a specific version via `CONTRACTS_VERSION.md` + SHA-256 hash verification.

## Çapraz-Repo Senkron — Değişmezler ve Doğrulama (DAİMA)

Üçlü senkron (contract = SSOT · platform + worker = consumer) aşağıdaki **5 değişmezle
(invariant)** güvence altındadır. Kural denetlenebilirdir — her değişmez bir komuta bağlıdır;
bir kuralı doğrulayacak komut yoksa o kural bir dilek, gate değildir.

**Senkron değişmezleri — her release'de TUTMALI:**
- **I-1 · Sürüm dizesi hizası:** `CONTRACTS_VERSION.md` sürümü üç repoda birebir aynı (contract `X.Y.Z` = platform `X.Y.Z` = worker `vX.Y.Z`; worker `v` önekli). Uyuşmazlık = senkron kırık.
- **I-2 · Kanonik release etiketli (annotated tag):** Her contract sürümü, release commit'ine **annotated git tag `vX.Y.Z`** alır (bkz. `docs/versioning_policy.md` §Release). Etiketsiz sürüm **eksik release**'tir — consumer tag ile pinlenemez, `git describe` bulanık kalır (`vA.B.C-N-g…`). Tag adımı release checklist'inin parçasıdır, atlanamaz.
- **I-3 · Platform ↔ Contract (bayt-özdeş):** Platform `contracts` submodule pini, contract'ın `vX.Y.Z` etiketli commit'ine eşittir; vendored agrega checksum + `CONTRACTS_SHA256.txt` per-dosya hash kanonikle birebir. Platform kanoniği **aynalar**, ikinci bir değer hesaplamaz.
- **I-4 · Worker ↔ Contract (subset — bayt-özdeş DEĞİL):** Worker `interface/contracts/`'te **8 izli dosyayı** vendor'lar; bunlar kanoniğin **superset** şemasının **dar runtime alt-kümesidir** — bayt-özdeşlik BEKLENMEZ, worker'ın KR-041 öz-hash gate'ini geçmesi beklenir. Kanonik superset worker'ın katı formunu kabul eder.
- **I-5 · Sapma yalnız GEÇİCİ (AK-4):** Worker bir alanı kanonikten önce re-pinleyebilir ama `denetim/*_devir_spec_*.md` bırakır; kanonik aynalayınca uzlaşılır. **Kalıcı divergence YASAK.**

**Doğrulama (contract — sürüm yükseltme/tag öncesi; hepsi yeşil olmadan release YOK):**
```bash
git describe --tags HEAD              # I-2: temiz vX.Y.Z dönmeli (etiketsizse: git tag -a vX.Y.Z <commit> && git push origin vX.Y.Z)
python tools/pin_version.py --verify  # I-3/I-4 kaynağı: agrega Contracts Checksum tutar
python tools/validate.py && pytest tests/ -q
```

### I-1'in KAPISI (AL-K30, 2026-08-11) — `tools/check_version_alignment.py`

I-1 üç `CLAUDE.md`'de yazılıydı ama **doğrulayan tek bir komut yoktu**: dört depo tarandı,
contract'ta 2 isabet düzyazı, platform'daki 8 isabet **başka bir numaralandırma**
(Dockerfile değişmezi), worker/edge **0**. Kuralın sessizce kırıldığı da ölçüldü —
edge `7.6.1`'i **hiç pinlemedi** ve kimse fark etmedi.

Kapı **burada yazılır, kardeş depolarda koşar** (D4-b — parite testleriyle aynı model).
İki kip vardır ve **karıştırılmamalıdır**:

```bash
# contract'ın kendisi — CI'da koşuyor. Sürüm etiketin GERİSİNDE olamaz;
# İLERİSİNDE olabilir (release PR'ının normal hâli: sürüm yükseldi, etiket henüz yok).
python tools/check_version_alignment.py --mode canonical \
  --pinned-file CONTRACTS_VERSION.md --label '## Version:' --latest-from-git .

# kardeş depo — kendi CI'ında koşar. Pin en yeni yayımlanmış sürüme EŞİT olmalı.
python tools/check_version_alignment.py --mode consumer \
  --pinned-file CONTRACTS_VERSION.md --label 'Upstream Contract Set' --latest 7.7.2
```

Üç kural, üçü de mutasyonla sınandı (`tests/test_version_alignment_gate.py`, 34 test):

- ⚠️ **Kardeşin KENDİ checkout'uyla karşılaştırmak TOTOLOJİDİR** — kardeş CI sözleşmeyi
  `ref: v${pin}` ile çeker, çektiği ağacın sürümü elbette pinine eşittir. Bu yüzden
  `--latest` / `--latest-from-git` **zorunludur**.
- 🔴 **`--label` şart.** Sürüm dosyaları değişiklik geçmişini de taşıyor: contract'ta **30**,
  worker'da **22**, edge'de **27** farklı sürüm dizesi var. Etiketsiz koşum edge dosyasında
  `1.7.0` (edge'in **kendi** SemVer'i) okudu — kapı doğru cevabı yanlış gerekçeyle verdi.
  Artık belirsizlikte **tahmin etmez, fail-closed kapanır**.
- **`fetch-depth: 0` gerekli.** Varsayılan sığ checkout etiket getirmez; etiketsiz ortamda
  kapı fail-closed kırmızı verir (ölçüldü). *"Ölçemedim" asla "hizalı" sayılmaz.*

I-5 gereği geçici gerilik **yalnız** `--allow-lag-until <tarih> --reason <gerekçe>` ile
kabul edilir; gerekçesiz ya da süresi dolmuş muafiyet kırmızıdır.
