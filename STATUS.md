# STATUS — session handoff

> Keep it short (≤60 lines). Updated by the `/handoff` skill. "Recent sessions" keeps at most 5 one-line entries; drop the oldest.

**Phase:** 1 data pipeline done in code (bench test pending) · 2 rt-core without hardware: ISO-TP, host layer and **Ç3 done: UDS client + UDS server**; Ç1 CAN error handling next
**Last updated:** 2026-09-30

## Where we are

- 11 platform repos + `moto-workspace`, public (D-033), MIT (D-036). Decisions D-001..D-040. D-030 awaits confirmation.
- **Releases (manifest pinned):** defs **v0.2.0**, rt-core **v0.3.0** (the Ç3 client); conn, mobile and server v0.1.0. rt-core `main` also has the Ç3 server, **not tagged yet**.
- **defs v0.2.0 (defs#10, D-040):** `uds_iso14229.h` (conn gets only the D-020 client subset); the RT_CORE server contract `platform_uds.{h,c}`; Q-021 resolved with watch-only OBD functional IDs 0x7DF and 0x18DB33F1.
- **rt-core Ç3 UDS server (rt-core#9, merged):**
  - `features/uds/uds_server` + `_core` on the platform bus only (0x710/0x718, functional 0x7DF), and `services/diag`.
  - Services: 0x10 / 0x3E / 0x22 / 0x19 / 0x14 (extended only), with NRCs, 0x78/P2*, S3.
  - DIDs 0xF186, 0xF189, 0xFD00, 0xFD01, 0xFD10-14; DTCs U0100-00 and U3000-00 (RAM, level-triggered).
  - The vehicle-tester status is fail-safe (NOT_RUNNING when missing or stale).
  - The client watches the functional IDs and reports to diag. The temporary `uds_iso14229.h` is gone.
- **Checks:** ctest 13/13 incl. SIL `--uds-scenario` (13 steps, P2 2 ms / 50 ms); coverage 97.4 % / 90.7 %; MISRA clean; M7: server 468 B RAM, about 2.7 kB flash.
- **Reviews:** architecture-guard OK; vss-schema-guardian CLEAN; safety-reviewer ×2 with no blocker, MAJOR-1 fixed. The rest are recorded in the uds README → "Reviews of the UDS server".
- **Vehicle bus unchanged:** one read-only tester (D-037), gates byte-identical, Q-020 deferred. Start sessions from the workspace root.

## Next up (in order)

1. **rt-core v0.4.0 (the Ç3 server):** `project(VERSION 0.4.0)` PR, merge when green, `gh release create v0.4.0 -R moto-platform/moto-rt-core --target main --title v0.4.0 --generate-notes`, then pin the tag in `manifest.yaml`.
2. **rt-core Ç1, CAN error state machine + H7 HAL requirements** (`/feature-module moto-rt-core can`, then architecture-guard and safety-reviewer):
   - bus-off recovery (`VEHICLE_CL250_BUS_OFF_BACKOFF_*`), error counters, N_As
   - FDCAN1 filters that pass the vehicle request IDs and the functional watch IDs; FDCAN2 filters for 0x710/0x7DF
   - FDCAN2 in Tx-Queue (priority) mode, and 0x7xx routed to FIFO1 (safety review MINOR-4)
   - one comms task, with the client step before the server step (MINOR-3/C)
3. **Platform-bus republisher** of `vehicle_signals`: NONE/STALE become INVALID, and speed is E2E-protected to safety-node (D-021).
4. **Consumers of defs v0.2.0:** conn (bump if its tester latch should also watch `vehicle_cl250_functional_watch[]`) and hil-bench (gets `uds_iso14229.h`); then run `vss-schema-guardian`.
5. **Before the first rt-core ride:** the Q-001 listen-only probe must include 0x7DF and 0x18DB33F1 (D-040 item 7).
6. **Standards:** a MISRA step for defs `gen/c`; per-repo hooks for the safety rules; Q-006 (requirements, Ç8); 0x27 before a flash-backed DTC memory or any write/programming service (D-040).
7. **Workshop / hardware / small:**
   - ESP32 + APK end to end; connectivity#3 bench checks
   - the OBD chain; the D-029 measurements
   - the hil-bench live model (D-035) and the HIL scenarios from the uds README
   - BLE latch wording; server `session_id` + unzip cap; tag the skeleton repos

## Blockers / pending decisions

- Q-019 (board) blocks CubeMX, Renode and Ç6. Q-009 blocks the hil-bench host. Q-020 is deferred (D-037).
- D-030 awaits confirmation. Q-017; Q-014/Q-015 are provisional (D-029). Q-002, Q-016, Q-001, Q-003, Q-004, Q-006.

## Recent sessions

- 2026-09-30 (local, Ç3 server): rt-core v0.3.0 released + pinned; defs v0.2.0 (defs#10: ISO codes in gen/, server contract, Q-021 → D-040) released + pinned; rt-core#9 UDS server + diag + functional watch merged; arch-guard, vss CLEAN, safety-reviewer ×2 (MAJOR-1 fixed).
- 2026-09-29/30 (local, rt-core Ç3 client): pre-checks + prune; UDS client + vehicle_signals (rt-core#5, #6 merged); D-039 + Q-021; vss ×2, safety-reviewer ×2 (all MAJORs fixed).
- 2026-09-29 (local, consistency pass): rt-core v0.2.0 released; worktree lifecycle script (ws#7); 3-way audit; D-037 read-only vehicle tester, D-038 tr archive; rules single-sourced + synced to 11 repos; rt-core blocking MISRA + coverage; Q-020 deferred.
- 2026-09-28 (local, rt-core glue): v0.1.0 releases for conn/mobile/server/rt-core, manifest pinned; rt-core#2 host layer + ISO-TP link + can_if D-020 guard + SIL; Q-020 (defs#6).
- 2026-09-28 (local): Q-018 hardening (connectivity#3) merged; D-032 confirmed (defs#4); server#1 merged; rt-core bootstrapped + ISO-TP core (rt-core#1); D-034 proposed, Q-018 closed (defs#5).
