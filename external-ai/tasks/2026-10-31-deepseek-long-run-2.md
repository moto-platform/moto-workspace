# DeepSeek long run 2 — 2026-10-31 (vehicle-ml stage 1 + exact statistics)

Written by Claude for opencode/DeepSeek. Work through the tasks **in order**, without asking
between tasks. One commit per task (Conventional Commits, `AI-Agent: opencode/<model>` trailer).
If a task is blocked, write why in the log's *For Claude* section and go on to the next one.

## 0. Before you start (read, do not skip)

- `AGENTS.md` at the workspace root: zones, branches, commit trailer, log format. Check every
  changed path with `python3 scripts/check_zones.py <repo> --base origin/main` before each push.
  **Red = stop**, write the request into the log.
- `vehicle-ml/CLAUDE.md` methodology rules 1-5 (non-negotiable), `vehicle-ml/README.md` (the data
  layer you build on: `SessionStore`, `split`, `windows`, `features`, `normalize`, `dataset`).
- `vehicle-defs/docs/DECISIONS.md` **D-083** (staged physics-informed anomaly model, compared
  with a model without physics) and `vehicle-defs/docs/ideas/physics-informed-anomaly.md` §1
  (stage-0 table and the stage-1 estimators). This run is **D-083 stage 1 on synthetic data**.
- `vehicle-defs/docs/DECISIONS.md` **D-092** (vehicle-mcp v0.1 tools and boundaries) for Part B.
- `PLATFORM-RULES.md` invariants 2 (never invent signals), 3 (ML never feeds the safety
  partition) and 7 (position; the LLM never does its own math).
- Never commit real ride data, GPS positions, keys or tokens (D-033). All test data is synthetic.

Branches (one PR each, opened against `main`, PR body says `needs-claude-review` if any path is yellow):

| Part | Repo | Branch | Tasks |
|---|---|---|---|
| A | vehicle-ml | `ext/opencode-ml-stage1` | ML-10 … ML-18 |
| B1 | vehicle-server | `ext/opencode-server-stats` | SV-2 |
| B2 | vehicle-mcp | `ext/opencode-mcp-exact-stats` | MCP-1 |

One session log for the whole run: `external-ai/log/2026-10-31-opencode-long-run-2.md` (copy
`TEMPLATE.md`; `review: pending`; a result row per task with code `file:line`, test names, status).

## Part A — vehicle-ml, D-083 stage 1 (the main work)

