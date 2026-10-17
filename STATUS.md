# STATUS — session handoff

> Keep it short (≤60 lines). Updated by the `/handoff` skill. "Recent sessions" keeps at most 5 one-line entries; drop the oldest.

**Phase:** 0 hardware build (user, ESP32-only data-collection prototype) + measurement tools (D-058..D-062) · 1 data pipeline done in code; D-068/D-069 in conn (rt-core in draft #33) · D-070 derived signals: defs definitions + server Python reference parts 1-3 + golden vectors done, rt-core `features/derived` next · 2 rt-core without hardware: republisher, heartbeat, D-059 FC check, EKF lean (D-065) · defs v0.14.0
**Last updated:** 2026-10-17

## Where we are

- 11 platform repos + `moto-workspace`, public (D-033), MIT (D-036). Decisions D-001..D-071 (open Q up to Q-031); **D-057 intentionally unused**. Normally **the user merges PRs**; the 2026-10-17 autonomous session merged with the user's written authorisation (green CI + reviewers).
- **Phase 0 build (user):** desk B0 passed 2026-10-15. ESP32-S3 (FT232R `/dev/cu.usbserial-A5069RR4`), IMU MPU-6500 on SDA GPIO7 / SCL GPIO6 (header unsoldered), CAN GPIO4/5, GPS GPIO15/16. Not wired yet: SN65HVD230 (check its 120 Ω), DLC adapter, NEO-M8N. Data path by zip → `moto-server import` into `~/moto-data` (never in a repo). Mac has Java 8: APKs from CI.
- **Releases (all in `manifest.yaml`):** defs **v0.14.0** (d65ab9a: 0xFD03 `LEAN_HEALTH` definition, derived `stale_after_ms` ≥ slowest input period + codegen check, D-070 implementation part 3); conn **v0.2.0** (55f5e2c, defs v0.12.0, `PROJECT_VER` in the image); server **v0.3.0** (3b2fa67, defs v0.14.0); mobile **v0.4.0** (b0fff1c, 0.4.0+5, defs v0.14.0). rt-core v0.8.0 (pins defs v0.5.0; main pins v0.9.0).
- **moto-server derived reference (D-070 item 2):** 34 class-A signals (`derived.parquet`, event kind with `stop_event`), 19/46 class-B ride summaries (`derived_summary.parquet`, one session = one ride), `moto-server derive`; `moto-server golden --out <rt-core>/tests/host/vectors` writes synthetic C-header vectors (28 signals, 4 scenarios, drift manifest `tests/golden/MANIFEST.sha256`; the expected values need the defs **v0.14.0** derived table). Unimplemented signals carry a `not_implemented` reason (missing threshold/definition).
- **conn main:** D-068 stop rule, D-069 re-ask, conn#20 timeout-log rate limit + long-gap test (202 native tests).
- **rt-core open drafts:** **#33** D-068 rule + D-069 re-ask, defs v0.13.0 (E-19 (1)+(5)); safety-reviewer no BLOCKER, MAJOR-1 + MINORs fixed, CI green; **open:** MAJOR-2 (NRC 0x7E/0x7F loop re-arms all unverified DIDs; also in conn), ENGINE_SPEED 280 ms vs the 260 ms D-068 bound with VEHICLE_SPEED faulty, N_Bs hold repeated per failed unverified reception (verified DIDs STALE ~35 s). **#34** golden vectors + shape test, stacked on #33.
- **Vehicle bus:** one read-only tester (D-037); `tester_policy` and the gates unchanged all session. Local: Flutter 3.44.8 vs CI 3.47.5 (never commit a local `pubspec.lock` rewrite); local MISRA needs `--addon-python=/usr/bin/python3`.

## Next up (in order)

1. **User:** decide the three open items of rt-core#33 (comment on the PR: MAJOR-2 option (a) or (b), the 260 ms bound, the N_Bs hold); then Claude applies it in rt-core **and conn**, records the decision (D-072), re-runs `safety-reviewer`, merges #33, retargets #34 to main and merges it.
2. **User + Claude, vehicle data path:** solder the IMU header; wire SN65HVD230 + adapter; B2 on the desk with conn v0.2.0; on the bike §7.1 listen-only capture (**Q-001**) before V0/V1, probe env at key-on and warm idle (D-069 item 2), GPS §7.3 steps 1-4. Read the HDS data list (CL250 service manual, PGM-FI) before §3.1 discovery.
3. **User:** threshold/definition proposals for the not-implemented derived signals (list in the 2026-10-17 report: clutch/neutral, shift/launch/braking/pitch/refuel events, wheel slip, road roughness band, VE/intake models, heat soak, charging, cold-abuse/over-rev/lugging, idle quality, fuel cut, fuel-level filter, data-quality mask, warm-up/thermal cycles/fan, final drive, speedometer, aggressiveness weights) → `/signal-change` (defs) then server formulas.
4. Claude, without hardware: E-17 (a) in rt-core (0xFD03 handler per defs v0.14.0, `/feature-module`, `safety-reviewer`), then rt-core defs v0.14.0 and the `features/derived` module against the golden vectors (`architecture-guard`).
5. Claude, after 2: tune the D-068 tiers (`/signal-change`, budget ≤ 0.8); define 0x01, 0x03, the O2 PID, §2.1 PIDs; then Q-031 (broadcast frames, probe-mode decision) and GPS into conn's main env.
6. Small: server ingest evaluates class A twice (derived + summary); store `can_bus_off_count`; export DID `stale_after_ms` in `moto_defs` Python (server uses 3 × period for events); E-18; HIL scenarios of E-19 (2).

## Blockers / pending decisions

- rt-core#33 open items (above, user). Derived-signal thresholds (above, user).
- **Q-031** waits for Q-001; Q-001 waits for the listen-only capture.
- Q-019 (board) blocks CubeMX, Renode, Ç6, the H7 FDCAN port and on-target D-070 budgets. Q-009 blocks the hil-bench host.
- Before safety-node Layer 1 code: Q-029, Q-023, Q-026; Q-022 after fallback validation.
- **User:** C-4 (old `can-dbc-conventions` skill on claude.ai); Q-024, Q-025; D-030 confirmation; Q-027/Q-028 later.

## Recent sessions

- 2026-10-17 (autonomous, task 8 + handoff): rt-core#33 draft (D-068/D-069 tester rule, defs v0.13.0, 113 client-core tests, local MISRA/pedantic/TSan/coverage green; 3 items need the user), rt-core#34 draft (golden vectors, stacked).
- 2026-10-17 (autonomous, tasks 4+7): server#14 golden vectors generator; releases conn v0.2.0, mobile v0.4.0, server v0.3.0 + manifest pins (workspace#70).
- 2026-10-17 (autonomous, tasks 2, 3, 5, 6): server#12 (part 2, 15 class-A + `stop_event`), server#13 (class-B summaries 19/46), conn#20 (log rate limit, long-gap test), mobile#15 (defs v0.14.0); all merged after reviewers.
- 2026-10-17 (autonomous, tasks 0-1): defs v0.14.0 (defs#70: 0xFD03 + staleness rule; safety-reviewer MAJOR-1/-2 fixed), manifest pin (workspace#67).
- 2026-10-16 (local, D-070 item 2 part 1): moto-server#11 derived reference (19 class-A signals); defs v0.13.0 released (defs#69), manifest pin (workspace#65).
