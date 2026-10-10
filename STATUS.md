# STATUS — session handoff

> Keep it short (≤60 lines). Updated by the `/handoff` skill. "Recent sessions" keeps at most 5 one-line entries; drop the oldest.

**Phase:** 0 hardware build + measurement tools (D-058..D-062) · 1 data pipeline done in code · 2 rt-core without hardware: republisher, heartbeat, D-059 FC link-state check (rt-core pins defs v0.8.0); EKF lean (D-065) PR 1 of 3 merged (cross-task infra + heartbeat EKF-alive) · defs v0.9.0
**Last updated:** 2026-10-10

## Where we are

- 11 platform repos + `moto-workspace`, public (D-033), MIT (D-036). Decisions D-001..D-065 (open Q up to Q-029); **D-057 intentionally unused**. Since 2026-10-09 Claude merges PRs itself, in dependency order, after green CI.
- **defs:** **v0.9.0** is the latest tag (`manifest.yaml` pins it): defs#52 `lean_angle_clamp_max_deg` = 55 deg (D-065 item 3; codegen: tan(clamp) > k_red·µ_max so CLAMPED reads RED, > atan(µ_max), < 90) + the `gpsBlock.sequenceRule` wording. Merged 2026-10-09: defs#48 (ideas review), defs#49 (**D-064** heartbeat 0x081), defs#50 (D-059 note: rt-core implements the link-state check), defs#51 (**D-065** EKF lean design).
- **rt-core main** (no release tag since the bootstrap; not in `manifest.yaml`):
  - rt-core#24: `services/com` + `com_core` extracted from the republisher (behaviour-identical), `features/heartbeat` sends 0x081 every 100 ms (E2E, dedicated buffer). NODE_MODE INIT/DEGRADED/NORMAL from the DTC monitors and their unmonitored conditions, ERROR_COUNT = DTC failure onsets (0x14 does not touch it), UPTIME never decreases; NORMAL does not attest the EKF.
  - rt-core#25: defs v0.5.0 → v0.8.0 + the D-059 link-state check. The vehicle link sends the gen/ FC.CTS only when the client armed it for its own session/read request, once, FF_DL ≤ 64, matching response SID; every other FC is withheld (reception cancelled, 2 s hold). `can_if` guard passes the FC byte-exact. A segmented answer to a table read is "unavailable".
  - Both: architecture-guard + safety-reviewer no blocker, findings applied; host 21/21, cppcheck/MISRA clean, M7 builds. Follow-ups in ISSUES **E-16**.
  - rt-core#26: SIL tests for the 2000 ms cap firing during a reception after the FC (E-16 (3)); test-only.
  - rt-core#27 (D-065 PR 1): `hal/hal_atomic.h` (host `__atomic`; H7 = PRIMASK save/restore), `services/snapshot` (index-only SPSC triple buffer, no retry, fault latches), `services/alive` + `alive_core`, heartbeat `ekf_stalled` through `app/comms` (`comms_ekf_t`: zeroed = no EKF, never ran/stalled > 60 ms = DEGRADED; no EKF registered yet, so behaviour unchanged). Tests incl. exhaustive interleavings + pthread stress, new `host-tsan` CI job. architecture-guard + safety-reviewer: no blocker, findings applied; M7 text +352 B.
