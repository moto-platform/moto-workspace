# STATUS — session handoff

> Keep it short (≤60 lines). Updated by the `/handoff` skill. "Recent sessions" keeps at most 5 one-line entries; drop the oldest.

**Phase:** 0 hardware build (user, ESP32-only data-collection prototype; enclosure placement Q-034) · 1 data pipeline done in code; D-068/D-069 + D-075 stop epoch in conn and rt-core · D-070 derived: defs + server reference + golden vectors in rt-core, rt-core `features/derived` next · 2 rt-core without hardware: republisher, heartbeat, FC check, EKF lean, 0xFD03 `LEAN_HEALTH` (D-067) · defs v0.16.0
**Last updated:** 2026-10-19

## Where we are

- 11 platform repos + `moto-workspace`, public (D-033), MIT (D-036). Decisions D-001..D-080 (open Q up to Q-035); **D-057 intentionally unused**. The user merges PRs; on 2026-10-18 they allowed Claude to merge its own PRs (both sessions that day, explicit instruction each time).
- **Architecture (D-072, D-073):** one STM32H755 (NUCLEO-H755ZI-Q, not ordered yet): M7 = rt-core, M4 = safety partition (cornering + own IMU, blind spot, immobilizer, LED ring/mirror LEDs); io-node retired; bike ESP32 + helmet ESP32. Platform bus v0.15.0: 0x023 `SafetyWarningStatus`, 0x120 `SafetyRequest`. Procurement list v2.0 (6 waves).
- **D-075 (provisional, user: "use changeable, standard-accepted values for now"; defs#77-80):**
  - Item 1: a stop epoch for the D-068 stop rule and the D-069 re-ask. Amendments (a)-(f): the fast session re-request on a counted 0x7E/0x7F; the "valid 0 seen" state belongs to the epoch; quiet-window bound; per-DID stop reason; conn's 2000 ms First-Frame hold; answered unverified DIDs stop after two 0x7E/0x7F refusals. (f) amended (user, defs#81): the D-069 re-ask clears the NRC counts and the 0x31 mark of **every** unverified DID, so the 0x31-before-0x7E/0x7F precedence holds per run of the stop rule; timeout counts are kept.
  - Item 2: single-fault-class bounds.
  - Item 3: the N_Bs hold is kept.
  - Items 4-6: provisional answers to Q-033 (own M4 indicator input, 1.5 s hold), Q-029 (yes) and Q-023 items 1-4. Q-022 and Q-023 (5)-(6) are still open.
- **2026-10-18 decisions (defs#82, rules in workspace#79, synced to all repos):** D-076 (provisional) position may go to the user's own servers and the LLM via moto-mcp, never committed, the LLM still does no math; Q-035 tracks the revisit. Not implemented: BLE GPS block + codegen guard, conn, mobile D-063 guard, server, mcp. D-077 moto-server on the Raspi (edge) + remote (user's machine now, VPS-ready), moto-mcp on both. D-078 CL250 prototype now, commercial multi-vehicle product later (PLATFORM-RULES scope note). zones: moto-server `*gps*`/`*position*` yellow.
- **Q-034 (open):** enclosure placement on the CL250. There is no room under the seat. Claude recommends a rigid rear-subframe tray on the left side with the IMUs on the frame; analysis in `hardware-integration.md` §4.1, which also lists the measurements to take.
- **rt-core main:**
  - defs **v0.15.0** (#40). Golden vectors and 0xFD03 landed via **#39**: #34 and #37 had been merged into stacked branches and never reached main.
  - D-075 (a)-(d) via #38 + #41, (f) via #42; the 3rd safety-review round on #42 (no BLOCKER/MAJOR) and its MINORs via **#43** (re-ask clears every unverified DID's counts, 7 tests, docs; reviewed again, no BLOCKER/MAJOR). 135 client-core tests.
- **conn main:** D-075 via #24-#26; #27 closes review test gap 2 (quiet-window 0x7F keeps the 2000 ms retry, vs the fast request outside it); #28 mirrors rt-core#43 (re-ask counts + precedence test). 109 can_protocol tests. conn still pins defs v0.12.0.
- **Releases:** defs **v0.16.0** re-created on 9310893 (the first tag sat on f7847a7, without its content); `manifest.yaml` pins v0.16.0. rt-core v0.8.0 and conn v0.2.0 are the last releases; both mains are well ahead.
- Phase 0 build, data path and Mac setup are unchanged: see memory and `hardware-integration.md` §1-3.

## Next up (in order)

1. User: Q-034 measurements on the bike (§4.1 list, photos never committed); order Wave 1 (NUCLEO-H755ZI-Q first); confirm or change the D-075 provisional values whenever convenient. Open point for that: a never-answered unverified DID gets one engine-start re-ask per epoch, then stays stopped until key-off (no later recovery).
2. **User merges defs#83 and workspace#81** (independent, any order). Then Claude: defs v0.17.0 (`/signal-change`: OBD catalog / per-vehicle poll-list split (D-078 item 2), 0x19 + multi-value PID decode, identification DIDs, D-079 window schema, W1/W2 vs `RIDE_ELECTRICAL` 0xFD44) → testers implement D-080 with `safety-reviewer` → group B on the CL250 poll list after the V0/V1 bitmap, group C after Q-001 → group F with Wave 2 sensors.
2a. Claude, D-076/D-077 implementation when the server work starts: `/signal-change` BLE GPS position fields + codegen guard (then conn, mobile, server together, `vss-schema-guardian`); moto-server packaging (compose, TLS proxy, per-device token), live ingest protocol, moto-mcp HTTP transport (`architecture-guard`).
3. Claude: safety-node Layer 1. Steps: `/repo-bootstrap moto-safety-node`, then `/feature-module` cornering decision on the D-075 items 4-6 defaults, using `pack_checked` (defs v0.16.0), then `safety-reviewer`.
4. Claude: rt-core `features/derived` against the golden vectors (`/feature-module`, `architecture-guard`).
5. Claude, D-072 follow-ups: rt-core sends 0x120 and consumes 0x023; conn bumps defs (v0.12.0 → v0.16.0) and reads 0x023 for the HUD/phone; hil-bench restbus drops 0x083 and adds 0x023/0x120 when it exists.
6. Claude: expose the per-DID stop reason in the D-069 item 2 record (BLE vehicle-signal block / rt-core 0xFD02); needs a defs change (`/signal-change`).
7. User + Claude, vehicle data path: IMU header, SN65HVD230 (check its 120 Ω), DLC adapter; B2 on the desk; on the bike Q-001 listen-only capture, then V0/V1, GPS. **Also record the user's intermittent stall under load** (ride sessions + DTC read afterwards; the server's `stop_event` marks it) as a case study.
8. User: threshold proposals for the not-implemented derived signals (list in the 2026-10-17 report) → `/signal-change`.
9. Small: server ingest evaluates class A twice; HIL scenarios of E-19 and the D-075 reviews (0x7F ECU, short reset at crank, disagreeing response IDs; answered DIDs that then refuse every read with a crank re-ask: ≤ 1 + 4N session requests per epoch, verified DIDs never STALE).

## Blockers / pending decisions

- **Q-035** (when D-076 is revisited) waits for its first trigger (second user, foreign hosting, commercial use, published data). **Q-034** (placement) waits for the measurements. **Q-032** waits for HUD stages H0/H1. **Q-031** waits for Q-001; Q-001 waits for the listen-only capture.
- The NUCLEO-H755ZI-Q (not ordered) blocks CubeMX, Renode, Ç6, the FDCAN port and on-target budgets. Q-009 blocks the hil-bench host.
- Before safety-node Layer 1: Q-022 after fallback validation; Q-023 (5)-(6) in its design.
- **User:** C-4 (old `can-dbc-conventions` skill on claude.ai); Q-024, Q-025; D-030 confirmation; Q-027/Q-028 later; the friend's stack before a contributor task list is written (the Gemini plan was not saved).

## Recent sessions

- 2026-10-19 (local): Gemini contributor-plan log reviewed (analysis only, plan not saved → TEMPLATE Result section); logs + strategy note committed, `docs-presentation/` and `learning/` kept local (workspace#81); anomaly stage 1: D-079 windows W1-W5 (no burst), D-080 0x19 freeze frames, G/I taxonomy, procurement 2.1 (defs#83, architecture-guard fixed); 14 worktrees pruned.
- 2026-10-18 (local, external review): Antigravity anomaly-sensor log reviewed (design only; verdicts in its Claude review); user decisions D-076 position relaxed + Q-035, D-077 two servers, D-078 scope (defs#82), invariant 7 + zones (workspace#79), 10 sync PRs; all merged on the user's instruction.
- 2026-10-18 (local, follow-up): rt-core#42 round-3 safety review → rt-core#43 + conn#28 (re-ask clears all unverified counts; reviewed, no BLOCKER/MAJOR), conn#27 test gap 2, D-075 (f) precedence recorded (defs#81); all merged on the user's instruction.
- 2026-10-18 (local, long): D-075 provisional defaults (defs#77-80), Q-034 placement analysis, rt-core#38-42 (stop epoch, (f), orphaned #34/#37 recovered, defs v0.15.0), conn#24-26, v0.16.0 tag fixed; three safety-reviewer rounds on rt-core, two on conn.
- 2026-10-18 (local): D-074 data paths (defs#73), platform bus v0.15.0 with 0x023/0x120 (defs#74), signal-change skill node list (workspace#74); Q-033 opened (defs#75).
