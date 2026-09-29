# STATUS — session handoff

> Keep it short (≤60 lines). Updated by the `/handoff` skill. "Recent sessions" keeps at most 5 one-line entries; drop the oldest.

**Phase:** 1 data pipeline done in code (bench test pending) · 2 rt-core without hardware: ISO-TP core + host platform layer/glue (Ç2)
**Last updated:** 2026-09-29

## Where we are

- 11 repos + `moto-workspace`, public (D-033), MIT (D-036). Decisions D-001..D-036. D-030 is still a Claude proposal awaiting confirmation.
- **Releases v0.1.0:** defs (`acef075`), rt-core (`9ea9ab9`), connectivity-node, mobile and server. `manifest.yaml` pins these five tags. The other six repos are skeletons with no tag and stay on `main`.
- **rt-core#2 merged** (`05b5efe`, D-034 host layer + ISO-TP glue; not tagged yet):
  - `hal/can_types.h`, `can_port.h`, `hal_time.h`
  - `hal/host`: in-process vbus, SocketCAN, and a monotonic or manual ms clock
  - `services/timebase` and `services/can_if` (RX routing + a **fixed, fail-closed D-020 vehicle-bus guard**)
  - `features/uds/isotp_link`: `isotp_link_open_vehicle_cl250()` is the only vehicle link and takes its IDs and padding from gen/
  - the `moto_rtcore_host` SIL program with a simulated CL250 ECU (or `--vcan`)
  - 63 Unity tests + SocketCAN test (runs in CI on `vcan0`) + SIL smoke run; CI layering checks
  - The new firmware code is ~1.2 kB flash, 176 B RAM.
  - safety-reviewer: the blocker (opt-in gates) is fixed and the re-review is clean. vss-schema-guardian: clean.
- **defs#6 merged:** Q-020 (vehicle-bus Flow Control) is recorded as an open question, docs only (no tag). Workspace#5 merged (manifest pins + this STATUS).
- The H7 board (Q-019) is still open, so there is no CubeMX project, startup code or linker script. `HondaCl250_Telemetry` untouched.

## Next up (in order)

1. **rt-core v0.2.0:** bump `project(VERSION 0.2.0)` in rt-core (PR, CI green), then `gh release create v0.2.0 -R moto-platform/moto-rt-core --target main --generate-notes`, then pin `manifest.yaml` to `v0.2.0` (D-036).
2. **User decision Q-020:** allow a byte-exact FC.CTS on the vehicle bus?
   - Without it, 0x19 (several DTCs) and 0x09 (VIN) cannot work.
   - If yes: `/signal-change` in defs (gate + tests, tag), then the rt-core link-state check, then the safety-reviewer.
3. **rt-core Ç3, UDS client (vehicle poller) on `isotp_link`:**
   - D-020 session handling: 0x10 03, 0x3E 80.
   - Round-robin over the gen/ DIDs with poll/stale periods, one request in flight.
   - Treat `N_TIMEOUT_CR` as "unavailable" and use the skip cooldown (uds README conditions).
   - `/feature-module moto-rt-core uds` + safety-reviewer.
4. **rt-core Ç3, UDS server (platform bus):**
   - Server IDs and own DIDs first via `/signal-change` (`uds/dids.yaml`, platform.dbc).
   - Then 0x10 / 0x3E / 0x22 / 0x19 / 0x14, NRCs, P2 / P2* / S3.
5. **rt-core Ç1, CAN error state machine** behind `hal/can_port` (bus-off recovery, error counters), host tests.
6. **Workshop (ESP32 on USB):** flash the mock env + install the APK, BLE → recording → upload end-to-end; connectivity#3 bench checks (TX at boot/mode switch, reset reasons, TXD pull-up, ignition power).
7. **Small follow-ups:** BLE latch wording (3 repos); moto-server `session_id` validation + unzip cap; connectivity CI anonymous defs clone; swap rt-core `app/host/sim_ecu` for the hil-bench live model (D-035) when it exists.
8. **Hardware / measurement:** OBD chain (6-pin → Honda adapter → OBD2 pigtail → ESP); mass, weight split, rolling radius, tire pressures → replace the D-029 provisional values.
9. **Skeleton repos:** tag `v0.1.0` when they get code:
   `for r in moto-safety-node moto-io-node moto-linux-node moto-hil-bench moto-ml moto-mcp; do gh release create v0.1.0 -R moto-platform/$r --target main --title v0.1.0 --generate-notes; done`

## Blockers / pending decisions

- Q-019 (board) blocks CubeMX, Renode and Ç6. Q-009 (first HIL test function) blocks the hil-bench host. Q-020 blocks multi-frame vehicle reads.
- D-030 awaits confirmation. Q-017 (BLE schema in defs codegen). Q-014/Q-015: provisional D-029 values until measured.
- Q-002, Q-016 remainder, Q-001 remainder, Q-003, Q-004 (bridge format), Q-006 (requirements location, needed for Ç8 traceability).

## Recent sessions

- 2026-09-28 (local, rt-core glue): v0.1.0 releases for conn/mobile/server/rt-core, manifest pinned; rt-core#2 host layer + ISO-TP link + can_if D-020 guard + SIL (safety-review blocker fixed); Q-020 (defs#6).
- 2026-09-28 (local): Q-018 hardening (connectivity#3, 2 safety-review rounds) merged; D-032 confirmed (defs#4); repo secrets set, server#1 merged; APK downloaded; rt-core bootstrapped + ISO-TP core (rt-core#1); D-034 proposed, Q-018 closed (defs#5).
- 2026-09-27 (local, cont.): merged connectivity#2, mobile#4 (BLE v3, IMU, upload), defs#3 (D-032, Q-017/Q-018), workspace#3; moto-server#1 waited for the secret; repos made public (D-033, history scanned clean).
- 2026-09-27 (cloud, data pipeline): BLE schema v3 + IMU blocks (conn#2, CI green), mobile v3/imu.csv/upload (mobile#4), moto-server bootstrap (server#1); D-032 proposed, Q-017/Q-018; guardians + safety review done.
- 2026-09-27 (local): moto-mobile#2/#3 and connectivity-node#1 merged; defs v0.1.0 tagged; ESP32 BLE 4.2 build fix; CI submodule fix + classic PAT (D-031); disk cleanup; APK downloaded. OBD adapter left at home.
