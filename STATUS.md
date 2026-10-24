# STATUS — session handoff

> Keep it short (≤60 lines). Updated by the `/handoff` skill. "Recent sessions" keeps at most 5 one-line entries; drop the oldest.

**Phase:** 0 hardware build (user, ESP32-only data-collection prototype; enclosure placement Q-034) · 1 data pipeline done in code; D-068/D-069 + D-075 stop epoch in conn and rt-core · D-070 derived: defs + server reference + golden vectors in rt-core, rt-core `features/derived` next · analyzer A3 done (recorded sessions) · 2 rt-core without hardware: republisher, heartbeat, FC check, EKF lean, 0xFD03 `LEAN_HEALTH` (D-067) · defs v0.18.1 · roadmap: three parallel tracks (S schematics/CAD, C code, H hardware) below
**Last updated:** 2026-10-24

## Where we are

- **12 platform repos** + `moto-workspace` (D-081 adds moto-analyzer), public (D-033), MIT (D-036). Decisions D-001..D-085 (open Q up to Q-037); **D-057 intentionally unused**. The user merges PRs (or tells Claude to).
- **Architecture (D-072, D-073):** one STM32H755 (NUCLEO-H755ZI-Q, not ordered): M7 = rt-core, M4 = safety partition; bike ESP32 + helmet ESP32. **Boards (D-082):** A power/CAN, B detachable Scale 1B (no safety input), C1 split (user, 2026-10-24) into C1-IO (main box) + C1-IMU (frame box), C2 M7 chassis IMU; C1-IMU and C2 share one small IP65/67 box type (product CONFIRM, Q-034); ACS758LCB-200B; 1 kHz ADC only (burst = Q-036). Procurement v2.9: DT-0505/0508 are really 126×136 mm with no IP rating (store pages), input electrolytic ≥ 50 V.
- **On hand (user, 2026-10-23):** Pi 5 8 GB, Pi 3B+, Arduino Uno/Nano, ONE IMU board marked "MPU-6590" (likely the WHO_AM_I 0x70 MPU-6500 of 2026-10-15, CONFIRM). No STM32 board.
- **Anomaly direction:** D-083 physics-informed, staged, compared with a model without physics; D-084 sourced fault catalog in defs, moto-mcp matches, the LLM only explains. Stage-0 note + deep-research brief: `ideas/physics-informed-anomaly.md`.
- **moto-analyzer** (web host; Tauri later; tasks in `docs/ROADMAP.md`): defs-only, listen-only SLCAN, sim-only composer, pins defs v0.18.0; **A1** cluster (key F), **A2** live source (server `/ws/live`, hello with token, `MOTO_LIVE_SOURCE=mock`; real source open under D-077) and **A3** recorded sessions (key E: list, report summary, Open = replay, Load all; server `GET /sessions/{id}/series` min/max downsampled, `MOTO_CORS_ORIGINS=http://localhost:5173` for the browser) on main. Replay transport plays `ReplayItem` (frame | sample). Antigravity's Tauri commits on `ext/antigravity-cluster-tauri` stay as the A6 reference (its cluster part is replaced by A1).
- **D-075** provisional values (stop epoch etc.) and Q-022/Q-023 (5)-(6) unchanged. conn has D-080 with the round-2 fixes (conn#31 + #33) and pins defs v0.18.0; rt-core main pins v0.15.0, no D-080 yet. Releases (all pinned in the manifest, 2026-10-24): defs v0.18.1, rt-core v0.9.0, conn v0.3.0, server v0.4.0, analyzer v0.1.0, mobile v0.4.0. **A3 is unreleased** (server#26, analyzer#16 on main). Server pins defs **v0.14.0** (analyzer v0.18.0): bump separately.

## Open PRs (merge order)

None. Merged 2026-10-24 on the user's instruction: workspace#91, server#26 (series endpoint + CORS), analyzer#16 (A3), server#27 (CLAUDE.md) and this handoff PR.

## Roadmap (parallel tracks; G = gate)

- **S, schematics/CAD (user, now):** S0 done (procurement v2.9 on defs main) → S1 `moto-bike-p0` schematic (ESP32 Phase 0) before soldering → S2 CubeMX pin plan for the H755 (no board needed; fixes the CONFIRM/TBD pins) → S3 `moto-bike` sheets: power, M7, Board B, C1/C2 → S4 Fusion: bike mesh, boxes, brackets once Q-034 is chosen. `models/fusion-lib` (local, untracked): SCHEMATIC-README v1.2 and the libraries match v2.9/D-082; still needs the English translation and git-lfs (`brew install git-lfs`) before its commit.
- **C, code without hardware (Claude):** C1 rt-core D-080 (`safety-reviewer`) → C2 safety-node Layer 1 → C3 rt-core `features/derived` + D-072 follow-ups → C4 server D-076/D-077 packaging (`/ws/live` and `/series` done) → C5 fault-catalog schema in defs once the user's deep research lands (D-084) → C6 analyzer (task list `moto-analyzer/docs/ROADMAP.md`; A1-A3 done; next A4 session comparison, later A6 Tauri shell + listen-only HAL tests, needs rustup).
- **H, hardware (user):** H0 Q-034 measurements + Wave 1 order (NUCLEO-H755ZI-Q, MPU-6500 for C1) → H1 Phase 0 ESP32 build → **G1** bike listen-only capture (Q-001), V0/V1 → H2 NUCLEO arrives: flash, Renode, FDCAN → H3 Wave 2 sensors (ACS758-200B, NTCs) → D-083 stage 1 data.

## Next up (in order)

1. User: decide D-082 item 6 (latching relay stays locked when the M4 loses power; bypass needed); pick the small IP65/67 IMU box (C1-IMU, C2) and check that C1-IO fits beside A/B on the 2nd story (Q-034); run the fault-catalog deep research with the brief in `ideas/physics-informed-anomaly.md` §3.
2. Claude: **C1** = rt-core D-080 freeze frames (`/feature-module`, `safety-reviewer`); **or A4** = analyzer session comparison (common time/distance axis, difference trace, CSV). Before either, optionally: user clicks through A3 in the browser (server with `MOTO_CORS_ORIGINS`, analyzer key E) — not yet done by Claude; releases server v0.5.0 / analyzer v0.2.0 (D-036) + manifest pin; server defs bump v0.14.0 → v0.18.1. Smaller: ISSUES E-21 (conn D-080 MINOR-1 lock on NRC 0x78 + two tests, `safety-reviewer`), E-22 (rt-core 0xFD03 bus-path test; H7 boot must enforce a failed `lean_tx_open()`), analyzer A1.1 (tach rev limit needs a sourced defs constant via `/signal-change`; today the DBC range 0-16383 rpm), E-20 (ISSUES).
3. User: Q-034 measurements (§4.1 list, photos never committed); Wave 1 order; D-075 values when convenient.
4. User + Claude: vehicle data path (IMU header, SN65HVD230 120 Ω, DLC adapter; Q-001 capture, V0/V1, GPS; record the intermittent stall under load as a case study).
5. User: threshold proposals for the not-implemented derived signals → `/signal-change`.

## Blockers / pending decisions

- **Q-036** waits for rt-core on the H755 (CPU/DMA, SD load). **Q-035** waits for its first trigger. **Q-034** waits for the measurements. **Q-032** waits for HUD H0/H1. **Q-031** waits for Q-001; Q-001 waits for the listen-only capture.
- The NUCLEO-H755ZI-Q (not ordered) blocks flashing, Renode, Ç6, the FDCAN port and on-target budgets (not the CubeMX pin plan). Q-009 blocks the hil-bench host.
- Before safety-node Layer 1: Q-022 after fallback validation; Q-023 (5)-(6) in its design.
- **User:** D-082 item 6; IMU box product; C-4; Q-024, Q-025; D-030 confirmation; Q-027/Q-028 later.

## Recent sessions

- 2026-10-24 (local, A3): workspace#91 (previous handoff); A3 built by two sonnet agents in parallel against a fixed contract: server#26 `GET /sessions/{id}/series` (SessionInputs reuse, derived.parquet, shared t0, min/max buckets, header-only token, opt-in CORS) + analyzer#16 (Session source/tab, ReplayItem replay, `did.X` → defs DID channel); Claude fixed recorded labels lost on backward seek, curl end-to-end on fixtures, guardian CLEAN, CI green, merged; worktrees pruned; server#27 CLAUDE.md.
- 2026-10-24 (local, hardware cross-check): Argon's 8 findings checked (6 right, item 4's reasoning and item 5 wrong); found the DT box sizes unsourced (store: 126×136 mm, no IP) and the 35 V input cap under-rated; defs#98 (procurement v2.8, hardware-integration §3.4/§9/§10, docs index); user approved the C1-IO / C1-IMU split → D-082 item 2 decided (defs#99, v2.9); local SCHEMATIC-README v1.2, fusion-lib README/modules.py, moto-core.lbr regenerated.
- 2026-10-24 (local, audit): merged the A1/A2 set + docs (analyzer#15, defs#96, workspace#88); audit found two commits pushed 3 min after their PR merged and lost (conn D-080 round-2 fixes, rt-core 0xFD03 follow-ups), recovered with safety-reviewer (conn#33, rt-core#46; MINORs → E-21/E-22); releases defs v0.18.1, rt-core v0.9.0, conn v0.3.0, server v0.4.0, analyzer v0.1.0 pinned; 34 worktrees and 328 merged remote branches removed (only `ext/antigravity-cluster-tauri` kept, A6 reference); all AI-Agent commits have closed logs.
- 2026-10-24 (local, cont.): server + analyzer run locally (ports 8000, 5173); D-085 layer split + Q-037 (defs#95); analyzer roadmap A1-A9 (analyzer#12); A1 cluster built by sonnet, Claude fixed the stale-on-silent-source gap, guardian clean (analyzer#13); A2 `/ws/live` + analyzer hello (server#24, analyzer#14).
- 2026-10-24 (local): merged the 2026-10-23 PR set on the user's instruction (defs#92 updated with main, CI green), synced rules + analyzer assets to all 12 repos.
