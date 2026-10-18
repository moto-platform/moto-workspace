---
date: 2026-10-18
tool: antigravity/gemini-4-argon
topic: contributor-task-plan
repos: [moto-workspace]
branches: []
prs: []
zone: green
review: done 2026-10-19 (analysis only, no repo change; the plan itself was not saved, so nothing to verify; TEMPLATE gains a Result section, workspace PR)
---

# contributor-task-plan

## Goal
Analyze the current state of moto-platform and design a safe, isolated onboarding plan and concrete starter tasks for a friend contributing to the senior thesis project without risking core architecture or safety-critical foundations.

## Changes
- `moto-workspace/external-ai/log/2026-10-18-gemini-contributor-task-plan.md`: session log for analysis and contributor task planning (no code modified).

## Checks
- `python3 scripts/check_zones.py . --path external-ai/log/2026-10-18-gemini-contributor-task-plan.md`: GREEN

## Unsure about
- The friend's preferred tech stack (Python/Backend, Flutter/Mobile, ML/Data Science, or Embedded C). Providing options across the green/yellow isolated zones (`moto-mobile`, `moto-server`, `moto-mcp`, `moto-ml`) so the user can pick the best fit.

## For Claude
- No red-zone edits or architecture/signal changes requested in this session.

## Claude review
Analysis-only session: no branch, commit or PR in any repo (checked: no `AI-Agent:` commit since 2026-10-17 and no `ext/` branch in the 11 repos). Zone green.

Finding: the log records that a contributor plan and starter tasks were designed, but the plan is not in the log or in any file, so it cannot be reviewed or reused. Rule gap closed: `log/TEMPLATE.md` now has a *Result* section where analysis and planning sessions write their output.

Direction for when the contributor starts (from the zones, not from the lost plan): green and yellow paths in moto-mobile, moto-server, moto-mcp and moto-ml suit an isolated start; red paths (defs signals, safety partition, tester, invariant-8 modules) stay Claude-only. The contributor follows `AGENTS.md` (D-071) like any external tool: `ext/<tool>-<topic>` branches, the `AI-Agent:` trailer when an AI wrote the code, and a log per session.

Open: the friend's stack is still unknown (the log's *Unsure about*); the user decides it before a task list is written.
