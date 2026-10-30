# DeepSeek long run — 2026-10-30 (vehicle-ml data layer + two small items)

Written by Claude for opencode/DeepSeek. Work through the tasks **in order**, without asking
between tasks. One commit per task (Conventional Commits, `AI-Agent: opencode/<model>` trailer).
If a task is blocked, write why in the log's *For Claude* section and go on to the next one.

## 0. Before you start (read, do not skip)

- `AGENTS.md` at the workspace root: zones, branches, commit trailer, log format. Check every
  changed path with `python3 scripts/check_zones.py <repo> --base origin/main` before each push.
  **Red = stop**, write the request into the log.
- `vehicle-ml/CLAUDE.md` (methodology rules 1-5 are non-negotiable), `vehicle-server/README.md`
  §Storage layout, §GPS, §Vehicle signals, §Derived signals (to know the files you read).
- `PLATFORM-RULES.md` invariants 2 (never invent signals) and 7 (position).
- Never commit real ride data, GPS positions, keys or tokens (D-033). All test data is synthetic.

Branches (one PR each, opened against `main`, PR body says `needs-claude-review` if any path is yellow):

| Part | Repo | Branch | Tasks |
|---|---|---|---|
| A | vehicle-ml | `ext/opencode-ml-data-layer` | ML-1 … ML-9 |
| B | vehicle-server | `ext/opencode-server-e18-verify` | SV-1 |
| C | vehicle-analyzer | `ext/opencode-analyzer-session-filter` | AN-1 |

One session log for the whole run: `external-ai/log/2026-10-30-opencode-long-run.md` (copy
`TEMPLATE.md`; `review: pending`; a result row per task with code `file:line`, test names, status).

## Part A — vehicle-ml data layer (the main work)

Context: vehicle-ml is an empty skeleton (README says "no code yet"). It trains offline on the
Parquet files that vehicle-server writes. This run builds only the **data layer**: load sessions,
split by session, cut windows, compute features, write a dataset. **No model training, no model
choice, no labels** (those need user decisions).

Hard rules for every ML task:
1. **Session-based split only** (CLAUDE.md rule 1). Nothing may split rows of one session across
   train/val/test. Every frame the library returns carries a `session_id` column.
2. **No hand-written signal names in library code** (invariant 2). Column names come from the
   Parquet files (the server took them from vehicle-defs) or from the caller's config. Tests may
   use the example column names that `vehicle-server/README.md` documents (`engine_speed_rpm`,
   `vehicle_speed_kmh`, ...), and nothing else.
3. **Never load a position.** Drop any column whose name looks like a position component, with
   the same rule as `vehicle-mcp/src/vehicle_mcp/tools.py` `is_position_name` (lat/lon/lng/latitude/
   longitude anywhere; height/alt/altitude only as the last token). Copy the rule into
   `vehicle_ml/data/position.py` with a comment naming its source; test it with the mcp cases.
4. Read-only on the data dir: open `index.sqlite` with `sqlite3.connect("file:...?mode=ro", uri=True)`;
   never write next to the server's files. Outputs go to a caller-given directory.
5. Runtime dependencies: `numpy`, `pandas`, `pyarrow` only (all BSD/Apache). Dev: `pytest`, `ruff`.
   Any other dependency → *For Claude*, do not add it.
6. Python ≥ 3.11, `uv`, `ruff` (line length 100, like vehicle-mcp), type hints, docstrings in English.

Do **not** create: `external/` (the defs submodule), `.github/` (CI), `CLAUDE.md` or `AGENTS.md`
edits — all red. Put "add the vehicle-defs submodule and CI to vehicle-ml" into *For Claude*.

### ML-1 Scaffold
`pyproject.toml` (name `vehicle-ml`, src layout `src/vehicle_ml/`, console script `vehicle-ml`),
`uv.lock`, `.gitignore` (add `data/`, `out/`, `*.parquet` outside `tests/`), `src/vehicle_ml/__init__.py`,
`tests/`. README: replace "no code yet" with a short status and a Build section
(`uv sync`, `uv run pytest`, `uv run ruff check .`, `uv run ruff format --check .`).
Done when the three commands pass on an empty test.

### ML-2 Synthetic data dir for tests
`tests/synthetic.py`: `make_data_dir(tmp_path, sessions=...)` writes a directory in the
vehicle-server layout (`index.sqlite` + `sessions/<id>/parquet/*.parquet`) with N synthetic
sessions. Mirror the **real** schemas: read the server code that creates `index.sqlite`
(`vehicle-server/src/vehicle_server/index.py`) and that writes each Parquet file
(grep `to_parquet`/`write_table` in `vehicle-server/src/vehicle_server/`) and copy the column names
and types you need (document the source file:line in a comment). Include: telemetry with a
`device_time_ms` axis, an IMU file at a higher rate, a gps file with speed/heading only, a
signals file, a long-format derived file, one session without IMU, one with a time gap, one
with an extra column named like a position (`gps_latitude`) to prove it is dropped.

### ML-3 `vehicle_ml.data.store.SessionStore`
`SessionStore(data_dir)`: `sessions()` → DataFrame from `index.sqlite` (session_id, created_utc,
status, packet_count, loss_percent, has_imu, has_gps, has_vehicle_signals, has_derived);
`load(session_id, kind)` for `kind` in `telemetry|imu|gps|signals|derived` → DataFrame with
`session_id` added, position-like columns dropped, `None` when the file does not exist;
`channels(session_id)` → available column names per kind. Clear error for an unknown session.
Tests: every kind, missing files, unknown id, position column dropped, read-only (the test makes
the dir read-only with `chmod` and still loads).

