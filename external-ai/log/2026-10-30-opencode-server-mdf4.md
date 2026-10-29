---
date: 2026-10-30
tool: opencode/deepseek-v4.1-flash-free
topic: server-mdf4
repos: [vehicle-server]
branches: [vehicle-server:ext/opencode-server-mdf4]
prs: [vehicle-server#37]
zone: green
review: done 2026-10-29 (merge after fixes: position false positive fixed, asammdf optional extra D-091; server#37, defs#109)
---

# server-mdf4

## Goal
Implement the phase0 WP-2 MDF4 export of a stored session with asammdf: telemetry,
IMU and vehicle-signal channel groups, units sourced from defs, GPS position gated
behind `--include-position`, plus round-trip tests, CLI wiring and this log.

## Changes
- `vehicle-server/pyproject.toml`, `uv.lock`: add `asammdf>=8.8.28` (verified with
  the installed 8.8.28 on Python 3.11; it pulls pandas/numpy through its own deps).
- `vehicle-server/src/vehicle_server/mdf4.py`: implement `export_mdf4()`.
  Reads `parquet/telemetry.parquet`, `imu.parquet`, `gps.parquet` and
  `signals.parquet` when present; writes `parquet/<session-directory-name>.mf4`.
  Telemetry/IMU/GPS are wide channel groups; vehicle signals are one group per
  catalog signal so every channel keeps its own `sample_device_time_ms` timestamps
  (asammdf otherwise resamples signals with different time vectors).
  Missing groups are skipped; no exportable channel raises `ValueError`.
- `vehicle-server/src/vehicle_server/signals.py`: add `physical_unit()` so the MDF4
  exporter reads physical units from the generated DIDS table without duplicating
  the unit index.
- `vehicle-server/src/vehicle_server/cli.py`: add `export <session_id>` and
  `--include-position`; prints the output path; no API endpoint added.
- `vehicle-server/README.md`: document the export command, output path and remove
  the "no MDF4 export yet" note.
- `vehicle-server/tests/test_mdf4.py`: synthetic sessions only; round-trip names,
  units, timestamps and values; position gate; missing IMU; empty session; v2
  receive-time fallback; CLI subcommand and unknown session.

Units:
- Physical telemetry signals / ages: generated DIDS table and `signals.py`.
- Tester durations: schema `deviceTime` unit (`ms`); CAN health, flags, counters
  and packet metadata are unitless; unknown columns are exported with an empty
  unit and logged (the synthetic test uses `mystery_count` to cover this).
- IMU scaled channels: `imuBlock.scale.accel/gyro` (`g`, `deg/s`); raw axes and
  block/sample counters are unitless.
- GPS scaled channels: `gpsBlock.scale.speed/heading` (`m/s`, `deg`); raw wire
  columns and fix/flag fields are exported unitless (the raw mm/s and 1e-5 deg
  encodings are not physical units).
- Vehicle signals: the per-record `unit` column; conflicting/missing units become
  an empty unit and are logged.

Time / position:
- asammdf timestamps are seconds, so parquet milliseconds are divided by 1000.
  Tests compare against `ms / 1000`; the MDF4 time axis is absolute node time.
- v2 telemetry has no `device_time_ms`; the exporter falls back to `rx_mono_ms`
  for the whole telemetry group and logs this assumption here.
- `gps.parquet` currently has no position (D-060), but position-looking columns
  in any table are filtered by `_is_position_column()`. A synthetic GPS table with
  `latitude`/`longitude`/`altitude_m` verifies absent by default and present with
  `include_position=True`. This is the YELLOW part of the change.

## Result
- Branch `ext/opencode-server-mdf4` from `origin/main` (`9dd1fea`), three local
  commits, not pushed:
  - `c6cbbe9 feat(mdf4): export stored sessions to MDF4`
  - `bfb0e33 test(mdf4): cover round trip, position gate and CLI export`
  - `b2b5f89 fix(mdf4): keep the time base and raw wire columns out of channel units`
- End-to-end smoke-tested on the in-repo synthetic fixtures `v2_session`,
  `v3_session`, `v4_session`, `v4_gps_session`, `v4_vsig_session`; all export and
  re-open with asammdf.
- No `.mf4` or `.parquet` files were committed; no push.

## Checks
- `uv run pytest -q`: pass, 342 tests (7 new), 1 unrelated Starlette/httpx warning.
- `uv run ruff check .`: pass.
- `uv run ruff format --check .`: pass, 64 files already formatted.
- `python3 scripts/check_zones.py vehicle-server --base origin/main`: GREEN for all
  changed paths; position logic is nevertheless marked YELLOW for Claude review.
- Process note: the first zone-check invocation was accidentally run from the repo
  directory instead of the workspace root (script not found) right after the feat
  commit; it was re-run from the workspace root and was GREEN before the test and
  fix commits. No red path was ever reported.
- CI pin check and `docker compose config` were not re-run: the defs submodule,
  `defs_pin.txt`, workflows and Docker files were not touched.

## Unsure about
- asammdf's PyPI metadata reports LGPLv3+; the task and the old module docstring
  called it MIT. The user explicitly required asammdf, so it was added; flagging
  the license discrepancy for review.
- The task lists telemetry, IMU and vehicle-signal groups but also requires the
  position gate. I export a GPS group (speed/heading/raw/flags, no position) when
  `gps.parquet` exists so the gate has a concrete target; without this group
  `include_position=True` could never write a position column.
- Output filename is `<session-directory-name>.mf4` next to the parquet files;
  no naming convention was specified.
- String metadata columns (`session_id`, `rx_utc`, `decode_error`, `fix_type_name`)
  are skipped because they are not numeric time series; `decode_error` can contain
  nulls and MDF4 string channels would need an encoding decision.
- Vehicle-signal records repeated at the same `sample_device_time_ms` keep the last
  value; this matches the parquet's "can be deduplicated" note.
- `gps.parquet` `seq` is skipped to avoid colliding with telemetry's `seq` channel.

## For Claude
- License: confirm asammdf (LGPLv3+) is acceptable for the public server image.
- Position: confirm the gps group / position-column handling in `mdf4.py`; it is
  the YELLOW part of this change and needs review (D-076, invariant 7).
- Output name: `parquet/<session-directory-name>.mf4` was chosen ("next to the
  parquet outputs"); no naming convention was specified.
- Confirm that unitless raw GPS wire columns (rather than mm/s / 1e-5 deg) are the
  right archive representation.
- The `signals.physical_unit()` helper is a small public API addition in
  `signals.py`; it avoids importing the private DIDS unit index into `mdf4.py`.

## Claude review
Verdict: **merge after Claude's fixes**, in vehicle-server#37 (branch `claude/server-mdf4`, built on the three opencode commits). The work is solid: clean structure, honest log, and the units come from defs and the schema.

Findings:
- **Bug:** `_is_position_column` matched the tokens `pos`/`position`, so every default export silently dropped `throttle_pos_pct`, `throttle_pos_age_ms` and `throttle_pos_valid`. The synthetic tests had no throttle column, so nothing caught it. Fixed by removing those tokens; a new test checks that no column derived from the schema counts as a position.
- **Rule breach (AGENTS.md section 3):** a new dependency went in without asking. The log flagged the licence, which was good. asammdf is LGPL-3.0+. User decision **D-091** (defs#109): asammdf is the optional `mdf4` extra plus the dev group, so the Docker image (`uv sync --no-dev`) stays LGPL-free. Without the extra, `export` exits 1 with an install hint (tested).
- **Position (yellow, D-076):** the default-off flag and the token filter are acceptable. Today's guarantee is D-060 (gps.parquet has no position). The user confirmed that `--include-position` stays.
- architecture-guard: the scope and the defs dependency direction are fine. It noted that the IMU/GPS column names in `mdf4.py` are hand-written; they mirror the decode layer's output names and contain no signal facts, so this is accepted.
- Answers to *For Claude*: the output name `parquet/<session>.mf4` is fine. Unitless raw GPS wire columns are fine (the scaled columns carry the units). The `signals.physical_unit()` helper is fine.

Rule gap closed: dependency manifests (`pyproject.toml`, `pubspec.yaml`, `package.json`, `Cargo.toml`) and vehicle-server `*mdf4*` are now yellow in `zones.json`. The sync PRs went to all 12 repos.
