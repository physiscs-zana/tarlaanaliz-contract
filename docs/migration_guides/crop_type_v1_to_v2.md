# Migration Guide — `crop_type` enum v1 → worker-canonical (contracts 3.0.0)

**Breaking:** YES (MAJOR)
**Date:** 2026-05-30
**Affected:** `enums/crop_type.enum.v1.json` (metadata.version 1.1.0 → 2.0.0)

## What changed

`crop_type` is now aligned **1:1 with the Worker `CropType` enum** (`tarlaanaliz-worker/src/core/domain/enums.py`), which is the canonical reference for the analysis pipeline.

| Action | Values |
|---|---|
| **Removed** | `BARLEY`, `POTATO` |
| **Added** | `CHERRY`, `FIG` |
| Unchanged | `COTTON, CORN, WHEAT, SUNFLOWER, PISTACHIO, GRAPE, OLIVE, LENTIL, APPLE, PEACH, HAZELNUT` |

Final canonical set (13): `COTTON, CORN, WHEAT, SUNFLOWER, PISTACHIO, GRAPE, OLIVE, LENTIL, APPLE, PEACH, HAZELNUT, CHERRY, FIG`.

Aliases preserved: `MAIZE→CORN`, `RED_LENTIL→LENTIL`, plus new `KIRAZ→CHERRY`, `INCIR→FIG`.

## Why

- Worker removed `BARLEY` and `POTATO` in worker v3.0.0 (no production-grade disease/analysis pipeline; tuber pipeline out of scope). Worker CHANGELOG explicitly flagged that `tarlaanaliz-contracts` must mirror this with a v3.0.0 bump.
- `CHERRY` and `FIG` are active Tarla-region pilot crops (Alaşehir/Tariş scope) already present in worker's enum.
- The SSOT's own `crop_type` note already declared "Worker CropType enum is the reference"; before 3.0.0 the SSOT contradicted that note.

## Impact & required consumer actions

### Data / DB
- Any persisted `crop_type = 'BARLEY'` or `'POTATO'` is now **invalid** against the contract.
  - Inventory: `SELECT DISTINCT crop_type FROM fields WHERE crop_type IN ('BARLEY','POTATO');`
  - These crops were not in active production scope; if rows exist, remap to the correct crop or quarantine for manual review. Do **not** silently coerce to another crop.

### Platform
- `crop_type` enums in code (`mission_schemas.py`, domain entities) already narrowed to the active Tarla set (CORN/GRAPE/OLIVE/CHERRY); ensure no code path emits `BARLEY`/`POTATO`.
- Re-pin to contracts `3.0.0` (`CONTRACTS_VERSION.md` + `CONTRACTS_SHA256.txt`).

### Edge
- Edge does not constrain `crop_type` via the contract enum (sends free string in `worker_result`); no change required beyond pin bump.

### Worker
- Already aligned (worker is the reference). Only the contract pin reference moves to `3.0.0` (see `docs/sync/worker_required_changes_2026-05-30.md`).

## Backwards compatibility

None for the removed values — this is a MAJOR change by policy (enum value removal). Adding `CHERRY`/`FIG` is non-breaking on its own; the removal of `BARLEY`/`POTATO` is what forces the major bump.