- **EKF lean (D-065, user):** 2-state roll EKF [roll, gyro bias] with tan(roll) = v·yaw rate/g; triple buffers (`services/snapshot`) between the EKF task and comms, comms sends 0x020; CLAMPED from defs `lean_angle_clamp_max_deg`; PRs (0) and (1) done, (2) and (3) open. Carry-overs: ISSUES **E-17**.
- **conn:** pins v0.8.0; GPS notify (conn#13) and the D-059 probe env (conn#14). Until rt-core runs on hardware, conn stays the temporary sole tester (D-023).
- **server / mobile:** v0.2.0 (pin defs v0.8.0). moto-mobile has no `ios/` project (Android only).
- **Vehicle bus:** one read-only tester (D-037). `tester_policy` and the golden D-020 copy unchanged.
- **Local, uncommitted (on purpose):** workspace `docs-presentation/` md files (never commit). Session clones of conn, defs and rt-core sit in the ignored `moto-*/` of the `handoff-1008-gps` worktree (all clean, merged).
- Local Flutter is 3.44.8 (`~/development/flutter/bin`, not on PATH); CI uses 3.47.5, so never commit a `pubspec.lock` rewritten by a local `pub get`.

## Next up (in order)

1. Hardware with GPS (**user**, hardware-integration.md §7.3): steps 1-4 at the desk, then Claude folds GPS into conn's main tester env (step 5, needs the confirmed pins), then the D-058 step gap on the bike (step 6).
2. On the bike, flash conn `esp32-s3-devkitc-1-probe`; keep `[SCAN]` output local (D-033); findings → `/signal-change` with `verified: false` (D-059 item 4). Follow-ups ISSUES E-15.
3. EKF lean per D-065, one PR per session, each with `safety-reviewer` + `vss-schema-guardian`, E-17 items applied:
   (0) ~~defs lean clamp limit + v0.9.0~~ done (defs#52, manifest pin);
   (1) ~~snapshot + alive + heartbeat `ekf_stalled`~~ done (rt-core#27);
   (2) **next:** rt-core `/feature-module` pure lean core (`features/cornering/` core only, float32, `isfinite`, innovation gate, 100 % coverage) + `safety-reviewer`;
   (3) `services/imu`, 0x020 glue (defs bump to v0.9.0), SIL IMU feed, `comms_ekf_register()` before the scheduler + fail-closed 0x020 open, SIL "never ran → DEGRADED" / "1/3 rate → INVALID" tests (E-17).
4. Optional: an rt-core release (D-036, v0.8.0 → v0.9.0) and its `manifest.yaml` pin. Remaining E-16: (2) H7 FDCAN port (Q-019), NITs, (4) HIL scenarios (Q-009).

## Blockers / pending decisions

- Q-019 (board) blocks CubeMX, Renode, Ç6 and the H7 FDCAN port (E-16 (2)). Q-009 blocks the hil-bench host (E-15/E-16 HIL scenarios). Q-001 waits for the listen-only capture on the bike.
- Before safety-node Layer 1 code: Q-029 (plausibility check on the lean clamp), Q-023 (incl. (4) return hysteresis after DEGRADED), Q-026 (Group 7 hardware); Q-022 after fallback validation (k_red ≤ 0.8).
- **User:** confirm that 0x020's open fails closed without a registered EKF counter (E-17; tightens D-065 item 2, architecture-guard). C-4 (turn off the old `can-dbc-conventions` skill on claude.ai). Q-024, Q-025; D-030 awaits confirmation. Q-027/Q-028 wait until moto-mcp / voice work starts. Optional: scrub the pricing text of `docs/ideas/mcp-scenarios.md` §5 from the defs history (public since 2026-10-07).

## Recent sessions

- 2026-10-10 (local, EKF PR 1): `/feature-module` D-065 PR (1) → rt-core#27 merged (snapshot, alive, hal atomics, heartbeat `ekf_stalled` via app/comms, TSan job). architecture-guard + safety-reviewer no blocker (MAJOR: zero-state monitor stalled, fail-closed 0x020 open → E-17). vss-schema-guardian stalled twice; literal check done by grep (clean). CI needed two gcc/cppcheck fixes to the host lock-free check.
- 2026-10-09 (local, lean clamp): `/signal-change` D-065 PR (0): user chose 55 deg; safety-reviewer no blocker (Q-029 opened, MAJOR-1 → E-17); defs#52 merged, **v0.9.0** released and pinned.
- 2026-10-09 (local, EKF plan): EKF judged too big for one PR, so plan only: docs-researcher + architecture-guard (2 BLOCKERs → E-17); user chose **D-065** (defs#51). Small E-16 items done: defs#50, rt-core#26. All merged by Claude.
- 2026-10-09 (local, heartbeat + D-059 check): rt-core#24 (com extraction + heartbeat 0x081, D-064), defs#49 (D-064), rt-core#25 (defs v0.8.0 + FC link-state check); safety-reviewer/architecture-guard findings applied; ISSUES E-16. User now lets Claude merge (merge order had slipped: rt-core#24 before defs#49).
- 2026-10-09 (local, ideas review): conn#14 merged; workspace#47 (STATUS/ISSUES E-15); pruned conn `discovery-probe`. Reviewed `docs/ideas/*` → defs#48; user chose open Q-027/Q-028 (no new D-xxx) and removal of commercial text.
