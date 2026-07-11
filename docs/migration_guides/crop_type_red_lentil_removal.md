# Migration Guide — `crop_type` RED_LENTIL Removal (enum v4.0.0)

**Breaking:** YES (MAJOR — enum value removal)
**Date:** 2026-07-11
**Scope:** `enums/crop_type.enum.v1.json` and every schema/endpoint that references it.

## Reason

The worker is **dropping LENTIL (Mercimek)** from its crop vocabulary. The contract
mirrors that removal to stay 100% synced with the worker (no latent cross-repo
divergence). `RED_LENTIL` was the GAP-canonical spelling bridged to the worker/platform
`LENTIL` value via `metadata.aliases` (`RED_LENTIL↔LENTIL`); that cross-repo alias is now
retired and `RED_LENTIL` moves to `metadata.archived`.

## Change

`crop_type` goes from 9 values to **8**:

| Before (v3.0.0) | After (v4.0.0) |
|---|---|
| COTTON, PISTACHIO, CORN, WHEAT, SUNFLOWER, GRAPE, OLIVE, **RED_LENTIL**, RICE | COTTON, PISTACHIO, CORN, WHEAT, SUNFLOWER, GRAPE, OLIVE, RICE |

Naming is otherwise unchanged: CORN stays canonical (MAIZE remains a read-only legacy
alias). Aegean crops (CHERRY/FIG/APPLE/PEACH) remain out of scope. The `RED_LENTIL↔LENTIL`
alias is removed from `metadata.aliases`.

## Required consumer actions

- **Platform / Edge / Worker:** remove `RED_LENTIL` (and its `LENTIL` alias) from any crop
  dropdown, routing table, pricing book, or model/label vocabulary. Reject inbound payloads
  with `crop_type = RED_LENTIL` (HTTP 422 `allowed_crop_types`).
- Re-pin to the new `CONTRACTS_VERSION.md` checksum.
- No data backfill is expected for GAP fields; audit any legacy rows that carry
  `RED_LENTIL`/`LENTIL` and reclassify or archive them. Note: an immutable Postgres ENUM
  (`KIRMIZI_MERCIMEK`, added by an already-applied Alembic migration) still carries the
  legacy DDL value on the platform side — a forward enum-value drop is a separate,
  worker-coordinated DB migration (tracked as COORDINATE), not part of this contract bump.

## Re-adding

Re-adding RED_LENTIL later would be a **MINOR** (non-breaking) change.

## Verification

```bash
python tools/validate.py
pytest tests/ -v          # test_crop_type_enum_matches_gap_canonical asserts the 8-set
python tools/pin_version.py --verify
```
