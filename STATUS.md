# STATUS — session handoff

> Keep it short (≤60 lines). Updated by the `/handoff` skill. "Recent sessions" keeps at most 5 one-line entries; drop the oldest.

**Phase:** 1 data pipeline done in code (bench test pending) · 2 rt-core without hardware: ISO-TP, host layer, Ç3 UDS client + server, the DID poller fault handling and Ç1 CAN error state machine done (rt-core v0.6.0) · safety architecture decided (D-041..D-045) · ISSUES groups 1-4, D-2, E-1, E-4, E-5, E-7..E-9, E-10 (rt-core) and C-6..C-8 done · defs v0.3.3
**Last updated:** 2026-10-02

## Where we are

- 11 platform repos + `moto-workspace`, public (D-033), MIT (D-036). Decisions D-001..D-054. D-030 awaits confirmation except its bus-off latch (confirmed for rt-core in D-054).
- **Releases (all pinned in `manifest.yaml`):** defs v0.3.3, rt-core v0.6.0, conn/mobile/server v0.1.0. defs v0.3.3 (2026-10-02, defs#30, 7d121b6) = D-053. rt-core v0.6.0 (2026-10-02, rt-core#19, e9beb90) = Ç1 on defs v0.3.3. defs#31 (D-054) is docs only, no tag. conn `main` pins defs v0.3.0 (conn#8, no conn release yet). Nothing unreleased in defs or rt-core.
- **Ç1 done (2026-10-02, D-054), rt-core#19:** `services/can_sm` (pure core + glue): error active/passive/bus-off per port, a bus-off aborts pending TX and counts once (ISR counter + flag credit), recovery after 1, 2, 4 … 30 s (gen/ backoff), no recovery while a frame is pending, N_As 1000 ms abort → `ISOTP_N_TIMEOUT_A` in the links. Vehicle port latches on its 5th bus-off since boot (RAM; persistence with the board); platform port never latches (same backoff, local provisional). `can_if`: bus-off/latched → `CAN_PORT_ERR_IO`, never a guard refusal; `can_if_apply_filters()` (platform UDS IDs → FIFO1). `app/comms` = client before server. H7 FDCAN requirements table in `src/hal/README.md` (FDCAN2: dedicated replace-on-new buffers for the safety range + Tx FIFO). +1.45 KB flash, +183 B RAM. architecture-guard no blocker, vss CLEAN, safety-reviewer no blocker (MAJOR-1..3 + MINORs applied, delta review nothing MAJOR).
- **DID poller fault handling (D-050..D-053):** a timed-out or slow DID competes as normal with no 0x78 extension until it answers in time or is skipped (D-050, D-051); samples stamped with the oldest unanswered read (D-051); slow answers keep the skip count, `poll_period_ms` ≥ base timeout (D-052); and ≥ base + step S (D-053), so an answer seen one step late is in time and its DID not yet due.
- **E-10 done for rt-core (2026-10-02), rt-core#18:** `stats.step_overruns` / `step_gap_max_ms` (SIL summary only). E-11 (1) decided in D-054: a new rt-core health DID (step counters + CAN state); not done yet.
- **E-6 (1)-(4) done:** rt-core#14 (`not_sent` restores session/TP/read schedules and is not counted, 10 ms step test, +4 B RAM; delta review no blocker), defs#21 (bool timing values refused).
- **Group 3 done (2026-10-01):** C-5 `setup.sh`, C-3 safety-reviewer sync, C-2 blocking `make misra` on defs `gen/c` (register `misra/README.md`, DEV-001..005) and blocking cppcheck in conn. rt-core#11 merged.
- **Group 4 done (2026-10-01), conn#8 (C-1):** defs v0.3.0, gen/ `uds_iso14229.h` (conn's own header removed; ISO-TP transport constants in `src/IsoTpCan.h`), foreign-tester watch IDs from `vehicle_cl250_functional_watch[]`. conn's 29-bit watch matches any SA; rt-core's matches 0x18DB33F1 exactly. Vehicle-bus behaviour unchanged.
- **cppcheck is pinned to 2.22.0 in CI** (built from the tag and cached; runner ubuntu-24.04) in defs, conn and rt-core. Ubuntu's apt 2.13 misses findings (15.6 on the canary).
- **C-6/C-7 (2026-10-01), defs#18, released in v0.3.1:** the gate is single-exit with a fail-closed `bool ok = false`; `test_gate_equivalence.py` proves it equal to the old gate (every byte the request/frame gates read, -O0/-O2). DEV-005 and the gate part of DEV-004 are gone; `make misra` clean. safety-reviewer follow-ups are ISSUES C-9.
- **Branch protection on `main` (D-049, C-8, 2026-10-01)** in all 12 repos: PR required (0 approvals), admin bypass on, no force push or deletion. Required checks (strict, github-actions): defs `check`, conn/rt-core `build-and-test`, server `test`, mobile `flutter` + `build-apk`; the other 7 repos (workspace included) have the PR rule only. **No direct pushes to `main`; every change, STATUS included, goes through a PR.** A new repo's first CI workflow must also add its job as a required check.
- **`ISSUES.md`:** sections A-E; read only the group you work on. Open: C-4 (user), C-9, D-3..D-6, E-3, E-6 (5)/(6), E-10 (conn part), E-11, E-12, B-9.
- **Vehicle bus unchanged:** one read-only tester (D-037); tester_policy and the golden D-020 copy are untouched. Start sessions from the workspace root.

## Next up (in order)

1. **rt-core health DID** (ISSUES E-11 (1) + E-12 (1), D-054 item 8): `/signal-change` in defs (new platform DID: `step_overruns`, `step_gap_max_ms`, per-port CAN state, bus-offs, recoveries/deferred, N_As aborts, vehicle latch; maybe a DTC "vehicle bus-off latched"), defs minor + safety-reviewer, then rt-core provider in `uds_server` and the defs bump.
2. **Platform-bus republisher** of `vehicle_signals`: NONE/STALE become INVALID, and 0x021 clamps to 255 km/h (D-048). Uses `comms_pass()` order and the FDCAN2 TX rules of `src/hal/README.md` (safety range in dedicated replace-on-new buffers).
3. **Optional:** bump conn's defs submodule to v0.3.3 (E-10 conn part), then a conn release (D-036). Small defs docs PR: align D-053 item 5's S wording with the yaml (E-11 (2)).
4. **Hardware-dependent (group 6), with E-6 (5)/(6) and E-12 (2)/(3):**
   - Board (Q-019) → CubeMX, the FDCAN port of `hal/can_port.h` per the hal README table, bus-off count in no-init RAM
   - D-029 bench: ECU round trip + target step period/jitter (`stats.step_gap_max_ms`) → `assumed_round_trip_ms`, `client_step_max_ms`; CL250 reaction to a new 0x22 after 0x78 (D-050)
   - HIL: the uds README fault scenarios, plus `fdcan_bus_off_count_edges`, `fdcan2_txqueue_same_id_order`, `platform_stall_no_stale_e2e`, `vehicle_bus_off_recovery_session`, TX cancel with CCCR.INIT = 1
   - A-4 polling budget + PID check in the Q-001 probe (0x7DF and 0x18DB33xx); A-5 and E-3 BOM; ESP32 + APK end to end

## Blockers / pending decisions

- Q-019 (board) blocks CubeMX, Renode and Ç6. Q-009 blocks the hil-bench host. Q-020 is deferred (D-037).
- Before safety-node Layer 1 code: Q-023 (fallback details) and Q-026 (LED ring owner), both with the Group 7 hardware. Q-022 comes after fallback validation (k_red ≤ 0.8 until then).
- **User:** C-4: turn off the old `can-dbc-conventions` skill on claude.ai (still active on 2026-10-01).
- Q-024 (voice path, ESP32 PSRAM, wake-word default), Q-025 (vibration features). D-030 awaits confirmation. Q-017; Q-014/Q-015 provisional. Q-016, Q-001, Q-003, Q-004, Q-006.

## Recent sessions

- 2026-10-02 (local, Ç1 / D-054): user chose platform no latch + same backoff, latch in RAM now (persistent with the board), E-11 (1) = new health DID. rt-core#19 (`services/can_sm`, N_As, filters, `app/comms`) → v0.6.0 (e9beb90), defs#31 (D-054), pinned in `manifest.yaml`. architecture-guard no blocker, vss CLEAN, safety-reviewer no blocker (MAJOR-1..3 applied). Worktree prune asked at the end of the session.
- 2026-10-02 (local, releases + E-10): defs#30 → defs v0.3.3 (7d121b6); rt-core#18 (defs v0.3.3, step-gap counter, tests at S, README re-measured) → rt-core v0.5.1 (9af2a5d); both pinned in `manifest.yaml`. vss CLEAN, safety-reviewer no blocker/MAJOR (NITs applied, MINOR-1/2 → E-11). No worktree to prune at start.
- 2026-10-02 (local, E-9 / D-053): user chose (b), step 10 ms, speed stale 300. defs#28 (rule, 110 ms periods, B + S fault hold, round trip > step check) + defs#29 (D-053); vss CLEAN, safety-reviewer no blocker/MAJOR (MINOR-1/2, NITs applied; rt-core/conn items → E-10). Pruned e8-handoff.
- 2026-10-02 (local, releases): defs#27 → defs v0.3.2 (f744511); rt-core#17 → rt-core v0.5.0 (5ed2f2d): defs pin v0.3.2, v0.3.1 slow-RPM test deleted, period rule asserted, uds README re-measured; no module assumes 20 Hz RPM (anomaly-safety-net not written yet; docs say RPM 10-20 Hz; hardware-architecture's "20 Hz is enough for display" is a UX note for the HMI). vss CLEAN. Both pinned in `manifest.yaml`.
- 2026-10-01 (local, E-8 / D-052): user chose (1) c, (2) b, (3) a (kept after the measured 28.1 % cost), (4) HIL. defs#25 and rt-core#16 merged by the user; defs#26 went out of date, was updated with main and merged; vss CLEAN, safety-reviewer no blocker/MAJOR (MINOR-1/4 applied, MINOR-2 → E-9). ISSUES: E-8 done, E-6 (6) scenarios, E-9 opened.
