# STATUS — session handoff

> Keep it short (≤60 lines). Updated by the `/handoff` skill. "Recent sessions" keeps at most 5 one-line entries; drop the oldest.

**Phase:** 0 — environment and architecture ready, no code yet
**Last updated:** 2026-09-25

## Where we are

- Every repo has only README + CLAUDE.md (one "Initial commit"). All 11 repos + `moto-workspace` live in the org `github.com/moto-platform` (transferred 2026-09-25), pushed, **private** (D-017). Claude GitHub app is connected to the org.
- Architecture and decisions: `moto-vehicle-defs/docs/ARCHITECTURE.md`, `DECISIONS.md` (D-001..D-018, Q-001..Q-010).
- Docs are translated to English. Turkish originals live in `moto-vehicle-defs/docs/tr/`, and the advisor docs (`tr/bitirme-*`) stay Turkish.
- Claude environment: root `CLAUDE.md` + `PLATFORM-RULES.md` (synced into every repo by `scripts/sync_claude.py`, D-018), `.claude/agents` (4), `.claude/skills` (4), `.claude/settings.json`, and English CLAUDE.md files in every repo.

## Next up (in order)

1. **moto-vehicle-defs skeleton** → `/repo-bootstrap moto-vehicle-defs` (platform.dbc draft, codegen, CI) → tag `v0.1.0`.
2. **moto-hil-bench host** skeleton after deciding Q-009. Q-005: update the advisor scope doc?

## Blockers / pending decisions

- Q-001 (CL250 bus type/bitrate) blocks `cl250.dbc` content, not `platform.dbc`.
- Q-003 (F103 dual role), Q-006 (HARA/requirements location).

## Recent sessions

- 2026-09-25 (cont.): Org created, repos transferred and pushed, back to private, per-repo Claude asset sync added. Cloud credit = cloud sessions only.
- 2026-09-25: Reviewed all docs, resolved contradictions (D-008, D-009), wrote ARCHITECTURE + ADR log, built the Claude environment, translated the docs to English.
