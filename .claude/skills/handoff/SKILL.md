---
name: handoff
description: End-of-session handoff for moto-platform. Updates STATUS.md (and DECISIONS.md if decisions were made) so the next chat can resume with minimal context. Use when the user says "handoff", "wrap up", "save progress", "let's continue in a new chat", or when a task is finished and the context is getting large.
---

# Session handoff

Goal: the next session should resume by reading only `STATUS.md` (≤60 lines), not by replaying this conversation.

## Steps

1. **Collect facts from this session** (do not re-read large files):
   - what was done (files/repos touched, features finished),
   - what is uncommitted: run `git -C <repo> status --short` for each repo touched this session,
   - decisions made with the user, open questions raised or resolved,
   - the next concrete step and any blockers.
2. **Decisions:** for every decision the user made (or approved), append a `D-0NN` entry to `moto-vehicle-defs/docs/DECISIONS.md` (next free number, date, who decided, what, why). For a resolved `Q-0NN`, move it into a decision and remove the row from the open-questions table. New open questions get a new `Q-0NN` row.
3. **Rewrite `STATUS.md`** at the workspace root, keeping its sections:
   - header: phase + last updated date (absolute, e.g. 2026-09-25),
   - `Where we are` — current state, max ~8 bullets,
   - `Next up` — ordered, each item actionable and naming the skill/agent to use (e.g. "`/signal-change` add IMU messages to platform.dbc"),
   - `Blockers / pending decisions` — reference Q-IDs,
   - `Recent sessions` — prepend one line for this session; keep at most 5 lines, drop the oldest.
   Stay under 60 lines. Remove anything stale.
4. **Worktrees:** run `python3 scripts/worktrees.py --check` from the workspace root. List the rows marked **remove** in the reply and ask the user before running `python3 scripts/worktrees.py --prune`. Never delete a worktree marked keep/review.
5. If a repo's `CLAUDE.md` became inaccurate (new module, changed build command), fix that line too.
6. Reply to the user with a 3-5 line summary, list the uncommitted repos, and suggest `/clear` (or a fresh chat) to continue with a clean context.

Do not commit unless the user asks.