### ML-4 Session split `vehicle_ml.split`
- `assign_split(session_id, fractions=(0.7, 0.15, 0.15), seed=0) -> "train"|"val"|"test"`: a
  stable hash of `(seed, session_id)` (use `hashlib.sha256`, not `hash()`), so adding a session
  never moves an existing one.
- `split_sessions(ids, fractions, seed) -> dict[str, list[str]]`.
- `group_kfold(ids, k, seed)` → k (train_ids, test_ids) folds by session.
- `assert_no_leakage(*frames_or_id_lists)` raises if any session_id appears in two parts.
Tests: determinism, stability when a session is added, fractions within tolerance on 1000 ids,
fractions that do not sum to 1 rejected, leakage detected.

### ML-5 Windows `vehicle_ml.windows`
`make_windows(frame, channels, window_ms, stride_ms, max_gap_ms, max_missing=0.2)`:
on the `device_time_ms` axis of **one** session; a window never spans two sessions and never
spans a gap in the axis larger than `max_gap_ms` (it is dropped, and counted); a window whose
missing fraction of any channel exceeds `max_missing` is dropped (counted by reason). Returns the
windows (session_id, start_ms, end_ms, per-channel arrays) plus a drop report. A helper aligns
two kinds (e.g. telemetry + IMU) on a common grid by nearest-previous sample within a tolerance;
no interpolation across a gap. Tests with the synthetic gap session and with an empty session.

### ML-6 Features `vehicle_ml.features`
Per window and channel: `count`, `mean`, `std`, `min`, `max`, `rms`, `p05`, `p50`, `p95`;
optional spectral band energy with `numpy.fft.rfft` for channels the caller lists, bands in Hz
given by the caller, sample rate measured from the window's timestamps (reject a window whose
rate varies more than a tolerance). Feature names `<channel>.<stat>` / `<channel>.band_<lo>_<hi>hz`.
NaN-safe; units unchanged. Tests against hand-computed values on small arrays (a pure sine
lands in the right band).

### ML-7 Normalisation `vehicle_ml.normalize`
`Standardizer.fit(train_features)` / `.transform(any)` / `to_json` / `from_json`; constant
features get std 1 and are listed; `fit` takes the split manifest and raises if it is given a
row whose session is not in train. Tests for round-trip and the train-only guard.

### ML-8 Dataset builder + CLI
`vehicle-ml dataset --data-dir D --out O --kinds telemetry,imu --channels <comma list or "all">
--window-ms 2000 --stride-ms 1000 --max-gap-ms 500 --seed 0 [--bands imu_col:0-5,5-20]`
writes to `O/`: `features.parquet` (one row per window, `session_id`, `split`, `start_ms`,
features), `split.json` (session → split, seed, fractions), `scaler.json` (fit on train),
`dataset.md` (dataset card: sessions and windows per split, channels per kind, per-modality
availability per session — supports CLAUDE.md rule 3 —, the drop report, the defs version found
in each session's `report.json` if present). Refuse to write into `D`. Exit codes 0 ok / 2 bad
arguments / 1 error. Test the CLI end to end on the synthetic dir.

### ML-9 README
Sections: what the data layer does, the split rule and why (rule 1), the position rule, CLI
example, outputs. English, short. No claims about models.

## Part B — vehicle-server

### SV-1 Verify ISSUES E-18 (4)
`ISSUES.md` row E-18 item (4): "cross-check `lost_since_prev`, the `vsig_gap` event and the
summary `vehicle_signal_*` keys; reject an unknown `vehicle_signal_block_version` once
`gps_block_version` is checked too". Claude believes `src/vehicle_server/report.py` already does
this (`_vsig_gap_events`, `_block_version_problem` near line 616). For each sub-item give
evidence (code file:line + an existing test name). Where a sub-item has code but **no test**,
add the test. Do not change behaviour; if you find a real gap, describe it in *For Claude*
instead of fixing it. Do not edit `ISSUES.md` (Claude closes the row).
Checks: `uv run pytest`, `uv run ruff check .`, `uv run ruff format --check .`.

## Part C — vehicle-analyzer

### AN-1 Session list filter (A3 panel)
In `src/components/SessionPanel.tsx` (key E) add, above the session list: a text filter on the
session id, status chips for the statuses that occur in the loaded list (do not hard-code
`ok/warn/fail`; take them from the data), a `created_utc` from/to date filter (date-only = whole
UTC day, same rule as vehicle-mcp `query_ride_history`), and sort by created_utc (newest first
by default) or by loss. Pure filtering logic in a new `src/services/sessionFilter.ts` with unit
tests; a component test for the panel. Remember the filter per viewer in `localStorage`
(wrapped in try/catch). Do not touch `src/services/webSerialCan*`, `src/services/udsComposer*`,
`src-tauri/` (red) or `src/defs/` (yellow, not needed).
Checks: `npm test`, `npm run build`, the Playwright smoke test if it runs locally.

## Finish

- Push each branch, open its PR, fill the log (Result table, Checks, Unsure about, For Claude),
  commit the log on a `ext/opencode-long-run-log` branch in vehicle-workspace and open that PR.
- Do not merge anything. Do not edit `STATUS.md`, `ISSUES.md`, `DECISIONS.md`.
