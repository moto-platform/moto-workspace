# STATUS — session handoff

> Keep it short (≤60 lines). Updated by the `/handoff` skill. "Recent sessions" keeps at most 5 one-line entries; drop the oldest.

**Phase:** 0 hardware build + measurement tools (D-058..D-061) · 1 data pipeline done in code · 2 rt-core without hardware done up to the republisher (rt-core v0.8.0) · defs v0.6.0 (BLE schema in defs)
**Last updated:** 2026-10-07

## Where we are

- 11 platform repos + `moto-workspace`, public (D-033), MIT (D-036). Decisions D-001..D-061; **D-057 intentionally unused**. Semver plan approved: defs v0.7.0 = D-059 (FC gate + discovery scan), v0.8.0 = D-060 (GPS BLE block).
- **Merged since 2026-10-03:** conn#10 (f0cde3e: D-058 tester stats on BLE v4, listen-only capture env, TWAI listen-only errata config; safety-reviewer no blocker), defs#39 (de76e7d: D-058 implementation notes, hardware-integration §7.1/§7.2). defs v0.6.0 (BLE schema in defs, D-061) is tagged and conn `main` pins it; **`manifest.yaml` still pins defs v0.5.1**.
- **Merged 2026-10-07, in order (CI green each time):** defs#40 (9e30877: `docs/ideas/` Gemini notes with conflicts listed, not decisions; feature-pool V9-V24; procurement Group 0; §5 B2C kept out of the repo in `~/Desktop/moto-private/ideas-b2c.md`), workspace#40 (58413aa: ignore `docs-presentation/references/*.pdf`, `/moto-apk/`), defs#42 (9ac216a: D-059), defs#41 (7a74a7f: D-060), conn#11 (6be6e2f: GPS parser).
  - D-059 on defs main: `transport.flow_control` (FC.CTS `30 00 00 AA×5`, BS 0, STmin 0, `max_ff_dl` 255, `FC_MAX_CF_BURST` 36), golden copy for the one FC, `discovery_scan` (24 read requests checked against tester_policy and the gate). vss CLEAN; safety-reviewer no technical blocker.
  - D-060 on defs main: `gpsBlock` (26 B, `gps` characteristic; no lat/lon/height, codegen refuses position-like names), C/Python/Dart.
  - conn main: `UbxParser`, `Seqlock`, `UbxConfig`, `GpsCore`, `hal/EspGpsUart`, `GpsModule` (core-0 static task), env `esp32-s3-devkitc-1-gps` with pins GPIO15/16 **CONFIRM** (`CONN_GPS_PINS_CONFIRMED=0` never installs the UART); not on BLE yet; conn still pins defs v0.6.0.
- defs `CHANGELOG.md`: `[Unreleased]` = D-060 (planned v0.8.0), `[0.7.0] — not yet tagged` = D-059. **Neither is tagged.**
- **Vehicle bus:** one read-only tester (D-037). `tester_policy` unchanged; the D-020 frame gate now passes one byte-exact FC.CTS (D-059, defs main; no consumer pins it yet).
- **Local, uncommitted (left on purpose):** workspace `docs-presentation/` md files (never commit). `ISSUES.md`: unchanged this session.

## Next up (in order)

1. **User:** confirm the D-059 values (`30 00 00 AA×5`, `max_ff_dl` 255, the 24 requests) before the v0.7.0 tag (safety-reviewer's procedural stop for a gate widening).
2. On request: a defs PR dating `[0.7.0]` and `[Unreleased]` → `[0.8.0]`, then tag v0.7.0 and v0.8.0 (`gh release create`), pin both in `manifest.yaml` (also the missing v0.6.0 pin), CHANGELOG dates.
3. conn after v0.8.0: bump the submodule, wire `GpsModule` to the BLE `gps` characteristic (`BLE_GPS_*`), moto-mobile `gps.csv`, moto-server storage (`/feature-module`, together per D-061).
4. conn D-059 probe env `esp32-s3-devkitc-1-probe` (`CONN_DISCOVERY_PROBE=1`): size the TWAI RX queue ≥ `VEHICLE_CL250_FC_MAX_CF_BURST` + margin (safety-reviewer MAJOR-1), FC only for the in-flight request's FF, abort on N_Cr/sequence gap/lost frame, VIN masked; add the env to `scripts/check_no_twai_tx.sh`; safety-reviewer on the PR.
5. Hardware: confirm GPS UART pins (record in hardware-integration.md, set `CONN_GPS_PINS_CONFIRMED=1`, fold GPS into the main env); measure the PVT rate (10 Hz with GPS+GLONASS?).
6. Evaluate the Gemini conflicts in `docs/ideas/` (each file lists them at the top).
7. Then: rt-core heartbeat 0x081 or EKF lean (former next-up 1, choice still open); rt-core needs the D-059 link-state check + host test before its defs bump (safety-reviewer MINOR-2).

## Blockers / pending decisions

- D-059 values await user confirmation before the v0.7.0 tag.
- Q-019 (board) blocks CubeMX, Renode and Ç6. Q-009 blocks the hil-bench host. Q-001 waits for the listen-only capture on the bike.
- Before safety-node Layer 1 code: Q-023, Q-026 (Group 7 hardware); Q-022 after fallback validation (k_red ≤ 0.8).
- **User:** C-4 (turn off the old `can-dbc-conventions` skill on claude.ai). Q-024, Q-025; D-030 awaits confirmation. Q-017 resolved (D-061).

## Recent sessions

- 2026-10-07 (local, Phase 0 PR batch): opened and, on the user's one-time request, merged in order defs#40, workspace#40, defs#42 (D-059), defs#41 (D-060, CHANGELOG conflict resolved by a merge), conn#11 (GPS parser); no tag. Reviews: vss CLEAN ×2, safety-reviewer no technical blocker on defs#42, architecture-guard approve-with-changes on conn#11. Worktree prune not run (6 remove rows listed).
- 2026-10-03 (local, defs patch + conn bump): defs#34 → defs v0.5.1 (f211781), conn#9 → defs v0.5.1 (03b9b99), manifest pinned. vss CLEAN ×2.
- 2026-10-03 (local, republisher / D-056): defs#33 → defs v0.5.0 (db2feec); rt-core#22 + #23 → rt-core v0.8.0 (f51b214). architecture-guard no blocker, vss CLEAN, safety-reviewer no blocker ×3.
- 2026-10-02 (local, health DID / D-055): defs#32 → defs v0.4.0 (866d8be), rt-core#20 → rt-core v0.7.0 (1369d8a).
- 2026-10-02 (local, Ç1 / D-054): rt-core#19 → v0.6.0 (e9beb90), defs#31 (D-054).
