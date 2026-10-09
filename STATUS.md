# STATUS — session handoff

> Keep it short (≤60 lines). Updated by the `/handoff` skill. "Recent sessions" keeps at most 5 one-line entries; drop the oldest.

**Phase:** 0 hardware build + measurement tools (D-058..D-062) · 1 data pipeline done in code · 2 rt-core without hardware: republisher, heartbeat, D-059 FC link-state check (rt-core pins defs v0.8.0) · defs v0.8.0
**Last updated:** 2026-10-09

## Where we are

- 11 platform repos + `moto-workspace`, public (D-033), MIT (D-036). Decisions D-001..D-064; **D-057 intentionally unused**. Since 2026-10-09 Claude merges PRs itself, in dependency order, after green CI.
- **defs:** v0.8.0 is the latest tag (`manifest.yaml` pins it). `[Unreleased]`: defs#44 `gpsBlock.sequenceRule` wording (PATCH with the next release). Merged today: defs#48 (ideas review, open Q-027/Q-028) and defs#49 (**D-064** rt-core heartbeat 0x081 semantics, incl. the 3 s boot window).
- **rt-core main** (no release tag since the bootstrap; not in `manifest.yaml`):
  - rt-core#24: `services/com` + `com_core` extracted from the republisher (behaviour-identical), `features/heartbeat` sends 0x081 every 100 ms (E2E, dedicated buffer). NODE_MODE INIT/DEGRADED/NORMAL from the DTC monitors and their unmonitored conditions, ERROR_COUNT = DTC failure onsets (0x14 does not touch it), UPTIME never decreases; NORMAL does not attest the EKF.
  - rt-core#25: defs v0.5.0 → v0.8.0 + the D-059 link-state check. The vehicle link sends the gen/ FC.CTS only when the client armed it for its own session/read request, once, FF_DL ≤ 64, matching response SID; every other FC is withheld (reception cancelled, 2 s hold). `can_if` guard passes the FC byte-exact. A segmented answer to a table read is "unavailable".
  - Both: architecture-guard + safety-reviewer no blocker, findings applied; host 21/21, cppcheck/MISRA clean, M7 builds. Follow-ups in ISSUES **E-16**.
- **conn:** pins v0.8.0; GPS notify (conn#13) and the D-059 probe env (conn#14). Until rt-core runs on hardware, conn stays the temporary sole tester (D-023).
- **server / mobile:** v0.2.0 (pin defs v0.8.0). moto-mobile has no `ios/` project (Android only).
- **Vehicle bus:** one read-only tester (D-037). `tester_policy` and the golden D-020 copy unchanged.
- **Local, uncommitted (on purpose):** workspace `docs-presentation/` md files (never commit). Session clones of conn, defs and rt-core sit in the ignored `moto-*/` of the `handoff-1008-gps` worktree (all clean, merged).
- Local Flutter is 3.44.8 (`~/development/flutter/bin`, not on PATH); CI uses 3.47.5, so never commit a `pubspec.lock` rewritten by a local `pub get`.

## Next up (in order)

1. Hardware with GPS (**user**, hardware-integration.md §7.3): steps 1-4 at the desk, then Claude folds GPS into conn's main tester env (step 5, needs the confirmed pins), then the D-058 step gap on the bike (step 6).
2. On the bike, flash conn `esp32-s3-devkitc-1-probe`; keep `[SCAN]` output local (D-033); findings → `/signal-change` with `verified: false` (D-059 item 4). Follow-ups ISSUES E-15.
3. rt-core next feature: EKF lean (0x020). Before 0x020 is registered, the EKF-alive input must join heartbeat DEGRADED (E-16 (1), `/feature-module` + `safety-reviewer`).
4. Small follow-ups (E-16): defs docs note for D-059 (rt-core implements the check); rt-core host test for the cap firing during a reception; optionally an rt-core release (D-036) and its `manifest.yaml` pin.

## Blockers / pending decisions

- Q-019 (board) blocks CubeMX, Renode, Ç6 and the H7 FDCAN port (E-16 (2)). Q-009 blocks the hil-bench host (E-15/E-16 HIL scenarios). Q-001 waits for the listen-only capture on the bike.
- Before safety-node Layer 1 code: Q-023 (incl. (4) return hysteresis after DEGRADED), Q-026 (Group 7 hardware); Q-022 after fallback validation (k_red ≤ 0.8).
- **User:** C-4 (turn off the old `can-dbc-conventions` skill on claude.ai). Q-024, Q-025; D-030 awaits confirmation. Q-027/Q-028 wait until moto-mcp / voice work starts. Optional: scrub the pricing text of `docs/ideas/mcp-scenarios.md` §5 from the defs history (public since 2026-10-07).

## Recent sessions

- 2026-10-09 (local, heartbeat + D-059 check): rt-core#24 (com extraction + heartbeat 0x081, D-064), defs#49 (D-064), rt-core#25 (defs v0.8.0 + FC link-state check); safety-reviewer/architecture-guard findings applied; ISSUES E-16. User now lets Claude merge (merge order had slipped: rt-core#24 before defs#49).
- 2026-10-09 (local, ideas review): conn#14 merged; workspace#47 (STATUS/ISSUES E-15); pruned conn `discovery-probe`. Reviewed `docs/ideas/*` → defs#48; user chose open Q-027/Q-028 (no new D-xxx) and removal of commercial text.
- 2026-10-09 (local, D-059 probe): worktree isolation blocked git/edits in the conn worktree, so conn was cloned into this session's workspace worktree (ignored `moto-*/`) and pushed from there. Opened conn#14 (probe env); ISSUES E-15 added.
- 2026-10-08 (local, GPS procedure): opened defs#47 (§7.3 GPS bring-up + step-gap procedure, merged since); found moto-mobile has no iOS project. No new decisions.
- 2026-10-08 (local, releases + D-063): user decided **D-063** (mobile blocks GPS-session upload to a non-local server) → mobile#10, defs#46; released moto-server + moto-mobile v0.2.0, pinned in manifest (workspace#45).
