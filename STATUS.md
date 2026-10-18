# STATUS — session handoff

> Keep it short (≤60 lines). Updated by the `/handoff` skill. "Recent sessions" keeps at most 5 one-line entries; drop the oldest.

**Phase:** 0 hardware build (user, ESP32-only data-collection prototype; enclosure placement Q-034) · 1 data pipeline done in code; D-068/D-069 + D-075 stop epoch in conn and rt-core · D-070 derived: defs + server reference + golden vectors in rt-core, rt-core `features/derived` next · 2 rt-core without hardware: republisher, heartbeat, FC check, EKF lean, 0xFD03 `LEAN_HEALTH` (D-067) · defs v0.16.0
**Last updated:** 2026-10-18

## Where we are

- 11 platform repos + `moto-workspace`, public (D-033), MIT (D-036). Decisions D-001..D-075 (open Q up to Q-034); **D-057 intentionally unused**. The user merges PRs; on 2026-10-18 they allowed Claude to merge its own PRs for that session only.
- **Architecture (D-072, D-073):** one STM32H755 (NUCLEO-H755ZI-Q, not ordered yet): M7 = rt-core, M4 = safety partition (cornering + own IMU, blind spot, immobilizer, LED ring/mirror LEDs); io-node retired; bike ESP32 + helmet ESP32. Platform bus v0.15.0: 0x023 `SafetyWarningStatus`, 0x120 `SafetyRequest`. Procurement list v2.0 (6 waves).
- **D-075 (provisional, user: "use changeable, standard-accepted values for now"; defs#77-80):**
  - Item 1: a stop epoch for the D-068 stop rule and the D-069 re-ask. Amendments (a)-(f): the fast session re-request on a counted 0x7E/0x7F; the "valid 0 seen" state belongs to the epoch; quiet-window bound; per-DID stop reason; conn's 2000 ms First-Frame hold; answered unverified DIDs stop after two 0x7E/0x7F refusals.
  - Item 2: single-fault-class bounds.
  - Item 3: the N_Bs hold is kept.
  - Items 4-6: provisional answers to Q-033 (own M4 indicator input, 1.5 s hold), Q-029 (yes) and Q-023 items 1-4. Q-022 and Q-023 (5)-(6) are still open.
- **Q-034 (open):** enclosure placement on the CL250. There is no room under the seat. Claude recommends a rigid rear-subframe tray on the left side with the IMUs on the frame; analysis in `hardware-integration.md` §4.1, which also lists the measurements to take.
- **rt-core main:**
  - defs **v0.15.0** (#40). Golden vectors and 0xFD03 landed via **#39**: #34 and #37 had been merged into stacked branches and never reached main.
  - D-075 (a)-(d) via #38 + #41, (f) + MINORs via **#42**. #42 merged before its 3rd safety-review round finished (rate limit): **re-run `safety-reviewer` on #42**.
- **conn main:** D-075 via #24 + #25. The MINORs of #25's review landed via conn#26. conn still pins defs v0.12.0.
- **Releases:** defs **v0.16.0** re-created on 9310893 (the first tag sat on f7847a7, without its content); `manifest.yaml` pins v0.16.0. rt-core v0.8.0 and conn v0.2.0 are the last releases; both mains are well ahead.
- Phase 0 build, data path and Mac setup are unchanged: see memory and `hardware-integration.md` §1-3.

## Next up (in order)

1. Claude: re-run `safety-reviewer` on rt-core#42 (merged at its head). Fix any finding in a **new** branch → PR to main (never stacked, memory `pr-merge-pitfalls`).
2. Claude: conn test gap 2 from the conn#25 review. The quiet-window and tester-present tests must tell the fast session request from the 2000 ms retry; the quiet-window scenario needs a refusal less than 2000 ms after the last session request.
3. User: Q-034 measurements on the bike (§4.1 list, photos never committed); order Wave 1 (NUCLEO-H755ZI-Q first); confirm or change the D-075 provisional values whenever convenient.
4. Claude: safety-node Layer 1. Steps: `/repo-bootstrap moto-safety-node`, then `/feature-module` cornering decision on the D-075 items 4-6 defaults, using `pack_checked` (defs v0.16.0), then `safety-reviewer`.
5. Claude: rt-core `features/derived` against the golden vectors (`/feature-module`, `architecture-guard`).
6. Claude, D-072 follow-ups: rt-core sends 0x120 and consumes 0x023; conn bumps defs (v0.12.0 → v0.16.0) and reads 0x023 for the HUD/phone; hil-bench restbus drops 0x083 and adds 0x023/0x120 when it exists.
7. Claude: expose the per-DID stop reason in the D-069 item 2 record (BLE vehicle-signal block / rt-core 0xFD02); needs a defs change (`/signal-change`).
8. User + Claude, vehicle data path: IMU header, SN65HVD230 (check its 120 Ω), DLC adapter; B2 on the desk; on the bike Q-001 listen-only capture, then V0/V1, GPS. **Also record the user's intermittent stall under load** (ride sessions + DTC read afterwards; the server's `stop_event` marks it) as a case study.
9. User: threshold proposals for the not-implemented derived signals (list in the 2026-10-17 report) → `/signal-change`.
10. Small: server ingest evaluates class A twice; HIL scenarios of E-19 and the D-075 reviews (0x7F ECU, short reset at crank, disagreeing response IDs).

## Blockers / pending decisions

- **Q-034** (placement) waits for the measurements. **Q-032** waits for HUD stages H0/H1. **Q-031** waits for Q-001; Q-001 waits for the listen-only capture.
- The NUCLEO-H755ZI-Q (not ordered) blocks CubeMX, Renode, Ç6, the FDCAN port and on-target budgets. Q-009 blocks the hil-bench host.
- Before safety-node Layer 1: Q-022 after fallback validation; Q-023 (5)-(6) in its design.
- **User:** C-4 (old `can-dbc-conventions` skill on claude.ai); Q-024, Q-025; D-030 confirmation; Q-027/Q-028 later; untracked workspace files `CAN-DISCOVERY-AND-POLLING-STRATEGY.md`, `docs-presentation/`, `learning/` (commit or keep local?).

## Recent sessions

- 2026-10-18 (local, long): D-075 provisional defaults (defs#77-80), Q-034 placement analysis, rt-core#38-42 (stop epoch, (f), orphaned #34/#37 recovered, defs v0.15.0), conn#24-26, v0.16.0 tag fixed; three safety-reviewer rounds on rt-core, two on conn.
- 2026-10-18 (local): D-074 data paths (defs#73), platform bus v0.15.0 with 0x023/0x120 (defs#74), signal-change skill node list (workspace#74); Q-033 opened (defs#75).
- 2026-10-17 (local, architecture): D-072 one STM32H755, D-073 helmet unit; procurement list v2.0; rules synced to all repos.
- 2026-10-17 (autonomous, task 8 + handoff): rt-core#33 draft (D-068/D-069 tester rule), rt-core#34 draft (golden vectors, stacked).
- 2026-10-17 (autonomous, tasks 4+7): server#14 golden vectors generator; releases conn v0.2.0, mobile v0.4.0, server v0.3.0 + manifest pins (workspace#70).
