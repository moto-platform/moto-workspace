# STATUS — session handoff

> Keep it short (≤60 lines). Updated by the `/handoff` skill. "Recent sessions" keeps at most 5 one-line entries; drop the oldest.

**Phase:** 0 hardware build (user, ESP32-only data-collection prototype; enclosure placement Q-034) · 1 data pipeline done in code; D-068/D-069 + D-075 stop epoch and **D-080 freeze frames in conn and rt-core** · D-070 derived: defs + server reference + **rt-core `features/derived` part 1 (28 class-A signals, rt-core#51)** · analyzer A3 + A4 done (recorded sessions, session comparison) · 2 rt-core without hardware: republisher, heartbeat, FC check, EKF lean, 0xFD03 `LEAN_HEALTH` (D-067, D-086) · defs v0.19.0 (0x19 gate narrowed, per-signal tables in `moto_defs.platform`) pinned by rt-core, conn and server · roadmap: three parallel tracks (S schematics/CAD, C code, H hardware) below
**Last updated:** 2026-10-26

## Where we are

- **12 platform repos** + `moto-workspace` (D-081 adds moto-analyzer), public (D-033), MIT (D-036). Decisions D-001..D-088 (open Q up to Q-037); **D-057 intentionally unused**. The user merges PRs (or tells Claude to).
- **Architecture (D-072, D-073):** one STM32H755 (NUCLEO-H755ZI-Q, not ordered): M7 = rt-core, M4 = safety partition; bike ESP32 + helmet ESP32. **Boards (D-082):** A power/CAN, B detachable Scale 1B (no safety input), C1 split (user, 2026-10-24) into C1-IO (main box) + C1-IMU (frame box), C2 M7 chassis IMU; C1-IMU and C2 share one small IP65/67 box type (product CONFIRM, Q-034); ACS758LCB-200B; 1 kHz ADC only (burst = Q-036). Procurement v2.9: DT-0505/0508 are really 126×136 mm with no IP rating (store pages), input electrolytic ≥ 50 V.
- **On hand (user, 2026-10-23):** Pi 5 8 GB, Pi 3B+, Arduino Uno/Nano, ONE IMU board marked "MPU-6590" (likely the WHO_AM_I 0x70 MPU-6500 of 2026-10-15, CONFIRM). No STM32 board.
- **Anomaly direction:** D-083 physics-informed, staged, compared with a model without physics; D-084 sourced fault catalog in defs, moto-mcp matches, the LLM only explains. Stage-0 note + deep-research brief: `ideas/physics-informed-anomaly.md`.
- **moto-analyzer** (web host; Tauri later; tasks in `docs/ROADMAP.md`): defs-only, listen-only SLCAN, sim-only composer, pins defs v0.18.0; **A1** cluster (key F), **A2** live source (server `/ws/live`, hello with token, `MOTO_LIVE_SOURCE=mock`; real source open under D-077) and **A3** recorded sessions (key E: list, report summary, Open = replay, Load all; server `GET /sessions/{id}/series` min/max downsampled, `MOTO_CORS_ORIGINS=http://localhost:5173` for the browser) on main. Replay transport plays `ReplayItem` (frame | sample). Antigravity's Tauri commits on `ext/antigravity-cluster-tauri` stay as the A6 reference (its cluster part is replaced by A1).
- **D-075** provisional values (stop epoch etc.) and Q-022/Q-023 (5)-(6) unchanged. **D-080 in rt-core (rt-core#49, 2026-10-25):** `dtc_snapshot_core`, 0x19 only in a step with no DID due, FC needs the response prefix + a per-request FF_DL cap (reads 64 B, 0x19 255 B), late 0x59 First Frame never charged to a DID, worst case ~3.6 s tester silence once per epoch; defs pin v0.18.1; safety-reviewer three rounds (follow-ups ISSUES E-23). **D-086** (user): a registered EKF without an open 0x020 sender reads as stalled (rt-core#48, closes E-22). Server pins defs v0.18.1 (server#28).
- **D-070 derived on rt-core:** part 1 (28 class-A signals, rt-core#51) on main; **D-087** (user): every DID input, events and ride summaries too, uses its own `stale_after_ms` (server#33, rt-core#53), and a ride on rt-core = one D-075 stop epoch. **Part 2a done (rt-core#54):** 12 scalar class-B ride signals per stop epoch (`services/tester_epoch` → `derived_inputs` snapshot, ride change on an epoch-counter change), golden replay incl. two rides exact (server#34 vectors); RAM ~13.9 KB accepted by the user (**D-088**: measured costs set the budget, out of the EKF DTCM). E-23 (1)/(2) done (defs#102).
- **Releases (2026-10-25, all pinned in the manifest):** defs **v0.19.0**, rt-core **v0.11.0** (v0.10.0 skipped), conn **v0.4.0**, server **v0.6.0**, analyzer **v0.2.0**, mobile v0.4.0 (pins defs v0.14.0).

## Open PRs (merge order)

None open. Merged 2026-10-26: defs#105 (D-088 + the 2b proposal) and this handoff PR. Main is ahead of the tags: server (#33, #34) and rt-core (#53, #54) unreleased.

## Roadmap (parallel tracks; G = gate)

- **S, schematics/CAD (user, now):** S0 done (procurement v2.9 on defs main) → S1 `moto-bike-p0` schematic (ESP32 Phase 0) before soldering → S2 CubeMX pin plan for the H755 (no board needed; fixes the CONFIRM/TBD pins) → S3 `moto-bike` sheets: power, M7, Board B, C1/C2 → S4 Fusion: bike mesh, boxes, brackets once Q-034 is chosen. `models/fusion-lib` (local, untracked): SCHEMATIC-README v1.2 and the libraries match v2.9/D-082; still needs the English translation and git-lfs (`brew install git-lfs`) before its commit.
- **C, code without hardware (Claude):** ~~C1 rt-core D-080~~ done (rt-core#49) → C2 safety-node Layer 1 → C3 rt-core `features/derived` (part 1 done, rt-core#51; part 2 E-24) + D-072 follow-ups → C4 server D-076/D-077 packaging (`/ws/live` and `/series` done) → C5 fault-catalog schema in defs once the user's deep research lands (D-084) → C6 analyzer (task list `moto-analyzer/docs/ROADMAP.md`; A1-A4 done; next A5 decoded freeze frames (needs a defs snapshot layout), later A6 Tauri shell + listen-only HAL tests, needs rustup).
- **H, hardware (user):** H0 Q-034 measurements + Wave 1 order (NUCLEO-H755ZI-Q, MPU-6500 for C1) → H1 Phase 0 ESP32 build → **G1** bike listen-only capture (Q-001), V0/V1 → H2 NUCLEO arrives: flash, Renode, FDCAN → H3 Wave 2 sensors (ACS758-200B, NTCs) → D-083 stage 1 data.

## Next up (in order)

1. User: review the **C3 part 2b proposal** `moto-vehicle-defs/docs/ideas/ride-summary-did-layout.md` (generated 0xFD40-0xFD4E layouts: raw = (value − range.min)/resolution in 1/2/4 B, all-ones = NOT_AVAILABLE, 4 B header with the stop-epoch counter and RIDE_CLOSED, last closed ride only, histograms/per-gear later). On approval Claude records a decision, does the `/signal-change` (defs MINOR), then rt-core serves them from the platform UDS server via a derived → comms snapshot.
1b. User: decide D-082 item 6 (latching relay stays locked when the M4 loses power; bypass needed); pick the small IP65/67 IMU box (C1-IMU, C2) and check that C1-IO fits beside A/B on the 2nd story (Q-034); run the fault-catalog deep research with the brief in `ideas/physics-informed-anomaly.md` §3.
2. Claude (in order): **A5** analyzer decoded freeze frames (needs a snapshot record layout in defs first, `/signal-change`); **C3** rt-core D-072 follow-ups. Smaller: analyzer A1.1 (tach rev limit needs a sourced defs constant via `/signal-change`), E-20. Optional: user clicks through A3 (key E) and A4 Compare (key A, CSV on V) in the browser against a local server; neither was clicked through by Claude.
3. User: Q-034 measurements (§4.1 list, photos never committed); Wave 1 order; D-075 values when convenient.
4. User + Claude: vehicle data path (IMU header, SN65HVD230 120 Ω, DLC adapter; Q-001 capture, V0/V1, GPS; record the intermittent stall under load as a case study).
5. User: threshold proposals for the not-implemented derived signals → `/signal-change`.

## Blockers / pending decisions

- **Q-036** waits for rt-core on the H755 (CPU/DMA, SD load). **Q-035** waits for its first trigger. **Q-034** waits for the measurements. **Q-032** waits for HUD H0/H1. **Q-031** waits for Q-001; Q-001 waits for the listen-only capture.
- The NUCLEO-H755ZI-Q (not ordered) blocks flashing, Renode, Ç6, the FDCAN port and on-target budgets (not the CubeMX pin plan). Q-009 blocks the hil-bench host.
- Before safety-node Layer 1: Q-022 after fallback validation; Q-023 (5)-(6) in its design.
- **User:** D-082 item 6; IMU box product; C-4; Q-024, Q-025; D-030 confirmation; Q-027/Q-028 later.

## Recent sessions

- 2026-10-26 (local): user accepted the derived RAM (D-088, defs#105); Claude wrote the C3 part 2b ride-summary DID layout proposal (`docs/ideas/ride-summary-did-layout.md`, sizes 8-22 B per record, computed from the YAML), awaiting the user.
- 2026-10-25 (local, C3 2a): rt-core#54 class-B ride summaries per stop epoch (sonnet; architecture-guard on plan + diff, safety-reviewer on the tester path, guardian: no BLOCKER/MAJOR; latch/re-open epoch tests added); CI needed two reruns for runner apt timeouts (vcan0, toolchains).
- 2026-10-25 (local, D-087 + C3 2a start): user created the remaining tags (all pinned); user decided D-087 (DID's own stale limit everywhere; ride = stop epoch) → defs#104, server#33, rt-core#53; architecture-guard on the 2a plan (tester_epoch service, counter-based ride change, power-down close deferred); server#34 class-B golden vectors; rt-core 2a running in `claude/c3-classb`. Network drops slowed merges.
- 2026-10-25 (local, releases): user had Claude create defs v0.19.0, server v0.5.0, analyzer v0.2.0; defs v0.19.0 bumps in server (E-20 (1): `can_codec` adapter over `moto_defs.platform.SIGNALS`, old reader output byte-identical, server#32), rt-core (#52) and conn (#36) with version bumps 0.6.0 / 0.11.0 / 0.4.0; manifest pins (workspace#97).
- 2026-10-25 (local, E-20 (1)/(2), autonomous): server#31 drops the `_load_e2e()` workaround; defs#103 generates per-signal tables (`Signal`, `SIGNALS`) in `moto_defs.platform`, folded into the untagged v0.19.0. Loop stopped here: the remaining items need the user (tags, E-24 (1), ride boundary for C3 part 2, A1.1 constant) or hardware.
