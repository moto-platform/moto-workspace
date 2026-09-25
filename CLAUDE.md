# CLAUDE.md — moto-workspace (workspace root)

@PLATFORM-RULES.md

This folder is the `moto-workspace` repo (manifest, setup, shared `.claude/`). It ignores the 11 independent platform repos cloned inside it (D-015). Locally, **always start Claude from this root** so every repo and the shared agents/skills are available. Each repo also carries synced copies of its relevant agents/skills and of `PLATFORM-RULES.md` for single-repo cloud sessions.

## Session protocol

1. At session start read `STATUS.md` (short). Do NOT read the large docs.
2. Architecture: `moto-vehicle-defs/docs/ARCHITECTURE.md` + `DECISIONS.md` first. For details, use the `docs/README.md` index or the `docs-researcher` agent.
3. Broad code search → `Explore` agent. Single file/symbol → Grep/Read directly.
4. One session = one task. When done, run `/handoff` to update `STATUS.md` and suggest `/clear`.
5. Keep Opus for architecture and safety judgment. Bulk work goes to `sonnet`/`haiku` subagents.

## Shared Claude assets (source of truth here)

- `PLATFORM-RULES.md`, `.claude/agents/`, `.claude/skills/` are the **only** place to edit these. After editing, run `python3 scripts/sync_claude.py` to copy them into each repo's `.claude/`, then commit in the affected repos. `--check` reports drift without writing.
- Which repo receives which agent/skill is defined in `scripts/sync_claude.py` (`REPO_ASSETS`).

| Agent | Model | Use |
|---|---|---|
| `docs-researcher` | haiku | Answers questions from the docs without loading them into the main context |
| `vss-schema-guardian` | haiku | Detects hardcoded CAN IDs/signals/VSS paths, checks the defs submodule pin |
| `architecture-guard` | sonnet | Checks repo scope, layering, dependency direction, bus rules and decisions |
| `safety-reviewer` | opus | ISO 26262/MISRA-aware review of safety-critical changes |
| `hil-scenario-validator` | — | Repo-owned by moto-hil-bench (not synced) |
