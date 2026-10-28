---
date: 2026-10-27
tool: opencode/deepseek-v4.1-flash-free
topic: project-analysis-and-rename-preparation
repos: [moto-workspace]
branches: []
prs: []
zone: yellow
review: done 2026-10-28 (reports kept as a dated snapshot; C-01 false at origin, C-06 and the safety items → ISSUES E-25)
---

# Project analysis and rename preparation

> **Post-rename note (2026-10-28):** the analysis snapshot below predates the `moto` → `vehicle` rename and therefore uses the old names. The execution is recorded in `2026-10-28-opencode-moto-to-vehicle.md`; the "no repo was modified" statement applies to the analysis phase only.

## Goal

The user asked for a full-project read (every file, not only markdown), a separate report of problems/contradictions, an outside-view summary, a signature on every change, and execution of `RENAME-PLAN.md` (moto → vehicle, motorcycle → general vehicle category).

## Changes

- `moto-workspace/PROJECT-OVERVIEW.md` (new, yellow): outside-view summary, architecture, maturity matrix, strengths/weaknesses, rename status.
- `moto-workspace/PROJECT-CONTRADICTIONS.md` (new, yellow): 55 findings with `file:line` evidence, severity and owner.
- `moto-workspace/external-ai/log/2026-10-27-opencode-project-analysis.md` (new, green): this log.
- No repo was modified, no branch or PR was created. `RENAME-PLAN.md` was read, not edited.

## Result

### Verified before the rename

1. **The GitHub org rename is already done.** `moto-platform` returns 404 and `vehicle-platform/moto-workspace` resolves via `gh`; repo names are still `moto-*`. `RENAME-PLAN.md` still says "not applied", and `README.md:3` org-root link is now 404.
2. **The plan's numbers are wrong.** 490 tracked files mention `moto` (459 in repos + 31 in the workspace), not 680. Only 5/12 consumers have the defs submodule (rt-core, conn, server, mobile, analyzer). D-089 does not exist; D-088 is the latest on `origin/main`.
3. **The plan is not executable by a non-Claude tool.** It touches defs codegen/packages, `gen/`, safety-node, io-node, `.claude/`, `AGENTS.md`, `PLATFORM-RULES.md`, `manifest.yaml` and `scripts/*` — all red zones. D-036 also forbids external tools from tags, version bumps, pin changes and manifest edits.
4. **Local workspace is stale.** defs 2 commits behind, rt-core 3, conn 2, analyzer 1; mobile fetch failed with an SSL timeout. `STATUS.md:21` describes `origin/main`, not this checkout.
5. **Release integrity defect.** defs tags `v0.15.0` and `v0.16.0` both point at `f7847a7`; `manifest.yaml:9` expects `v0.16.0 = 9310893`.
6. **Safety findings.** Analyzer never verifies the SLCAN `L` acknowledgement (`webSerialCan.ts:42-45`) though the UI claims listen-only; connectivity-node allocates `std::string`/`sscanf` after init in the BLE write path (`BLEServerModule.cpp:219-252`); tester transmit can block 5 ms (`TwaiCanBus.cpp:57`).

The detailed evidence is in the two report files.

### Rename execution state

Blocked on user decisions. The safe sequence I recommend:

- **Claude (red):** record D-089; rename the defs package `moto_defs`/`moto_codegen`, `gen/` trees, C macros and the submodule path; update `zones.json`, `scripts/*`, `.claude/*`, `AGENTS.md`, `PLATFORM-RULES.md`, `manifest.yaml`; cut the defs release that consumers pin.
- **External tool (yellow/green):** repo READMEs/CLAUDE.md, non-generated code references, workspace `README.md`/`STATUS.md`/`ISSUES.md`, mobile/analyzer display strings, this analysis pair.
- **User:** GitHub repo renames via `gh repo rename` (11 repos; archive `moto-io-node` or keep its name), local folder renames, PR merges.
- **Order:** defs release first, then one consumer per PR, then workspace docs/setup, then local folder rename last. Never a bulk find-and-replace.

## Checks

- `python3 scripts/check_zones.py . --path PROJECT-OVERVIEW.md PROJECT-CONTRADICTIONS.md external-ai/log/2026-10-27-opencode-project-analysis.md`: YELLOW, YELLOW, GREEN (workspace docs are yellow; log is green).
- Git state: workspace on `main`, no commits made; `RENAME-PLAN.md`, `models/` and the two new reports are untracked.
- No build/test commands were run: no code changed and no repo was checked out for editing. Repo test commands belong to the rename PRs.

## Unsure about

- `moto-mobile` and part of the analyzer origin state could not be fetched (network/SSL), so their findings use the local HEAD; the mobile tree may already be ahead.
- The defs codegen drift check (`make check`) was not executed; generated trees were compared structurally.
- Hardware, on-target timing and CI-only checks were not run.
- Whether the user wants in-file signature headers on every future project file or only a commit trailer + manifest. In-file headers in firmware/generated code would violate the "no comments" and generated-file rules, so I recommend trailer + manifest only.
- Whether `moto-io-node` should be renamed or archived. The org has it unarchived but it has no code (D-072).

## For Claude

- **Decision:** record the naming decision (org already `vehicle-platform`) in `DECISIONS.md` as D-089 and correct the plan's org/step-0 statement.
- **Red-zone edits:** defs package/codegen rename, `gen/` regeneration, C macro prefix, submodule path rename, `zones.json`/`scripts/*`/`.claude/*`/`AGENTS.md`/`GEMINI.md`/`PLATFORM-RULES.md`/`manifest.yaml` updates, defs release tag.
- **Review:** the two new yellow reports; correct any finding that is wrong at `origin/main` (especially mobile/analyzer, which the network prevented me from refreshing).
- **Release integrity:** fix the `v0.16.0` tag (do not move it silently; decide whether to retag or record the defect) and the `moto-server` `defs_pin.txt` (v0.14.0 → v0.19.0).
- **Safety:** analyzer SLCAN `L` verification and conn BLE heap/string + 5 ms transmit belong to their repos' owners; both are red or yellow paths and need tests.

## Claude review

- **Decision / red-zone work:** done by the 2026-10-28 rename (see that log) and D-089 (defs#107).
- **C-01 (P0) is false at `origin`:** remote `v0.16.0` = `9310893`, matching the manifest; only the local defs clone had a stale tag (now fixed with `git fetch --tags --force`). `setup.sh` not force-updating tags is the real cause.
- **Verified true, tracked as ISSUES E-25:** C-06 server `defs_pin.txt` still `v0.14.0`; analyzer sends SLCAN `C`/`S6`/`L` without checking the adapter's reply; conn `onWrite` copies into a `std::string` and parses with `sscanf` on the BLE task (non-safety path, heap avoided rule); conn `twai_transmit` waits up to 5 ms.
- The other findings were not re-verified; the two reports stay as a dated pre-rename snapshot, not a backlog. A future session picks findings from them into ISSUES after checking each at `origin/main`.
