# DeepSeek long run 3 — 2026-10-31 (vehicle-ml modality attribution + analyzer composer)

Written by Claude for opencode/DeepSeek. Work through the tasks **in order**, without asking
between tasks. One commit per task (Conventional Commits, `AI-Agent: opencode/<model>` trailer).
If a task is blocked, write why in the log's *For Claude* section and go on to the next one.

## 0. Before you start (read, do not skip)

- `AGENTS.md` at the workspace root: zones, branches, commit trailer, log format. Check every
  changed path with `python3 scripts/check_zones.py <repo> --base origin/main` before each push.
  **Red = stop**, write the request into the log.
- `vehicle-ml/CLAUDE.md` methodology rules 1-5 (non-negotiable). This run is about **rule 3**
  ("which modality catches which fault is reported separately; at least one fault scenario must
  leave a weak trace on CAN") and **rule 4** (no generalisation claim).
- `vehicle-ml/README.md`: the data layer (`SessionStore`, `split`, `windows`, `features` incl.
  `--bands` FFT band features, `normalize`, `dataset`) and the "Stage 1 (D-083)" section you
  build on (`physics/`, `baseline.py`, `evaluate.py`, `configs/physics_cl250.toml`).
- `vehicle-defs/docs/DECISIONS.md` **D-083** and `vehicle-defs/docs/ideas/physics-informed-anomaly.md` §1.
- `PLATFORM-RULES.md` invariants 2 (never invent signals: names, units and vehicle constants
  come from `vehicle_ml.defs`), 3 (ML never feeds the safety partition) and 7.
- Never commit real ride data, GPS positions, keys or tokens (D-033). All test data is synthetic.
- Last run's review (`external-ai/log/2026-10-31-opencode-long-run-2.md`, *Claude review*):
  hand-written vehicle facts in tests were the one real finding. Read every vehicle constant
  (gear ratios, wheel radius, reductions) from `vehicle_ml.defs.vehicle_constants`.

Branches (one PR each, opened against `main`, PR body says `needs-claude-review` if any path is yellow):

| Part | Repo | Branch | Tasks |
|---|---|---|---|
| A | vehicle-ml | `ext/opencode-ml-modality` | ML-19 .. ML-22 |
| B | vehicle-analyzer | `ext/opencode-composer-defaults` | AN-1 |

One session log for the whole run: `external-ai/log/2026-10-31-opencode-long-run-3.md` (copy
`TEMPLATE.md`; `review: pending`; a result row per task with code `file:line`, test names, status).

## Part A — vehicle-ml, rule 3 on synthetic data

Context: stage 1 is on main (vehicle-ml#12). Its report labels "the detecting modality" with the
arg-max of the detector that fired (`evaluate.py`, the `features_pca` / `features_robust_z`
fallback labels). That names a model, not a signal group, so rule 3 is only partly met, and every
synthetic fault is visible on CAN. This part fixes both. Same hard rules as run 2 (session split,
roles not names in library code, numpy/pandas/pyarrow only, no safety use).

### ML-19 Modality and signal group of every feature
Give every feature column a **source**: the series it came from (`did.<NAME>`, `derived.<name>`,
`sensor.<name>`) and a **modality** derived from it: `can` for `did.*` and `derived.*`, `imu` for
`sensor.imu_*`, `other` for any remaining `sensor.*`. Derive it from the name prefix and the defs
tables (`vehicle_cl250.DIDS`, `vehicle_derived.SIGNALS`, `vehicle_derived.SENSORS`), never from a
hand-written list of names. Physics features also carry their estimator group (`cooling`,
`charging`, `longitudinal`), taken from the role config (add a `group` per estimator in
`configs/physics_cl250.toml` if needed, validated at load).
Tests: every feature column of an ML-8 feature frame has a source and a modality; an unknown
prefix fails with the name; physics features carry their group.

### ML-20 A fault with a weak CAN trace
In `tests/physics_synthetic.py` add IMU channels to the physics sessions (the server IMU layout of
`tests/synthetic.py`, sensor names from `vehicle_derived.SENSORS`, 10 ms period from the defs
`sample_period_ms`) and a fault kind `wheel_vibration`: from `onset_ms` a narrow-band vibration
line in `imu_accel_z` at a fixed multiple of the rear-wheel rotation frequency,
`f = speed / (2 * pi * rear_wheel_radius_dynamic_m)` (radius from `vehicle_constants`; keep `f`
below the 50 Hz Nyquist limit of the 10 ms period, state the multiple). Healthy sessions get
broadband road noise on all six IMU axes. Every CAN and derived column of a `wheel_vibration`
session is **identical** to its healthy twin with the same seed.
Tests: CAN/derived frames equal the healthy twin; IMU differs only after onset; a numpy FFT of a
post-onset window peaks at the expected frequency; the generator stays deterministic per seed.

### ML-21 Attribution in the evaluation
`evaluate.py`: add IMU FFT band features (the data layer's `--bands`) to the baseline windows.
For every alarm record the **modality** (and, for physics alarms, the group) that raised it:
- physics: the estimator's group, modality `can`;
- PCA baseline: the modality whose features hold the largest share of the window's squared
  reconstruction error (per-feature residuals summed per modality);
- robust-z baseline: the modality of the feature with the largest |z|.
Each fault kind in the ground truth gets an `expected_modality` (`can` for the four run-2 kinds,
`imu` for `wheel_vibration`). `evaluation.json` / `evaluation.md` gain a table per model × fault
kind: detections per modality, the modality of the first alarm after onset, and whether it equals
the expected one. Replace the arg-max labels. Report misses as misses: the CAN-only physics
models are expected to miss `wheel_vibration`; say so in the report and do not tune them to
catch it (rule 4).
Tests: on an ML-20 data dir the physics models never attribute to `imu`; the attribution of a
hand-built PCA residual vector and of a hand-built z vector is the expected modality; the report
contains the per-modality table and the synthetic-data sentence.

### ML-22 Several split seeds and the defs pin
1. `vehicle-ml evaluate --seeds 0,1,2` (keeps `--seed` as the single-seed form): runs the
   session split and the whole evaluation once per seed and writes per-seed results plus
   mean/min/max per metric. A seed never changes the data, only the split.
2. A test that `src/vehicle_ml/defs_pin.txt` equals the tag of the `external/vehicle-defs`
   submodule (`git describe --tags --exact-match`; skip with a reason when git metadata is
   missing), so the fallback pin cannot drift on a defs bump.
3. README "Stage 1" section: attribution, the `wheel_vibration` scenario as the rule-3 weak-CAN
   case, `--seeds`. No result numbers presented as findings.
Tests: `--seeds 0,1` writes two per-seed entries and an aggregate; a bad seed list exits non-zero.

Checks for Part A: `uv run pytest -q`, `uv run ruff check .`, `uv run ruff format --check .`.

## Part B — vehicle-analyzer composer defaults

### AN-1 Composer starts on an allowed service
`src/components/UdsPanel.tsx` starts the simulated-ECU composer with the literals `0x22` / `0x03`
(`useState<number>(0x22)`, `useState<number>(0x03)`). Take the defaults from
`composerServices(defs)` instead: the first allowed service and its first sub-function (none →
no sub-function), and reset the sub-function when the service changes to one that does not offer
it. **Do not edit `src/services/udsComposer*`** (red zone): only read its exported function.
Tests (in `tests/components/UdsPanel.test.tsx`): the initial selection equals the
first allowed service of the test defs; changing to a service without sub-functions clears it.
Checks (as in `.github/workflows/`): `npm ci`, `npm test`, `npm run build`, `npm run test:ui`.

## Finish

- Push each branch, open its PR, fill the log (Result table, Checks, Unsure about, For Claude),
  commit the log on an `ext/opencode-long-run-3-log` branch in vehicle-workspace and open that PR.
- Do not merge anything. Do not edit `STATUS.md`, `ISSUES.md`, `DECISIONS.md`, any `CLAUDE.md`.
- Put into *For Claude*: any dependency you wanted (with licence), any sensor or constant you
  could not find in defs, the frequency multiple you chose and why, and every place where the
  attribution rule was ambiguous and the choice you made.
