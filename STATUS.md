# STATUS — session handoff

> Keep it short (≤60 lines). Updated by the `/handoff` skill. "Recent sessions" keeps at most 5 one-line entries; drop the oldest.

**Phase:** 0 hardware build + measurement tools (D-058..D-062) · 1 data pipeline done in code · 2 rt-core without hardware done up to the republisher (rt-core v0.8.0) · defs v0.8.0
**Last updated:** 2026-10-08

## Where we are

- 11 platform repos + `moto-workspace`, public (D-033), MIT (D-036). Decisions D-001..D-063; **D-057 intentionally unused**.
- **defs:** v0.8.0 is the latest tag (`manifest.yaml` pins it). `[Unreleased]`: defs#44 `gpsBlock.sequenceRule` wording (PATCH with the next release). defs#45 (D-062 text) merged.
- **conn:** pins v0.8.0; conn#13 merged (GPS notify in every build, bonded-only CCCD cleared on every connect, `GpsNotifyTracker.h`).
- **Merged:** moto-server#7 + moto-mobile#8 (GPS sessions on defs v0.8.0; pytest 76, flutter test 124).
- **Open PRs (the user merges), CI green:**
  - **moto-server#8** `claude/release-0.2.0` (3164c76): version 0.1.0 → 0.2.0 (`pyproject.toml`, `__init__`, FastAPI, `uv.lock`).
  - **moto-mobile#9** `claude/release-0.2.0` (9b81507): `0.1.0+2` → `0.2.0+3` (`pubspec.yaml`, `kAppVersion`).
  - **moto-mobile#10** `claude/gps-local-only` (61a2093): D-063 guard, `isLocalServerUrl()` + `SessionUploader` check before any network call; flutter test 128 (4 new). Merge before #9's release so v0.2.0 carries it.
  - **defs#46** `claude/d-063-gps-local-upload`: D-063 text, D-060 item 5 points to it (docs only, no tag).
- **Vehicle bus:** one read-only tester (D-037). `tester_policy` unchanged; D-020 gate passes one byte-exact FC.CTS (D-059; conn has no probe code yet).
- **Local, uncommitted (left on purpose):** workspace `docs-presentation/` md files (never commit). `ISSUES.md`: unchanged.
- Local Flutter is 3.44.8 (`~/development/flutter/bin`, not on PATH); CI uses 3.47.5, so never commit a `pubspec.lock` rewritten by a local `pub get`.

## Next up (in order)

1. After the user merges server#8, mobile#10, mobile#9 (and defs#46): `gh release create v0.2.0` for moto-server and moto-mobile, then pin both in `manifest.yaml` (workspace PR).
2. Hardware with GPS: confirm UART pins (hardware-integration.md, `CONN_GPS_PINS_CONFIRMED=1`, fold GPS into the main env), measure the PVT rate (10 Hz with GPS+GLONASS?), **re-measure the D-058 step gap with GPS notify on**, and check on a real phone that bonding + the `gps` subscription work (Android and iOS) and `gps.csv` imports cleanly into moto-server.
3. conn D-059 probe env `esp32-s3-devkitc-1-probe` (`CONN_DISCOVERY_PROBE=1`): TWAI RX queue ≥ `VEHICLE_CL250_FC_MAX_CF_BURST` + margin (safety-reviewer MAJOR-1), FC only for the in-flight request's FF, abort on N_Cr/sequence gap/lost frame, VIN masked; add the env to `scripts/check_no_twai_tx.sh`; safety-reviewer on the PR.
4. Evaluate the Gemini conflicts in `docs/ideas/` (each file lists them at the top).
5. Then: rt-core heartbeat 0x081 or EKF lean (choice still open); rt-core needs the D-059 link-state check + host test before its defs bump (safety-reviewer MINOR-2).

## Blockers / pending decisions

- Q-019 (board) blocks CubeMX, Renode and Ç6. Q-009 blocks the hil-bench host. Q-001 waits for the listen-only capture on the bike.
- Before safety-node Layer 1 code: Q-023, Q-026 (Group 7 hardware); Q-022 after fallback validation (k_red ≤ 0.8).
- **User:** C-4 (turn off the old `can-dbc-conventions` skill on claude.ai). Q-024, Q-025; D-030 awaits confirmation.

## Recent sessions

- 2026-10-08 (local, releases + D-063): pruned 2 merged worktrees; opened server#8 + mobile#9 (0.2.0 bumps); user decided **D-063** (mobile blocks GPS-session upload to a non-local server) → mobile#10, defs#46. CI green on all four.
- 2026-10-08 (local, GPS sessions): pruned 4 merged worktrees; opened moto-server#7 + moto-mobile#8 (defs v0.8.0, `gps.csv` record/store, bonded subscribe per D-062). CI green, guardians clean. No new decisions.
- 2026-10-08 (local, GPS on BLE): user decided D-062 (bonded subscribe; seq counts MTU-skipped blocks). defs#44 merged (wording); opened defs#45 (D-062) and conn#13 (GPS notify wiring, `GpsNotifyTracker.h`, 9 new tests).
- 2026-10-07 (local, Phase 0 PR batch): merged defs#40, workspace#40, defs#42 (D-059), defs#41 (D-060), conn#11 (GPS parser); released defs v0.7.0 + v0.8.0 (defs#43), pinned v0.8.0; later conn#12 (defs v0.8.0 + GPS block packer).
- 2026-10-03 (local, defs patch + conn bump): defs#34 → defs v0.5.1 (f211781), conn#9 → defs v0.5.1 (03b9b99), manifest pinned. vss CLEAN ×2.
