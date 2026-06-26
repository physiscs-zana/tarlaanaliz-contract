# Worker — Required Changes for Contracts 3.0.0 Alignment (REPORT ONLY)

**Date:** 2026-05-30
**Status:** NOT APPLIED — the `tarlaanaliz-worker` repository was treated as **read-only** during this contracts 3.0.0 sync (parallel work session; write requires explicit owner permission). This file documents the worker-side changes needed for full bidirectional alignment so they can be applied by the worker owner.

The SSOT now validates the worker's actual on-the-wire payloads (verified — see `docs/examples/analysis_result_worker.example.json` etc.). The items below are worker-internal consistency gaps that the SSOT exposed but cannot fix from this side.

---

## 1. Contract pin reference → 3.0.0

- Worker pins via `tarlaanaliz-worker/CONTRACTS_VERSION.md` (`v4.0.0`) using its **own** hash scheme: byte-concat of `interface/contracts/*.json`, sorted by filename, LF-normalized (KR-041 CI gate). This is independent of the SSOT `tools/pin_version.py` checksum.
- **Action:** record alignment with contracts `3.0.0`. The worker's local `interface/contracts/*.json` are now mirrored in the SSOT under `schemas/worker/` (1:1 field parity), so the two are content-equivalent; the worker's KR-041 hash stays as-is unless the worker adopts the items below.

## 2. (BUG) `analysis_result.v1` lacks `summary` / `yield_estimate` that worker code writes

- Worker code `src/core/services/yield_forecast/*` writes `analysis_result.summary.yield_estimate` (states "1:1 uyumlu" with `analysis_result.v1.schema.json YieldEstimate`).
- But the worker's **own** pinned `interface/contracts/analysis_result.v1.schema.json` has **no** `summary` object and no `ResultSummary`/`YieldEstimate` `$def`. With `additionalProperties:false`, the worker's own schema would **reject** the output its own code produces.
- The SSOT 3.0.0 `worker/analysis_result.v1` **does** carry `summary.yield_estimate` (KR-089) and validates that output (proven by `docs/examples/analysis_result_with_yield.example.json`).
- **Action (worker):** add `ResultSummary` (with `yield_estimate` → `YieldEstimate`) to `interface/contracts/analysis_result.v1.schema.json`, mirroring the SSOT `$defs`. This closes the worker-internal validation gap.

## 3. `calibration_type` enum inconsistency inside the worker

Three worker definitions disagree on whether `ABSOLUTE` is a valid `calibration_type`:

| Location | Includes `ABSOLUTE`? |
|---|---|
| `interface/contracts/analysis_job.v1` → `CalibrationMetadata.calibration_type` | YES (`ABSOLUTE, PANEL_ABSOLUTE, DLS2_RELATIVE, RELATIVE, NONE`) |
| `interface/contracts/calibration_metadata.v1` | NO (`PANEL_ABSOLUTE, DLS2_RELATIVE, RELATIVE, NONE`) |
| `interface/contracts/calibrated_dataset.v1` | NO |
| code `src/core/domain/enums.py::CalibrationLevel` | YES |

- The SSOT 3.0.0 mirrors each worker file **faithfully** (does not silently unify), so the SSOT reproduces this inconsistency intentionally — see the `x-note` in `schemas/worker/calibration_metadata.v1`.
- **Action (worker):** decide the canonical set and unify all three schemas + `CalibrationLevel`. Then the SSOT can be unified to match.

## 4. `$id` host mismatch

- Worker `interface/contracts/*.json` use `$id` host `https://tarlaanaliz.com/schemas/...`; SSOT uses `https://api.tarlaanaliz.com/schemas/...` (KR-081 canonical URL rule, enforced by `tools/validate.py`).
- **Action (worker):** optionally adopt the `api.tarlaanaliz.com` host for `$id` to match SSOT. Cosmetic (refs are resolved locally), but removes a divergence.

## 5. `expert_feedback.v1` `notes` pattern contains a raw control byte

- The worker file embeds a literal `0x7F` (DEL) byte inside the `notes` regex (`...-` + raw DEL), making the file **not strict-JSON-valid** (`json.load(strict=True)` raises `Invalid control character`).
- The SSOT mirror escapes it as `\u007f` (semantically identical regex, strict-JSON-valid).
- **Action (worker):** replace the raw DEL byte with the escape `\u007f` in `interface/contracts/expert_feedback.v1.schema.json`.

## 6. `expert_labeling_card.v1` uses a URN `$id`

- Worker uses `"$id": "urn:tarlaanaliz:schemas:expert_labeling_card:v2"`. SSOT requires the canonical `https://api.tarlaanaliz.com/schemas/...` URL (preserved the URN as `x-urn`).
- **Action (worker):** optional — adopt the URL `$id` for cross-repo `$ref` consistency.

---

## Not a worker bug (informational)

- The worker `analysis_job`/`analysis_result` `status` enums (`COMPLETED/FAILED/REJECTED`, `PENDING/QUEUED/...`) differ from the orchestration enums. The SSOT 3.0.0 supersets accept **both** (`status` = union), so no worker change is required for validation.
- The worker's `escalation_reason` enum is already in sync with the SSOT `expert_review_queue.v1` (parity test `TestReasonEnumParity`).
