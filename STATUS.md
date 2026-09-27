# STATUS — session handoff

> Keep it short (≤60 lines). Updated by the `/handoff` skill. "Recent sessions" keeps at most 5 one-line entries; drop the oldest.

**Phase:** 1 — data-collection pipeline (BLE v3 + IMU → app → moto-server) in review
**Last updated:** 2026-09-27

## Where we are

- 11 repos + `moto-workspace` in `github.com/moto-platform`, **public** (D-033). Decisions D-001..D-032 (D-030, D-032 = Claude proposals pending confirmation). Open questions Q-001..Q-018.
- moto-vehicle-defs `v0.1.0` = `acef075` (tag pushed). Consumers pin it. `manifest.yaml` is unchanged until the PRs below merge.
- **Data pipeline (D-032), 3 PRs open for user review. Merge order: conn → mobile → server:**
  - [connectivity-node#2](https://github.com/moto-platform/moto-connectivity-node/pull/2): BLE telemetry v3 (node clock, ages, CAN health; v2 fallback at low MTU) + 100 Hz IMU blocks (MPU-6050 compatible, GPIO1/2) + read-only CAN health. **CI green**: 52 native tests, schema check, 3 ESP32 builds. safety-reviewer OK (no effect on the poller or TX gate); vss-schema-guardian clean; architecture-guard OK.
  - [moto-mobile#4](https://github.com/moto-platform/moto-mobile/pull/4): v3/v2 + IMU decoder, `imu.csv`, CAN health/MTU events, firmware-update banner, upload with settings, status and retry. The token is in the keystore. 98 tests. CI builds the `moto-mobile-apk` artifact.
  - [moto-server#1](https://github.com/moto-platform/moto-server/pull/1): FastAPI `POST/GET /sessions`, report, CLI `import`, schema-driven re-decode, validation report, Parquet + SQLite, MDF4 stub, docker-compose. 46 tests locally. **CI red only because the repo secret `MOTO_DEFS_TOKEN` is missing.**
  - The session format is `moto-mobile/docs/session-format.md`. The BLE schema single source is `moto-connectivity-node/docs/ble_telemetry_packet_schema.json`; mobile and server keep verbatim copies with drift tests (Q-017).
- D-032 + Q-017/Q-018 are on moto-vehicle-defs branch `claude/jolly-euler-rdlvqr` (no PR yet); this STATUS is on the workspace branch of the same name.
- `HondaCl250_Telemetry` untouched.

## Next up (in order)

1. **User (before anything else):** create 2 **organization** secrets at github.com/organizations/moto-platform/settings/secrets/actions, both with the same classic PAT (`repo` scope, expires ~2026-12-26, D-031), Repository access = All repositories:
   - `MOTO_DEFS_TOKEN`: CI fetch of the defs submodule.
   - `MOTO_CONN_READ_TOKEN`: BLE schema drift check in moto-mobile / moto-server CI.
   Repos are public now (D-033), so org secrets reach them on the Free plan. connectivity-node also has a repo-level `MOTO_DEFS_TOKEN` (takes precedence; delete it or keep it in sync).
2. **moto-server#1** (D-032 bootstrap: upload API, CLI import, v2/v3 re-decode, validation report, Parquet, SQLite index). Verified locally (ruff clean, 45 passed, 1 skipped). CI failed only for the missing secret → rerun CI → merge.
3. **User decision:** confirm D-032 (BLE v3 37 B + v2 fallback, 100 Hz raw IMU ±8 g/±500 dps on a 2nd characteristic, session upload, server re-decodes from raw_hex). Already merged in connectivity#2 / mobile#4 → mark it "user-confirmed".
4. **Q-018 hardening BEFORE connecting to the bike's DLC:** persist the D-030 latches across resets (RTC no-init + CRC), listen-only ≥2 s before the first request, drain RX before the UDS timeout check. `/feature-module moto-connectivity-node` + safety-reviewer.
5. **Workshop / local:** when the ESP32 is on USB, flash the mock env (`pio run -e esp32-s3-devkitc-1-mock -t upload` in moto-connectivity-node; `platformio_local.ini` exists locally), install the new APK (v3; from the latest moto-mobile main CI artifact) and verify BLE → recording → export → upload end-to-end. The real env goes on the bike only after item 4.
6. **Hardware:** the OBD adapter was left at home. Chain: CL250 6-pin DLC → Honda adapter (OBD2 16F) → robust OBD2 **male** pigtail (or OBD2→DB9 with a screw lock) → ESP. Pins 6/14/4-5. Continuity-test the adapter. Ties/tape on the joints plus strain relief. Later: a direct Honda 6-pin harness.
7. **Measure** (no OBD needed): mass with/without rider, front/rear split, rear rolling radius, tire pressures (vehicle-work-plan §5) → replace the D-029 provisional values via `/signal-change` or a limits update.
8. Optional CI simplification: fall back to an anonymous defs clone when the token is empty (defs is public now).
9. **License decision** (repos are public with no LICENSE; moto-mcp is intended to be open source). Then the moto-hil-bench host skeleton (Q-009 first).

## Blockers / pending decisions

- D-032 (BLE v3 layout, IMU part/scale, session upload path) and D-030 await user confirmation. Q-017: move the BLE schema into defs codegen? Q-018: tester hardening.
- Q-009 (HIL realism level) blocks the hil-bench host.
- Q-014/Q-015: provisional values in D-029; final values from measurements (this pipeline).
- Q-002, Q-016 remainder, Q-001 remainder, Q-003, Q-006. License not decided.

## Recent sessions

- 2026-09-27 (local, cont.): merged connectivity#2, mobile#4 (BLE v3, IMU, upload), defs#3 (D-032, Q-017/Q-018), workspace#3; moto-server#1 waits for the secret; repos made public (D-033, history scanned clean).
- 2026-09-27 (cloud, data pipeline): BLE schema v3 + IMU blocks (conn#2, CI green), mobile v3/imu.csv/upload (mobile#4), moto-server bootstrap (server#1); D-032 proposed, Q-017/Q-018; guardians + safety review done.
- 2026-09-27 (local): moto-mobile#2/#3 and connectivity-node#1 merged; defs v0.1.0 tagged; ESP32 BLE 4.2 build fix; CI submodule fix + classic PAT (D-031); disk cleanup; APK downloaded. OBD adapter left at home.
- 2026-09-26 (cloud A, release): D-024..D-027 confirmed, defs v0.1.0, manifest pinned, defs#1/workspace#1 closed, connectivity-node#1 realigned + safety-reviewed, mobile#2 drift test; D-030 proposed.
- 2026-09-26 (cloud A, cont.): codegen refactor, defs#2 merged; D-028 Motorcycle VSS extensions, D-029 provisional limits + faster speed polling.
