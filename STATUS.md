# STATUS — session handoff

> Keep it short (≤60 lines). Updated by the `/handoff` skill. "Recent sessions" keeps at most 5 one-line entries; drop the oldest.

**Phase:** 1 data pipeline done in code (bench test pending) · 2 rt-core without hardware: ISO-TP, host layer, Ç3 UDS client + server, the DID poller fault handling, Ç1 CAN error state machine and the health DID done (rt-core v0.7.0) · safety architecture decided (D-041..D-045) · ISSUES groups 1-4, D-2, E-1, E-4, E-5, E-7..E-9, E-10 (rt-core), E-11 (1), E-12 (1) and C-6..C-8 done · defs v0.4.0
**Last updated:** 2026-10-02

## Where we are

- 11 platform repos + `moto-workspace`, public (D-033), MIT (D-036). Decisions D-001..D-055. D-030 awaits confirmation except its bus-off latch (confirmed for rt-core in D-054).
- **Releases (all pinned in `manifest.yaml`):** defs v0.4.0, rt-core v0.7.0, conn/mobile/server v0.1.0. defs v0.4.0 (2026-10-02, defs#32, 866d8be) = D-055. rt-core v0.7.0 (2026-10-02, rt-core#20, 1369d8a) = the D-055 provider on defs v0.4.0. conn `main` pins defs v0.3.0 (conn#8, no conn release yet). Nothing unreleased in defs or rt-core.
- **Health DID done (2026-10-02, D-055):** defs: RT_CORE DID 0xFD02 `RT_CORE_HEALTH` (23 B: flags `STEP_STATS_FRESH` / `VEHICLE_LATCHED`, u16 `STEP_OVERRUNS` / `STEP_GAP_MAX_MS`, per port `STATE` u8 with UNKNOWN 0xFF + u16 bus-offs, recoveries, deferred recoveries, N_As aborts, big-endian, saturating) and DTC 0xC00188 U0001-88 `VEHICLE_BUS_OFF_LATCHED` (fails while latched, no report while UNKNOWN); codegen `record` encoding, refuses unknown field keys (found a YAML comma that had cut 0xFD00 FAULT's description). rt-core: `can_sm_state_known()`, diag step counters (sticky, wrap-safe freshness), provider + monitor in `uds_server`, SIL `--uds-scenario` 14/14. About +0.6 KB flash, +107 B RAM (`uds_server_t` 564 B: 0x22 buffers 57 → 101 B). architecture-guard no blocker, vss CLEAN (both), safety-reviewer no blocker on both PRs (defs MAJOR-1 = UNKNOWN state, applied; m1-m5, MINOR-1/2, NITs applied; leftovers in E-13).
- **Ç1 done (D-054), rt-core v0.6.0:** `services/can_sm` (bus-off backoff 1 → 30 s, vehicle latch on the 5th bus-off since boot in RAM, platform never latches), N_As 1000 ms, `can_if_apply_filters()`, `app/comms` (client before server). H7 FDCAN requirements in `src/hal/README.md`.
- **DID poller fault handling (D-050..D-053):** slow/timed-out DIDs compete as normal, oldest-unanswered stamps, `poll_period_ms` ≥ base timeout + step S; step counters now readable on 0xFD02.
- **cppcheck is pinned to 2.22.0 in CI** (built from the tag, cached; ubuntu-24.04) in defs, conn and rt-core; `make misra` blocking on defs `gen/c`.
- **Branch protection on `main` (D-049)** in all 12 repos: PR required, no force push. Required checks: defs `check`, conn/rt-core `build-and-test`, server `test`, mobile `flutter` + `build-apk`. **Every change, STATUS included, goes through a PR.**
- **`ISSUES.md`:** sections A-E; read only the group you work on. Open: C-4 (user), C-9, D-3..D-6, E-3, E-6 (5)/(6), E-10 (conn part), E-11 (2), E-12 (2)-(4), E-13, B-9.
- **Vehicle bus unchanged:** one read-only tester (D-037); tester_policy and the golden D-020 copy are untouched. Start sessions from the workspace root.

## Next up (in order)

1. **Platform-bus republisher** of `vehicle_signals` (ISSUES D-5, `/feature-module` in rt-core): NONE/STALE become INVALID, and 0x021 clamps to 255 km/h (D-048). Uses `comms_pass()` order and the FDCAN2 TX rules of `src/hal/README.md` (safety range in dedicated replace-on-new buffers); safety-reviewer (E2E).
2. **Optional small defs PR** (docs + codegen comment, patch or no tag): E-11 (2) align D-053 item 5's S wording with the yaml; E-13 (1) no "counters saturate" comment on a STATE `*_MAX`.
3. **Optional:** bump conn's defs submodule to v0.4.0 (E-10 conn part: its step and order against S), then a conn release (D-036).
4. **Hardware-dependent (group 6), with E-6 (5)/(6), E-12 (2)/(3) and E-13 (2):**
   - Board (Q-019) → CubeMX, the FDCAN port of `hal/can_port.h` per the hal README table, bus-off count in no-init RAM
   - D-029 bench: ECU round trip + target step period/jitter (now on 0xFD02 `STEP_GAP_MAX_MS`) → `assumed_round_trip_ms`, `client_step_max_ms`; CL250 reaction to a new 0x22 after 0x78 (D-050)
   - HIL: the uds README fault scenarios incl. `uds_server_health_*`, plus `fdcan_bus_off_count_edges`, `fdcan2_txqueue_same_id_order`, `platform_stall_no_stale_e2e`, `vehicle_bus_off_recovery_session`, TX cancel with CCCR.INIT = 1
   - A-4 polling budget + PID check in the Q-001 probe (0x7DF and 0x18DB33xx); A-5 and E-3 BOM; ESP32 + APK end to end

## Blockers / pending decisions

- Q-019 (board) blocks CubeMX, Renode and Ç6. Q-009 blocks the hil-bench host. Q-020 is deferred (D-037).
- Before safety-node Layer 1 code: Q-023 (fallback details) and Q-026 (LED ring owner), both with the Group 7 hardware. Q-022 comes after fallback validation (k_red ≤ 0.8 until then).
- **User:** C-4: turn off the old `can-dbc-conventions` skill on claude.ai (still active on 2026-10-01).
- Q-024 (voice path, ESP32 PSRAM, wake-word default), Q-025 (vibration features). D-030 awaits confirmation. Q-017; Q-014/Q-015 provisional. Q-016, Q-001, Q-003, Q-004, Q-006.

## Recent sessions

- 2026-10-02 (local, health DID / D-055): user chose the 23 B u16 layout and DTC U0001-88 while latched. defs#32 → defs v0.4.0 (866d8be), rt-core#20 → rt-core v0.7.0 (1369d8a), both pinned in `manifest.yaml`. architecture-guard no blocker, vss CLEAN ×2, safety-reviewer no blocker ×2 (defs MAJOR-1 UNKNOWN state applied; follow-ups E-13). No worktree to prune at start.
- 2026-10-02 (local, Ç1 / D-054): user chose platform no latch + same backoff, latch in RAM now (persistent with the board), E-11 (1) = new health DID. rt-core#19 (`services/can_sm`, N_As, filters, `app/comms`) → v0.6.0 (e9beb90), defs#31 (D-054), pinned in `manifest.yaml`. architecture-guard no blocker, vss CLEAN, safety-reviewer no blocker (MAJOR-1..3 applied).
- 2026-10-02 (local, releases + E-10): defs#30 → defs v0.3.3 (7d121b6); rt-core#18 (defs v0.3.3, step-gap counter, tests at S, README re-measured) → rt-core v0.5.1 (9af2a5d); both pinned in `manifest.yaml`. vss CLEAN, safety-reviewer no blocker/MAJOR (NITs applied, MINOR-1/2 → E-11).
- 2026-10-02 (local, E-9 / D-053): user chose (b), step 10 ms, speed stale 300. defs#28 (rule, 110 ms periods, B + S fault hold, round trip > step check) + defs#29 (D-053); vss CLEAN, safety-reviewer no blocker/MAJOR (MINOR-1/2, NITs applied; rt-core/conn items → E-10).
- 2026-10-02 (local, releases): defs#27 → defs v0.3.2 (f744511); rt-core#17 → rt-core v0.5.0 (5ed2f2d): defs pin v0.3.2, v0.3.1 slow-RPM test deleted, period rule asserted, uds README re-measured. vss CLEAN. Both pinned in `manifest.yaml`.
