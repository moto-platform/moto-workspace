# STATUS — session handoff

> Keep it short (≤60 lines). Updated by the `/handoff` skill. "Recent sessions" keeps at most 5 one-line entries; drop the oldest.

**Phase:** 0 hardware build (user, ESP32-only data-collection prototype; enclosure placement Q-034) · 1 data pipeline done in code; D-068/D-069 + D-075 stop epoch in conn and rt-core · D-070 derived: defs + server reference + golden vectors in rt-core, rt-core `features/derived` next · 2 rt-core without hardware: republisher, heartbeat, FC check, EKF lean, 0xFD03 `LEAN_HEALTH` (D-067) · defs v0.18.0 · roadmap: three parallel tracks (S schematics/CAD, C code, H hardware) below
**Last updated:** 2026-10-24

## Where we are

- **12 platform repos** + `moto-workspace` (D-081 adds moto-analyzer), public (D-033), MIT (D-036). Decisions D-001..D-085 (open Q up to Q-037); **D-057 intentionally unused**. The user merges PRs (or tells Claude to).
- **Architecture (D-072, D-073):** one STM32H755 (NUCLEO-H755ZI-Q, not ordered): M7 = rt-core, M4 = safety partition; bike ESP32 + helmet ESP32. **Boards (D-082):** A power/CAN, B detachable Scale 1B (no safety input), C1 M4 safety board, C2 M7 chassis IMU; ACS758LCB-200B; 1 kHz ADC only (burst = Q-036). Procurement v2.7.
- **On hand (user, 2026-10-23):** Pi 5 8 GB, Pi 3B+, Arduino Uno/Nano, ONE IMU board marked "MPU-6590" (likely the WHO_AM_I 0x70 MPU-6500 of 2026-10-15, CONFIRM). No STM32 board.
- **Anomaly direction:** D-083 physics-informed, staged, compared with a model without physics; D-084 sourced fault catalog in defs, moto-mcp matches, the LLM only explains. Stage-0 note + deep-research brief: `ideas/physics-informed-anomaly.md`.
- **moto-analyzer** (web host; Tauri later; tasks in `docs/ROADMAP.md`): defs-only, listen-only SLCAN, sim-only composer, pins defs v0.18.0; **A1** cluster (key F) and **A2** live source (server `/ws/live`, hello with token, `MOTO_LIVE_SOURCE=mock`; real source open under D-077) on main. Antigravity's Tauri commits on `ext/antigravity-cluster-tauri` stay as the A6 reference (its cluster part is replaced by A1).
- **D-075** provisional values (stop epoch etc.) and Q-022/Q-023 (5)-(6) unchanged. conn has D-080 (conn#31) and pins defs v0.17.0; rt-core main pins v0.15.0, no D-080 yet. Releases: defs v0.18.0 (manifest pinned), rt-core v0.8.0, conn v0.2.0, server v0.3.0, mobile v0.4.0.

## Open PRs (merge order)

None. Merged 2026-10-24 on the user's instruction: defs#95 (D-085, Q-037), #96 (ARCHITECTURE §7 `/ws/live`); analyzer#12, #13, #14, #15 (ROADMAP A1/A2 built, A1.1 open; README); server#24; workspace#87.

## Roadmap (parallel tracks; G = gate)

- **S, schematics/CAD (user, now):** S0 done (procurement v2.7 on defs main) → S1 `moto-bike-p0` schematic (ESP32 Phase 0) before soldering → S2 CubeMX pin plan for the H755 (no board needed; fixes the CONFIRM/TBD pins) → S3 `moto-bike` sheets: power, M7, Board B, C1/C2 → S4 Fusion: bike mesh, boxes, brackets once Q-034 is chosen. fusion-lib needs a v2.7 regeneration, English translation and git-lfs (`brew install git-lfs`) before its commit.
- **C, code without hardware (Claude):** C1 rt-core D-080 (`safety-reviewer`) → C2 safety-node Layer 1 → C3 rt-core `features/derived` + D-072 follow-ups → C4 server series endpoint (`/ws/live` done, server#24) and D-076/D-077 packaging → C5 fault-catalog schema in defs once the user's deep research lands (D-084) → C6 analyzer (task list `moto-analyzer/docs/ROADMAP.md`; A1, A2 done; next A3, later A6 Tauri shell + listen-only HAL tests, needs rustup).
- **H, hardware (user):** H0 Q-034 measurements + Wave 1 order (NUCLEO-H755ZI-Q, MPU-6500 for C1) → H1 Phase 0 ESP32 build → **G1** bike listen-only capture (Q-001), V0/V1 → H2 NUCLEO arrives: flash, Renode, FDCAN → H3 Wave 2 sensors (ACS758-200B, NTCs) → D-083 stage 1 data.

## Next up (in order)

1. User: decide D-082 item 6 (latching relay stays locked when the M4 loses power; bypass needed) and the C1-IMU / C1-IO split (safety-reviewer recommends C1-IO in the main box); run the fault-catalog deep research with the brief in `ideas/physics-informed-anomaly.md` §3.
2. Claude: **A3** = server `/sessions/{id}/series` (downsampled) + analyzer recorded-session source (scope + replay, token out of the URL); **or C1** = rt-core D-080 freeze frames (`safety-reviewer`). Smaller: analyzer A1.1 (tach rev limit needs a sourced defs constant via `/signal-change`; today the DBC range 0-16383 rpm), E-20 (ISSUES).
3. User: Q-034 measurements (§4.1 list, photos never committed); Wave 1 order; D-075 values when convenient.
4. User + Claude: vehicle data path (IMU header, SN65HVD230 120 Ω, DLC adapter; Q-001 capture, V0/V1, GPS; record the intermittent stall under load as a case study).
5. User: threshold proposals for the not-implemented derived signals → `/signal-change`.

## Blockers / pending decisions

- **Q-036** waits for rt-core on the H755 (CPU/DMA, SD load). **Q-035** waits for its first trigger. **Q-034** waits for the measurements. **Q-032** waits for HUD H0/H1. **Q-031** waits for Q-001; Q-001 waits for the listen-only capture.
- The NUCLEO-H755ZI-Q (not ordered) blocks flashing, Renode, Ç6, the FDCAN port and on-target budgets (not the CubeMX pin plan). Q-009 blocks the hil-bench host.
- Before safety-node Layer 1: Q-022 after fallback validation; Q-023 (5)-(6) in its design.
- **User:** D-082 item 6 and the C1 split; C-4; Q-024, Q-025; D-030 confirmation; Q-027/Q-028 later.

## Recent sessions

- 2026-10-24 (local, cont.): server + analyzer run locally (ports 8000, 5173); D-085 layer split + Q-037 (defs#95); analyzer roadmap A1-A9 (analyzer#12); A1 cluster built by sonnet, Claude fixed the stale-on-silent-source gap, guardian clean (analyzer#13); A2 `/ws/live` + analyzer hello (server#24, analyzer#14).
- 2026-10-24 (local): merged the 2026-10-23 PR set on the user's instruction (defs#92 updated with main, CI green), synced rules + analyzer assets to all 12 repos.
- 2026-10-23/24 (local, external review): 4 Antigravity logs closed (CAN analyzer, anomaly sensors, CAD, procurement v2.6); D-081 analyzer repo, D-082 board split, D-083 physics-informed model, D-084 fault catalog, Q-036 (defs#93); charging_ripple pending (defs#92); workspace#84 analyzer registration; analyzer#10 CI; server#22 mock stream from defs; architecture-guard + safety-reviewer on the hardware docs; two AGENTS.base rules (no new repos, sourced hardware facts).
- 2026-10-19 (local): Gemini contributor-plan log reviewed (analysis only, plan not saved → TEMPLATE Result section); logs + strategy note committed, `docs-presentation/` and `learning/` kept local (workspace#81); anomaly stage 1: D-079 windows W1-W5 (no burst), D-080 0x19 freeze frames, G/I taxonomy, procurement 2.1 (defs#83, architecture-guard fixed); v0.17.0 content in defs#84 (windows) + #85 (OBD catalog, D-080 constants), sonnet-built, Claude-reviewed; 14 worktrees pruned; the user merged everything and tagged **defs v0.17.0** (#86, 86f8f3e); manifest pin in workspace#82.
- 2026-10-18 (local, external review): Antigravity anomaly-sensor log reviewed (design only; verdicts in its Claude review); user decisions D-076 position relaxed + Q-035, D-077 two servers, D-078 scope (defs#82), invariant 7 + zones (workspace#79), 10 sync PRs; all merged on the user's instruction.
