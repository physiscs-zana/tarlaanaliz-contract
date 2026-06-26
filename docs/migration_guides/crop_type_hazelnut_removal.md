# Migration Guide — `crop_type` HAZELNUT Removal (enum v2.0.0)

**Breaking:** YES (MAJOR — enum value removal)
**Date:** 2026-06-26
**Scope:** `enums/crop_type.enum.v1.json` and every schema/endpoint that references it.

## Reason

TarlaAnaliz serves **only the GAP (Southeastern Anatolia Project) region**. HAZELNUT
(Fındık) is a Black Sea region crop and is **not grown in GAP** — it was present in the
original `crop_type` set in error. It is removed to keep the contract faithful to the
served region.

## Change

`crop_type` goes from 9 values to **8**:

| Before (v1.0.0) | After (v2.0.0) |
|---|---|
| COTTON, PISTACHIO, MAIZE, WHEAT, SUNFLOWER, GRAPE, **HAZELNUT**, OLIVE, RED_LENTIL | COTTON, PISTACHIO, MAIZE, WHEAT, SUNFLOWER, GRAPE, OLIVE, RED_LENTIL |

Naming is unchanged: MAIZE and RED_LENTIL are kept (worker uses CORN/LENTIL; translate
via `crop_type.enum.v1.json` → `metadata.aliases`). Aegean crops (CHERRY/FIG/APPLE/PEACH)
remain out of scope.

## Required consumer actions

- **Platform / Edge / Worker:** remove `HAZELNUT` from any crop dropdown, routing table,
  pricing book, or model/label vocabulary. Reject inbound payloads with `crop_type = HAZELNUT`
  (HTTP 422 `allowed_crop_types`).
- Re-pin to the new `CONTRACTS_VERSION.md` checksum.
- No data backfill is expected (no GAP fields are hazelnut); audit any legacy rows that
  carry `HAZELNUT` and reclassify or archive them.

## Re-adding

Re-adding HAZELNUT later would be a **MINOR** (non-breaking) change.

## Verification

```bash
python tools/validate.py
pytest tests/ -v          # test_crop_type_enum_matches_gap_canonical asserts the 8-set
python tools/check_no_egeanaliz.py
python tools/pin_version.py --verify
```
