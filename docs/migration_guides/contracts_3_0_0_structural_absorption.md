# Migration Guide — Structural Absorption (incorporated into TarlaAnaliz Contracts 4.2.1)

**Breaking:** YES (MAJOR)
**Upstream date:** 2026-05-30 · **Incorporated into TarlaAnaliz 4.2.1:** 2026-06-26

> **TarlaAnaliz uygulanabilirlik notu.** Bu rehber, kardeş (sibling) repoda yapılan "structural absorption" (yapısal birleştirme) mekanizmasını anlatır ve aynı mekanizma TarlaAnaliz **4.2.1** senkronizasyonunda devralınmıştır. **crop_type istisnası:** TarlaAnaliz kendi GAP crop setini ve **MAIZE/RED_LENTIL adlandırmasını** korur (worker CORN/LENTIL yerine; aliaslarla eşlenir) ve Ege bitkilerini (CHERRY/FIG/APPLE/PEACH) **benimsemez**. TarlaAnaliz yalnızca GAP bölgesine hizmet ettiği için **HAZELNUT kaldırılmıştır** (Fındık Karadeniz bitkisidir, GAP'ta yetişmez) → GAP 8-crop seti (COTTON, PISTACHIO, MAIZE, WHEAT, SUNFLOWER, GRAPE, OLIVE, RED_LENTIL). Bkz. `crop_type_hazelnut_removal.md`. Aşağıdaki tüketici (consumer) pin sürümleri üst-akış (upstream) bağlamı içindir.

## Summary

Contracts 3.0.0 makes the SSOT a **true superset** that validates every consumer's actual on-the-wire payloads. Before 3.0.0 the SSOT had drifted behind the consumers and contradicted them; each consumer pinned a different version line (edge `1.2.0`, platform pin `2.0.1` / vendored `2.2.0`, worker `v4.0.0`).

Canonical direction:
- **Worker** is the reference for analysis I/O (`analysis_job`, `analysis_result`) and enum vocabulary — EXCEPT `crop_type`, where TarlaAnaliz keeps its own GAP 8-crop set with MAIZE/RED_LENTIL naming and no HAZELNUT (see `enums/crop_type.enum.v1.json`; cross-repo aliases MAIZE↔CORN, RED_LENTIL↔LENTIL).
- **Platform vendored** copy is the source for enum/feature additions (SALT_STRESS, DISTRICT_REP, PENDING_ADMIN_REVIEW, phenology, `/auth/change-pin`).
- **Edge** is the source for station-emitted manifests/reports.

## Two superset mechanisms

### 1. Loose union (heavily overlapping forms)
Used for `worker/analysis_job.v1` and `worker/analysis_result.v1`. The orchestration form and the worker runtime form share many fields, so a single object schema is used with:
- `required` reduced to the common intersection,
- identifier patterns relaxed (`job_id` accepts `job_<24hex>` **or** UUID; `field_id`/`mission_id` are plain strings),
- `status` enum = union of both forms,
- every producer-specific field defined as optional (because `unevaluatedProperties: false`).

### 2. `oneOf` of strict branches (disjoint forms)
Used for `edge/intake_manifest.v1`, `edge/scan_report.v1`, `edge/transfer_batch.v1`. The platform-canonical and edge-operational forms are field-disjoint, so each is a strict `$defs` branch and the root is `oneOf`. **Each payload validates against exactly one branch** — strict validation is preserved.

## New schemas (no migration, additive)

- Worker: `calibrated_dataset`, `calibration_metadata`, `expert_feedback`, `expert_labeling_card` (v2.5.0), `expert_review_queue` under `schemas/worker/`.
- Edge: `attestation_record`, `upload_receipt`, `worker_result`, `calibrated_dataset_manifest`, `evidence_bundle_ref` under `schemas/edge/`.
- Core: `phenology_flight_profile`; Enums: `phenology_stage`, `edge_custody_event`; Events: `dataset_quarantined`, `dataset_unquarantined`.

## Breaking items requiring action

| Item | Action |
|---|---|
| `crop_type` HAZELNUT removed (enum v2.0.0) | Drop HAZELNUT from any consumer crop routing/label maps; reject HAZELNUT payloads. See `crop_type_hazelnut_removal.md`. (MAIZE/RED_LENTIL naming kept; sibling's CORN/LENTIL rename + Aegean-crop migration guides intentionally NOT applied.) |
| `subscription.interval_days` → enum `[7,10,14,17,21]` | Reject/migrate any out-of-set values (e.g. 5, 28) |
| `analysis_job`/`analysis_result` required reduced + IDs relaxed | None for producers; consumers must not assume previously-required fields are present |

## Consumer pin updates

- **Platform:** update `CONTRACTS_VERSION.md` → `3.0.0`; re-vendor `contracts/` snapshot; recompute `CONTRACTS_SHA256.txt`. Runtime loads the vendored tree (`src/presentation/api/main.py`), so the vendored copy must be re-synced for changes to take effect.
- **Edge:** update `CONTRACTS_VERSION.md` reference to `3.0.0`; edge keeps its own LF-normalized per-file hash scheme (`scripts/verify_contracts_hashes.py`) — unchanged.
- **Worker:** worker keeps its own `interface/contracts` byte-concat hash (KR-041). Required worker-side changes are documented in `docs/sync/worker_required_changes_2026-05-30.md` (not applied to the worker repo in this change).

## Verification

```bash
python tools/validate.py
pytest tests/ -v
python tools/pin_version.py --verify
```

A payload from any consumer should now validate against the corresponding SSOT schema. See `docs/examples/*_worker.example.json` and `docs/examples/intake_manifest_edge.example.json` for proof payloads.
