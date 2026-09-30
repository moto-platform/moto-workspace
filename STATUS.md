# STATUS — session handoff

> Keep it short (≤60 lines). Updated by the `/handoff` skill. "Recent sessions" keeps at most 5 one-line entries; drop the oldest.

**Phase:** 1 data pipeline done in code (bench test pending) · 2 rt-core without hardware: ISO-TP, host layer and **Ç3 done: UDS client + UDS server** · safety architecture decided (D-041..D-045); ISSUES group 2 (docs sync) next
**Last updated:** 2026-09-30

## Where we are

- 11 platform repos + `moto-workspace`, public (D-033), MIT (D-036). Decisions D-001..D-045. D-030 awaits confirmation.
- **Releases (manifest pinned):** defs **v0.2.0**, rt-core **v0.3.0** (the Ç3 client); conn, mobile and server v0.1.0. rt-core `main` also has the Ç3 server (rt-core#9), **not tagged yet**.
- **rt-core Ç3 UDS server (rt-core#9):**
  - platform bus only: 0x710/0x718, functional 0x7DF
  - services 0x10/0x3E/0x22/0x19/0x14, own DIDs/DTCs, fail-safe tester status
  - checks: ctest 13/13, coverage 97.4 % / 90.7 %, MISRA clean; reviews in the uds README
- **Safety architecture (defs#11, ws#15, merged; ISSUES group 1 done):**
  - **D-041 Layer 1:** u = tan|θ| / µ_eff against k_yellow < k_red. The comparison is division-free and NaN gives RED. Speed and mass are **not** safety-node inputs; the speed-age rules move to rt-core. Lateral only (Q-022).
  - **D-042 (Q-002 closed):** safety-node gets its own IMU as a fallback. In fallback µ ≤ 0.5 and the ring shows DEGRADED; with no source it shows UNAVAILABLE, never GREEN. Open: Q-023, and the ring owner Q-026 (never rt-core).
  - **D-043:** a `priority` field per DID (order only). **D-044:** the sensor → node map, with no raw audio or vibration on CAN or VSS. **D-045:** BLE loss accepted, persistent logging belongs to rt-core.
  - safety-reviewer: no blocker, M1-M4 and m1-m8 applied in the D-texts.
- **`ISSUES.md`** (now on main): A/B/C/D + section E, the follow-ups of D-041..D-045. Read only the group you work on.
- **Vehicle bus unchanged:** one read-only tester (D-037), Q-020 deferred. Start sessions from the workspace root.

## Next up (in order)

1. **ISSUES group 2, docs sync** (a sonnet subagent edits, you review):
   - B-1, B-2, B-4, B-7, B-8
   - E-2: hardware §5b.2/§5b.6/§5b.7/§5b.9, ARCHITECTURE §3/§4 Q-002 lines, and the Phase 0 plan "superseded in part"
   - the D-034 text, after the C-2 decision
2. **E-1 `/signal-change`** (defs minor, safety-reviewer on the whole change):
   - `k_yellow`/`k_red` in `platform_limits.yaml`, plus a codegen check 0 < k_y < k_r < 1
   - speed rules re-scoped to rt-core
   - 0x021 range
   - the limits header
   - `priority` in `vehicle_cl250.yaml`
3. **rt-core v0.4.0 (the Ç3 server):**
   - `project(VERSION 0.4.0)` PR, merge when green
   - `gh release create v0.4.0 -R moto-platform/moto-rt-core --target main --title v0.4.0 --generate-notes`
   - pin the tag in `manifest.yaml`
4. **ISSUES group 3, tooling/CI:** C-2 MISRA for defs `gen/c` + conn (decision first), C-3 `REPO_ASSETS`, C-5 `setup.sh`.
5. **ISSUES group 4, conn alignment:** C-1 (defs v0.2.0, gen/ ISO header, functional watch) with safety-reviewer.
6. **rt-core Ç1, CAN error state machine + H7 HAL** (ISSUES D-2, `/feature-module moto-rt-core can`, then architecture-guard and safety-reviewer). After E-1, the priority scheduler (E-4).
7. **Platform-bus republisher** of `vehicle_signals` (NONE/STALE become INVALID). 0x021 keeps E2E for its other consumers; safety-node no longer reads it (D-041).
8. **Hardware-dependent (group 6):** A-4 polling budget and PID check in the Q-001 probe (with 0x7DF / 0x18DB33F1), A-5 and E-3 BOM (safety-node IMU, engine mic, engine accelerometer), D-029 measurements, ESP32 + APK end to end.

## Blockers / pending decisions

- Q-019 (board) blocks CubeMX, Renode and Ç6. Q-009 blocks the hil-bench host. Q-020 is deferred (D-037).
- Before safety-node Layer 1 code: Q-023 (fallback details) and Q-026 (LED ring owner), both with the Group 7 hardware. Q-022 comes after fallback validation.
- Q-024 (voice path, ESP32 PSRAM), Q-025 (vibration features). D-030 awaits confirmation. Q-017; Q-014/Q-015 provisional. Q-016, Q-001, Q-003, Q-004, Q-006.

## Recent sessions

- 2026-09-30 (local, ISSUES group 1): ISSUES.md recovered to main (ws#15, its commit had missed ws#14); D-041..D-045 + Q-022..Q-026 decided by the user (defs#11); safety-reviewer no blocker, all MAJORs applied; both merged.
- 2026-09-30 (local, Ç3 server): rt-core v0.3.0 + defs v0.2.0 released and pinned (defs#10, D-040); rt-core#9 UDS server + diag + functional watch merged; arch-guard, vss CLEAN, safety-reviewer ×2.
- 2026-09-29/30 (local, rt-core Ç3 client): UDS client + vehicle_signals (rt-core#5, #6 merged); D-039 + Q-021; vss ×2, safety-reviewer ×2 (all MAJORs fixed).
- 2026-09-29 (local, consistency pass): rt-core v0.2.0; worktree lifecycle script (ws#7); 3-way audit; D-037, D-038; rules single-sourced + synced; rt-core blocking MISRA + coverage; Q-020 deferred.
- 2026-09-28 (local, rt-core glue): v0.1.0 releases for conn/mobile/server/rt-core; rt-core#2 host layer + ISO-TP link + can_if D-020 guard + SIL; Q-020 (defs#6).
