# STATUS — session handoff

> Keep it short (≤60 lines). Updated by the `/handoff` skill. "Recent sessions" keeps at most 5 one-line entries; drop the oldest.

**Phase:** 1 data pipeline done in code (bench test pending) · 2 rt-core without hardware: ISO-TP, host layer, Ç3 UDS client + server, DID poller fault handling, Ç1 CAN error state machine, health DID and the platform-bus republisher done (rt-core v0.8.0) · safety architecture decided (D-041..D-045) · ISSUES groups 1-4, D-2, D-5, E-1, E-4, E-5, E-7..E-9, E-10, E-11, E-12 (1), E-13 (1), E-14 (1)/(2)/(6) and C-6..C-8 done · defs v0.5.1
**Last updated:** 2026-10-03

## Where we are

- 11 platform repos + `moto-workspace`, public (D-033), MIT (D-036). Decisions D-001..D-056. D-030 awaits confirmation except its bus-off latch (confirmed for rt-core in D-054).
- **Releases (all pinned in `manifest.yaml`):** defs v0.5.1, rt-core v0.8.0, conn/mobile/server v0.1.0. defs v0.5.1 (2026-10-03, defs#34, f211781) = comment/docs patch on v0.5.0 (D-056 encoders). rt-core v0.8.0 (f51b214) = republisher, pins defs v0.5.0 (v0.5.1 differs in gen/ comments only; take it at the next rt-core defs bump). conn `main` pins defs v0.5.1 (conn#9, 03b9b99); no conn release (conn has no build-file version for D-036). Nothing unreleased in defs or rt-core.
- **Republisher done (2026-10-03, D-056, ISSUES D-5):**
  - defs: cantools' C `*_encode()` truncated while Python rounds (0x110 BATTERY_VOLTAGE lost 1 LSB on 38863/65536 values). codegen now rounds, saturates at the C type and maps NaN to 0. C-7 checks every raw value up to 16 bits.
  - rt-core#22: FDCAN2 dedicated replace-on-new TX buffers (`can_if_register_tx_dedicated()` → `can_port_set_tx_dedicated()`; a replace returns TX_FULL and is never an N_As abort) and one Tx FIFO element at a time (M_CAN erratum "Tx FIFO message sequence inversion").
  - rt-core#23: `features/vehicle_republish` sends 0x021 (E2E, dedicated buffer) and 0x110 (FIFO) every 50 ms in `comms_pass()` after the platform dispatch, before the UDS server. INVALID means value 0 and AGE 2550, with no clamping. The counter advances only on accepted frames. A refused open sends nothing. The SIL listener checks E2E (40/40 in 2 s).
  - +936 B text, bss unchanged.
  - Reviews: architecture-guard no blocker, vss CLEAN, safety-reviewer no blocker ×3 (MAJORs applied; leftovers in E-14).
- **Health DID (D-055), Ç1 (D-054), DID poller fault handling (D-050..D-053):** done in v0.6.0/v0.7.0; step counters on 0xFD02, H7 FDCAN requirements in `src/hal/README.md`.
- **cppcheck 2.22.0 in CI** (defs, conn, rt-core); MISRA and coverage floors blocking (D-046). **Branch protection on `main` (D-049)** in all 12 repos: every change, STATUS included, goes through a PR.
- **defs patch + conn bump (2026-10-03):** v0.5.1 = 0x021 `VEHICLE_SPEED_AGE` comment (D-051 stamp, one-write buffer wait, consumer worst case ~351 ms), no saturation note on STATE `*_MAX`, D-053 item 5 / D-054 item 6 / D-056 item 6 wording (one Tx FIFO element, ST errata with Q-019). conn#9: tests derive timing from gen/; README records that its `loop()` step is unbounded vs S = 10 ms (residual, G0.1 report).
- **`ISSUES.md`:** sections A-E; read only the group you work on. Open: C-4 (user), C-9, D-3, D-4, D-6, E-3, E-6 (5)/(6), E-10 (EKF stamps), E-12 (2)-(4), E-13 (2)/(3), E-14 (3)-(5), B-9.
- **Vehicle bus unchanged:** one read-only tester (D-037); tester_policy and the golden D-020 copy untouched. Start sessions from the workspace root.

## Next up (in order)

1. **User decision, then the next rt-core feature without hardware:** heartbeat 0x081 (recommended: watchdog/heartbeat, `/feature-module` + safety-reviewer; reuse the dedicated TX API, extract `services/com` with the second E2E sender, D-056 item 7) or the EKF lean (0x020/0x022) in its own 20 ms task (not in the comms pass, CLAUDE.md rule 4). The trade-off (AUTOSAR E2E, ISO 26262 FFI, memory) was given on 2026-10-03; record the choice as D-057.
2. **Optional:** a conn release needs a build-file version first (D-036; conn has none); rt-core takes defs v0.5.1 at its next defs bump.
3. **Hardware-dependent (group 6), with E-6 (5)/(6), E-12 (2)/(3), E-13 (2), E-14 (3):**
   - Board (Q-019) → CubeMX, the FDCAN port of `hal/can_port.h` per the hal README table (dedicated buffers, one FIFO element, ST errata check), bus-off count in no-init RAM
   - D-029 bench: ECU round trip + target step period/jitter (0xFD02 `STEP_GAP_MAX_MS`) → `assumed_round_trip_ms`, `client_step_max_ms`; CL250 reaction to a new 0x22 after 0x78 (D-050)
   - HIL: the uds README fault scenarios, `uds_server_health_*`, the FDCAN/dedicated-buffer and republisher scenarios (E-14 (3))
   - A-4 polling budget + PID check in the Q-001 probe (0x7DF and 0x18DB33xx); A-5 and E-3 BOM; ESP32 + APK end to end

## Blockers / pending decisions

- Q-019 (board) blocks CubeMX, Renode and Ç6. Q-009 blocks the hil-bench host. Q-020 is deferred (D-037).
- Before safety-node Layer 1 code: Q-023 (fallback details) and Q-026 (LED ring owner), both with the Group 7 hardware. Q-022 comes after fallback validation (k_red ≤ 0.8 until then).
- **User:** C-4: turn off the old `can-dbc-conventions` skill on claude.ai (still active on 2026-10-01).
- Q-024 (voice path, ESP32 PSRAM, wake-word default), Q-025 (vibration features). D-030 awaits confirmation. Q-017; Q-014/Q-015 provisional. Q-016, Q-001, Q-003, Q-004, Q-006.

## Recent sessions

- 2026-10-03 (local, defs patch + conn bump): user away, recommended options taken. defs#34 → defs v0.5.1 (f211781, PATCH: gen/ comments only), conn#9 → defs v0.5.1 (03b9b99), manifest pinned. vss CLEAN ×2; no safety-reviewer (no safety module, codegen E2E/encode paths untouched). Prune of 4 old worktrees denied by auto mode (user to run). Next-up 3 choice asked.
- 2026-10-03 (local, republisher / D-056): user chose defs rounding first, PR-A + PR-B, INVALID = value 0 + AGE 2550 (no clamp). defs#33 → defs v0.5.0 (db2feec); rt-core#22 + #23 → rt-core v0.8.0 (f51b214); both pinned. Pruned 4 worktrees at start. architecture-guard no blocker, vss CLEAN, safety-reviewer no blocker ×3 (MAJORs applied; erratum found; follow-ups E-14).
- 2026-10-02 (local, health DID / D-055): user chose the 23 B u16 layout and DTC U0001-88 while latched. defs#32 → defs v0.4.0 (866d8be), rt-core#20 → rt-core v0.7.0 (1369d8a), both pinned in `manifest.yaml`. architecture-guard no blocker, vss CLEAN ×2, safety-reviewer no blocker ×2 (follow-ups E-13).
- 2026-10-02 (local, Ç1 / D-054): user chose platform no latch + same backoff, latch in RAM now, E-11 (1) = new health DID. rt-core#19 → v0.6.0 (e9beb90), defs#31 (D-054), pinned. architecture-guard no blocker, vss CLEAN, safety-reviewer no blocker (MAJOR-1..3 applied).
- 2026-10-02 (local, releases + E-10): defs#30 → defs v0.3.3 (7d121b6); rt-core#18 → rt-core v0.5.1 (9af2a5d); both pinned. vss CLEAN, safety-reviewer no blocker/MAJOR (MINOR-1/2 → E-11).
