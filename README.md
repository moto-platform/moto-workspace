# moto-workspace

Workspace for the [moto-platform](https://github.com/moto-platform) motorcycle SDV / ADAS project.
It holds the cross-repo tooling. The 12 platform repos are independent and are cloned next to this file by `setup.sh`.

| Path | Purpose |
|---|---|
| `manifest.yaml` | Known-good version combination of all repos |
| `setup.sh` | Clone/update every repo and its submodules at its manifest ref; stops on any git error (`brew install yq` first) |
| `CLAUDE.md` | Platform-wide instructions for Claude Code |
| `STATUS.md` | Session handoff: where we are, what's next |
| `.claude/agents/`, `.claude/skills/` | Shared Claude Code agents and skills |
| `AGENTS.md`, `GEMINI.md` | Rules for AI tools other than Claude Code (generated, D-071) |
| `external-ai/` | Their edit zones, session logs and how-to (`external-ai/README.md`) |

Architecture and decisions live in [`moto-vehicle-defs/docs`](https://github.com/moto-platform/moto-vehicle-defs/tree/main/docs) (`ARCHITECTURE.md`, `DECISIONS.md`).

## Quick start

```bash
git clone https://github.com/moto-platform/moto-workspace.git moto-platform
cd moto-platform && ./setup.sh
claude   # always start Claude Code from this root
```
