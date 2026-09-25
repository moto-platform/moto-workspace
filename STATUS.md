# STATUS — session handoff

> Keep it short (≤60 lines). Updated by the `/handoff` skill. "Recent sessions" keeps at most 5 one-line entries; drop the oldest.

**Phase:** 0 — environment and architecture ready, no code yet
**Last updated:** 2026-09-25

## Where we are

- Every repo has only README + CLAUDE.md (one "Initial commit"). Remotes are at `github.com/alihanesentas/*`. The `moto-platform` org has not been created yet.
- Architecture and decisions: `moto-vehicle-defs/docs/ARCHITECTURE.md`, `DECISIONS.md` (D-001..D-014, Q-001..Q-010).
- Docs are translated to English. Turkish originals live in `moto-vehicle-defs/docs/tr/`, and the advisor docs (`tr/bitirme-*`) stay Turkish.
- Claude environment: root `CLAUDE.md`, `.claude/agents` (4), `.claude/skills` (4), `.claude/settings.json`, and English CLAUDE.md files in every repo.
- Uncommitted: `moto-vehicle-defs` (CLAUDE.md, docs/), plus CLAUDE.md in every other repo (and the translated hil-scenario-validator in moto-hil-bench).

## Next up (in order)

1. Commit the setup changes in each repo (user approval; e.g. `docs: add Claude instructions and architecture docs`).
2. **moto-vehicle-defs skeleton** → `/repo-bootstrap moto-vehicle-defs`: `platform.dbc` draft (node list, attributes, heartbeats 0x081-0x085, rt-core→safety EKF messages with E2E), empty `cl250.dbc`, `vss/overlay.vspec`, `uds/dids.yaml`, `tools/codegen` (cantools + per-node filter + E2E), `CHANGELOG.md`, CI (strict parse + gen drift check) → tag `v0.1.0`.
3. **moto-hil-bench host** skeleton (uv, scenario schema, pytest, python-can virtual bus) after deciding Q-009.
4. Create the GitHub org, transfer the repos, add a `.github` org profile repo.
5. Q-005: decide whether to update `tr/bitirme-projesi-kapsam.md` to match D-001 before the advisor meeting.

## Blockers / pending decisions

- Q-001 (CL250 bus type/bitrate) blocks `cl250.dbc` content, not `platform.dbc`.
- Q-003 (F103 dual role), Q-006 (HARA/requirements location).

## Recent sessions

- 2026-09-25: Reviewed all docs, resolved contradictions (D-008, D-009), wrote ARCHITECTURE + ADR log, built the Claude environment, translated the docs to English.
