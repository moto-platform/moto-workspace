---
date: 2026-10-31
tool: opencode/deepseek-v4.1-flash-free
topic: long-run-2-stage1-exact-stats
repos: [vehicle-ml, vehicle-server, vehicle-mcp, vehicle-workspace]
branches: [vehicle-ml:ext/opencode-ml-stage1, vehicle-server:ext/opencode-server-stats, vehicle-mcp:ext/opencode-mcp-exact-stats, vehicle-workspace:ext/opencode-long-run-2-log]
prs: [vehicle-ml#11, vehicle-server#40, vehicle-mcp#13]
zone: yellow
review: pending
---

# DeepSeek long run 2 — vehicle-ml stage 1 and exact statistics

## Goal
Implement D-083 stage 1 on synthetic data in vehicle-ml (ML-10..ML-18), add exact
`GET /sessions/{id}/stats` to vehicle-server (SV-2), and make vehicle-mcp use it with an
old-server fallback (MCP-1).

## Changes
- `vehicle-ml`: added the defs bridge, server naming rule, role config, synthetic physics
  sessions with injected faults, cooling/charging/gearing estimators, online RLS cooling,
  PCA/robust-z baselines, the evaluation CLI/harness and the stage-1 README section.
  Commits `fa47b32`..`52f0c02`.
- `vehicle-server`: added exact session statistics helpers and
  `GET /sessions/{id}/stats`, kept position-looking names hidden, and documented the endpoint.
  Commit `d1113f3`.
- `vehicle-mcp`: added `stats()` to `HistorySource` and the HTTP client, made
  `compute_signal_stats`/`compare_sessions` prefer the exact route and fall back only on a
  route-level 404, and updated the fake source/tests/README. Commit `85fd698`.
- `vehicle-workspace`: this session log.

## Result
| Task | Code | Tests | Status |
|---|---|---|---|
| ML-10 | `vehicle-ml/src/vehicle_ml/physics/config.py:78` (`load_roles`), `src/vehicle_ml/defs.py:39`, `src/vehicle_ml/data/naming.py:41` | `tests/test_defs_roles.py::test_bridge_imports_the_pinned_defs_version`, `::test_valid_role_config_loads`, `::test_unknown_did_fails_with_the_name` | done `fa47b32` |
| ML-11 | `vehicle-ml/tests/physics_synthetic.py:342` (`make_physics_data_dir`) | `tests/test_physics_synthetic.py::test_every_fault_differs_only_after_onset`, `::test_generator_is_deterministic_per_seed`, `::test_generated_frames_have_no_position_columns` | done `4922e2a` |
| ML-12 | `vehicle-ml/src/vehicle_ml/physics/cooling.py:84` (`fit_cooling`) | `tests/test_cooling.py::test_recovers_known_parameters`, `::test_stuck_thermostat_raises_the_heat_transfer_gain`, `::test_gap_is_never_bridged` | done `6d8b973` |
| ML-13 | `vehicle-ml/src/vehicle_ml/physics/charging.py:38` (`fit_charging`) | `tests/test_charging.py::test_recovers_plateau_cut_in_and_slope`, `::test_plateau_sag_is_visible_in_the_parameters`, `::test_idle_only_data_is_not_identifiable` | done `bbc0584` |
| ML-14 | `vehicle-ml/src/vehicle_ml/physics/gearing.py:28` (`GearTable.fit`) | `tests/test_gearing.py::test_recovers_the_per_gear_median`, `::test_clutch_slip_is_positive_under_load_only`, `::test_gear_zero_is_ignored` | done `5108752` |
| ML-15 | `vehicle-ml/src/vehicle_ml/physics/cooling.py:158` (`fit_cooling_online`), `src/vehicle_ml/physics/rls.py:18` (`RLS`) | `tests/test_cooling.py::test_online_fit_matches_the_batch_fit_without_forgetting`, `tests/test_rls.py::test_converges_to_a_known_linear_system`, `::test_forgetting_tracks_a_step_change` | done `1109e49` |
| ML-16 | `vehicle-ml/src/vehicle_ml/baseline.py:33` (`BaselineModel`) | `tests/test_baseline.py::test_feature_outlier_scores_high`, `::test_fit_rejects_rows_outside_train`, `::test_json_round_trip_preserves_scores` | done `b338cfa` |
| ML-17 | `vehicle-ml/src/vehicle_ml/evaluate.py:472` (`evaluate`) | `tests/test_evaluate.py::test_evaluate_writes_reports_and_per_fault_metrics`, `::test_no_test_session_is_used_for_fit_or_thresholds`, `::test_cli_evaluate_end_to_end` | done `00e1d64` |
| ML-18 | `vehicle-ml/README.md:57` (Stage 1 section) | docs only | done `52f0c02` |
| SV-2 | `vehicle-server/src/vehicle_server/api.py:150`, `src/vehicle_server/series.py:130` (`build_stats_response`) | `tests/test_stats.py::test_stats_are_exact_over_more_than_max_points`, `::test_stats_window_is_relative_to_t0`, `::test_stats_empty_window_has_zero_count_and_nulls`, `::test_stats_unknown_or_position_name_is_404` | done `d1113f3` |
| MCP-1 | `vehicle-mcp/src/vehicle_mcp/tools.py:264` (`compute_signal_stats`), `src/vehicle_mcp/client.py:154` (`stats`) | `tests/test_tools.py::test_compute_signal_stats_requests_exact_stats_route`, `::test_compute_signal_stats_uses_exact_stats_without_approximation`, `::test_compute_signal_stats_falls_back_for_old_server`, `::test_compare_sessions_uses_exact_stats`, `::test_compare_sessions_falls_back_for_old_server` | done `85fd698` |

## Checks
- `cd vehicle-ml && uv run pytest -q`: pass (116 passed).
- `cd vehicle-ml && uv run ruff check . && uv run ruff format --check .`: pass.
- `cd vehicle-server && uv sync && uv run pytest`: pass (356 passed).
- `cd vehicle-server && uv run ruff check . && uv run ruff format --check .`: pass.
- `cd vehicle-mcp && uv run pytest -q`: pass (76 passed).
- `cd vehicle-mcp && uv run ruff check . && uv run ruff format --check .`: pass.
- `python3 scripts/check_zones.py vehicle-ml --base origin/main`: green.
- `python3 scripts/check_zones.py vehicle-server --base origin/main`: green.
- `python3 scripts/check_zones.py vehicle-mcp --base origin/main`: yellow (read-only-tools rule; PR #13 marked `needs-claude-review`).
- `python3 scripts/check_zones.py . --base origin/main`: green for this log.
- `gh pr checks 11 --repo vehicle-platform/vehicle-ml`: pass.
- `gh pr checks 40 --repo vehicle-platform/vehicle-server`: pass.
- `gh pr checks 13 --repo vehicle-platform/vehicle-mcp`: pass.

## Unsure about
- vehicle-ml is proven only on deterministic synthetic sessions; the evaluation is descriptive
  and has no pass/fail threshold, so it is not a generalisation claim.
- The MCP fallback treats a 404 whose detail is empty, `Not Found` or `not found.` as the old
  server's missing route. A proxy with a different 404 body would surface as an error instead.
- SV-2's position protection is name-based, matching the existing `/series` rule; it is not a
  data-level guarantee.
- The evaluation run used one synthetic seed; no real ride data was available or committed.

## For Claude
- Add `GET /sessions/{id}/stats` to the Read API list in `vehicle-server/CLAUDE.md` (red zone).
- vehicle-mcp PR #13 is yellow and needs review.
- No new dependencies or missing role names were needed.
- Review whether the name-based position filter is sufficient for the new `/stats` route.

## Claude review
(Filled by Claude's /external-review: findings, fixes, PRs.)
