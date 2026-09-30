# STATUS — session handoff

> Keep it short (≤60 lines). Updated by the `/handoff` skill. "Recent sessions" keeps at most 5 one-line entries; drop the oldest.

**Phase:** 1 data pipeline done in code (bench test pending) · 2 rt-core without hardware: ISO-TP, host layer and the **Ç3 UDS client done**; Ç3 UDS server next
**Last updated:** 2026-09-30

## Where we are

- 11 platform repos + `moto-workspace`, public (D-033), MIT (D-036). Decisions D-001..D-039 (D-039: defs#9). D-030 awaits confirmation.
- **Releases:** rt-core v0.2.0 (manifest pinned); defs, conn, mobile, server v0.1.0. rt-core `main` also has the Ç3 UDS client, **not tagged yet**.
- **rt-core Ç3 UDS client merged** (rt-core#5 + #6, D-039):
  - Modules: `features/uds/uds_client` + `_core`, `services/vehicle_signals`, the temporary `uds_iso14229.h`.
  - Session: 0x10 03 with retry, 0x3E 80 every period.
  - Polling: round-robin over the gen/ DIDs, 0x78 extension under a total cap, skip cooldown, ECU-absent timeout.
  - Q-020: a failed reception means "unavailable", then a hold of N_Bs.
  - Fail-closed latch with a reason: gate, guard, or a second tester. STALE stays sticky.
- **Checks:** 57 new tests including SIL end to end; coverage 98.2 % / 90.0 %; about 2 kB flash on the M7.
- **Reviews:** vss-schema-guardian CLEAN; safety-reviewer ×2, no blocker, every MAJOR fixed. The remaining MINORs are in the uds README → "Reviews".
- **Vehicle bus:** one read-only tester (D-037); Q-020 deferred. connectivity-node's poller must be off while rt-core polls (D-021).
- **Start sessions from the workspace root** (a session started in defs does not get `safety-reviewer`). Q-019 (board) is still open.

## Next up (in order)

1. **User:** merge defs#9 (D-039/Q-021), rt-core#7 (README) and this STATUS PR. Then `python3 scripts/worktrees.py --prune`.
2. **rt-core v0.3.0:**
   - bump `project(VERSION 0.3.0)` in a PR, merge when CI is green
   - `gh release create v0.3.0 -R moto-platform/moto-rt-core --target main --title v0.3.0 --generate-notes`
   - pin the tag in `manifest.yaml` (D-036)
3. **rt-core Ç3, UDS server (platform bus):**
   - first `/signal-change` for the server IDs and own DIDs/DTCs (`uds/dids.yaml`, `platform.dbc`), then tag defs
   - then `/feature-module moto-rt-core uds`: 0x10 / 0x3E / 0x22 / 0x19 / 0x14, NRCs, P2 / P2* / S3
   - reviews: architecture-guard, safety-reviewer, vss-schema-guardian
4. **defs `/signal-change`** (can share the release from step 3):
   - the ISO 14229 codes (0x22, 0x7F, 0x78, 0x7E) into gen/, then delete `uds_iso14229.h` (D-039)
   - decide Q-021
5. **rt-core Ç1, CAN error state machine:**
   - bus-off recovery (`VEHICLE_CL250_BUS_OFF_BACKOFF_*`), error counters, N_As
   - FDCAN filters that pass both request IDs
   - host tests
6. **Platform-bus republisher** of `vehicle_signals`: NONE/STALE become INVALID; speed E2E-protected to safety-node (D-021).
7. **Standards:** a MISRA step for defs `gen/c`; per-repo hooks for the safety rules; Q-006 (requirements, Ç8).
8. **Workshop / hardware / small:** ESP32 + APK end to end, connectivity#3 bench checks, the OBD chain, D-029 measurements, hil-bench live model (D-035), BLE latch wording, server `session_id` + unzip cap, tag the skeleton repos.

## Blockers / pending decisions

- Q-019 (board) blocks CubeMX, Renode and Ç6. Q-009 blocks the hil-bench host. Q-020 deferred (D-037). Q-021 open.
- D-030 awaits confirmation. Q-017; Q-014/Q-015 provisional (D-029). Q-002, Q-016, Q-001, Q-003, Q-004, Q-006.

## Recent sessions

- 2026-09-29/30 (local, rt-core Ç3 client): pre-checks + prune; UDS client + vehicle_signals (rt-core#5, #6 merged); D-039 + Q-021; vss ×2, safety-reviewer ×2 (all MAJORs fixed).
- 2026-09-29 (local, consistency pass): rt-core v0.2.0 released; worktree lifecycle script (ws#7); 3-way audit (docs, Claude setup, code standards); D-037 read-only vehicle tester, D-038 tr archive; rules single-sourced + synced to 11 repos; rt-core blocking MISRA + coverage; Q-020 deferred.
- 2026-09-28 (local, rt-core glue): v0.1.0 releases for conn/mobile/server/rt-core, manifest pinned; rt-core#2 host layer + ISO-TP link + can_if D-020 guard + SIL (safety-review blocker fixed); Q-020 (defs#6).
- 2026-09-28 (local): Q-018 hardening (connectivity#3, 2 safety-review rounds) merged; D-032 confirmed (defs#4); repo secrets set, server#1 merged; APK downloaded; rt-core bootstrapped + ISO-TP core (rt-core#1); D-034 proposed, Q-018 closed (defs#5).
- 2026-09-27 (local, cont.): merged connectivity#2, mobile#4 (BLE v3, IMU, upload), defs#3 (D-032, Q-017/Q-018), workspace#3; moto-server#1 waited for the secret; repos made public (D-033, history scanned clean).
