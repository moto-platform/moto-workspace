# ISSUES — open findings backlog

> Source: the user's cross-repo audit of 2026-09-30, plus follow-ups from the Ç3 server reviews. Audit items were not re-verified when this file was written: check the cited file before you fix. Work **one group per session** (see "Fix plan"). When an item is fixed, set its status and add the PR. Architecture or safety changes need a D-xxx or Q-xxx in `moto-vehicle-defs/docs/DECISIONS.md` first.
>
> Status: **open** · **partial** · **fixed (PR)** · **decision** (needs the user first) · **decided** (recorded as D-xxx; follow-ups tracked)

## A. Architecture / safety (the most important)

| ID | Finding | Where | Proposed fix | Status |
|---|---|---|---|---|
| A-1 | **Layer 1 inputs are defined three different ways.** hardware §5b.2 lists lean, µ and mass. `platform_limits.yaml` does not treat mass as a Layer 1 input. D-021/D-029 and the DBC also give safety-node speed (E2E 0x021, age ≤ 400 ms, +5 m/s² margin). The decision function is not written down anywhere. If the check is tanθ ≤ µ, speed cancels out (v²/(gR) = tanθ) and is needed only when R comes from another source. Without speed, the costliest chain (UDS polling → rt-core → E2E) goes away. | hardware-architecture §5b.2, `limits/platform_limits.yaml`, D-021, D-029, platform.dbc 0x021 | Write the Layer 1 decision function (equation, inputs, units, the threshold source). Then decide whether speed is needed and align all three sources. `docs-researcher` → user decision → `safety-reviewer` | decided: D-041 (defs#11); follow-ups E-1, E-2 |
| A-2 | **"Isolated, works even if rt-core crashes" does not hold.** Every Layer 1 input comes from rt-core (D-021), and Q-002 is open. Today safety-node compares rt-core's estimate; it is not an independent monitor. | invariant 3, D-021, Q-002 | Decide on Q-002: its own minimal IMU in safety-node (independent) or a conservative mode. Then fix the isolation wording in ARCHITECTURE and the rules. `safety-reviewer` | decided: D-042, Q-023, Q-026 (defs#11); follow-ups E-2, E-3 |
| A-3 | **The sensor-to-node mapping is unclear.** One I2S microphone is assigned to three consumers: ESP-SR on ESP32, the LLM VAD on the Raspi, and the acoustic anomaly model on the Raspi. The node that reads the engine-block accelerometer (1 kHz+) is not named. §5b.9 says "Kuksa already carries CAN + IMU", but the Kuksa/VSS path is defined at 100 ms and cannot carry high-rate vibration. | hardware-architecture §5b.9, sensor tables | Build one sensor → node → transport table (rate, bus, consumer), and choose a high-rate path for vibration and audio (not VSS). User decision | decided: D-044, Q-024, Q-025 (defs#11); follow-up E-2 |
| A-4 | **The polling budget is nearly full.** 0.4 + 0.2 + 0.1 + 0.025 + 0.025 = 0.75 against a limit of 0.8, at an assumed 20 ms round trip. The Phase 0 plan and the anomaly schema want MAP, fuel trim and wheel speed, which do not fit. Whether the CL250 supports those PIDs is unknown. | `uds/vehicle_cl250.yaml` timing and DIDs; Phase 0 plan; anomaly schema | Measure the real round trip on the bike (D-029) and check PID support with 0x01 0x00/0x20 in the Q-001 probe. Then reprioritise (see B-6) or lower the rates. Blocked on hardware | open |
| A-5 | **The BOM may be short.** rt-core uses two buses (FDCAN1 + FDCAN2), but Group 2 lists one transceiver. If the HIL simulator imitates both buses, the ×2 in Group 1 is not enough. The architecture specifies a 2-channel CAN HAT for the Raspi, but the list has a single channel. | BOM groups 1/2, hardware-architecture | Recount the transceivers and HAT channels per node and bus, and update the BOM | open |

## B. Docs out of sync with decisions

| ID | Finding | Where | Proposed fix | Status |
|---|---|---|---|---|
| B-1 | Context classification and TinyML are still placed "on the ESP32-S3". D-008 moved them to rt-core `context/`. §5b.9 still says "ESP32-S3 (H7) safety net". | hardware §2, §3, §5b.0 table, §5b.9 | Edit the text to match D-008 | open |
| B-2 | Several stale references. | vehicle-work-plan §3.6, §3.1; hardware §8 table | §3.6: "for the G4 module" → audio runs on the ESP32-S3. §3.1: DUT → H7 (D-001). hardware §8: "Python/Go" → D-010, "Flutter/RN" → Flutter (D-022) | open |
| B-3 | **The Phase 0 data path contradicts D-032.** The Phase 0 plan (marked "Authoritative" in the README) says microSD binary + Wi-Fi sync. D-032 says BLE → phone → zip upload. The implemented path keeps no local copy on the ESP, so data is lost when the phone disconnects. | Phase 0 plan, docs/README, D-032, connectivity-node | Decide: add a local ring buffer or microSD on the ESP, or accept the loss. Then mark the Phase 0 plan superseded where it conflicts | decided: D-045 (defs#11); follow-up E-2 |
| B-4 | moto-server `CLAUDE.md` describes "rt-core binary log + Kuksa MQTT/Zenoh", but the real v0 is `POST /sessions`. | moto-server/CLAUDE.md | Describe v0 as built and list the rest as planned | open |
| B-5 | STATUS "Next up 1" was stale: those merges were already done. | STATUS.md | STATUS rewritten on 2026-09-30 | fixed (ws#14) |
| B-6 | `vehicle_cl250.yaml` says "order = poll priority", but rt-core polls round-robin. Speed is a safety input yet gets no priority. | uds/vehicle_cl250.yaml comment; rt-core `uds_client_core` | Decide: priority-first scheduling for safety DIDs (a defs field, e.g. `priority: safety`), or fix the comment. Tied to A-1: if speed leaves Layer 1, only the comment needs fixing | decided: D-043 (defs#11); follow-up E-1, E-4 |
| B-7 | The Ç3 scope differs between documents. ARCH §9 lists 0x10/22/19/14/27/2E/31; what was built is 0x10/3E/22/19/14. Bootloader/OTA needs 0x11 and 0x34/36/37, and neither document lists them. | ARCHITECTURE §9; D-040 | Update ARCH §9 to the built scope. Move 0x27/2E/31/11/34/36/37 to Ç5 (bootloader) with the D-040 item 7 precondition: 0x27 before any write or programming service | partial (D-040 item 7) |
| B-8 | Small inconsistencies. | README/STATUS vs D-033/D-036; D-025; platform.dbc 0x021; DID 0xF40D | Repo count: 11 platform repos + workspace = 12, so say it the same way everywhere. D-025 rationale still says "800 ms". DBC speed range is 300 km/h but the DID max is 255. The source resolution is 1 km/h but the DBC scale is 0.01: pick 255 and document the resolution | open |

## C. Code / CI / process

| ID | Finding | Where | Proposed fix | Status |
|---|---|---|---|---|
| C-1 | D-039 claims parity with conn, but conn's foreign-tester latch covered the functional IDs and rt-core's did not (Q-021). Two separate `uds_iso14229.h` exist (one C++ namespace, one macros), so they can drift. | rt-core, connectivity-node | rt-core part fixed: D-040, rt-core#9 (gen/ watch table, gen/ ISO header). Remaining: bump conn to defs v0.2.0, replace its own `uds_iso14229.h` with the gen/ client subset, and take the watch IDs from `vehicle_cl250_functional_watch[]`. `safety-reviewer` | partial |
| C-2 | **MISRA and coverage are not decisions.** The blocking MISRA step and the 95/80 coverage floors are enforced in CI but not recorded in DECISIONS. D-034 still says "MISRA only reports". The D-020 gates in `gen/c` are outside MISRA. conn CI has no static analysis at all, although conn is the temporary sole tester. | DECISIONS D-034; defs CI; conn CI | Record a decision for MISRA blocking + coverage floors (user approval). Add a MISRA/cppcheck step for defs `gen/c` and for conn | decision |
| C-3 | `safety-reviewer` is not synced to conn, linux-node or server. conn's tester latch and linux-node's OTA fall under invariant 8. | scripts/sync_claude.py `REPO_ASSETS` | Add safety-reviewer to those repos, run `python3 scripts/sync_claude.py`, and commit in each repo | open |
| C-4 | The old user-level `can-dbc-conventions` skill is still installed and triggers on the same requests as `/signal-change`. D-004 rejects its `mappings.yaml` format (judged from its description; the content was not read). | claude.ai synced skills | **User:** turn it off on claude.ai (already noted in an earlier STATUS) | open (user) |
| C-5 | `setup.sh` does not run `git submodule update` after a checkout in an existing repo, and `\|\| true` also swallows checkout errors. | moto-workspace/setup.sh | Run `git submodule update --init --recursive` after the checkout, and fail loudly on checkout errors | open |

## D. Planned follow-ups (from the Ç3 reviews and STATUS)

- D-1 rt-core **v0.4.0** release (the Ç3 server), then pin it in `manifest.yaml`.
- D-2 **Ç1 H7 HAL requirements** (safety review of the Ç3 server):
  - N_As
  - bus-off backoff
  - FDCAN1 filters that pass the vehicle request and watch IDs; FDCAN2 filters for 0x710/0x7DF
  - FDCAN2 Tx-Queue (priority) mode, and 0x7xx routed to FIFO1
  - one comms task, with the client step before the server step
- D-3 **Q-001 probe before the first rt-core ride:** include 0x7DF and 0x18DB33F1 (D-040 item 7), plus the PID support check for A-4.
- D-4 **0x27** (or a rate limit) before a flash-backed DTC memory or any write/programming service (D-040 item 7).
- D-5 Platform-bus republisher of `vehicle_signals` (NONE/STALE become INVALID). Speed keeps 0x021 and its E2E for its other consumers, but safety-node no longer reads it (D-041).
- D-6 HIL scenarios from the rt-core uds README (`uds_server_*`, `uds_client_*`), once the hil-bench host schema exists (Q-009).

## E. Follow-ups from the group 1 decisions (D-041..D-045)

| ID | Follow-up | Where | Status |
|---|---|---|---|
| E-1 | `/signal-change` (defs minor release, `safety-reviewer`): add `k_yellow` / `k_red` to `platform_limits.yaml` (provisional, conservative); re-scope `vehicle_speed_max_age_ms` and `vehicle_speed_accel_margin_mps2` to rt-core (no ESTIMATED lean from stale speed); decide whether 0x021 stays in the safety range; fix the `platform_limits.yaml` header (Q-002 resolved); codegen check 0 < k_yellow < k_red < 1; add the `priority` field to `vehicle_cl250.yaml` (0xF40D `high`) and rewrite the "Order = poll priority" comment | defs `limits/`, `uds/`, `dbc/platform.dbc`, CHANGELOG | open |
| E-2 | Docs sync for D-041..D-045: hardware §5b.2 (inputs, the function, the fallback, "no additional hardware"), §5b.6/§5b.7/§5b.9 (sensor map, the Kuksa sentence), ARCHITECTURE (Q-002 lines, the cornering data-flow row), the Phase 0 plan + docs/README "superseded in part" note | defs docs | open (group 2) |
| E-3 | BOM: one IMU for safety-node (D-042), an engine-facing microphone for the Raspi and the engine-block accelerometer for rt-core (D-044) | BOM, with A-5 | open (group 6) |
| E-4 | rt-core `uds_client_core`: priority-first scheduling from the gen/ `priority` field, with tests (after E-1) | moto-rt-core | open (group 5) |

## Fix plan (one group per session, in this order)

1. ~~**Safety architecture decisions**: A-1, A-2, A-3, B-6, and B-3.~~ Done 2026-09-30: D-041..D-045, Q-022..Q-025 (defs#11); follow-ups in section E.
2. **Docs sync** (a sonnet subagent does the edits; you review): B-1, B-2, B-4, B-7, B-8, E-2, and the D-034 text, after the C-2 decision. E-1 (`/signal-change`) can go in the same or the next session.
3. **Tooling / CI**: C-2 (MISRA for defs `gen/c` and conn), C-3 (sync `REPO_ASSETS`), C-5 (`setup.sh`).
4. **conn alignment**: C-1 (defs v0.2.0, gen/ ISO header, functional watch), with `safety-reviewer`.
5. **rt-core**: D-1 release, then Ç1 (D-2) with `/feature-module`; E-4 after E-1.
6. **Hardware-dependent**: A-4, A-5, D-3, E-3.
