# STATUS — session handoff

> Keep it short (≤60 lines). Updated by the `/handoff` skill. "Recent sessions" keeps at most 5 one-line entries; drop the oldest.

**Phase:** 0 — environment and architecture ready, no code yet
**Last updated:** 2026-09-25

## Where we are

- Every repo has only README + CLAUDE.md (one "Initial commit"). All 11 repos + `moto-workspace` live in the org `github.com/moto-platform` (transferred 2026-09-25), pushed, **private** (D-017). Claude GitHub app is connected to the org.
- Architecture and decisions: `moto-vehicle-defs/docs/ARCHITECTURE.md`, `DECISIONS.md` (D-001..D-023, Q-001..Q-010).
- Docs are translated to English. Turkish originals live in `moto-vehicle-defs/docs/tr/`, and the advisor docs (`tr/bitirme-*`) stay Turkish.
- Claude environment: root `CLAUDE.md` + `PLATFORM-RULES.md` (synced into every repo by `scripts/sync_claude.py`, D-018), `.claude/agents` (4), `.claude/skills` (4), `.claude/settings.json`, and English CLAUDE.md files in every repo.

## Next up (in order)

1. **Cloud session A: moto-vehicle-defs bootstrap + legacy extraction** (repos: moto-workspace, moto-vehicle-defs, HondaCl250_Telemetry). `/repo-bootstrap moto-vehicle-defs` with `uds/vehicle_cl250.yaml` (D-019/D-023 facts), `docs/legacy-telemetry-notes.md`, platform.dbc incl. rt-core vehicle-signal republish + heartbeats + EKF messages, codegen, CI. No tag without the user.
2. **Cloud session B: legacy port** (after A is merged; repos: moto-workspace, moto-vehicle-defs, moto-connectivity-node, moto-mobile, HondaCl250_Telemetry). Port per D-023 into connectivity-node (PlatformIO arduino+espidf) and moto-mobile (Flutter).
3. **moto-hil-bench host** skeleton (simulated CL250 UDS responder) after deciding Q-009.

## Blockers / pending decisions

- Q-002 (safety-node on INVALID/lost rt-core data) got more important with D-021.
- Q-001 remainder: is there passive broadcast traffic on the CL250 bus?
- Q-003 (F103 dual role), Q-006 (HARA/requirements location).

## Recent sessions

- 2026-09-25 (cont.): Legacy HondaCl250_Telemetry analysed, transferred (private, archived, tag legacy-final). Verified CL250 facts D-019; D-020..D-023 (allow-list, single tester, Flutter, hybrid port).
- 2026-09-25 (cont.): Org created, repos transferred and pushed, back to private, per-repo Claude asset sync added. Cloud credit = cloud sessions only.
- 2026-09-25: Reviewed all docs, resolved contradictions (D-008, D-009), wrote ARCHITECTURE + ADR log, built the Claude environment, translated the docs to English.
