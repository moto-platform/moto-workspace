---
name: external-review
description: Review, fix and refactor work done on vehicle-platform by AI tools other than Claude Code (D-071), using their session logs in external-ai/log and their `AI-Agent:` commits. Use when the user says "review what Gemini/DeepSeek/Codex did", "external review", "check the ext/ branches", or when STATUS.md or a session start shows pending external logs.
---

# External review (D-071)

Goal: other models write code cheaply; Claude spends its tokens on judgment — zones, architecture, signals, safety — and on refactoring where the code does not read like the rest of the repo. Workspace only (not synced to repos).

## Steps

1. **Collect** (cheap, no large reads):
   - `grep -l '^review: pending' external-ai/log/*.md` → the pending logs. Read their front matter and *For Claude* sections first.
   - Per repo named in them (or, if no log exists, per repo with activity): `git -C <repo> fetch -q`, then `git -C <repo> log origin/main --grep '^AI-Agent:' --since=<last review>` and `gh pr list -R vehicle-platform/<repo> --search 'head:ext/'`. Unlogged `AI-Agent:` commits or `ext/` PRs are findings too (missing log).
2. **Zones:** for each branch, `python3 scripts/check_zones.py <repo-or-worktree> --base origin/main`. Any red path → BLOCKER: the PR must not merge as is; Claude redoes that part on a `claude/` branch with the normal process (`/signal-change`, `/feature-module`, `safety-reviewer`).
3. **Review**, delegated to keep the main context small:
   - always `architecture-guard` (sonnet) on the diff: scope, layering, dependency direction, recorded decisions, the hard rules of `external-ai/AGENTS.base.md` §3;
   - `vss-schema-guardian` (haiku) if CAN, UDS, VSS, BLE or signal names are touched (hand-written literals are the most likely external-tool error);
   - `safety-reviewer` (opus) if anything in an invariant-8 module changed (should be red, so this means a zone breach);
   - run the repo's checks locally if CI has not run (the table in `AGENTS.base.md` §4).
4. **Fix or refactor** in a `claude/<topic>` worktree on top of the `ext/` branch (or a follow-up PR after the user merged it): style and naming of the surrounding code, tests, removed shortcuts. Keep the external author's commits; add Claude's on top. Open PRs per the user's merge-by-user rule and state the merge order.
5. **Close the log:** set `review: done YYYY-MM-DD (<one-line result, PRs>)` and fill its *Claude review* section. Turn *For Claude* requests into work: a `Next up` line in `STATUS.md`, an `ISSUES.md` row, or a question for the user. Rule gaps found (a path that should have been red, a tool that ignored AGENTS.md) → update `external-ai/zones.json` or `AGENTS.base.md`, run `python3 scripts/sync_claude.py`, and say so.
6. **Report** to the user (Turkish): per log — verdict (merge / fix first / redo), what Claude changed, open requests. Then `/handoff` if the session ends.
