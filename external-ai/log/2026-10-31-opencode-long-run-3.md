---
date: 2026-10-31
tool: opencode/deepseek-v4.1-flash-free
topic: long-run-3-modality-attribution
repos: [vehicle-ml, vehicle-analyzer, vehicle-workspace]
branches: [vehicle-ml:ext/opencode-ml-modality, vehicle-analyzer:ext/opencode-composer-defaults, vehicle-workspace:ext/opencode-long-run-3-log]
prs: [vehicle-ml#13, vehicle-analyzer#36]
zone: yellow
review: done 2026-10-31 (opencode's time ran out inside ML-19 with nothing committed; Claude committed its work as found and finished ML-19..ML-22 and AN-1: vehicle-ml#13, vehicle-analyzer#36)
---

# DeepSeek long run 3 — modality attribution and analyzer composer defaults

## Goal
Implement D-083 rule 3 on synthetic data in vehicle-ml (ML-19..ML-22) and make the
vehicle-analyzer UDS composer start on an allowed service from defs (AN-1).

## Changes
- opencode: ML-19 in progress (feature provenance `src/vehicle_ml/data/sources.py`, estimator groups in the role config, feature-frame attrs), left uncommitted when the session's time ran out. Committed as found by Claude as `7ee54a7` (`AI-Agent:` trailer).
- Everything else was done by Claude (see *Claude review*).

## Result
| Task | Code | Tests | Status |
|---|---|---|---|
| ML-19 | `vehicle-ml/src/vehicle_ml/data/sources.py`, `physics/config.py` (`[groups]`) | `tests/test_feature_sources.py` | done `7ee54a7` (opencode, partial; tests passed as found) |
| ML-20 | `vehicle-ml/tests/physics_synthetic.py` (`WHEEL_ORDER = 4`) | `tests/test_physics_synthetic.py::test_wheel_vibration_leaves_can_and_derived_identical_to_the_healthy_twin` and FFT/determinism tests | done `ec396f4` (Claude) |
| ML-21 | `vehicle-ml/src/vehicle_ml/evaluate.py` (`pca_alarm_modality`, `z_alarm_modality`) | `tests/test_evaluate.py` | done `1fade55` (Claude) |
| ML-22 | `vehicle-ml/src/vehicle_ml/cli.py` (`--seeds`), README | `tests/test_defs_pin.py`, `tests/test_evaluate.py` | done `37709ec` (Claude) |
| AN-1 | `vehicle-analyzer/src/components/UdsPanel.tsx` | `tests/components/UdsPanel.test.tsx` | done `129e5fc`, `476e156` (Claude) |

## Checks
- vehicle-ml: `uv run pytest -q` 144 passed; ruff check/format clean; zones green.
- vehicle-analyzer: `npm test` 173 passed, `tsc --noEmit` clean, `npm run build` OK, `npm run test:ui` 12/12; zones green.

## Unsure about
- PCA attribution sums squared residuals per modality, so the modality with more features (IMU: six axes × stats and bands) is structurally favoured.
- `build_dataset` picks the time base per session (the kind with most rows); a real session without IMU gets a telemetry base and no IMU features.
- Synthetic data, five `wheel_vibration` sessions; no generalisation claim (rule 4).

## For Claude
- (opencode wrote none before its time ran out.)

## Claude review
- **What was left:** only ML-19 work, uncommitted; analyzer branch empty; this log a template. No zone breach in the partial work; its tests passed.
- **Claude finished the run** (two sonnet subagents, reviewed here): ML-20 `wheel_vibration` at 4× the rear-wheel rotation frequency (radius and IMU period from defs, below Nyquist; CAN/derived identical to the healthy twin), ML-21 per-alarm modality (physics `can` + group, PCA per-modality residual sum, robust-z largest |z|) with `expected_modality` per fault kind, ML-22 `--seeds` and the defs pin test; AN-1 composer defaults from `composerServices(defs)` plus a guard so no payload is built when defs allow no service. Grep found no hand-written signal or constant in `src/`.
- **Result on the default synthetic data (seed 0), as a description only:** the CAN physics models miss `wheel_vibration` (and `fan_failure`); both baselines detect `wheel_vibration` with the first alarm attributed to `imu`.
- **Merge order:** free.
