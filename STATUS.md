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

1. **User:** add the repo secret `MOTO_DEFS_TOKEN` to moto-server (D-031), then re-run its CI. Review and merge conn#2 → mobile#4 → server#1. Confirm or change D-032 and merge the defs/workspace `claude/jolly-euler-rdlvqr` branches.
2. **Workshop:** flash the mock env, then the real env. With the IMU wired to GPIO1/2 (SDA/SCL, 3V3), check the `[IMU]` boot line and the `[HEAP]` line in the 10 s report. Record a session in the app, upload it to `moto-server serve` on the laptop (http on the LAN; the app warns), and read `moto-server report <id>`.
3. Bench: loop timing with BLE at MTU 185/50/23 and IMU present/absent/unplugged (safety-reviewer scenarios 5-8).
4. Q-018 tester hardening in connectivity-node (latch persistence, listen-only start, RX before the timeout check) → safety-reviewer. Needs a user decision (D-030 amendment).
5. defs: fix generated `vehicle_cl250.decode()` (unpacks 10 of 9 fields; suggested task) → patch release v0.1.1 (the user tags it).
6. moto-server: MDF4 export (asammdf), a TLS reverse-proxy example for exposed deployments.
7. **moto-hil-bench host** skeleton after deciding Q-009.

## Blockers / pending decisions

- D-032 (BLE v3 layout, IMU part/scale, session upload path) and D-030 await user confirmation. Q-017: move the BLE schema into defs codegen? Q-018: tester hardening.
- Q-009 (HIL realism level) blocks the hil-bench host.
- Q-014/Q-015: provisional values in D-029; final values from measurements (this pipeline).
- Q-002, Q-016 remainder, Q-001 remainder, Q-003, Q-006. License not decided.

## Recent sessions

- 2026-09-27 (cloud, data pipeline): BLE schema v3 + IMU blocks (conn#2, CI green), mobile v3/imu.csv/upload (mobile#4), moto-server bootstrap (server#1); D-032 proposed, Q-017/Q-018; guardians + safety review done.
- 2026-09-27 (local): moto-mobile#2/#3 and connectivity-node#1 merged; defs v0.1.0 tagged; ESP32 BLE 4.2 build fix; CI submodule fix + classic PAT (D-031); disk cleanup; APK downloaded. OBD adapter left at home.
- 2026-09-26 (cloud A, release): D-024..D-027 confirmed, defs v0.1.0, manifest pinned, defs#1/workspace#1 closed, connectivity-node#1 realigned + safety-reviewed, mobile#2 drift test; D-030 proposed.
- 2026-09-26 (cloud A, cont.): codegen refactor, defs#2 merged; D-028 Motorcycle VSS extensions, D-029 provisional limits + faster speed polling.
- 2026-09-25 (cloud A): moto-vehicle-defs bootstrap — CL250 YAML, platform.dbc, VSS overlay, codegen + CI, legacy notes; D-024..D-027, Q-014..Q-016.
