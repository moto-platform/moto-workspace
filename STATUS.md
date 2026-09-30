# STATUS — session handoff

> Keep it short (≤60 lines). Updated by the `/handoff` skill. "Recent sessions" keeps at most 5 one-line entries; drop the oldest.

**Phase:** 1 data pipeline done in code (bench test pending) · 2 rt-core without hardware: ISO-TP, host layer and **Ç3 done: UDS client + UDS server (rt-core v0.4.0)** · safety architecture decided (D-041..D-045) · ISSUES groups 1-2 and **E-1 done (defs v0.3.0)**
**Last updated:** 2026-10-01

## Where we are

- 11 platform repos + `moto-workspace`, public (D-033), MIT (D-036). Decisions D-001..D-048. D-030 awaits confirmation.
- **Releases (all pinned in `manifest.yaml`):** defs **v0.3.0**, rt-core **v0.4.0** (Ç3 client + server, commit 8e4de3a); conn, mobile and server v0.1.0. rt-core and conn submodules still pin defs v0.2.0 or older (bumps in E-4 / C-1).
- **E-1 / D-048 (defs#13 + #14 merged, v0.3.0):**
  - `k_yellow` 0.6 / `k_red` 0.8 (RED leaves 0.6·µ for braking); codegen: 0 < k_y < k_r < 1 and k_r ≤ 0.8 until Q-022
  - speed rules are rt-core's: max age 400 → 300 ms (= stale_after_ms), accel margin only in rt-core's lean estimate; a limits `scope` map keeps them out of `gen/c/safety`
  - 0x021: range 0-255 km/h, 0.01 scale kept (1 km/h source resolution documented), SAFETY off the receivers; codegen `SAFETY_RX_ALLOWED` = EkfLean, EkfFrictionMass, HeartbeatRtCore
  - DID `priority` high | normal (0xF40D high), `VEHICLE_CL250_PRIORITY_*` + `vehicle_cl250_did_t.priority`; tester_policy and golden D-020 unchanged
  - fixed `moto_defs.vehicle_cl250.decode()` (it always raised ValueError); 251 tests, drift clean
  - vss-schema-guardian CLEAN; safety-reviewer no blocker, M1/M2 + m1/m2/m4/m5 applied, m3 → E-4
- **Safety architecture:** D-041 Layer 1 (u = tan|θ|/µ_eff, division-free, NaN → RED, lateral only Q-022), D-042 own-IMU fallback (DEGRADED/UNAVAILABLE, never GREEN), D-043..D-047 as recorded.
- **`ISSUES.md`**: A/B/C/D/E; read only the group you work on. B-8 and E-1 done. Leftover: B-9 (BOM, needs Q-019).
- **Vehicle bus unchanged:** one read-only tester (D-037), Q-020 deferred. Start sessions from the workspace root.

## Next up (in order)

1. **ISSUES group 3, tooling/CI:** C-2 per D-046 (MISRA blocking on defs `gen/c` via codegen templates, with DEV entries e.g. rule 2.5 for header constants; conn cppcheck warning blocking + MISRA report), C-3 `REPO_ASSETS`, C-5 `setup.sh`.
2. **ISSUES group 4, conn alignment:** C-1, now to defs **v0.3.0** (gen/ ISO header, functional watch, 0x021 range 255) with safety-reviewer.
3. **E-4 in rt-core** (`/feature-module moto-rt-core uds`, then safety-reviewer):
   - bump the defs submodule to v0.3.0
   - priority-first scheduler from `vehicle_cl250_did_t.priority`
   - tests: 0xF40D timeout / NRC 0x78, a 301 ms speed sample (lean not ESTIMATED)
   - plus a defs codegen no-starvation bound for `normal` DIDs (safety-reviewer m3)
4. **rt-core Ç1, CAN error state machine + H7 HAL** (ISSUES D-2, `/feature-module moto-rt-core can`, then architecture-guard and safety-reviewer).
5. **Platform-bus republisher** of `vehicle_signals`: NONE/STALE become INVALID, and 0x021 clamps to 255 km/h. No accel margin in the republished value (D-048).
6. **Hardware-dependent (group 6):** A-4 polling budget and PID check in the Q-001 probe (with 0x7DF / 0x18DB33F1), A-5 and E-3 BOM (safety-node IMU, engine mic, engine accelerometer), D-029 measurements, ESP32 + APK end to end.

## Blockers / pending decisions

- Q-019 (board) blocks CubeMX, Renode and Ç6. Q-009 blocks the hil-bench host. Q-020 is deferred (D-037).
- Before safety-node Layer 1 code: Q-023 (fallback details) and Q-026 (LED ring owner), both with the Group 7 hardware. Q-022 comes after fallback validation (k_red ≤ 0.8 until then).
- Q-024 (voice path, ESP32 PSRAM, wake-word default), Q-025 (vibration features). D-030 awaits confirmation. Q-017; Q-014/Q-015 provisional. Q-016, Q-001, Q-003, Q-004, Q-006.

## Recent sessions

- 2026-09-30/10-01 (local, rt-core v0.4.0 release): ws#19/#20 + defs#15 merged, their worktrees pruned; rt-core#10 (VERSION 0.4.0; README/CLAUDE.md no longer say "UDS server / diag not yet"; defs submodule stays v0.2.0) merged after a CI rerun (the first run hung 16 min in "Install toolchains"); v0.4.0 released; ws#21 manifest pin merged. No new decisions.
- 2026-09-30 (local, E-1 `/signal-change`): D-048 by the user (k 0.6/0.8, speed age 300 ms, 0x021 range 255 with scale 0.01, priority high/normal); defs#13 merged (user) before the bump, so defs#14 bumped; defs v0.3.0 released; ws#19 (ISSUES/STATUS), ws#20 (pin) open; vss CLEAN, safety-reviewer no blocker, MAJORs applied.
- 2026-09-30 (local, ISSUES group 2): docs sync by a sonnet subagent, reviewed against D-texts; D-046 (MISRA/coverage, user: "standard-conforming") + D-047 (voice trigger, user: both); defs#12, moto-server#4, ws#17 merged.
- 2026-09-30 (local, ISSUES group 1): ISSUES.md recovered to main (ws#15, its commit had missed ws#14); D-041..D-045 + Q-022..Q-026 decided by the user (defs#11); safety-reviewer no blocker, all MAJORs applied; both merged.
- 2026-09-30 (local, Ç3 server): rt-core v0.3.0 + defs v0.2.0 released and pinned (defs#10, D-040); rt-core#9 UDS server + diag + functional watch merged; arch-guard, vss CLEAN, safety-reviewer ×2.
