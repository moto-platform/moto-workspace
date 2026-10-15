# STATUS — session handoff

> Keep it short (≤60 lines). Updated by the `/handoff` skill. "Recent sessions" keeps at most 5 one-line entries; drop the oldest.

**Phase:** 0 hardware build (user, ESP32-only data-collection prototype) + measurement tools (D-058..D-062) · 1 data pipeline done in code; D-068: all 40 catalog DIDs polled by conn, unserved ones stopped at runtime · 2 rt-core without hardware: republisher, heartbeat, D-059 FC check, EKF lean (D-065) complete in SIL + `lean_link_t` TSan stress test (E-17 (b)) · defs v0.12.0
**Last updated:** 2026-10-15

## Where we are

- 11 platform repos + `moto-workspace`, public (D-033), MIT (D-036). Decisions D-001..D-068 (open Q up to Q-031); **D-057 intentionally unused**. **The user merges PRs** (since 2026-10-14): Claude opens them, states the merge order, and runs `/handoff` after the merge.
- **Phase 0 build (user):** ESP32-S3 + MPU-6050 + SN65HVD230 + NEO-M8N on the bike; the phone is the only live display (`hardware-integration.md`, defs#55). Check the SN65HVD230 breakout's 120 Ω resistor before connecting.
- **defs v0.12.0** (`manifest.yaml`, defs#60, **D-068**, supersedes D-066 item 3): the 35 J1979 candidates are polled DIDs, `verified: false`, priority normal, after the five verified DIDs (codegen enforces it); tiers 2000 ms (16) / 5000 ms (12) / 10000 ms (7), stale = 3 × period; budget 0.514 → 0.736. `candidates: []`; NRC 0x31 `client: true`. `tester_policy` and gates unchanged. Bus load 2.8 % at 40 DIDs; the ECU slot is the limit. defs#61: `docs/vehicle-data-catalog.md` (every signal read / pollable / discoverable / derivable, switch and ABS paths).
- **conn main** (conn#16, defs v0.12.0, no release): D-068 tester rule in `HondaCANModule`: unverified DIDs only in a confirmed session, all due at each confirmation (`armUnverifiedReads()`), stopped until the next one after NRC 0x31 on 2 reads / 5 timeouts / a First Frame (a positive answer undoes it), no 0x78 extension for them, NRC 0x7E/0x7F re-requests the session. 11 `test_d068_*` tests; safety-reviewer MAJOR-1/2 + MINOR-1/2 applied, vss-schema-guardian clean. BLE block 19+19+2 records at MTU 185. ~2.4 KB more static RAM.
- **mobile / server main** (defs v0.11.0, no release): already decode the D-068 DIDs from the catalog (shown as `candidate` until bumped to v0.12.0). mobile 214 tests, server 102.
- **rt-core main** (defs v0.9.0, no release): #24-#31 (heartbeat, D-059 FC check, D-065 PRs 1-3b, D-067 stress test). **Must not pass defs v0.11.0 before the D-068 rule** (ISSUES **E-19** (1)). Follow-ups E-16, E-17 (a), (c)-(e). Local MISRA needs `--addon-python=/usr/bin/python3` (memory).
- **Vehicle bus:** one read-only tester (D-037). Local: `docs-presentation/` never committed; local Flutter 3.44.8, CI 3.47.5 (never commit a local `pubspec.lock` rewrite).

## Next up (in order)

1. **User, on the bike** (`hardware-integration.md` §6-7) with conn main (defs v0.12.0): desk B0 (conn `-mock` + mobile APK from main), B1/B2, §7.1 listen-only capture (**Q-001**, also the first step of Q-031) before V0, V0 (key on) / V1 (idle) with the tester: the Signals screen shows which D-068 DIDs the CL250 serves (LIVE / NRC 0x31 / skipped), at key-on and after the engine start. GPS §7.3 steps 1-4. Optional probe env (`22 F4 xx` / `01 xx` bitmaps, never `09 02`).
2. Claude, after 1: tune the D-068 tiers from the first rides (`/signal-change`: faster for DIDs with information, drop the dead ones; budget ≤ 0.8), decide **Q-030** with the user (engine-start re-arm, branch `claude/d068-engine-rearm` + the reviewer fixes listed there), define the one-cylinder DEF PIDs 0x01, 0x03 and the O2 PID (`/signal-change`).
3. Claude, after the Q-001 capture: **Q-031** (clutch/neutral/side stand/gear/brake/wheel speed) with `architecture-guard`: broadcast frames into `dbc/cl250.dbc`, or a D-xxx for proprietary-DID discovery or opto-isolated taps.
4. Claude, after GPS steps 1-4: fold GPS into conn's main tester env (step 5), then the D-058 step gap with GPS on the bike (step 6).
5. Claude, without hardware: E-17 (a) per **D-067**: `/signal-change` new rt-core DID **0xFD03 `LEAN_HEALTH`** (fields, `max_age_ms`, fail-safe reading with the user), defs MINOR **v0.13.0**; rt-core bump only together with the D-068 rule (E-19 (1)); `safety-reviewer` + `vss-schema-guardian`. Then µ/mass (cornering Layer 2) needs a plan with `architecture-guard`.
6. Optional: releases (D-036) for conn/mobile/server main + manifest pins; mobile/server bump to v0.12.0 (E-19 (4)); E-18 follow-ups.

## Blockers / pending decisions

- **Q-030** (engine-start re-arm, D-068 amendment) and **Q-031** (switch/brake/wheel-speed source) are new; Q-031 waits for Q-001.
- Q-019 (board) blocks CubeMX, Renode, Ç6 and the H7 FDCAN port. Q-009 blocks the hil-bench host. Q-001 waits for the listen-only capture.
- Before safety-node Layer 1 code: Q-029, Q-023 (incl. (4) return hysteresis after DEGRADED), Q-026 (Group 7 hardware); Q-022 after fallback validation (k_red ≤ 0.8).
- **User:** C-4 (turn off the old `can-dbc-conventions` skill on claude.ai). Q-024, Q-025; D-030 awaits confirmation. Q-027/Q-028 wait for moto-mcp / voice work. Optional: scrub the pricing text of `docs/ideas/mcp-scenarios.md` §5 from the defs history.

## Recent sessions

- 2026-10-15 (local, D-068): user asked for every DID, slow polls, for the anomaly data set → **D-068**, defs#60 **v0.12.0** (released by Claude after the user merged), conn#16 (tester stop rule; safety-reviewer 2 rounds, vss-schema-guardian clean), defs#61 data catalog; engine-start re-arm parked on `claude/d068-engine-rearm` (Q-030); ISSUES E-19. All merged by the user.
- 2026-10-14 (local, E-17 (b)): user chose (b) before (a) and a new DID 0xFD03 for (a) → **D-067** (defs#59); rt-core#31 `test_lean_link_stress` (safety-reviewer 2 rounds), vss-schema-guardian clean; CI coverage fixed with atomic gcov counters. Both merged by the user.
- 2026-10-14 (local, EKF 3b): rt-core#30 merged (lean glue + 0x020; 13 new tests incl. real RAM-fault and 62° CLAMPED SIL); safety-reviewer 2 rounds, vss-schema-guardian clean; user set the EKF WCET budget to 1 ms; defs#58 merged.
- 2026-10-11 (local, D-066 item 4): user approved the BLE block with **DID keys** → defs#57 **v0.11.0**, conn#15, mobile#12, server#9; vss-schema-guardian on each. All merged by Claude; ISSUES E-18.
- 2026-10-11 (local, Phase 0 build + D-066 + mobile redesign): parts on hand (defs#55); user decided **D-066** → defs#56 **v0.10.0**; mobile#11 **v0.3.0** (catalog-driven Signals); manifest pinned (workspace#53).
