# STATUS — session handoff

> Keep it short (≤60 lines). Updated by the `/handoff` skill. "Recent sessions" keeps at most 5 one-line entries; drop the oldest.

**Phase:** 1 data pipeline done in code (bench test pending) · 2 rt-core started without hardware (Ç2 ISO-TP)
**Last updated:** 2026-09-28

## Where we are

- 11 repos + `moto-workspace`, public (D-033). Decisions D-001..D-034. D-030 and D-034 are Claude proposals waiting for user confirmation; D-032 is confirmed.
- **Data pipeline merged:** connectivity#2, mobile#4 and server#1 (BLE v3 + 100 Hz IMU → app → `POST /sessions` → re-decode, Parquet, SQLite). Repo secrets `MOTO_DEFS_TOKEN` / `MOTO_CONN_READ_TOKEN` are set on server and mobile (org secrets did not reach the repos). APK: `~/Desktop/moto-apk/app-release.apk` (`102d5a1`).
- **Q-018 done (connectivity#3 merged):** latch + bus-off budget persist across resets (RTC no-init + CRC, fail-safe; only power-on clears them); ≥2 s listen-only before the first request; RX drained before any TX or timeout check. safety-reviewer: all findings fixed.
- **moto-rt-core#1 open, CI green:** CMake presets `host-tests` (Unity, ASan/UBSan) and `target-m7-*` (Cortex-M7, no board yet), defs `v0.1.0`; ISO-TP core `features/uds/isotp_core` (34 tests, 1220 B flash, 0 B RAM). Recorded as D-034 in defs#5 (open).
- The H7 board (H743 vs H723) is not chosen, so there is no CubeMX project, startup code or linker script yet.
- defs `main` is `v0.1.0` + docs commits. No schema changes since the tag. `HondaCl250_Telemetry` untouched.

## Next up (in order)

1. **User:** review and merge rt-core#1 and defs#5. Confirm or amend D-034 (and D-030).
2. **rt-core, ISO-TP glue** (`/feature-module moto-rt-core uds`):
   - a HAL-free CAN port interface plus a `services/` timebase
   - one link per (req, resp) ID, the vehicle link using the gen/ padding byte
   - mock-bus tests
3. **rt-core Ç3, UDS server core** (platform bus): 0x10 / 0x3E / 0x22 / 0x19 / 0x14 state machine, NRC handling, session timing (P2 / P2*, S3).
   - The server request/response IDs and own DIDs must first go through `/signal-change` in defs (`uds/dids.yaml`, platform.dbc).
   - Then `/feature-module`.
4. **rt-core Ç1, CAN error state machine** behind the HAL interface (bus-off recovery, error counters), host tests.
5. **Workshop:** with the ESP32 on USB:
   - flash the mock env (`pio run -e esp32-s3-devkitc-1-mock -t upload`)
   - install the APK
   - test BLE → recording → export → upload end-to-end
   - bench checks from connectivity#3: scope TX during boot and the mode switch; reset reasons (esp_restart, WDT, EN, USB); TXD pull-up; is the node on ignition-switched power?
6. **Follow-ups (small):**
   - BLE schema wording for latch semantics, in 3 repos together (both flags = cause unknown; "until power-on").
   - moto-server: validate `session_id` in `GET /sessions/{id}/report`; cap the unzipped size.
   - connectivity CI: switch to the anonymous public defs clone like rt-core (D-033).
7. **Hardware / measurement:**
   - OBD chain: CL250 6-pin → Honda adapter → OBD2 pigtail → ESP, with continuity test and strain relief.
   - Mass, weight split, rolling radius and tire pressures → replace the D-029 provisional values.
8. **Decisions needed:**
   - license (repos are public with no LICENSE)
   - H7 board (unblocks CubeMX + Renode L1)
   - Q-009 HIL realism level (unblocks the moto-hil-bench host)

## Blockers / pending decisions

- The board choice (H743/H723) blocks CubeMX, Renode and Ç6. Q-009 blocks the hil-bench host. The license is undecided.
- D-030 and D-034 await confirmation. Q-017 (BLE schema in defs codegen). Q-014/Q-015: provisional D-029 values until measured.
- Q-002, Q-016 remainder, Q-001 remainder, Q-003, Q-004 (bridge format), Q-006 (requirements location, needed for Ç8 traceability).

## Recent sessions

- 2026-09-28 (local): Q-018 hardening (connectivity#3, 2 safety-review rounds) merged; D-032 confirmed (defs#4); repo secrets set, server#1 merged; APK downloaded; rt-core bootstrapped + ISO-TP core (rt-core#1); D-034 proposed, Q-018 closed (defs#5).
- 2026-09-27 (local, cont.): merged connectivity#2, mobile#4 (BLE v3, IMU, upload), defs#3 (D-032, Q-017/Q-018), workspace#3; moto-server#1 waited for the secret; repos made public (D-033, history scanned clean).
- 2026-09-27 (cloud, data pipeline): BLE schema v3 + IMU blocks (conn#2, CI green), mobile v3/imu.csv/upload (mobile#4), moto-server bootstrap (server#1); D-032 proposed, Q-017/Q-018; guardians + safety review done.
- 2026-09-27 (local): moto-mobile#2/#3 and connectivity-node#1 merged; defs v0.1.0 tagged; ESP32 BLE 4.2 build fix; CI submodule fix + classic PAT (D-031); disk cleanup; APK downloaded. OBD adapter left at home.
- 2026-09-26 (cloud A, release): D-024..D-027 confirmed, defs v0.1.0, manifest pinned, defs#1/workspace#1 closed, connectivity-node#1 realigned + safety-reviewed, mobile#2 drift test; D-030 proposed.
