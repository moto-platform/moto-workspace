# STATUS — session handoff

> Keep it short (≤60 lines). Updated by the `/handoff` skill. "Recent sessions" keeps at most 5 one-line entries; drop the oldest.

**Phase:** 0 hardware build (user, ESP32-only data-collection prototype; enclosure placement Q-034) · 1 data pipeline done in code; D-068/D-069 + D-075 stop epoch and **D-080 freeze frames in conn and rt-core** · D-070 derived: defs + server reference + golden vectors in rt-core, rt-core `features/derived` next · analyzer A3 done (recorded sessions) · 2 rt-core without hardware: republisher, heartbeat, FC check, EKF lean, 0xFD03 `LEAN_HEALTH` (D-067, D-086) · defs v0.18.1 everywhere but mobile · roadmap: three parallel tracks (S schematics/CAD, C code, H hardware) below
**Last updated:** 2026-10-25

## Where we are

- **12 platform repos** + `moto-workspace` (D-081 adds moto-analyzer), public (D-033), MIT (D-036). Decisions D-001..D-086 (open Q up to Q-037); **D-057 intentionally unused**. The user merges PRs (or tells Claude to).
- **Architecture (D-072, D-073):** one STM32H755 (NUCLEO-H755ZI-Q, not ordered): M7 = rt-core, M4 = safety partition; bike ESP32 + helmet ESP32. **Boards (D-082):** A power/CAN, B detachable Scale 1B (no safety input), C1 split (user, 2026-10-24) into C1-IO (main box) + C1-IMU (frame box), C2 M7 chassis IMU; C1-IMU and C2 share one small IP65/67 box type (product CONFIRM, Q-034); ACS758LCB-200B; 1 kHz ADC only (burst = Q-036). Procurement v2.9: DT-0505/0508 are really 126×136 mm with no IP rating (store pages), input electrolytic ≥ 50 V.
- **On hand (user, 2026-10-23):** Pi 5 8 GB, Pi 3B+, Arduino Uno/Nano, ONE IMU board marked "MPU-6590" (likely the WHO_AM_I 0x70 MPU-6500 of 2026-10-15, CONFIRM). No STM32 board.
- **Anomaly direction:** D-083 physics-informed, staged, compared with a model without physics; D-084 sourced fault catalog in defs, moto-mcp matches, the LLM only explains. Stage-0 note + deep-research brief: `ideas/physics-informed-anomaly.md`.
- **moto-analyzer** (web host; Tauri later; tasks in `docs/ROADMAP.md`): defs-only, listen-only SLCAN, sim-only composer, pins defs v0.18.0; **A1** cluster (key F), **A2** live source (server `/ws/live`, hello with token, `MOTO_LIVE_SOURCE=mock`; real source open under D-077) and **A3** recorded sessions (key E: list, report summary, Open = replay, Load all; server `GET /sessions/{id}/series` min/max downsampled, `MOTO_CORS_ORIGINS=http://localhost:5173` for the browser) on main. Replay transport plays `ReplayItem` (frame | sample). Antigravity's Tauri commits on `ext/antigravity-cluster-tauri` stay as the A6 reference (its cluster part is replaced by A1).
- **D-075** provisional values (stop epoch etc.) and Q-022/Q-023 (5)-(6) unchanged. **D-080 in rt-core (rt-core#49, 2026-10-25):** `dtc_snapshot_core`, 0x19 only in a step with no DID due, FC needs the response prefix + a per-request FF_DL cap (reads 64 B, 0x19 255 B), late 0x59 First Frame never charged to a DID, worst case ~3.6 s tester silence once per epoch; defs pin v0.18.1; safety-reviewer three rounds (follow-ups ISSUES E-23). **D-086** (user): a registered EKF without an open 0x020 sender reads as stalled (rt-core#48, closes E-22). Server pins defs v0.18.1 (server#28).
- **Releases:** version PRs merged for rt-core **0.10.0** (#50), server **0.5.0** (#29), analyzer **0.2.0** (#17), but the **tags are not created** (Claude's `gh release create` was refused by the permission classifier as a public surface): user runs the three commands in Next up 1, then the manifest pins follow. Manifest today: defs v0.18.1, rt-core v0.9.0, conn v0.3.0, server v0.4.0, analyzer v0.1.0, mobile v0.4.0.

## Open PRs (merge order)

None. Merged 2026-10-24/25 on the user's instruction: defs#100, rt-core#48, server#28, server#29, analyzer#17, rt-core#49, defs#101, rt-core#50 and this handoff PR.

## Roadmap (parallel tracks; G = gate)

- **S, schematics/CAD (user, now):** S0 done (procurement v2.9 on defs main) → S1 `moto-bike-p0` schematic (ESP32 Phase 0) before soldering → S2 CubeMX pin plan for the H755 (no board needed; fixes the CONFIRM/TBD pins) → S3 `moto-bike` sheets: power, M7, Board B, C1/C2 → S4 Fusion: bike mesh, boxes, brackets once Q-034 is chosen. `models/fusion-lib` (local, untracked): SCHEMATIC-README v1.2 and the libraries match v2.9/D-082; still needs the English translation and git-lfs (`brew install git-lfs`) before its commit.
- **C, code without hardware (Claude):** ~~C1 rt-core D-080~~ done (rt-core#49) → C2 safety-node Layer 1 → C3 rt-core `features/derived` + D-072 follow-ups → C4 server D-076/D-077 packaging (`/ws/live` and `/series` done) → C5 fault-catalog schema in defs once the user's deep research lands (D-084) → C6 analyzer (task list `moto-analyzer/docs/ROADMAP.md`; A1-A3 done; next A4 session comparison, later A6 Tauri shell + listen-only HAL tests, needs rustup).
- **H, hardware (user):** H0 Q-034 measurements + Wave 1 order (NUCLEO-H755ZI-Q, MPU-6500 for C1) → H1 Phase 0 ESP32 build → **G1** bike listen-only capture (Q-001), V0/V1 → H2 NUCLEO arrives: flash, Renode, FDCAN → H3 Wave 2 sensors (ACS758-200B, NTCs) → D-083 stage 1 data.

## Next up (in order)

1. User: `gh release create v0.10.0 -R moto-platform/moto-rt-core --target main --title v0.10.0 --generate-notes`, the same for `v0.5.0` moto-server and `v0.2.0` moto-analyzer (or allow Claude to); then Claude pins them in `manifest.yaml` (workspace PR).
1b. User: decide D-082 item 6 (latching relay stays locked when the M4 loses power; bypass needed); pick the small IP65/67 IMU box (C1-IMU, C2) and check that C1-IO fits beside A/B on the 2nd story (Q-034); run the fault-catalog deep research with the brief in `ideas/physics-informed-anomaly.md` §3.
2. Claude (in order): ISSUES **E-21** (conn D-080 MINOR-1 lock on NRC 0x78 + tests, `safety-reviewer`); **E-23 (1)/(2)** defs gate narrowing + dids.yaml wording (`/signal-change`, `safety-reviewer`, defs PATCH/MINOR + consumer bumps); **A4** = analyzer session comparison (common time/distance axis, difference trace, CSV); **C3** rt-core `features/derived` (`/feature-module`). Smaller: analyzer A1.1 (tach rev limit needs a sourced defs constant via `/signal-change`), E-20. Optional: user clicks through A3 in the browser.
3. User: Q-034 measurements (§4.1 list, photos never committed); Wave 1 order; D-075 values when convenient.
4. User + Claude: vehicle data path (IMU header, SN65HVD230 120 Ω, DLC adapter; Q-001 capture, V0/V1, GPS; record the intermittent stall under load as a case study).
5. User: threshold proposals for the not-implemented derived signals → `/signal-change`.

## Blockers / pending decisions

- **Q-036** waits for rt-core on the H755 (CPU/DMA, SD load). **Q-035** waits for its first trigger. **Q-034** waits for the measurements. **Q-032** waits for HUD H0/H1. **Q-031** waits for Q-001; Q-001 waits for the listen-only capture.
- The NUCLEO-H755ZI-Q (not ordered) blocks flashing, Renode, Ç6, the FDCAN port and on-target budgets (not the CubeMX pin plan). Q-009 blocks the hil-bench host.
- Before safety-node Layer 1: Q-022 after fallback validation; Q-023 (5)-(6) in its design.
- **User:** D-082 item 6; IMU box product; C-4; Q-024, Q-025; D-030 confirmation; Q-027/Q-028 later.

## Recent sessions

- 2026-10-24/25 (local, C1 + E-22, autonomous on the user's instruction "merge, then the next task"): architecture-guard on the plan; sonnet wrote rt-core D-080 (rt-core#49) and E-22 (rt-core#48), Claude reviewed; user chose D-086 (defs#100); safety-reviewer three rounds on D-080 (MAJOR late 0x59 FF charged to a DID, cap cancel + presence refresh, remaining-CF hold, OVFLW byte) and one on E-22; guardian clean; D-080 rt-core note (defs#101); server defs v0.18.1 (server#28); version PRs rt-core#50, server#29, analyzer#17 merged, tags left to the user (permission).
- 2026-10-24 (local, A3): workspace#91 (previous handoff); A3 built by two sonnet agents in parallel against a fixed contract: server#26 `GET /sessions/{id}/series` (SessionInputs reuse, derived.parquet, shared t0, min/max buckets, header-only token, opt-in CORS) + analyzer#16 (Session source/tab, ReplayItem replay, `did.X` → defs DID channel); Claude fixed recorded labels lost on backward seek, curl end-to-end on fixtures, guardian CLEAN, CI green, merged; worktrees pruned; server#27 CLAUDE.md.
- 2026-10-24 (local, hardware cross-check): Argon's 8 findings checked (6 right, item 4's reasoning and item 5 wrong); found the DT box sizes unsourced (store: 126×136 mm, no IP) and the 35 V input cap under-rated; defs#98 (procurement v2.8, hardware-integration §3.4/§9/§10, docs index); user approved the C1-IO / C1-IMU split → D-082 item 2 decided (defs#99, v2.9); local SCHEMATIC-README v1.2, fusion-lib README/modules.py, moto-core.lbr regenerated.
- 2026-10-24 (local, audit): merged the A1/A2 set + docs (analyzer#15, defs#96, workspace#88); audit found two commits pushed 3 min after their PR merged and lost (conn D-080 round-2 fixes, rt-core 0xFD03 follow-ups), recovered with safety-reviewer (conn#33, rt-core#46; MINORs → E-21/E-22); releases defs v0.18.1, rt-core v0.9.0, conn v0.3.0, server v0.4.0, analyzer v0.1.0 pinned; 34 worktrees and 328 merged remote branches removed (only `ext/antigravity-cluster-tauri` kept, A6 reference); all AI-Agent commits have closed logs.
- 2026-10-24 (local, cont.): server + analyzer run locally (ports 8000, 5173); D-085 layer split + Q-037 (defs#95); analyzer roadmap A1-A9 (analyzer#12); A1 cluster built by sonnet, Claude fixed the stale-on-silent-source gap, guardian clean (analyzer#13); A2 `/ws/live` + analyzer hello (server#24, analyzer#14).
