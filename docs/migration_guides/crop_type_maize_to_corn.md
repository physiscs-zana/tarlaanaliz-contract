# Migration Guide — `crop_type` MAIZE → CORN Rename (enum v3.0.0)

**Breaking:** YES (MAJOR — enum value rename)
**Date:** 2026-07-06
**Scope:** `enums/crop_type.enum.v1.json` and every schema/endpoint/example that references it.

## Reason

The contract was the **only** repository still using `MAIZE` as the canonical maize
value. Both consumers already use `CORN`:

- **Platform** — `src/core/domain/value_objects/crop_type.py`: `_VALID_CODES` contains
  `CORN`; `LEGACY_CROP_CODE_MAP` normalizes `MAIZE → CORN` at construction, so the
  platform DB never stores `MAIZE`.
- **Worker** — `src/core/domain/enums.py`: `class CropType` declares `CORN = "CORN"`.

Keeping `MAIZE` canonical in the contract forced a permanent cross-repo alias bridge
(`MAIZE ↔ CORN`) on every consumer. Renaming the canonical value to `CORN` makes it a
single, consistent value everywhere and demotes `MAIZE` to a legacy read-only alias.

## Change

`crop_type` renames one value; the set size stays **9**:

| Before (v2.1.0) | After (v3.0.0) |
|---|---|
| COTTON, PISTACHIO, **MAIZE**, WHEAT, SUNFLOWER, GRAPE, OLIVE, RED_LENTIL, RICE | COTTON, PISTACHIO, **CORN**, WHEAT, SUNFLOWER, GRAPE, OLIVE, RED_LENTIL, RICE |

- `metadata.aliases` is flipped: was `"MAIZE": ["CORN"]`, now `"CORN": ["MAIZE"]`
  (interop/legacy translation only — `MAIZE` is NOT an accepted enum value).
- Display names re-keyed to `CORN` (tr: "Mısır", en: "Corn (Maize)").
- Mirror/inline crop lists updated: `schemas/worker/expert_review_queue.v1.schema.json`,
  `api/components/schemas.yaml`, `api/components/parameters.yaml`,
  `api/components/responses.yaml` (example error message),
  `schemas/core/seasonal_flight_calendar.v1.schema.json` (description).

## Explicitly NOT changed in this version (deferred, separate tasks)

1. **`RED_LENTIL` stays canonical.** The worker/platform vocabulary uses `LENTIL`, but the
   contract keeps `RED_LENTIL` and the `RED_LENTIL ↔ LENTIL` alias. Aligning that name is a
   separate coordinated breaking change (see repo governance notes).
2. **`phenology_stage.enum.v1.json` `MAIZE_*` stage codes are unchanged.** `PhenologyStage`
   is a distinct enum; its values (`MAIZE_EMERGENCE_V5`, …) are stage identifiers, not
   `crop_type` values. Consumers resolve phenology profiles **by `crop_type` through alias
   normalization** (platform `phenology_profile_loader._normalize_crop` maps `MAIZE → CORN`),
   so a `CORN` crop still finds its `MAIZE_*` stages and nothing breaks. Renaming the stage
   codes to `CORN_*` would be an additional breaking change to a different enum and is
   intentionally out of scope here.

## Required consumer actions

- **Platform / Edge / Worker:** treat `CORN` as the canonical value. Continue to accept
  legacy `MAIZE` on **inbound** payloads by normalizing to `CORN` (platform already does
  this via `LEGACY_CROP_CODE_MAP`); never emit `MAIZE` on **outbound** payloads.
- Update any crop dropdown, routing table, pricing book, or label vocabulary that hardcoded
  the string `"MAIZE"` to `"CORN"`.
- Re-pin to the new `CONTRACTS_VERSION.md` checksum and version string.
- No data backfill expected on the platform (DB is already `CORN`); audit any legacy rows or
  external feeds that still carry `MAIZE` and normalize them.

## Verification

```bash
python tools/validate.py
pytest tests/ -v          # test_crop_type_enum_matches_gap_canonical asserts the CORN 9-set
python tools/check_no_egeanaliz.py
python tools/breaking_change_detector.py --old <base-ref> --new .
python tools/pin_version.py --verify
```
