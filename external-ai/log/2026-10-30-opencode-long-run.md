---
date: 2026-10-30
tool: opencode/deepseek-v4.1-flash-free
topic: long-run
repos: [vehicle-ml, vehicle-server, vehicle-analyzer]
branches: [vehicle-ml:ext/opencode-ml-data-layer, vehicle-server:ext/opencode-server-e18-verify, vehicle-analyzer:ext/opencode-analyzer-session-filter]
prs: [vehicle-ml#9, vehicle-server#39, vehicle-analyzer#34]
zone: yellow
review: pending
---

# DeepSeek long run: vehicle-ml data layer, E-18 (4) verification, analyzer session filter

## Goal
Build the vehicle-ml data layer (ML-1..ML-9), verify ISSUES E-18 (4) in vehicle-server (SV-1), and add the analyzer session-list filter (AN-1), as specified in `external-ai/tasks/2026-10-30-deepseek-long-run.md`.

## Changes
- `vehicle-ml/pyproject.toml`, `uv.lock`, `.gitignore`, `src/vehicle_ml/__init__.py`, `tests/__init__.py`: uv/ruff/pytest scaffold, console script `vehicle-ml`, src layout, synthetic-data ignores.
- `vehicle-ml/tests/synthetic.py`: server-layout fixture (`index.sqlite`, Parquet kinds, `report.json`) with a full session, a no-IMU/gap session and a no-GPS/no-derived session with `gps_latitude`.
- `vehicle-ml/src/vehicle_ml/data/store.py`, `data/position.py`: read-only `SessionStore`, position-column rule copied from vehicle-mcp, `session_id` added on load.
- `vehicle-ml/src/vehicle_ml/split.py`: stable session-based train/val/test and grouped k-fold.
- `vehicle-ml/src/vehicle_ml/windows.py`: gap/missing-aware window cutting and nearest-previous cross-kind alignment.
- `vehicle-ml/src/vehicle_ml/features.py`: per-window statistics and optional FFT band energy with a rate-stability check.
- `vehicle-ml/src/vehicle_ml/normalize.py`: train-only `Standardizer`, constant-feature handling and JSON persistence.
- `vehicle-ml/src/vehicle_ml/dataset.py`, `cli.py`, `__main__.py`: `vehicle-ml dataset` builder, split/scaler/card outputs, band parsing and exit codes.
- `vehicle-ml/README.md`: data-layer description, split/position rules, CLI example and outputs.
- `vehicle-server/tests/test_vsig_consistency.py`: added a combined block-version test; no production behaviour changed.
- `vehicle-analyzer/src/services/sessionFilter.ts`, `src/components/SessionPanel.tsx`: pure filter/sort logic, status chips from the data, UTC date bounds, newest/loss sorting and localStorage persistence.
- `vehicle-analyzer/tests/sessionFilter.test.ts`, `tests/components/SessionPanel.test.tsx`: unit and component coverage.

## Result
| task | code (file:line) | tests | status |
|---|---|---|---|
| ML-1 | `vehicle-ml/pyproject.toml`; `src/vehicle_ml/__init__.py:3` | `test_scaffold.py::test_version_is_set` | pass |
| ML-2 | `tests/synthetic.py:33`, `:286` | `test_synthetic.py::test_make_data_dir_writes_the_server_layout`, `::test_gap_session_has_a_hole_and_position_session_has_a_position_column` | pass |
| ML-3 | `src/vehicle_ml/data/store.py:33`; `data/position.py:19` | `test_store.py::test_load_every_kind_adds_the_session_id`, `::test_position_columns_are_dropped`, `::test_read_only_data_dir_still_loads` | pass |
| ML-4 | `src/vehicle_ml/split.py:33`, `:89` | `test_split.py::test_assignment_is_deterministic`, `::test_leakage_is_detected_across_frames_and_lists` | pass |
| ML-5 | `src/vehicle_ml/windows.py:52`, `:131` | `test_windows.py::test_gap_session_drops_windows_that_span_the_gap`, `::test_align_frames_does_not_cross_a_gap` | pass |
| ML-6 | `src/vehicle_ml/features.py:56` | `test_features.py::test_hand_computed_statistics`, `::test_pure_sine_lands_in_the_right_band` | pass |
| ML-7 | `src/vehicle_ml/normalize.py:20` | `test_normalize.py::test_json_round_trip`, `::test_fit_rejects_rows_from_a_non_train_session` | pass |
| ML-8 | `src/vehicle_ml/dataset.py:163`, `:284`; `src/vehicle_ml/cli.py:54` | `test_dataset.py::test_cli_writes_all_outputs_end_to_end`, `::test_cli_accepts_band_spec`, `::test_cli_rejects_bad_arguments` | pass |
| ML-9 | `vehicle-ml/README.md:9` | docs only | pass |
| SV-1 | `vehicle-server/src/vehicle_server/report.py:169`, `:342`, `:615` | `test_vsig_consistency.py::test_lost_since_prev_must_match_the_block_seq_gap`, `::test_missing_vsig_gap_event`, `::test_summary_keys_must_match`, `::test_gps_and_vehicle_signal_block_versions_are_both_checked` | pass |
| AN-1 | `vehicle-analyzer/src/services/sessionFilter.ts:29`, `:78`, `:87`, `:137`; `src/components/SessionPanel.tsx:131` | `tests/sessionFilter.test.ts` (9), `tests/components/SessionPanel.test.tsx` (3) | pass |

## Checks
- `vehicle-ml`: `uv run pytest -q` -> 67 passed; `uv run ruff check .` -> pass; `uv run ruff format --check .` -> pass.
- `vehicle-server`: `uv run pytest -q` -> 346 passed; `uv run ruff check .` -> pass; `uv run ruff format --check .` -> pass.
- `vehicle-analyzer`: `npm test` -> 170 passed; `npm run build` -> pass; `npm run test:ui` -> 12 passed.
- `python3 scripts/check_zones.py vehicle-ml --base origin/main`: YELLOW for `vehicle-ml/pyproject.toml`; all other changed paths GREEN.
- `python3 scripts/check_zones.py vehicle-server --base origin/main`: GREEN.
- `python3 scripts/check_zones.py vehicle-analyzer --base origin/main`: GREEN.
- GitHub CI: vehicle-server#39 `test` SUCCESS; vehicle-analyzer#34 `test` SUCCESS. vehicle-ml has no CI workflow yet (red path, requested below), so its checks are local only.

## Unsure about
- ML-8 `--channels all` includes numeric metadata columns such as `*_age_ms`, `*_valid` and tester counters; only exact metadata names are excluded. An explicit `--channels` list avoids them. If "all" should mean measured signals only, the exclusion rule needs a decision.
- For mixed kinds the window grid is the kind with the most rows (usually IMU), so IMU band energy keeps its real rate and lower-rate kinds are held/nearest-previous aligned. If telemetry should always be the base, that is a small change in `dataset.py`.
- `vehicle-ml/pyproject.toml` is yellow: numpy/pandas/pyarrow are the task's allowed deps (BSD/Apache) and pytest/ruff are dev-only, but the dependency manifest still needs user approval and a licence check per AGENTS.md section 3 / D-091.
- SV-1 found code and tests for every sub-item already; the only addition is the combined block-version test. No production gap was found.
- The analyzer filter is remembered per browser viewer under one localStorage key, not per token/account; "per viewer" was read as per browser.
- vehicle-ml has no CI workflow yet (red path), so only its local checks cover PR #9.
- No hardware was used; all data is synthetic.

## For Claude
- Red-zone request: add the `external/vehicle-defs` submodule and CI (`.github/`) to vehicle-ml.
- Review `vehicle-ml/pyproject.toml` (yellow) and approve the numpy/pandas/pyarrow + pytest/ruff dependency set and licences.
- Review the two data-layer choices above (`--channels all` metadata inclusion and the mixed-kind time base).
- SV-1: `ISSUES.md` was not edited; E-18 item (4) can be closed with the code/test evidence in the Result table.
- PRs: https://github.com/vehicle-platform/vehicle-ml/pull/9, https://github.com/vehicle-platform/vehicle-server/pull/39, https://github.com/vehicle-platform/vehicle-analyzer/pull/34.

## Claude review
(Filled by Claude's /external-review: findings, fixes, PRs.)
