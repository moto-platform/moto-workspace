# STATUS — session handoff

> Keep it short (≤60 lines). Updated by the `/handoff` skill. "Recent sessions" keeps at most 5 one-line entries; drop the oldest.

**Phase:** 1 data pipeline done in code (bench test pending) · 2 rt-core without hardware: ISO-TP, host layer and Ç3 UDS client + server done (rt-core v0.4.0) · safety architecture decided (D-041..D-045) · ISSUES groups 1-4, E-1 and C-6..C-8 done · defs v0.3.1
**Last updated:** 2026-10-01

## Where we are

- 11 platform repos + `moto-workspace`, public (D-033), MIT (D-036). Decisions D-001..D-049. D-030 awaits confirmation.
- **Releases (all pinned in `manifest.yaml`):** defs v0.3.1, rt-core v0.4.0, conn/mobile/server v0.1.0. defs v0.3.1 (2026-10-01, defs#19, PATCH) = the MISRA gate and codegen fixes (C-2), the single-exit D-020 gate (C-6) and the cantools/E2E runtime tests (C-7); no API, signal, `tester_policy` or vehicle-bus behaviour change. conn `main` pins defs v0.3.0 (conn#8, no conn release yet); rt-core still pins v0.2.0 (bump to v0.3.1 in E-4). defs CHANGELOG `[Unreleased]` is empty.
- **Group 3 done (2026-10-01):** C-5 `setup.sh`, C-3 safety-reviewer sync, C-2 blocking `make misra` on defs `gen/c` (register `misra/README.md`, DEV-001..005) and blocking cppcheck in conn. rt-core#11 merged.
- **Group 4 done (2026-10-01), conn#8 (C-1):** defs v0.3.0, gen/ `uds_iso14229.h` (conn's own header removed; ISO-TP transport constants in `src/IsoTpCan.h`), foreign-tester watch IDs from `vehicle_cl250_functional_watch[]`. conn's 29-bit watch matches any SA; rt-core's matches 0x18DB33F1 exactly. Vehicle-bus behaviour unchanged.
- **cppcheck is pinned to 2.22.0 in CI** (built from the tag and cached; runner ubuntu-24.04) in defs, conn and rt-core. Ubuntu's apt 2.13 misses findings (15.6 on the canary).
- **C-6/C-7 (2026-10-01), defs#18, released in v0.3.1:** the gate is single-exit with a fail-closed `bool ok = false`; `test_gate_equivalence.py` proves it equal to the old gate (every byte the request/frame gates read, -O0/-O2). DEV-005 and the gate part of DEV-004 are gone; `make misra` clean. safety-reviewer follow-ups are ISSUES C-9.
- **Branch protection on `main` (D-049, C-8, 2026-10-01)** in all 12 repos: PR required (0 approvals), admin bypass on, no force push or deletion. Required checks (strict, github-actions): defs `check`, conn/rt-core `build-and-test`, server `test`, mobile `flutter` + `build-apk`; the other 7 repos (workspace included) have the PR rule only. **No direct pushes to `main`; every change, STATUS included, goes through a PR.** A new repo's first CI workflow must also add its job as a required check.
- **`ISSUES.md`:** sections A-E; read only the group you work on. Open: C-4 (user), C-9, D-*, E-3, E-4, B-9.
- **Vehicle bus unchanged:** one read-only tester (D-037); tester_policy and the golden D-020 copy are untouched. Start sessions from the workspace root.

## Next up (in order)

1. **E-4 in rt-core** (`/feature-module moto-rt-core uds`, then vss-schema-guardian and safety-reviewer):
   - bump the defs submodule v0.2.0 → **v0.3.1** (pin the tag)
   - priority-first scheduler
   - tests for 0xF40D timeout / NRC 0x78 and a 301 ms speed sample
   - defs codegen no-starvation bound (safety-reviewer m3)
2. **rt-core Ç1, CAN error state machine + H7 HAL** (ISSUES D-2, `/feature-module moto-rt-core can`, then architecture-guard and safety-reviewer).
3. **Platform-bus republisher** of `vehicle_signals`: NONE/STALE become INVALID, and 0x021 clamps to 255 km/h (D-048).
4. **Optional:** bump conn's defs submodule to v0.3.1, then a conn release (D-036) so `manifest.yaml` pins a conn tag.
5. **Hardware-dependent (group 6):**
   - A-4 polling budget + PID check in the Q-001 probe (with 0x7DF and 0x18DB33xx from any SA: conn latches on all of them)
   - A-5 and E-3 BOM
   - D-029 measurements
   - ESP32 + APK end to end

## Blockers / pending decisions

- Q-019 (board) blocks CubeMX, Renode and Ç6. Q-009 blocks the hil-bench host. Q-020 is deferred (D-037).
- Before safety-node Layer 1 code: Q-023 (fallback details) and Q-026 (LED ring owner), both with the Group 7 hardware. Q-022 comes after fallback validation (k_red ≤ 0.8 until then).
- **User:** C-4: turn off the old `can-dbc-conventions` skill on claude.ai (still active on 2026-10-01).
- Q-024 (voice path, ESP32 PSRAM, wake-word default), Q-025 (vibration features). D-030 awaits confirmation. Q-017; Q-014/Q-015 provisional. Q-016, Q-001, Q-003, Q-004, Q-006.

## Recent sessions

- 2026-10-01 (local, defs v0.3.1 release): merged defs#18 and ws#28; defs#19 (0.3.1 in pyproject/uv.lock/CLAUDE.md, CHANGELOG rolled; `make check`/`misra`/`drift` green); v0.3.1 released on 34664e0 after green main CI and pinned here. No new decisions.
- 2026-10-01 (local, C-6/C-7): defs#18 (single-exit gate, equivalence proof, cantools/E2E/_MISRA_FIXUPS runtime tests); vss CLEAN, safety-reviewer no blocker (MAJOR-1 + MINOR-2/3/5/6/7 applied, rest → C-9). CI caught a float→int UB on a synthetic 32-bit signal (test fixed, C-9 item 4). C-4 still open.
- 2026-10-01 (local, C-8 / D-049): branch protection applied with `gh api` to the 12 repos and verified per repo (strict checks pinned to github-actions); C-8 done in this workspace PR. User: defs release after C-6/C-7.
- 2026-10-01 (local, ISSUES group 4 / C-1): conn#8 merged (defs v0.3.0, gen/ ISO header, gen/ functional watch, known-answer latch test); vss CLEAN, safety-reviewer no blocker (MINOR-1/2/4 applied, MINOR-3 → Q-001 probe). D-049 (C-8, PR + required CI) via defs#17; ws#26 merged.
- 2026-10-01 (local, ISSUES group 3): merged ws#23/#24, conn#6/#7, linux-node#3, server#5, defs#16; rt-core#11 open (CI green). vss CLEAN; safety-reviewer no blocker (MAJOR-3/4 + MINORs applied, MAJOR-1/2 → C-7/C-6). The canary caught apt cppcheck 2.13 in CI. No new decisions.
