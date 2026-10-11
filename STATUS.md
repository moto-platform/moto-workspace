# STATUS — session handoff

> Keep it short (≤60 lines). Updated by the `/handoff` skill. "Recent sessions" keeps at most 5 one-line entries; drop the oldest.

**Phase:** 0 hardware build (user, ESP32-only data-collection prototype) + measurement tools (D-058..D-062) · 1 data pipeline done in code, D-066 catalog + generic BLE vehicle-signal block end to end (conn → mobile → server) · 2 rt-core without hardware: republisher, heartbeat, D-059 FC check; EKF lean (D-065) PRs 1, 2, 3a merged, 3b WIP · defs v0.11.0
**Last updated:** 2026-10-11

## Where we are

- 11 platform repos + `moto-workspace`, public (D-033), MIT (D-036). Decisions D-001..D-066 (open Q up to Q-029); **D-057 intentionally unused**. Claude merges PRs itself, in dependency order, after green CI (since 2026-10-09).
- **Phase 0 build (user):** ESP32-S3 + MPU-6050 + SN65HVD230 + NEO-M8N on the bike; the phone is the only live display (`hardware-integration.md`, defs#55). Check the SN65HVD230 breakout's 120 Ω resistor before connecting.
- **defs v0.11.0** (`manifest.yaml`, defs#57): D-066 item 4 `vehicleSignalBlock` (characteristic `vehicleSignals`): 10-byte header + 9-byte records **keyed by DID** (user: DID, not a catalog index; D-066 implementation note), state neverReceived/valid/stale/skipped/negativeResponse (raw = NRC), records per block = floor((MTU − 13) / 9), 1 at MTU 23 (never suspended), ≤ 3 blocks per 200 ms. v0.10.0 = the host-only catalog (35 unpolled candidates). `tester_policy`, polled DIDs and gen/c gates unchanged.
- **conn main** (conn#15, defs v0.11.0, no release): `src/VehicleSignalBlock.h` packer; `HondaCANModule` bookkeeping only (validated answer, non-0x78 NRC outside the post-timeout quiet window, skip cool-down; NRC cleared on timeout/latch). safety-reviewer no blocker, M1-M3 applied; guard test proves sending is unchanged.
- **mobile main** (mobile#12, defs v0.11.0, no release; v0.3.0 = previous release): decoder, Signals screen LIVE per DID (valid within 2000 ms; STALE / SKIPPED / NRC 0x.. / NOT POLLED); a promoted candidate turns LIVE with no code change. `signals.csv` session file (contract in mobile `docs/session-format.md`). 214 tests.
- **server main** (server#9, defs v0.11.0, no release): `signals.csv` ingest (exact header, catalog re-decode, mismatch = warn), `parquet/signals.parquet`, report `vehicle_signals`, index `has_vehicle_signals`. 102 tests.
- **rt-core main** (no release): #24-#29 (heartbeat, D-059 FC check, D-065 PRs 1, 2, 3a). **EKF 3b WIP** `claude/ekf-lean-glue` (c4525e0, pushed, no PR) in the rt-core clone of the `handoff-1008-gps` worktree; defs note branch `claude/d065-pr3a-note` (uncommitted DECISIONS.md) in its defs clone. Follow-ups ISSUES **E-16**, **E-17**.
- **Vehicle bus:** one read-only tester (D-037). Local: `docs-presentation/` never committed; local Flutter 3.44.8, CI 3.47.5 (never commit a local `pubspec.lock` rewrite).

## Next up (in order)

1. **User, on the bike** (`hardware-integration.md` §6-7): desk B0 (conn `-mock` + mobile APK from main), B1/B2, §7.1 listen-only capture (Q-001) before V0, V0/V1 with the tester, GPS §7.3 steps 1-4.
2. **User:** flash conn `esp32-s3-devkitc-1-probe` once; keep `[SCAN]` local (D-033); paste Claude the `22 F4 00/20/40/60` and `01 00/20/40/60` blocks (header, `+000:` hex, `supported:`) and the `done:` line, **never `09 02` (VIN)**. The 2026-10-11 session got only the template placeholder.
3. Claude, after 2 (D-066 item 3): decode the bitmaps, show a supported/unsupported table, then `/signal-change` move supported candidates into `uds/vehicle_cl250.yaml` (`verified: false`, appended at the table end, conn polls in table order), `priority: normal`, `stale_after_ms` = 3 × period. Proposed tiers (user not yet confirmed): A 1000 ms (load, MAP, timing, IAT, STFT, lambda, grip/throttle variants, injection timing, fuel rate, torque %), B 5000 ms (LTFT, pressures, purge, fuel level, ethanol, baro, ambient, oil, catalyst), C 10000 ms (run time, distance/time counters, warm-ups, reference torque). Today's budget 0.514; ≤ 0.8 (D-029); D-053 floor holds. `safety-reviewer` + `vss-schema-guardian`, defs release, manifest pin, conn bump.
4. Claude, after GPS steps 1-4: fold GPS into conn's main tester env (step 5), then the D-058 step gap with GPS on the bike (step 6).
5. EKF 3b (D-065): finish `claude/ekf-lean-glue` (rebase), coverage of `lean_tx.c`/`comms.c`, mutation checks, docs (cornering README priority table, boot order, WCET), `safety-reviewer` + `vss-schema-guardian`, PR, merge; also the defs D-065 3a note PR.
6. Optional: releases (D-036) for conn/mobile/server main on defs v0.11.0 + manifest pins; rt-core release. E-18 follow-ups (HIL vsig scenario, Record-screen status line, server cross-checks).

## Blockers / pending decisions

- D-066 item 3 waits for the probe output; the poll-period tiers above need user confirmation.
- Q-019 (board) blocks CubeMX, Renode, Ç6 and the H7 FDCAN port. Q-009 blocks the hil-bench host. Q-001 waits for the listen-only capture.
- Before safety-node Layer 1 code: Q-029, Q-023 (incl. (4) return hysteresis after DEGRADED), Q-026 (Group 7 hardware); Q-022 after fallback validation (k_red ≤ 0.8).
- **User:** C-4 (turn off the old `can-dbc-conventions` skill on claude.ai). Q-024, Q-025; D-030 awaits confirmation. Q-027/Q-028 wait for moto-mcp / voice work. Optional: scrub the pricing text of `docs/ideas/mcp-scenarios.md` §5 from the defs history.

## Recent sessions

- 2026-10-11 (local, D-066 item 4): bitmap paste missing (template placeholder), so promotion deferred; user approved the BLE block with **DID keys** → defs#57 **v0.11.0**, conn#15 (packer + tester bookkeeping; safety-reviewer M1-M3 applied), mobile#12 (decoder, Signals LIVE, `signals.csv`) and server#9 (ingest) via sonnet subagents; vss-schema-guardian on each (server state literals fixed). All merged by Claude; ISSUES E-18.
- 2026-10-11 (local, Phase 0 build + D-066 + mobile redesign): parts on hand (defs#55); user decided **D-066** → defs#56 **v0.10.0**; mobile#11 **v0.3.0** (catalog-driven Signals); manifest pinned (workspace#53).
- 2026-10-10/11 (local, EKF PR 3): user split PR 3 into 3a/3b; rt-core#29 (3a) merged after safety-reviewer 2 rounds; 3b coded + tested, pushed as WIP.
- 2026-10-10 (local, EKF PR 2): fail-closed 0x020 (defs#53); rt-core#28 pure lean core (defs#54); safety-reviewer 4 MAJORs fixed with mutation-checked tests.
- 2026-10-10 (local, EKF PR 1): rt-core#27 (snapshot, alive, hal atomics, heartbeat `ekf_stalled`, TSan job); MAJORs → E-17.
