# STATUS — session handoff

> Keep it short (≤60 lines). Updated by the `/handoff` skill. "Recent sessions" keeps at most 5 one-line entries; drop the oldest.

**Phase:** 1 data pipeline done in code (bench test pending) · 2 rt-core without hardware: host-first (D-034), Ç2 ISO-TP core done
**Last updated:** 2026-09-28

## Where we are

- 11 repos + `moto-workspace`, public (D-033), **MIT for all (D-036)**, semver from `v0.1.0` (manifest pins tags). Decisions D-001..D-036; only D-030 still awaits confirmation.
- **Merged:** data pipeline (connectivity#2, mobile#4, server#1), Q-018 hardening (connectivity#3), D-032 confirmed (defs#4). APK: `~/Desktop/moto-apk/app-release.apk` (`102d5a1`).
- **rt-core#1 (CI green):**
  - CMake presets `host-tests` (Unity, ASan/UBSan) and `target-m7-*` (Cortex-M7, H743/H723-neutral), defs `v0.1.0`
  - ISO-TP core `features/uds/isotp_core`: 34 tests, ~1.2 KB flash, 0 B RAM
- **D-034 confirmed:** rt-core also runs on the PC (SIL) through a host port of `hal/`, using the same services/features code. The H7 board is open (**Q-019**), so there is no CubeMX project yet.
- **D-035:** the HIL has two separate modes, log replay and a live vehicle model. The first target test function is still open (Q-009).
- **Local toolchain installed:**
  - cmake 4.4 / ninja / cppcheck 2.22 (brew)
  - arm-none-eabi-gcc 15.3 (`~/.local/opt/arm-gnu-toolchain-15.3.rel1-...`, symlinked into `~/.local/bin`)
- **CI without secrets (PRs open):** connectivity#4, server#2, mobile#5 read defs and the BLE schema from the public repos. The repo secrets can be deleted after these merge.

## Next up (in order)

1. **User:** merge the open PRs:
   - rt-core#1
   - defs#5 (D-034..D-036, Q-019)
   - workspace#4
   - connectivity#4, server#2, mobile#5
   - the LICENSE PRs #1 in hil-bench, io-node, linux-node, mcp, ml, safety-node

   Then tag `v0.1.0` on connectivity-node, moto-mobile, moto-server and moto-rt-core (after CI is green on `main`), and pin those tags in `manifest.yaml`.
2. **NEXT SESSION, rt-core host platform layer + ISO-TP glue (D-034)** (`/feature-module moto-rt-core uds`):
   - `hal/can_port.h`: a HAL-free CAN port interface (send / receive / state / error counters).
   - `hal/host/`:
     - an in-process virtual bus (macOS/CI)
     - Linux SocketCAN `vcan` (optional)
     - a monotonic ms timebase
   - `services/timebase`
   - `features/uds/isotp_link`: binds `isotp_core` to a port plus a (req, resp) ID pair. The vehicle link uses `VEHICLE_CL250_*` from `gen/`, including the padding byte.
   - A host executable `moto_rtcore_host` (SIL main loop) plus mock-bus tests. Keep `target-m7` building.
3. **rt-core Ç3, UDS server core** (platform bus):
   - First, `/signal-change` in defs for the server's request/response IDs and its own DIDs (`uds/dids.yaml`, platform.dbc).
   - Then `/feature-module`: a 0x10 / 0x3E / 0x22 / 0x19 / 0x14 state machine, NRCs, P2 / P2* / S3.
4. **rt-core Ç1:** CAN error state machine (bus-off recovery, error counters) behind `can_port.h`, host tests.
5. **moto-hil-bench host skeleton** (`/repo-bootstrap moto-hil-bench host`, Python): a shared scenario format with the two modes of D-035 (log replay, live model), driving the rt-core host build over vcan. Choose the first test function first (Q-009).
6. **Workshop:** with the ESP32 on USB, flash the mock env, install the APK, and test BLE → recording → upload end-to-end. Then the connectivity#3 bench checks: scope TX during boot and the mode switch, reset reasons, TXD pull-up, ignition-switched power.
7. **Follow-ups:**
   - BLE schema wording for the latch semantics, in 3 repos together.
   - moto-server: validate `session_id` in `GET /report`; cap the unzipped size.
   - MISRA advisory baseline in rt-core (15.5 ×28, 8.7, 15.7).
8. **Hardware / measurement:** OBD chain (CL250 6-pin → Honda adapter → OBD2 pigtail → ESP). Measure mass, weight split and rolling radius to replace the D-029 values.

## Blockers / pending decisions

- Q-019 (H743 vs H723) blocks CubeMX, Renode L1 and Ç6. Q-009 remainder: the first HIL test function. D-030 is not yet confirmed.
- Q-017 (BLE schema in defs codegen). Q-014/Q-015: the D-029 values are provisional until measured. Q-002, Q-001/Q-016 remainders, Q-003, Q-004 (bridge format), Q-006 (requirements location, for Ç8).
- Check the university's thesis IP rules before the first public release (D-036).

## Recent sessions

- 2026-09-28 (local): Q-018 merged (connectivity#3); D-032 confirmed; server#1 merged; rt-core bootstrapped + ISO-TP core (rt-core#1); D-034 confirmed (host layer), D-035 HIL modes, D-036 MIT + semver, Q-019 board; CI secrets removed (PRs); toolchains installed.
- 2026-09-27 (local, cont.): merged connectivity#2, mobile#4 (BLE v3, IMU, upload), defs#3 (D-032, Q-017/Q-018), workspace#3; moto-server#1 waited for the secret; repos made public (D-033, history scanned clean).
- 2026-09-27 (cloud, data pipeline): BLE schema v3 + IMU blocks (conn#2, CI green), mobile v3/imu.csv/upload (mobile#4), moto-server bootstrap (server#1); D-032 proposed, Q-017/Q-018; guardians + safety review done.
- 2026-09-27 (local): moto-mobile#2/#3 and connectivity-node#1 merged; defs v0.1.0 tagged; ESP32 BLE 4.2 build fix; CI submodule fix + classic PAT (D-031); disk cleanup; APK downloaded. OBD adapter left at home.
- 2026-09-26 (cloud A, release): D-024..D-027 confirmed, defs v0.1.0, manifest pinned, defs#1/workspace#1 closed, connectivity-node#1 realigned + safety-reviewed, mobile#2 drift test; D-030 proposed.
