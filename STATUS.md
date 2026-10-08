# STATUS — session handoff

> Keep it short (≤60 lines). Updated by the `/handoff` skill. "Recent sessions" keeps at most 5 one-line entries; drop the oldest.

**Phase:** 0 hardware build + measurement tools (D-058..D-062) · 1 data pipeline done in code · 2 rt-core without hardware done up to the republisher (rt-core v0.8.0) · defs v0.8.0
**Last updated:** 2026-10-08

## Where we are

- 11 platform repos + `moto-workspace`, public (D-033), MIT (D-036). Decisions D-001..D-062; **D-057 intentionally unused**.
- **defs:** v0.8.0 is the latest tag (`manifest.yaml` pins it). `[Unreleased]`: defs#44 `gpsBlock.sequenceRule` wording (PATCH with the next release). defs#45 (D-062 text) merged.
- **conn:** pins v0.8.0; conn#13 merged (GPS notify in every build, bonded-only CCCD cleared on every connect, `GpsNotifyTracker.h`).
- **Open PRs (the user merges; merge both together, D-061 item 3), CI green:**
  - **moto-server#7** `claude/gps-session` (61a36b2): defs v0.8.0; optional `gps.csv` with an exact header (no position column can pass), `raw_hex` re-decoded by schema-driven `decode_gps_block()` (int32 added), `gps.parquet`, report `gps` section (lost **or MTU-skipped** from seq, rate, fix types, speed-check-usable share, parse/UART flags), index `has_gps` with additive migration. pytest 76 (14 new, fixture `v4_gps_session`).
  - **moto-mobile#8** `claude/gps-session` (72c4693): defs v0.8.0; `GpsBlock` + `GpsSeqTracker`, bonded `gps` subscription after telemetry/IMU (Android `createBond`, once per connection, failure never touches telemetry/IMU, device ids redacted), `gps.csv` (same 20 columns), events `gps_gap` / `gps_subscribed` / `gps_subscribe_failed`, meta `gps_block_version`, summary GPS totals, Record-screen GPS line. `docs/session-format.md` is the contract. flutter test 124 (19 new).
  - architecture-guard (plan): no blocker. vss-schema-guardian: CLEAN on both.
- **Vehicle bus:** one read-only tester (D-037). `tester_policy` unchanged; D-020 gate passes one byte-exact FC.CTS (D-059; conn has no probe code yet).
- **Local, uncommitted (left on purpose):** workspace `docs-presentation/` md files (never commit). `ISSUES.md`: unchanged.
- Local Flutter is 3.44.8 (`~/development/flutter/bin`, not on PATH); CI uses 3.47.5, so never commit a `pubspec.lock` rewritten by a local `pub get`.

## Next up (in order)

1. Merge moto-server#7 and moto-mobile#8 together, then release both (D-036: version bump PR → `gh release create`) and pin them in `manifest.yaml` (workspace PR).
2. Hardware with GPS: confirm UART pins (hardware-integration.md, `CONN_GPS_PINS_CONFIRMED=1`, fold GPS into the main env), measure the PVT rate (10 Hz with GPS+GLONASS?), **re-measure the D-058 step gap with GPS notify on**, and check on a real phone that bonding + the `gps` subscription work (Android and iOS) and `gps.csv` imports cleanly into moto-server.
3. conn D-059 probe env `esp32-s3-devkitc-1-probe` (`CONN_DISCOVERY_PROBE=1`): TWAI RX queue ≥ `VEHICLE_CL250_FC_MAX_CF_BURST` + margin (safety-reviewer MAJOR-1), FC only for the in-flight request's FF, abort on N_Cr/sequence gap/lost frame, VIN masked; add the env to `scripts/check_no_twai_tx.sh`; safety-reviewer on the PR.
4. Evaluate the Gemini conflicts in `docs/ideas/` (each file lists them at the top).
5. Then: rt-core heartbeat 0x081 or EKF lean (choice still open); rt-core needs the D-059 link-state check + host test before its defs bump (safety-reviewer MINOR-2).

## Blockers / pending decisions

- **User (new, from architecture-guard):** add a guard so a session with `gps.csv` is never uploaded to a non-local server (D-060 item 5)? Docs already say "local server only"; a code guard would be a new decision (record as D-063 if yes).
- Q-019 (board) blocks CubeMX, Renode and Ç6. Q-009 blocks the hil-bench host. Q-001 waits for the listen-only capture on the bike.
- Before safety-node Layer 1 code: Q-023, Q-026 (Group 7 hardware); Q-022 after fallback validation (k_red ≤ 0.8).
- **User:** C-4 (turn off the old `can-dbc-conventions` skill on claude.ai). Q-024, Q-025; D-030 awaits confirmation.

## Recent sessions

- 2026-10-08 (local, GPS sessions): pruned 4 merged worktrees; opened moto-server#7 + moto-mobile#8 (defs v0.8.0, `gps.csv` record/store, bonded subscribe per D-062). CI green, guardians clean. No new decisions.
- 2026-10-08 (local, GPS on BLE): user decided D-062 (bonded subscribe; seq counts MTU-skipped blocks). defs#44 merged (wording); opened defs#45 (D-062) and conn#13 (GPS notify wiring, `GpsNotifyTracker.h`, 9 new tests).
- 2026-10-07 (local, Phase 0 PR batch): merged defs#40, workspace#40, defs#42 (D-059), defs#41 (D-060), conn#11 (GPS parser); released defs v0.7.0 + v0.8.0 (defs#43), pinned v0.8.0; later conn#12 (defs v0.8.0 + GPS block packer).
- 2026-10-03 (local, defs patch + conn bump): defs#34 → defs v0.5.1 (f211781), conn#9 → defs v0.5.1 (03b9b99), manifest pinned. vss CLEAN ×2.
- 2026-10-03 (local, republisher / D-056): defs#33 → defs v0.5.0 (db2feec); rt-core#22 + #23 → rt-core v0.8.0 (f51b214).
