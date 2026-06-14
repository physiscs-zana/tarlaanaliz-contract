# Migration Guide — `crop_type` enum v1 → worker-canonical (contracts 4.0.0)

**Breaking:** YES (MAJOR)
**Date:** 2026-06-14
**Affected:** `enums/crop_type.enum.v1.json` (metadata.version 1.1.0 → 2.0.0)

> Note: contracts `3.0.0` was the geographic `EGE` region removal (`field.v1` /
> `expert_labeling_card.v1`). This `crop_type` alignment lands in `4.0.0`.

## What changed

`crop_type` is now aligned **1:1 with the Worker `CropType` enum** (`tarlaanaliz-worker/src/core/domain/enums.py`), which is the canonical reference for the analysis pipeline.

| Action | Values |
|---|---|
| **Removed** | `BARLEY`, `POTATO` |
| **Added** | `CHERRY`, `FIG`, `RICE` |
| Unchanged | `COTTON, CORN, WHEAT, SUNFLOWER, PISTACHIO, GRAPE, OLIVE, LENTIL, APPLE, PEACH, HAZELNUT` |

Final canonical set (14): `COTTON, CORN, WHEAT, SUNFLOWER, PISTACHIO, GRAPE, OLIVE, LENTIL, APPLE, PEACH, HAZELNUT, CHERRY, FIG, RICE`.

Aliases preserved: `MAIZE→CORN`, `RED_LENTIL→LENTIL`.

## Why

- Worker removed `BARLEY` and `POTATO` on 2026-05-18 (yerel pazar + ihracat değeri yetersiz, drone WTP düşük, açık kaynak veri yok). Worker is the canonical reference; `tarlaanaliz-contracts` must mirror it.
- `CHERRY` is an active Tarla-region pilot crop (açık kaynak Armillaria UAV verisi var); `FIG` and `RICE` are research skeletons in the worker enum (kalibre açık veri YOK — `blocked_by_data`) but are valid enum members for forward compatibility.
- The enum's own note already declared "Worker CropType enum is the reference"; before this bump the contract enum (`BARLEY`/`POTATO`, missing `CHERRY`/`FIG`/`RICE`) contradicted that note.

## Impact & required consumer actions

### Data / DB
- Any persisted `crop_type = 'BARLEY'` or `'POTATO'` is now **invalid** against the contract.
  - Inventory: `SELECT DISTINCT crop_type FROM fields WHERE crop_type IN ('BARLEY','POTATO');`
  - These crops were not in active production scope; if rows exist, remap to the correct crop or quarantine for manual review. Do **not** silently coerce to another crop.

### Platform
- Ensure no code path emits `BARLEY`/`POTATO`.
- Re-pin to contracts `4.0.0` (`CONTRACTS_VERSION.md`).

### Edge
- Edge does not constrain `crop_type` via the contract enum (sends free string in `worker_result`); no change required beyond pin bump.

### Worker
- Already aligned (worker is the reference). Only the contract pin reference moves to `4.0.0`.

## Backwards compatibility

None for the removed values — this is a MAJOR change by policy (enum value removal). Adding `CHERRY`/`FIG`/`RICE` is non-breaking on its own; the removal of `BARLEY`/`POTATO` is what forces the major bump.
