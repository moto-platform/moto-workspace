# STATUS — session handoff

> Keep it short (≤60 lines). Updated by the `/handoff` skill. "Recent sessions" keeps at most 5 one-line entries; drop the oldest.

**Phase:** 1 data pipeline done in code (bench test pending) · 2 rt-core without hardware: ISO-TP, host layer and Ç3 UDS client + server and the DID poller fault handling done (rt-core v0.5.1) · safety architecture decided (D-041..D-045) · ISSUES groups 1-4, E-1, E-4, E-5, E-7..E-9, E-10 (rt-core) and C-6..C-8 done · defs v0.3.3
**Last updated:** 2026-10-02

## Where we are

- 11 platform repos + `moto-workspace`, public (D-033), MIT (D-036). Decisions D-001..D-053. D-030 awaits confirmation.
- **Releases (all pinned in `manifest.yaml`):** defs v0.3.3, rt-core v0.5.1, conn/mobile/server v0.1.0. defs v0.3.3 (2026-10-02, defs#30, 7d121b6, PATCH) = D-053: `client_step_max_ms` 10, 0xF40D/0xF40C 110 ms (~9.1 Hz), 0xF40C stale 330; no signal, `tester_policy` or D-020 change. rt-core v0.5.1 (2026-10-02, rt-core#18, 9af2a5d) = defs v0.3.3 + E-10. conn `main` pins defs v0.3.0 (conn#8, no conn release yet). Nothing unreleased in defs or rt-core.
- **DID poller fault handling (D-050..D-053):** a timed-out or slow DID competes as normal with no 0x78 extension until it answers in time or is skipped (D-050, D-051); samples stamped with the oldest unanswered read (D-051); slow answers keep the skip count, `poll_period_ms` ≥ base timeout (D-052); and ≥ base + step S (D-053), so an answer seen one step late is in time and its DID not yet due.
- **E-10 done for rt-core (2026-10-02), rt-core#18:** `stats.step_overruns` / `step_gap_max_ms` (diagnostic only, SIL summary prints them; +12 B RAM, +52 B flash), Unity tests at S (a P = B table fails 4 of them, checked by mutation), test fixes after the bump, uds README re-measured (endless 0x78: RPM STALE 23.5 %; slow 0xF40D: RPM ≤ 0.2 %; alternating 25.9 %; RPM at 51..B−1: no DID STALE). vss CLEAN, safety-reviewer no blocker/MAJOR; MINOR-1 (S definition wording) and MINOR-2 (no target read-out) → ISSUES E-11.
- **E-6 (1)-(4) done:** rt-core#14 (`not_sent` restores session/TP/read schedules and is not counted, 10 ms step test, +4 B RAM; delta review no blocker), defs#21 (bool timing values refused).
- **Group 3 done (2026-10-01):** C-5 `setup.sh`, C-3 safety-reviewer sync, C-2 blocking `make misra` on defs `gen/c` (register `misra/README.md`, DEV-001..005) and blocking cppcheck in conn. rt-core#11 merged.
- **Group 4 done (2026-10-01), conn#8 (C-1):** defs v0.3.0, gen/ `uds_iso14229.h` (conn's own header removed; ISO-TP transport constants in `src/IsoTpCan.h`), foreign-tester watch IDs from `vehicle_cl250_functional_watch[]`. conn's 29-bit watch matches any SA; rt-core's matches 0x18DB33F1 exactly. Vehicle-bus behaviour unchanged.
- **cppcheck is pinned to 2.22.0 in CI** (built from the tag and cached; runner ubuntu-24.04) in defs, conn and rt-core. Ubuntu's apt 2.13 misses findings (15.6 on the canary).
- **C-6/C-7 (2026-10-01), defs#18, released in v0.3.1:** the gate is single-exit with a fail-closed `bool ok = false`; `test_gate_equivalence.py` proves it equal to the old gate (every byte the request/frame gates read, -O0/-O2). DEV-005 and the gate part of DEV-004 are gone; `make misra` clean. safety-reviewer follow-ups are ISSUES C-9.
- **Branch protection on `main` (D-049, C-8, 2026-10-01)** in all 12 repos: PR required (0 approvals), admin bypass on, no force push or deletion. Required checks (strict, github-actions): defs `check`, conn/rt-core `build-and-test`, server `test`, mobile `flutter` + `build-apk`; the other 7 repos (workspace included) have the PR rule only. **No direct pushes to `main`; every change, STATUS included, goes through a PR.** A new repo's first CI workflow must also add its job as a required check.
- **`ISSUES.md`:** sections A-E; read only the group you work on. Open: C-4 (user), C-9, D-*, E-3, E-6 (5)/(6), E-10 (conn part), E-11, B-9.
- **Vehicle bus unchanged:** one read-only tester (D-037); tester_policy and the golden D-020 copy are untouched. Start sessions from the workspace root.

## Next up (in order)

1. **rt-core Ç1, CAN error state machine + H7 HAL** (ISSUES D-2, `/feature-module moto-rt-core can`, then architecture-guard and safety-reviewer). Plan a read-out of the D-053 step counters with it (ISSUES E-11 (1)).
2. **Platform-bus republisher** of `vehicle_signals`: NONE/STALE become INVALID, and 0x021 clamps to 255 km/h (D-048).
3. **Optional:** bump conn's defs submodule to v0.3.3 (its gen/ DID table then polls RPM and speed at 110 ms; check its step and its order, answer before the timeout check, against S: E-10 conn part), then a conn release (D-036) so `manifest.yaml` pins a conn tag. Small defs docs PR: align D-053 item 5's S wording with the yaml (E-11 (2)).
4. **Hardware-dependent (group 6), with E-6 (5)/(6):**
   - D-029 bench: ECU round trip + target `uds_client_step()` period → `assumed_round_trip_ms`; worst step gap incl. jitter (histogram, `stats.step_gap_max_ms`) → `client_step_max_ms` (D-053); check how the CL250 reacts to a new 0x22 after 0x78 (D-050 assumption)
   - HIL fault scenarios (silent / endless-0x78 / slow 0xF40D, answers to abandoned reads (D-051), the D-052 alternations, 0xF40C at 51-99 / 95-100 ms, a single lost frame)
   - A-4 polling budget + PID check in the Q-001 probe (with 0x7DF and 0x18DB33xx from any SA: conn latches on all of them)
   - A-5 and E-3 BOM, D-029 measurements, ESP32 + APK end to end

## Blockers / pending decisions

- Q-019 (board) blocks CubeMX, Renode and Ç6. Q-009 blocks the hil-bench host. Q-020 is deferred (D-037).
- Before safety-node Layer 1 code: Q-023 (fallback details) and Q-026 (LED ring owner), both with the Group 7 hardware. Q-022 comes after fallback validation (k_red ≤ 0.8 until then).
- **User:** C-4: turn off the old `can-dbc-conventions` skill on claude.ai (still active on 2026-10-01).
- Q-024 (voice path, ESP32 PSRAM, wake-word default), Q-025 (vibration features). D-030 awaits confirmation. Q-017; Q-014/Q-015 provisional. Q-016, Q-001, Q-003, Q-004, Q-006.

## Recent sessions

- 2026-10-02 (local, releases + E-10): defs#30 → defs v0.3.3 (7d121b6); rt-core#18 (defs v0.3.3, step-gap counter, tests at S, README re-measured) → rt-core v0.5.1 (9af2a5d); both pinned in `manifest.yaml`. vss CLEAN, safety-reviewer no blocker/MAJOR (NITs applied, MINOR-1/2 → E-11). No worktree to prune at start.
- 2026-10-02 (local, E-9 / D-053): user chose (b), step 10 ms, speed stale 300. defs#28 (rule, 110 ms periods, B + S fault hold, round trip > step check) + defs#29 (D-053); vss CLEAN, safety-reviewer no blocker/MAJOR (MINOR-1/2, NITs applied; rt-core/conn items → E-10). Pruned e8-handoff.
- 2026-10-02 (local, releases): defs#27 → defs v0.3.2 (f744511); rt-core#17 → rt-core v0.5.0 (5ed2f2d): defs pin v0.3.2, v0.3.1 slow-RPM test deleted, period rule asserted, uds README re-measured; no module assumes 20 Hz RPM (anomaly-safety-net not written yet; docs say RPM 10-20 Hz; hardware-architecture's "20 Hz is enough for display" is a UX note for the HMI). vss CLEAN. Both pinned in `manifest.yaml`.
- 2026-10-01 (local, E-8 / D-052): user chose (1) c, (2) b, (3) a (kept after the measured 28.1 % cost), (4) HIL. defs#25 and rt-core#16 merged by the user; defs#26 went out of date, was updated with main and merged; vss CLEAN, safety-reviewer no blocker/MAJOR (MINOR-1/4 applied, MINOR-2 → E-9). ISSUES: E-8 done, E-6 (6) scenarios, E-9 opened.
- 2026-10-01 (local, E-7 / D-051): user chose (1) a, (2) a+ (instead of a: a misattributed answer would still look ≥ 200 ms younger), (3) yes. defs#23 (fault-mode check), defs#24 (D-051), rt-core#15 merged; vss CLEAN, safety-reviewer no blocker (MAJOR-1/3, MINOR-1/3, NITs applied; MAJOR-2, MINOR-2 → E-8). Pruned 5 merged worktrees.
