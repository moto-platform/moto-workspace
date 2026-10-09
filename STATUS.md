# STATUS — session handoff

> Keep it short (≤60 lines). Updated by the `/handoff` skill. "Recent sessions" keeps at most 5 one-line entries; drop the oldest.

**Phase:** 0 hardware build + measurement tools (D-058..D-062) · 1 data pipeline done in code · 2 rt-core without hardware done up to the republisher (rt-core v0.8.0) · defs v0.8.0
**Last updated:** 2026-10-09

## Where we are

- 11 platform repos + `moto-workspace`, public (D-033), MIT (D-036). Decisions D-001..D-063; **D-057 intentionally unused**.
- **defs:** v0.8.0 is the latest tag (`manifest.yaml` pins it). `[Unreleased]`: defs#44 `gpsBlock.sequenceRule` wording (PATCH with the next release). defs#47 merged (GPS bring-up + step-gap procedure, `hardware-integration.md` §7.3). **Open: defs#48** (docs only): `docs/ideas/*` review tables (each Gemini conflict classified CONTRADICTS / EDIT / DECIDE with its D-xxx basis), commercial text removed, HW §5b.7 raw-GPS navigation exception marked superseded by invariant 7 + D-060, new open **Q-027** (moto-mcp write scope) and **Q-028** (voice assistant: templates / local LLM / hybrid cloud, and cloud data scope). architecture-guard no blocker, fixes applied. Waiting for user merge.
- **conn:** pins v0.8.0; main has conn#13 (GPS notify) and **conn#14 (merged 2026-10-09)**: D-059 probe env `esp32-s3-devkitc-1-probe` (`CONN_DISCOVERY_PROBE=1`): one-shot `discovery_scan`, segmented reception (`IsoTpReceiver.h`, `DiscoveryScan.h`), one FC.CTS per answer sent only after a complete drain, RX queue 64 (`hal/CanRxQueue.h`), VIN masked to the WMI (fail-closed), probe env in `check_no_twai_tx.sh` + CI. architecture-guard / safety-reviewer no blocker, vss-schema-guardian CLEAN.
- **server / mobile:** v0.2.0 released (both pin defs v0.8.0). mobile carries the D-063 guard. **moto-mobile has no `ios/` project** (Android only): the iOS bonding check waits (hardware-integration §10 item 8).
- **manifest.yaml** pins defs v0.8.0, server v0.2.0, mobile v0.2.0.
- **Vehicle bus:** one read-only tester (D-037). `tester_policy` and the golden D-020 copy unchanged; only conn's probe env (conn#14) sends the D-059 FC.CTS.
- **Local, uncommitted (left on purpose):** workspace `docs-presentation/` md files (never commit). Session clones of conn and defs sit in the ignored `moto-*/` of the `handoff-1008-gps` worktree (both clean, pushed).
- Local Flutter is 3.44.8 (`~/development/flutter/bin`, not on PATH); CI uses 3.47.5, so never commit a `pubspec.lock` rewritten by a local `pub get`.

## Next up (in order)

1. Hardware with GPS (**user**, procedure in hardware-integration.md §7.3): steps 1-4 at the desk (pins, `[GPS]` serial `pvt/s`, Android bonding + `gps` subscription, upload to the laptop LAN IP), then Claude folds GPS into the main tester env (step 5, needs the confirmed pins), then the D-058 step gap with GPS notify on the bike (step 6).
2. conn#14 is merged; on the bike, flash `esp32-s3-devkitc-1-probe` and keep the `[SCAN]` output local (never commit, D-033); discovered PIDs/DIDs → `/signal-change` with `verified: false` (D-059 item 4, D-029 budget ≤ 0.8). Follow-ups in ISSUES E-15 (defs `sensitive` flag, default-session retry, HIL scenarios).
3. Then: rt-core heartbeat 0x081 or EKF lean (choice still open); rt-core needs the D-059 link-state check + host test before its defs bump (safety-reviewer MINOR-2).

## Blockers / pending decisions

- Q-019 (board) blocks CubeMX, Renode and Ç6. Q-009 blocks the hil-bench host (and the E-15 HIL scenarios). Q-001 waits for the listen-only capture on the bike.
- Before safety-node Layer 1 code: Q-023, Q-026 (Group 7 hardware); Q-022 after fallback validation (k_red ≤ 0.8).
- **User:** C-4 (turn off the old `can-dbc-conventions` skill on claude.ai). Q-024, Q-025; D-030 awaits confirmation. Q-027/Q-028 (after defs#48) wait until moto-mcp / voice work starts. Optional: scrub the pricing text of `docs/ideas/mcp-scenarios.md` §5 from the defs history (public since 2026-10-07).

## Recent sessions

- 2026-10-09 (local, ideas review): conn#14 merged; workspace#47 (STATUS/ISSUES E-15); pruned conn `discovery-probe`. Reviewed `docs/ideas/*` with docs-researcher + architecture-guard → defs#48; user chose open Q-027/Q-028 (no new D-xxx) and removal of commercial text; "JEV" in the Gemini note is undefined.
- 2026-10-09 (local, D-059 probe): mains pulled by the user; worktree isolation blocked git/edits in the conn worktree, so conn was cloned into this session's workspace worktree (ignored `moto-*/`) and pushed from there. Opened conn#14 (probe env, merged 2026-10-09); ISSUES E-15 added. No new decisions. The 2026-10-08 handoff commit e78f219 had missed workspace#46; folded in here.
- 2026-10-08 (local, GPS procedure): opened defs#47 (§7.3 GPS bring-up + step-gap procedure, merged since); found moto-mobile has no iOS project. No new decisions.
- 2026-10-08 (local, releases + D-063): user decided **D-063** (mobile blocks GPS-session upload to a non-local server) → mobile#10, defs#46; released moto-server + moto-mobile v0.2.0, pinned in manifest (workspace#45).
- 2026-10-08 (local, GPS sessions): opened moto-server#7 + moto-mobile#8 (defs v0.8.0, `gps.csv` record/store, bonded subscribe per D-062). No new decisions.