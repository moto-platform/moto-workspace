# STATUS — session handoff

> Keep it short (≤60 lines). Updated by the `/handoff` skill. "Recent sessions" keeps at most 5 one-line entries; drop the oldest.

**Phase:** 1 data pipeline done in code (bench test pending) · 2 rt-core without hardware: ISO-TP, host layer and Ç3 UDS client + server done (rt-core v0.4.0) · safety architecture decided (D-041..D-045) · ISSUES groups 1-4, E-1, E-4, E-5, E-7, E-8 and C-6..C-8 done · defs v0.3.1
**Last updated:** 2026-10-01

## Where we are

- 11 platform repos + `moto-workspace`, public (D-033), MIT (D-036). Decisions D-001..D-052. D-030 awaits confirmation.
- **Releases (all pinned in `manifest.yaml`):** defs v0.3.1, rt-core v0.4.0, conn/mobile/server v0.1.0. defs v0.3.1 (2026-10-01, defs#19, PATCH) = the MISRA gate and codegen fixes (C-2), the single-exit D-020 gate (C-6) and the cantools/E2E runtime tests (C-7); no API, signal, `tester_policy` or vehicle-bus behaviour change. conn `main` pins defs v0.3.0 (conn#8, no conn release yet); rt-core `main` pins defs v0.3.1 (rt-core#12, no rt-core release yet; tag v0.4.0 pins v0.2.0). defs `[Unreleased]`: the D-043 no-starvation codegen check (defs#20), the bool timing fix (defs#21, E-6 n3), the D-050/D-051 fault-mode check (defs#23) and D-052 (defs#26: 0xF40C 100/300 in gen/ timing, `poll_period_ms` ≥ base timeout rule, any-DID fault check). rt-core `main` since v0.4.0: E-4, D-050 (rt-core#13), E-6 (rt-core#14), D-051 (rt-core#15), D-052 (rt-core#16).
- **E-4 done (2026-10-01), rt-core#12 + defs#20:** rt-core polls the due DIDs priority-first (gen/ `priority`, 0xF40D high), then table order. A timed-out DID restarts its period at the timeout, and a busy-dropped read keeps its schedule. defs codegen bounds every DID's worst sample gap (non-preemptive fixed priority at `assumed_round_trip_ms`, now required): 140/110/300/960/1000 ms vs `stale_after_ms` 300/150/600/2400/2400. Speed sample VALID at 300 ms, STALE at 301 ms (tested). vss CLEAN, safety-reviewer no blocker.
- **E-5 done (2026-10-01), D-050 (defs#22) + rt-core#13:** a DID whose last read timed out competes in the normal class with no NRC 0x78 extension until it answers or is skipped. Endless 0x78 on 0xF40D: RPM STALE ~25 % (was ~63 %); silent: never. +104 B flash.
- **E-7 done (2026-10-01), D-051 (defs#24) + rt-core#15 + defs#23:** user chose (1) a, (2) a+, (3) yes. A read answered later than its period after its stamp makes the DID faulty for one round (D-050 rules); a sample is stamped with the send time of the DID's oldest unanswered read (ages include the round trip; a late answer never looks younger); ECU absence ends the fault state; `stats.slow_answers`. Slow 0xF40D (SIL, 180 ms): RPM STALE 245/15000 ms (was 14897), speed fail-safe STALE. Cost: one lost frame = two degraded rounds; +24 B RAM, +176 B flash. defs `did_fault_gap_bounds`: 0xF40C 150/150 with 0xF40D faulty. vss CLEAN, safety-reviewer no blocker.
- **E-8 done (2026-10-01), D-052 (defs#25) + defs#26 + rt-core#16:** user chose (1) c, (2) b, (3) a, (4) HIL. RPM 0xF40C poll 50 → 100 ms, stale 300 ms (provisional, 10 Hz); defs requires `poll_period_ms` ≥ `response_timeout_base_ms`; the fault check covers any faulty DID incl. the alternating timeout/answer chain (0xF40C 240/300 … 0xF442 2160/2400). rt-core: a slow answer keeps the skip count (`unanswered` flag), so answer ↔ endless 0x78 is skipped too (RPM STALE 9.3 → 28.1 %, accepted); +20 B RAM, +24 B flash. vss CLEAN, safety-reviewer no blocker/MAJOR (MINOR-2 → E-9).
- **E-6 (1)-(4) done:** rt-core#14 (`not_sent` restores session/TP/read schedules and is not counted, 10 ms step test, +4 B RAM; delta review no blocker), defs#21 (bool timing values refused).
- **Group 3 done (2026-10-01):** C-5 `setup.sh`, C-3 safety-reviewer sync, C-2 blocking `make misra` on defs `gen/c` (register `misra/README.md`, DEV-001..005) and blocking cppcheck in conn. rt-core#11 merged.
- **Group 4 done (2026-10-01), conn#8 (C-1):** defs v0.3.0, gen/ `uds_iso14229.h` (conn's own header removed; ISO-TP transport constants in `src/IsoTpCan.h`), foreign-tester watch IDs from `vehicle_cl250_functional_watch[]`. conn's 29-bit watch matches any SA; rt-core's matches 0x18DB33F1 exactly. Vehicle-bus behaviour unchanged.
- **cppcheck is pinned to 2.22.0 in CI** (built from the tag and cached; runner ubuntu-24.04) in defs, conn and rt-core. Ubuntu's apt 2.13 misses findings (15.6 on the canary).
- **C-6/C-7 (2026-10-01), defs#18, released in v0.3.1:** the gate is single-exit with a fail-closed `bool ok = false`; `test_gate_equivalence.py` proves it equal to the old gate (every byte the request/frame gates read, -O0/-O2). DEV-005 and the gate part of DEV-004 are gone; `make misra` clean. safety-reviewer follow-ups are ISSUES C-9.
- **Branch protection on `main` (D-049, C-8, 2026-10-01)** in all 12 repos: PR required (0 approvals), admin bypass on, no force push or deletion. Required checks (strict, github-actions): defs `check`, conn/rt-core `build-and-test`, server `test`, mobile `flutter` + `build-apk`; the other 7 repos (workspace included) have the PR rule only. **No direct pushes to `main`; every change, STATUS included, goes through a PR.** A new repo's first CI workflow must also add its job as a required check.
- **`ISSUES.md`:** sections A-E; read only the group you work on. Open: C-4 (user), C-9, D-*, E-3, E-6 (5)/(6), E-9 (user), B-9.
- **Vehicle bus unchanged:** one read-only tester (D-037); tester_policy and the golden D-020 copy are untouched. Start sessions from the workspace root.

## Next up (in order)

1. **Optional releases (D-036, user):** rt-core v0.5.0 (E-4, D-050, E-6, D-051, D-052) and defs v0.3.2 (codegen checks + D-052 timing), then pin both in `manifest.yaml`. At rt-core's defs bump to v0.3.2: delete the v0.3.1 slow-RPM starvation test pair (gated on gen/ timing), re-measure the D-052 numbers (STALE shares, gaps) and re-check every 20 Hz RPM assumption for 10 Hz (tests, README, comments).
2. **User decision E-9** (safety-reviewer MINOR-2 on rt-core#16): slowness is judged at the step that sees the answer, not at arrival; with P = B an answer just inside B seen late is slow forever and never skipped. Options: document, defs margin `poll_period_ms` ≥ base + step, or judge against the read's own deadline. Best decided after the D-029 step measurement; then a D-0NN and, if code, `/feature-module moto-rt-core uds` + safety-reviewer.
3. **rt-core Ç1, CAN error state machine + H7 HAL** (ISSUES D-2, `/feature-module moto-rt-core can`, then architecture-guard and safety-reviewer).
4. **Platform-bus republisher** of `vehicle_signals`: NONE/STALE become INVALID, and 0x021 clamps to 255 km/h (D-048).
5. **Optional:** bump conn's defs submodule to v0.3.1, then a conn release (D-036) so `manifest.yaml` pins a conn tag.
6. **Hardware-dependent (group 6), with E-6 (5)/(6):**
   - D-029 bench: ECU round trip + target `uds_client_step()` period → `assumed_round_trip_ms`; check how the CL250 reacts to a new 0x22 after 0x78 (D-050 assumption)
   - HIL fault scenarios (silent / endless-0x78 / slow 0xF40D, answers to abandoned reads (D-051), the D-052 alternations, 0xF40C at 51-99 / 95-100 ms, a single lost frame)
   - A-4 polling budget + PID check in the Q-001 probe (with 0x7DF and 0x18DB33xx from any SA: conn latches on all of them)
   - A-5 and E-3 BOM, D-029 measurements, ESP32 + APK end to end

## Blockers / pending decisions

- Q-019 (board) blocks CubeMX, Renode and Ç6. Q-009 blocks the hil-bench host. Q-020 is deferred (D-037).
- Before safety-node Layer 1 code: Q-023 (fallback details) and Q-026 (LED ring owner), both with the Group 7 hardware. Q-022 comes after fallback validation (k_red ≤ 0.8 until then).
- **User:** merge defs#26 (CLEAN, green) before the defs v0.3.2 release.
- **User:** C-4: turn off the old `can-dbc-conventions` skill on claude.ai (still active on 2026-10-01).
- Q-024 (voice path, ESP32 PSRAM, wake-word default), Q-025 (vibration features). D-030 awaits confirmation. Q-017; Q-014/Q-015 provisional. Q-016, Q-001, Q-003, Q-004, Q-006.

## Recent sessions

- 2026-10-01 (local, E-8 / D-052): user chose (1) c, (2) b, (3) a (kept after the measured 28.1 % cost), (4) HIL. defs#25 and rt-core#16 merged by the user; defs#26 (timing + any-DID fault check) went out of date, was updated with main, CI green, merge left to the user; vss CLEAN, safety-reviewer no blocker/MAJOR (MINOR-1/4 applied, MINOR-2 → E-9). ISSUES: E-8 done, E-6 (6) scenarios, E-9 opened.
- 2026-10-01 (local, E-7 / D-051): user chose (1) a, (2) a+ (instead of a: a misattributed answer would still look ≥ 200 ms younger), (3) yes. defs#23 (fault-mode check), defs#24 (D-051), rt-core#15 merged; vss CLEAN, safety-reviewer no blocker (MAJOR-1/3, MINOR-1/3, NITs applied; MAJOR-2, MINOR-2 → E-8). Pruned 5 merged worktrees.
- 2026-10-01 (local, E-5 / D-050): user chose (c); defs#22 (D-050) + rt-core#13 merged; E-6: defs#21 merged, rt-core#14 (n1/n2/n4). vss CLEAN; safety-reviewer no blocker (MINOR-2/3/4/6 + NITs applied; MAJOR-1, MINOR-5 → E-7). Pruned 7 merged worktrees.
- 2026-10-01 (local, E-4): rt-core#12 (defs v0.3.1, priority-first DID polling, tests vs the D-043 bound, 300/301 ms speed age) + defs#20 (no-starvation codegen check); vss CLEAN, safety-reviewer no blocker (m1-m8 applied, delta re-review clean; E-5 user question, E-6 nits). Worktree prune for the merged rows was refused by the auto-mode classifier: left to the user.
- 2026-10-01 (local, defs v0.3.1 release): merged defs#18 and ws#28; defs#19 (0.3.1 in pyproject/uv.lock/CLAUDE.md, CHANGELOG rolled; `make check`/`misra`/`drift` green); v0.3.1 released on 34664e0 after green main CI and pinned here. No new decisions.
