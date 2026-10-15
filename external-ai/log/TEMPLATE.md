---
date: YYYY-MM-DD
tool: <tool>/<model>            # e.g. gemini-cli/gemini-2.5-pro, opencode/deepseek-v3, cursor/gpt-x
topic: <short-topic>
repos: [<repo>, ...]
branches: [<repo>:ext/<tool>-<topic>, ...]
prs: []                          # <repo>#<n> once opened
zone: green | yellow | red       # worst result of scripts/check_zones.py
review: pending                  # Claude sets: done YYYY-MM-DD (<summary>)
---

# <topic>

## Goal
What the user asked for, in one or two sentences.

## Changes
- `<repo>/<path>`: what changed and why.

## Checks
- `<command>`: pass / fail (paste the failing part).
- `python3 scripts/check_zones.py <repo>`: <result>

## Unsure about
Assumptions, shortcuts, things you could not verify (hardware, CI-only checks, missing context).

## For Claude
Red-zone requests (path + wanted change), signals or decisions that would be needed, suspected conflicts with PLATFORM-RULES or DECISIONS.md, refactors you would suggest.

## Claude review
(Filled by Claude's /external-review: findings, fixes, PRs.)
