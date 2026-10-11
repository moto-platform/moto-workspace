# STATUS — session handoff

> Keep it short (≤60 lines). Updated by the `/handoff` skill. "Recent sessions" keeps at most 5 one-line entries; drop the oldest.

**Phase:** 0 hardware build (user, ESP32-only data-collection prototype; parts on hand) + measurement tools (D-058..D-062) · 1 data pipeline done in code, mobile v0.3.0 shows the D-066 catalog · 2 rt-core without hardware: republisher, heartbeat, D-059 FC check; EKF lean (D-065) PRs 1, 2, 3a merged, 3b WIP · defs v0.10.0
**Last updated:** 2026-10-11

## Where we are

- 11 platform repos + `moto-workspace`, public (D-033), MIT (D-036). Decisions D-001..D-066 (open Q up to Q-029); **D-057 intentionally unused**. Claude merges PRs itself, in dependency order, after green CI (since 2026-10-09).
- **Phase 0 build (user, 2026-10-11):** further feature work pauses; the user mounts ESP32-S3 + MPU-6050 + SN65HVD230 + NEO-M8N on the bike and collects data. The phone is the only live display; the Nextion is deferred (`hardware-integration.md`, defs#55). Check the SN65HVD230 breakout's 120 Ω resistor before connecting.
- **defs v0.10.0** (`manifest.yaml`): D-066 host-only signal catalog (defs#56): `uds/vehicle_cl250_candidates.yaml` = 35 scalar J1979 PIDs as DIDs 0xF400 | PID, **not polled**, no `gen/c` change; generated `vehicle_catalog.py` + `vehicle_signals.dart` merge them with the 5 polled DIDs. vss-schema-guardian PASS. D-066 item 4: generic BLE vehicle-signal block = direction only, layout still to define.
- **mobile v0.3.0** (mobile#11, pins defs v0.10.0, `manifest.yaml`): dark high-contrast M3 redesign; Live, Signals (every catalog signal: LIVE / STALE / NO DATA / NOT POLLED), Record, Diagnostics, Settings. Models, services, session format and D-063 unchanged; 166 tests. Not yet tried on a phone. Android only (no `ios/`).
- **conn:** pins defs v0.8.0; GPS notify (conn#13), D-059 probe env (conn#14). Temporary sole tester until rt-core runs on hardware (D-023). The user's own conn checkout lacked the probe env (needs `git pull`).
- **server:** v0.2.0 (pins defs v0.8.0); does not use the catalog yet.
- **rt-core main** (no release since the bootstrap): #24 heartbeat 0x081 + `services/com`; #25 defs v0.8.0 + D-059 FC link-state check; #26 SIL cap tests; #27 (D-065 PR 1) snapshot/alive/heartbeat `ekf_stalled`; #28 (PR 2) pure `lean_core`; #29 (PR 3a) `hal/imu.h` + `services/imu` (interval-mean rates, z offset at standstill, fail-closed). Follow-ups ISSUES **E-16**, **E-17**.
- **EKF 3b WIP:** branch `claude/ekf-lean-glue` (c4525e0, pushed, **no PR**) in the rt-core clone of the `handoff-1008-gps` worktree: `features/cornering/lean` task, `lean_tx`/`lean_tx_core` (0x020, clamp 55°, 35 ms age budget), `comms_open_lean()` fail-closed, defs v0.9.0, SIL EKF + IMU feed; 32/32 host tests. Its STATUS/ISSUES draft and a defs note branch (`claude/d065-pr3a-note`, uncommitted DECISIONS.md) are still uncommitted in that worktree's clones.
- **Vehicle bus:** one read-only tester (D-037); `tester_policy` and the golden D-020 copy unchanged.
- Local: workspace `docs-presentation/` md files never committed. Local Flutter 3.44.8 (`~/development/flutter/bin`), CI 3.47.5: never commit a `pubspec.lock` rewritten by a local `pub get`.

## Next up (in order)

1. **User, on the bike** (`hardware-integration.md` §6-7): desk B0 with conn `-mock` + mobile v0.3.0 APK (`gh run download -R moto-platform/moto-mobile -n moto-mobile-apk`; Signals shows 5 LIVE + 35 NOT POLLED), B1/B2, then §7.1 listen-only capture (Q-001) before V0, V0/V1 with the tester, GPS §7.3 steps 1-4 at the desk.
2. **User:** flash conn `esp32-s3-devkitc-1-probe` on the bike once; keep `[SCAN]` local (D-033); hand Claude the 0x22 0xF4xx / OBD 0x01 support bitmaps (no VIN).
3. Claude, after 2: `/signal-change` promote the supported candidates into `uds/vehicle_cl250.yaml` (`verified: false`, slow periods, D-043 priority chosen with the user, D-029 budget ≤ 0.8, D-053 floor); mark unsupported ones. Then D-066 item 4: `/signal-change` the generic BLE vehicle-signal block (layout + MTU rule with user confirmation), conn packer (`/feature-module`-style, native tests), mobile decoder → Signals LIVE, server ingest; `vss-schema-guardian` on each.
4. Claude, after GPS steps 1-4: fold GPS into conn's main tester env (step 5, confirmed pins), then the D-058 step gap with GPS on the bike (step 6).
5. EKF 3b (D-065): finish `claude/ekf-lean-glue` (rebase on origin/main): cover open branches in `lean_tx.c`/`comms.c`, mutation-check clamp/age/switch/fail-closed open/alive bump, docs (cornering README task-priority table EKF > comms, boot order, EKF WCET; app/heartbeat README; rt-core CLAUDE.md pin), `safety-reviewer` + `vss-schema-guardian`, PR, merge; also the defs D-065 3a note PR.
6. Optional: rt-core release (D-036) + manifest pin. Remaining E-16: (2) H7 FDCAN port (Q-019), NITs, (4) HIL scenarios (Q-009).

## Blockers / pending decisions

- Candidate promotion (D-066 item 3) waits for the probe output on the bike; the generic BLE block layout (D-066 item 4) needs user confirmation.
- Q-019 (board) blocks CubeMX, Renode, Ç6 and the H7 FDCAN port. Q-009 blocks the hil-bench host. Q-001 waits for the listen-only capture.
- Before safety-node Layer 1 code: Q-029, Q-023 (incl. (4) return hysteresis after DEGRADED), Q-026 (Group 7 hardware); Q-022 after fallback validation (k_red ≤ 0.8).
- **User:** C-4 (turn off the old `can-dbc-conventions` skill on claude.ai). Q-024, Q-025; D-030 awaits confirmation. Q-027/Q-028 wait for moto-mcp / voice work. Optional: scrub the pricing text of `docs/ideas/mcp-scenarios.md` §5 from the defs history.

## Recent sessions

- 2026-10-11 (local, Phase 0 build + D-066 + mobile redesign): explained what runs on the bike now (conn + mobile + server; rt-core waits for Q-019); recorded the parts on hand (defs#55). User decided **D-066** (all candidate signals defined, polled only after the probe, generic BLE block later) → defs#56, **v0.10.0**. flutter-expert redesigned moto-mobile (dark, catalog-driven Signals screen) → mobile#11, **v0.3.0**; manifest pinned (workspace#53).
- 2026-10-10/11 (local, EKF PR 3): user split PR 3 into 3a/3b; chose 20 ms EKF, ODR ≥ 800 Hz FIFO interval mean, z offset 2 s standstill (≤ 2 deg/s, 3-axis stillness), fail-closed. rt-core#29 (3a) merged after safety-reviewer 2 rounds; 3b coded + tested, pushed as WIP.
- 2026-10-10 (local, EKF PR 2): fail-closed 0x020 (defs#53); rt-core#28 pure lean core (100 ms gate window, QUALITY ≤ 50, h at speed + margin, defs#54); safety-reviewer 4 MAJORs fixed with mutation-checked tests.
- 2026-10-10 (local, EKF PR 1): rt-core#27 (snapshot, alive, hal atomics, heartbeat `ekf_stalled`, TSan job); MAJORs → E-17.
- 2026-10-09 (local, lean clamp): D-065 PR (0): 55 deg; Q-029 opened; defs#52, **v0.9.0** released and pinned.
