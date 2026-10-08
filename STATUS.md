# STATUS — session handoff

> Keep it short (≤60 lines). Updated by the `/handoff` skill. "Recent sessions" keeps at most 5 one-line entries; drop the oldest.

**Phase:** 0 hardware build + measurement tools (D-058..D-062) · 1 data pipeline done in code · 2 rt-core without hardware done up to the republisher (rt-core v0.8.0) · defs v0.8.0
**Last updated:** 2026-10-08

## Where we are

- 11 platform repos + `moto-workspace`, public (D-033), MIT (D-036). Decisions D-001..D-062 (D-062 on defs#45, not merged yet); **D-057 intentionally unused**.
- **defs:** v0.7.0 (D-059 FC gate + discovery scan) and v0.8.0 (D-060 GPS block, 26 B, no lat/lon/height) released 2026-10-07; `manifest.yaml` pins v0.8.0. Only conn pins v0.8.0 so far (conn#12, 6feaea2).
- **Merged 2026-10-08:** defs#44 (d2f9e05): `gpsBlock.sequenceRule` wording, seq advances for sent **or MTU-skipped** blocks, error flags since the previous block (sent or skipped). Wording only, `gen/python` text regenerated, no tag (PATCH with the next release; CHANGELOG `[Unreleased]`).
- **Open PRs (the user merges):**
  - **defs#45** `claude/d062`: D-062 in DECISIONS.md (it missed #44's merge). Docs only.
  - **conn#13** `claude/gps-ble-wire`: `gps` notify characteristic in every build, data from `state.gps` (no GpsCore pointer), pure `GpsNotifyTracker.h` (navPvtCount delta → seq gap, MTU skip advances seq + error base, half-period min spacing that holds and never drops a PVT, reset on disconnect), GPS after telemetry + IMU in the chain (≤3 notifies/pass, D-053). CCCD bonded-only (D-062), cleared on every connect. native 4 suites green (test_gps 35/35), 5 esp32 envs build, cppcheck 2.22.0 clean, vss CLEAN.
- **Vehicle bus:** one read-only tester (D-037). `tester_policy` unchanged; the D-020 frame gate passes one byte-exact FC.CTS (D-059; conn pins it, conn has no probe code yet).
- **Local, uncommitted (left on purpose):** workspace `docs-presentation/` md files (never commit). `ISSUES.md`: unchanged.

## Next up (in order)

1. Merge defs#45 and conn#13 (CI green). Then moto-mobile `gps.csv` and moto-server storage take defs v0.8.0 together (D-061 item 3); the phone must bond before it subscribes to `gps` (D-062). architecture-guard first, one session per repo.
2. Hardware with GPS: confirm UART pins (hardware-integration.md, `CONN_GPS_PINS_CONFIRMED=1`, fold GPS into the main env), measure the PVT rate (10 Hz with GPS+GLONASS?) and **re-measure the D-058 step gap with GPS notify on** (bonded phone subscribed).
3. conn D-059 probe env `esp32-s3-devkitc-1-probe` (`CONN_DISCOVERY_PROBE=1`): TWAI RX queue ≥ `VEHICLE_CL250_FC_MAX_CF_BURST` + margin (safety-reviewer MAJOR-1), FC only for the in-flight request's FF, abort on N_Cr/sequence gap/lost frame, VIN masked; add the env to `scripts/check_no_twai_tx.sh`; safety-reviewer on the PR.
4. Evaluate the Gemini conflicts in `docs/ideas/` (each file lists them at the top).
5. Then: rt-core heartbeat 0x081 or EKF lean (choice still open); rt-core needs the D-059 link-state check + host test before its defs bump (safety-reviewer MINOR-2).

## Blockers / pending decisions

- Q-019 (board) blocks CubeMX, Renode and Ç6. Q-009 blocks the hil-bench host. Q-001 waits for the listen-only capture on the bike.
- Before safety-node Layer 1 code: Q-023, Q-026 (Group 7 hardware); Q-022 after fallback validation (k_red ≤ 0.8).
- **User:** C-4 (turn off the old `can-dbc-conventions` skill on claude.ai). Q-024, Q-025; D-030 awaits confirmation.

## Recent sessions

- 2026-10-08 (local, GPS on BLE): user decided D-062 (bonded subscribe; seq counts MTU-skipped blocks). defs#44 merged (wording); opened defs#45 (D-062) and conn#13 (GPS notify wiring, `GpsNotifyTracker.h`, 9 new tests). vss CLEAN; architecture-guard reused from the previous session (Option A). Pruned the gps-ble / gps-ble-notify worktrees.
- 2026-10-07 (local, Phase 0 PR batch): merged defs#40, workspace#40, defs#42 (D-059), defs#41 (D-060), conn#11 (GPS parser); released defs v0.7.0 + v0.8.0 (defs#43), pinned v0.8.0; later conn#12 (defs v0.8.0 + GPS block packer).
- 2026-10-03 (local, defs patch + conn bump): defs#34 → defs v0.5.1 (f211781), conn#9 → defs v0.5.1 (03b9b99), manifest pinned. vss CLEAN ×2.
- 2026-10-03 (local, republisher / D-056): defs#33 → defs v0.5.0 (db2feec); rt-core#22 + #23 → rt-core v0.8.0 (f51b214).
- 2026-10-02 (local, health DID / D-055): defs#32 → defs v0.4.0 (866d8be), rt-core#20 → rt-core v0.7.0 (1369d8a).
