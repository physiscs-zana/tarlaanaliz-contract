# Migration Guide — `phenology_stage` MAIZE_* → CORN_* Rename (contract v7.0.0)

**Breaking:** YES (MAJOR — enum value rename)
**Date:** 2026-07-12
**Scope:** `enums/phenology_stage.enum.v1.json` and every schema/consumer/data-file that
references its `MAIZE_*` stage codes.

## Reason

`crop_type` renamed `MAIZE → CORN` in enum v3.0.0 (contract v5.0.0); the canonical crop
value is now `CORN` across contract, platform and worker. `phenology_stage` was the **last
remaining `MAIZE` residue** — its stage codes were namespaced with the old crop prefix
(`MAIZE_EMERGENCE_V5`, …). That rename was deliberately deferred at the time (see
`crop_type_maize_to_corn.md`, "Explicitly NOT changed") because `PhenologyStage` is a
distinct enum and platform resolves phenology profiles **by `crop_type` through alias
normalization** (`phenology_profile_loader._normalize_crop` maps `MAIZE → CORN`), so a
`CORN` crop still found its `MAIZE_*` stages — nothing was actively broken.

This change closes that consistency gap: the stage-code namespace prefix now matches the
canonical `crop_type` value (`CORN_*`), removing the last place `MAIZE` appears in the
contract. It is a pure rename — no stages added or removed.

## Change

`phenology_stage` renames 4 values (GRAPE_* and OLIVE_* stages are unchanged); the set size
stays **14**:

| Before (v1, contract ≤6.2.0) | After (contract v7.0.0) |
|---|---|
| `MAIZE_EMERGENCE_V5` | `CORN_EMERGENCE_V5` |
| `MAIZE_V6_PRETASSEL` | `CORN_V6_PRETASSEL` |
| `MAIZE_TASSEL_SILK` | `CORN_TASSEL_SILK` |
| `MAIZE_GRAINFILL` | `CORN_GRAINFILL` |

Also updated in the same file:
- `x-enum-descriptions` keys re-keyed `MAIZE_* → CORN_*` (Turkish description text
  "Mısır — …" unchanged).
- `x-stage-order` key `"MAIZE" → "CORN"` and its 4 ordered values re-keyed.
- Top-level `description` namespace example `MAIZE_* → CORN_*`.
- `x-breaking-change` note added.

## Consumers affected

- **`schemas/core/phenology_flight_profile.v1.schema.json`** — references the enum via
  `$ref` (does **not** hardcode `MAIZE_*` string literals), so the schema needs no edit;
  it automatically validates against the renamed codes.
- **No example JSON in this repo** carries a `MAIZE_*` value (verified by grep), so there
  are no example files to update.
- **Worker** — if the worker consumes `phenology_stage` (separate repo), it **must** be
  aligned in the same round; otherwise a worker still emitting/expecting `MAIZE_*` will fail
  validation against the renamed enum.
- **Any phenology flight-profile / registry DATA** (e.g. `phenology_flight_profile`
  instances, seasonal flight calendars) that keys stages by the string `MAIZE_*` must be
  re-keyed to `CORN_*`.

## Required consumer actions

- **Platform / Worker / Edge:** treat `CORN_*` as the canonical stage codes. Update any
  stage lookup table, flight-profile registry, or hardcoded stage string from `MAIZE_*` to
  `CORN_*`.
- If a transition window is needed, accept legacy `MAIZE_*` on **inbound** payloads by
  normalizing to `CORN_*`; never emit `MAIZE_*` on **outbound** payloads.
- Re-pin to the new `CONTRACTS_VERSION.md` checksum and version string (7.0.0).
- Audit any stored phenology-profile rows or external feeds still carrying `MAIZE_*` and
  normalize them.

## Verification

```bash
python -X utf8 tools/validate.py
python -X utf8 -m pytest tests/ -q
python -X utf8 tools/breaking_change_detector.py --old <base-ref> --new .
python -X utf8 tools/pin_version.py --verify
```
