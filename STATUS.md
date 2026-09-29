# STATUS — session handoff

> Keep it short (≤60 lines). Updated by the `/handoff` skill. "Recent sessions" keeps at most 5 one-line entries; drop the oldest.

**Phase:** 1 data pipeline done in code (bench test pending) · 2 rt-core without hardware: ISO-TP + host layer done (v0.2.0), Ç3 next
**Last updated:** 2026-09-29

## Where we are

- 11 platform repos + `moto-workspace`, public (D-033), MIT (D-036). Decisions D-001..D-038 (D-037/D-038 in defs#7). D-030 still awaits confirmation.
- **Releases:** rt-core **v0.2.0** (`c39407f`, host layer + ISO-TP link + D-020 guard); defs, connectivity-node, mobile, server v0.1.0. Manifest pin for rt-core v0.2.0: workspace#8.
- **Vehicle bus scope (D-037, user):** the CL250 only answers requests, so the vehicle bus is not listen-only: one tester (rt-core) that only reads. What it may send lives only in `uds/vehicle_cl250.yaml` → `tester_policy` (narrow-only, D-027). Q-020 (FC.CTS) **deferred**: Ç3 client uses Single Frame responses only.
- **Consistency pass (open PRs, merge in this order):**
  1. defs#7: docs contradictions fixed (hardware-architecture topology, vehicle-work-plan bus note, stale D-001/9/13/14/33/34), English Ç1-Ç8 table in ARCHITECTURE §9, `docs/tr` → `docs/archive/tr` (D-038, Claude may not read it).
  2. workspace#9: PLATFORM-RULES invariant 1 rewritten, release procedure, agents/skills reference single sources, `Read(**/docs/archive/**)` denied.
  3. Sync PRs `chore: sync platform rules` in all 11 repos (defs#8, safety#2, io#2, hil#2, conn#5, linux#2, mcp#2, server#3, ml#2, mobile#6, plus rt-core#4). Skeleton READMEs filled; conn/server/rt-core CI fail unless defs is on a `vX.Y.Z` tag.
  4. rt-core#4 (CI green): MISRA addon **blocking** with a deviation register (`misra/`), coverage floors 95/80 % (gcc: 97.3 % lines / 88.2 % branches), CLAUDE.md rules renumbered. safety-reviewer ×2 + vss-schema-guardian: no blocker.
- Worktrees: `python3 scripts/worktrees.py` (workspace#7) reports and prunes them; `.claude/worktrees/` is excluded in every repo.
- User-level duplicates of `safety-reviewer`, `vss-schema-guardian` and `can-dbc-conventions` moved to `~/.claude/archive/moto-user-level-2026-09-29/` (they shadowed the project agents). The claude.ai-synced `can-dbc-conventions` skill must be turned off on claude.ai.
- Q-019 (board) still open: no CubeMX project, startup or linker script. `moto-apk/` left as is until the mobile rework.

## Next up (in order)

1. **User:** merge defs#7 → workspace#9 → the 11 sync PRs (rt-core#4 last) → workspace#8 (manifest) and this STATUS PR. Then `python3 scripts/worktrees.py --prune`.
2. **rt-core Ç3, UDS client (vehicle poller) on `isotp_link`** (`/feature-module moto-rt-core uds`, start the session from the workspace root):
   - D-020 session handling: `0x10 03` (retry until 0x50), `0x3E 80` every 1 s, from gen/.
   - Round-robin over the gen/ DIDs with poll/stale periods, one request in flight.
   - `N_TIMEOUT_CR` = "unavailable" + `VEHICLE_CL250_DID_SKIP_COOLDOWN_MS`; wait ≥ N_Bs after an aborted segmented response (uds README).
   - SIL against the simulated ECU; keep target-m7 building. safety-reviewer + vss-schema-guardian.
3. **rt-core Ç3, UDS server (platform bus):** server IDs and own DIDs via `/signal-change` (`uds/dids.yaml`, platform.dbc), then 0x10 / 0x3E / 0x22 / 0x19 / 0x14, NRCs, P2 / P2* / S3.
4. **rt-core Ç1, CAN error state machine** behind `hal/can_port` (bus-off recovery, error counters), host tests.
5. **Standards follow-ups:** MISRA step for defs `gen/c` (the D-020 gates are unchecked today); per-repo hooks / `settings.json` for the safety rules; Q-006 (HARA/FMEA/requirements location) for Ç8 traceability.
6. **Workshop (ESP32 on USB):** mock env + APK, BLE → recording → upload end-to-end; connectivity#3 bench checks.
7. **Small follow-ups:** BLE latch wording (3 repos); moto-server `session_id` validation + unzip cap; mobile BLE schema fetched from connectivity `main` (pin it during the mobile rework); swap rt-core `app/host/sim_ecu` for the hil-bench live model (D-035).
8. **Hardware / measurement:** OBD chain; mass, weight split, rolling radius, tire pressures → replace the D-029 provisional values.
9. **Skeleton repos:** tag `v0.1.0` when they get code (`/repo-bootstrap` adds CI then).

## Blockers / pending decisions

- Q-019 (board) blocks CubeMX, Renode and Ç6. Q-009 (first HIL test function) blocks the hil-bench host. Q-020 deferred (D-037).
- D-030 awaits confirmation. Q-017 (BLE schema in defs codegen). Q-014/Q-015: provisional D-029 values until measured.
- Q-002, Q-016 remainder, Q-001 remainder, Q-003, Q-004 (bridge format), Q-006 (requirements location, needed for Ç8).

## Recent sessions

- 2026-09-29 (local, consistency pass): rt-core v0.2.0 released; worktree lifecycle script (ws#7); 3-way audit (docs, Claude setup, code standards); D-037 read-only vehicle tester, D-038 tr archive; rules single-sourced + synced to 11 repos; rt-core blocking MISRA + coverage; Q-020 deferred.
- 2026-09-28 (local, rt-core glue): v0.1.0 releases for conn/mobile/server/rt-core, manifest pinned; rt-core#2 host layer + ISO-TP link + can_if D-020 guard + SIL (safety-review blocker fixed); Q-020 (defs#6).
- 2026-09-28 (local): Q-018 hardening (connectivity#3, 2 safety-review rounds) merged; D-032 confirmed (defs#4); repo secrets set, server#1 merged; APK downloaded; rt-core bootstrapped + ISO-TP core (rt-core#1); D-034 proposed, Q-018 closed (defs#5).
- 2026-09-27 (local, cont.): merged connectivity#2, mobile#4 (BLE v3, IMU, upload), defs#3 (D-032, Q-017/Q-018), workspace#3; moto-server#1 waited for the secret; repos made public (D-033, history scanned clean).
- 2026-09-27 (cloud, data pipeline): BLE schema v3 + IMU blocks (conn#2, CI green), mobile v3/imu.csv/upload (mobile#4), moto-server bootstrap (server#1); D-032 proposed, Q-017/Q-018; guardians + safety review done.