Context: the data layer is on main (vehicle-ml#10). Stage 1 of D-083 = classical physics
estimators per subsystem + a baseline **without physics** on the same features + an evaluation
harness that compares them. There is no real ride yet, so everything is proven on synthetic
sessions with **known injected faults**. No neural network, no training framework.

Hard rules for every ML task (in addition to the data-layer rules, which still hold):
1. **Session-based split only** (CLAUDE.md rule 1). Fit estimators' population statistics,
   baselines, scalers and thresholds on `train` (thresholds may use `val`), never on `test`.
2. **No signal names in library code** (invariant 2). Library code takes *roles*
   (`coolant_temp`, `engine_speed`, ...) and a role map. The role map lives in a per-vehicle
   config file `configs/physics_cl250.toml` (stdlib `tomllib`; D-078: vehicle facts in
   per-vehicle files). Each role names a **vehicle-defs signal**: `did.<NAME>` for a
   `vehicle_defs.vehicle_cl250.DIDS` key or `derived.<name>` for a
   `vehicle_defs.vehicle_derived` signal. The loader **validates every name against the pinned
   defs** and fails on an unknown one. Tests use the same config.
3. **Defs access:** vehicle-ml now has `external/vehicle-defs` (v0.20.0). Add
   `src/vehicle_ml/defs.py` that puts `external/vehicle-defs/gen/python` on `sys.path` and imports
   `vehicle_defs`, exactly like `vehicle-server/src/vehicle_server/defs.py` (copy its approach,
   cite it). Do **not** add `vehicle_defs` to `pyproject.toml`, do not edit `external/`.
4. **Column names:** a `did.<NAME>` role maps to its telemetry Parquet column with vehicle-server's
   naming rule (`vehicle-server/src/vehicle_server/signals.py`: lowercased name + normalized unit
   suffix, e.g. `engine_speed_rpm`). Copy that rule into `src/vehicle_ml/data/naming.py` with a
   source comment and test it against the server's documented examples. A `derived.<name>` role
   maps to the long-format `derived` kind (`signal` column).
5. **Runtime dependencies stay numpy, pandas, pyarrow.** No scikit-learn, scipy, torch.
   An isolation forest or autoencoder that needs a new dependency → *For Claude* (D-091 licence
   check and user approval), do not add it.
6. **No safety use.** Nothing here outputs to a node; no threshold here may loosen a safety
   ceiling (invariant 3). Say so in the README.
7. Not modelled in this run (inputs pending, stage-0 table): battery equivalent circuit (needs
   current and 1 kHz voltage), air/fuel trims (trim DIDs not verified, D-068). Do not build them.

### ML-10 Defs bridge, role config, naming
`defs.py` (rule 3), `data/naming.py` (rule 4), `configs/physics_cl250.toml` and
`src/vehicle_ml/physics/config.py`: `load_roles(path) -> RoleMap` with validation (rule 2).
Roles needed by ML-12..ML-14: `engine_speed`, `vehicle_speed`, `coolant_temp`,
`battery_voltage`, `gear_estimate`, `gearbox_ratio_measured`. Pick each name from defs
(`DIDS` / the derived table), never from memory. A role whose signal is missing in a session is
reported, not invented.
Tests: valid config loads; unknown `did.FOO` fails with the name in the message; naming matches
the server examples; the bridge imports the pinned version string.

### ML-11 Synthetic physics sessions with injected faults
`tests/physics_synthetic.py` (test helper, like `tests/synthetic.py`, same server layout):
sessions generated from the **same equations** as the estimators with seeded noise, plus a
fault switch that changes one physical parameter from a given time on:
- cooling: thermostat stuck open (heat-transfer gain up) and fan failure (gain at low speed down);
- charging: plateau sag (regulator plateau drops by a set voltage above cut-in RPM);
- longitudinal: clutch slip (measured ratio rises above the gear's table value under load).
Healthy sessions vary operating point (ambient offset, load) so a detector that only learns one
operating point fails. Return the ground truth (fault kind, onset time) next to the data.
Tests: a healthy and a faulty session differ only after onset; the generator is deterministic
per seed; no position columns.

### ML-12 Cooling: first-order thermal model
`src/vehicle_ml/physics/cooling.py`: per session, fit
`dT/dt = a * q(rpm) - h * (T - T_amb)` with `q` a fixed, documented proxy (e.g. normalised RPM)
and `T_amb` unknown (fit it as a per-session constant; ambient sensor is pending). Linear least
squares with numpy on gap-free stretches only (reuse `windows` gap rules). Outputs: parameters
(`a`, `h`, `T_amb`, time constant), their residual series and a fit-quality value; refuse
stretches that are too short or not excited (document the rule).
Tests: recovers known parameters within a stated tolerance on clean synthetic data; the stuck
thermostat raises `h`; a gap is never bridged; too-short data gives a clear "not identifiable".

### ML-13 Charging: plateau and cut-in
`src/vehicle_ml/physics/charging.py`: from battery voltage vs engine speed, estimate the regulated
plateau voltage, the cut-in RPM and the slope below cut-in (piecewise-linear fit, documented
method, no scipy). Residual = measured voltage − model voltage. The 14.0-15.0 V plateau in the
idea note is CONFIRM: do not hard-code it as a limit, only as a test value.
Tests: recovers plateau and cut-in on synthetic data; plateau sag is visible in the parameters
and the residual; idle-only data → "not identifiable".

### ML-14 Longitudinal: per-gear ratio table and slip residual
`src/vehicle_ml/physics/gearing.py`: learn the per-gear median of `gearbox_ratio_measured` from
`train` sessions (by `gear_estimate`, ignoring 0 = no gear), then per window the slip residual
(measured − table) per gear. Note in the docstring that `gear_estimate` itself is matched to the
defs constants, so the table is a learned check, not a new source of truth.
Tests: table recovered; clutch slip gives a positive residual under load only; gear 0 ignored.

### ML-15 Recursive least squares utility
`src/vehicle_ml/physics/rls.py`: RLS with a forgetting factor (vector parameters, covariance
reset guard), used by ML-12 as an **online** variant next to the batch fit (stage-1 note).
Tests: converges to a known linear system; tracks a step change with forgetting < 1; matches the
batch least-squares answer with forgetting = 1 on the same data.

### ML-16 Baseline without physics
`src/vehicle_ml/baseline.py`: on the ML-8 window features (same windows, same split), a
**PCA reconstruction-error** detector (a linear autoencoder, numpy SVD) and a robust per-feature
z-score (median/MAD) detector. Fit on `train` only (rule 1), keep the scaler from ML-7. Save and
load as JSON like `Standardizer`. Say in the docstring why it counts as the "without physics"
model of D-083 item 3 and that an isolation forest/autoencoder needs a dependency decision.
Tests: fit rejects non-train rows; a feature outlier scores high; JSON round trip.

### ML-17 Evaluation harness and CLI
`src/vehicle_ml/evaluate.py` + `vehicle-ml evaluate --data-dir --out --config [--seed]`:
1. Features for both models from the same windows: physics = ML-12..ML-14 parameters and
   residual statistics per window; baseline = ML-16 on the ML-8 features.
2. Threshold per model chosen on `val` healthy sessions for a target false-alarm rate (argument,
   default documented).
3. On `test`: false alarms per hour of healthy riding, detection delay after onset, missed
   faults, **per fault kind and per modality** (CLAUDE.md rule 3: which signal group caught it).
4. Writes `evaluation.json` and `evaluation.md` (table per model × fault kind, the split, the
   seed, defs version, the sentence "synthetic data; no generalisation claim (rule 4)").
Ground truth for tests comes from ML-11; the CLI reads it from an optional `faults.json` next to
the data dir and otherwise reports false alarms only.
Tests: end-to-end on an ML-11 data dir; no test session is used for fitting or thresholds (assert
via the split manifest); bad arguments exit non-zero.

### ML-18 README
Add a "Stage 1 (D-083)" section: what each estimator identifies, the baseline, the metrics, the
role config and defs bridge, what is deliberately not modelled (rule 7), the no-safety-use
sentence (rule 6). No result numbers presented as findings.

Checks for Part A: `uv run pytest -q`, `uv run ruff check .`, `uv run ruff format --check .`
(the `test` CI job runs the same on the PR).

## Part B — exact statistics for long windows

Context: vehicle-mcp's `compute_signal_stats` and `compare_sessions` read `GET /sessions/{id}/series`
with `max_points` 20000. For a longer window vehicle-server min/max-downsamples, so mean, std and
percentiles are only approximate (`vehicle-mcp/src/vehicle_mcp/stats.py` says so). Fix: the server
computes them exactly; the tool set and the tool outputs' shape do not change (D-092).

### SV-2 vehicle-server `GET /sessions/{id}/stats`
`GET /sessions/{session_id}/stats?signals=a,b&start_ms=&end_ms=` (bearer token like the other
read endpoints): for each requested series name (the same names `/series` serves: `did.*`,
`sensor.*`, `derived.*`) the exact `count`, `mean`, `std`, `min`, `max`, `p05`, `p50`, `p95`
over the full-resolution points in the window, plus `unit` and `t_first_ms`/`t_last_ms`, on the
same t0 as `/series`. Reuse `series.load_all`/`window` (do not duplicate loading). Never a
position-looking series (same rule as `/series`); unknown names → 404 listing them; empty window
→ count 0 and nulls. Document it in `README.md` (HTTP API) and keep the OpenAPI version test green.
Tests: a window longer than 20000 points gives the exact mean/percentiles (compare with numpy on
the fixture), units, auth, 404, empty window, position name refused.
Checks: `uv run pytest -q`, `uv run ruff check .`, `uv run ruff format --check .`.

### MCP-1 vehicle-mcp uses the exact statistics
Add `stats(session_id, signals, start_ms, end_ms)` to the `HistorySource` interface and the
vehicle-server client (one GET, like the others). `compute_signal_stats` and `compare_sessions`
use it; when the server answers 404 for the **route** (an older server without SV-2) they fall
back to today's path and keep the existing "downsampled" note. The statistics still come from
the server or the tool, never from the LLM (invariant 7). Update the fake source in the tests,
`README.md` (Data sources) and nothing in the tool list.
Tests: exact path used when available; fallback on an old server; the approximate note appears
only on the fallback; compare_sessions uses the same source.
Checks: `uv run pytest -q`, `uv run ruff check .`, `uv run ruff format --check .`.

## Finish

- Push each branch, open its PR, fill the log (Result table, Checks, Unsure about, For Claude),
  commit the log on an `ext/opencode-long-run-2-log` branch in vehicle-workspace and open that PR.
- Do not merge anything. Do not edit `STATUS.md`, `ISSUES.md`, `DECISIONS.md`.
- Put into *For Claude*: any dependency you wanted (with licence), any role whose defs name you
  could not find, any place the idea note's equations were ambiguous and the choice you made.
