# external-ai — working on vehicle-platform with AI tools other than Claude Code

D-071. Other models write code in the safe zones, log what they did, and Claude reviews and refactors it later, so the token budget goes to review and safety work instead of typing.

| File | Purpose |
|---|---|
| `AGENTS.base.md` | Source of `AGENTS.md` / `GEMINI.md` (rendered by `scripts/sync_claude.py` together with `PLATFORM-RULES.md` and `zones.json`) |
| `zones.json` | Which paths are red (Claude only), yellow (Claude review before merge) or green |
| `log/TEMPLATE.md` | Copy per session to `log/YYYY-MM-DD-<tool>-<topic>.md` |
| `log/*.md` | Session logs; `review: pending` until Claude's `/external-review` |
| `../scripts/check_zones.py` | Zone check of a repo's changes (exit 2 red, 1 yellow, 0 green) |

## Starting a tool

Always start it at the workspace root (`vehicle-platform/`), like Claude Code, so it sees `AGENTS.md`, `STATUS.md`, the log folder and every repo. A tool started inside one repo only sees that repo's synced `AGENTS.md` and cannot write the log; then the log text goes into the PR description.

| Tool | How it gets the rules |
|---|---|
| Codex CLI, opencode, Cursor, GitHub Copilot agent and most current agents | read `AGENTS.md` automatically |
| Gemini CLI | reads `GEMINI.md` (same content) |
| Aider (e.g. with a DeepSeek API key) | `aider --read AGENTS.md` (or `read: AGENTS.md` in `.aider.conf.yml`) |
| Web chat (DeepSeek, Gemini, ChatGPT) | paste `AGENTS.md` and the files to change; the chat cannot run checks, so run `python3 scripts/check_zones.py <repo>` and the repo's tests yourself before committing |

Check your tool's own documentation if it does not pick the file up.

**Pitfall:** the workspace `.gitignore` ignores the 11 repos (`/vehicle-*/`), and some tools hide gitignored files from their search and indexing. If the tool says it cannot find a repo's files, either turn off its gitignore filtering for this folder, or start it inside that repo (each repo carries a synced `AGENTS.md`) and write the log text into the PR description.

First prompt that works with any tool:

> Read AGENTS.md and STATUS.md. Task: <task>. Create the log file from external-ai/log/TEMPLATE.md first. Check zones before editing. Do not commit until I say so.

## Good tasks for other models

Green/yellow work with tests: vehicle-mobile screens, vehicle-server ingestion/reports, the D-070 Python reference of derived signals in vehicle-server, tests, scripts, docs drafts (`vehicle-defs/docs/ideas/`).

## Keep for Claude

Everything red in `zones.json`: vehicle-defs (signals, codegen), `DECISIONS.md`, safety-node, io-node, rt-core cornering/UDS/heartbeat/E2E/watchdog, conn's vehicle-bus tester, releases and pins.

## Afterwards, in Claude Code

Run `/external-review`: it lists pending logs and `AI-Agent:` commits, checks zones, runs `architecture-guard` (+ `vss-schema-guardian`, `safety-reviewer` where they apply), fixes or refactors on a `claude/` branch and marks the logs `review: done`.
