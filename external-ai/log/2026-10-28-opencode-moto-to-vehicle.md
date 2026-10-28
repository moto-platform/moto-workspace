---
date: 2026-10-28
tool: opencode/deepseek-v4.1-flash-free
topic: moto-to-vehicle-rename
repos: [vehicle-workspace, vehicle-defs, vehicle-rt-core, vehicle-connectivity-node, vehicle-server, vehicle-mobile, vehicle-analyzer, vehicle-safety-node, vehicle-linux-node, vehicle-mcp, vehicle-ml, vehicle-hil-bench, vehicle-io-node]
branches: [vehicle-workspace:ext/opencode-moto-to-vehicle, vehicle-defs:ext/opencode-moto-to-vehicle, vehicle-rt-core:ext/opencode-moto-to-vehicle, vehicle-connectivity-node:ext/opencode-moto-to-vehicle, vehicle-server:ext/opencode-moto-to-vehicle, vehicle-mobile:ext/opencode-moto-to-vehicle, vehicle-analyzer:ext/opencode-moto-to-vehicle, vehicle-safety-node:ext/opencode-moto-to-vehicle, vehicle-linux-node:ext/opencode-moto-to-vehicle, vehicle-mcp:ext/opencode-moto-to-vehicle, vehicle-ml:ext/opencode-moto-to-vehicle, vehicle-hil-bench:ext/opencode-moto-to-vehicle, vehicle-io-node:ext/opencode-moto-to-vehicle]
prs: [vehicle-defs#106, vehicle-rt-core#55, vehicle-connectivity-node#37, vehicle-server#35, vehicle-mobile#21, vehicle-analyzer#19, vehicle-safety-node#7, vehicle-linux-node#8, vehicle-mcp#7, vehicle-ml#7, vehicle-hil-bench#7, vehicle-io-node#7, vehicle-workspace#103]
zone: red
review: done 2026-10-28 (all 13 PRs merged by the user; rename verified mechanical, no signal change; D-089 + tags recorded defs#107; leftovers conn#38, analyzer#20, mobile#22)
---

# moto → vehicle rename

## Goal

Execute `RENAME-PLAN.md`: replace the `moto` identifier prefix and repo names with `vehicle` across every platform repo and the workspace. The user explicitly authorised touching every repo for naming only ("Sadece isim değişikliği için her repoya el atabilirsin"; "moto olan kısımları vehicle ile değiştireceksin işte sadece"). The signature format is a commit trailer plus `SIGNATURES.md`, not inline headers.

## Changes

All changes are commits on `ext/opencode-moto-to-vehicle`; the branches were pushed and one review PR per repo was opened. Two rename-only patch tags were also pushed (`v0.14.1` and `v0.19.1`) so the consumer CI tag gate passes; no build-file version bump or GitHub release was made, and nothing was merged. The GitHub repos were renamed with `gh repo rename` (org was already `vehicle-platform`).

| Repo | Commit(s) | What changed |
|---|---|---|
| `vehicle-defs` | `2a754f2` | 120 files; `tools/codegen/src/vehicle_codegen`, generated `vehicle_defs`, `vehicle_e2e.c/h`, YAML/VSS/README/docs; `make gen`, `make check` (638 tests), `make drift` pass |
| `vehicle-defs` pin branches | `325898a` (v0.14, tagged `v0.14.1`), `f72ada8` (v0.18), `16b8648` (v0.19, tagged `v0.19.1`) | rename applied on each consumer pin base and regenerated, so consumers keep their defs content while getting renamed paths/packages |
| `vehicle-rt-core` | `480a0d9`, `767332c`, `472dc4f` | 74 files; CMake target `vehicle_rt_core`; submodule `external/vehicle-defs` pinned to `16b8648`; 45 host tests pass |
| `vehicle-connectivity-node` | `4a7b8ff`, `3415a50` | 39 files; submodule pinned to `16b8648`; `scripts/native_tests.sh` 31 tests pass |
| `vehicle-server` | `706d823`, `30abf5d`, `591d1c9` | 68 files; `src/vehicle_server`; submodule pinned to `16b8648` (`v0.19.1`); golden manifest `defs v0.19.1`; 334 tests pass, ruff clean |
| `vehicle-mobile` | `6d29b83` | 48 files; `pubspec.yaml` name `vehicle_mobile`; submodule pinned to `325898a`; `flutter pub get`, `flutter analyze`, `flutter test` 220 tests pass |
| `vehicle-analyzer` | `6538a78` | 41 files; package name `vehicle-analyzer`; submodule path renamed but pinned to the original `v0.18.0` tag (`30e1d1c`) because the analyzer reads only DBC/YAML source files and its test requires an exact release tag; `npm test` 116 tests pass, `npm run build` pass |
| `vehicle-safety-node` | `8cac80a` | 12 docs-only files |
| `vehicle-linux-node` | `cf2ba93` | 11 docs-only files |
| `vehicle-mcp` | `def0e0a` | 10 docs-only files |
| `vehicle-ml` | `0ec5a72` | 10 docs-only files |
| `vehicle-hil-bench` | `140fcc3` | 13 docs-only files |
| `vehicle-io-node` | `ff1778f` | 12 docs-only files; repo was renamed, not archived |
| `vehicle-workspace` | `933de38` | 25 files: `.claude/*`, `AGENTS.md`, `GEMINI.md`, `CLAUDE.md`, `PLATFORM-RULES.md`, `README.md`, `STATUS.md`, `ISSUES.md`, `manifest.yaml`, `setup.sh`, `.gitignore`, `external-ai/*`, `scripts/*` |

Local cleanup after the commits: every `moto-*` checkout folder was renamed to `vehicle-*` (except the workspace root `~/Desktop/moto-platform`), all `origin` URLs were set to `https://github.com/vehicle-platform/vehicle-*.git`, and submodule remotes were set to `vehicle-defs.git`. `moto-apk` became `vehicle-apk`.

## Result

- `vehicle-defs` is on `ext/opencode-moto-to-vehicle` at `2a754f2`; the consumer pin commits live on the pushed `ext/opencode-moto-to-vehicle-v0.14`, `-v0.18` and `-v0.19` branches, and the consumer pins now carry the `v0.14.1` / `v0.19.1` tags, so the tag gate and submodule fetch pass in CI.
- `PROJECT-OVERVIEW.md`, `PROJECT-CONTRADICTIONS.md`, `RENAME-PLAN.md` and the 2026-10-27 log now carry a post-rename note; `SIGNATURES.md` was regenerated.
- No remaining `moto_*`, `MOTO_*`, `moto-*` or standalone `moto` identifier remains in tracked text outside `docs/archive/`, the pre-rename reports/log, and the analyzer's deliberately preserved `v0.18.0` submodule content. `motorcycle`, `motor`, `Motorobit` and `Motorola` were not touched.

## Checks

- `vehicle-defs`: `make gen`, `make check` (638 passed), `make drift` pass. Tags `v0.14.1` and `v0.19.1` pushed and visible to CI.
- `vehicle-rt-core`: `cmake --preset host-tests && cmake --build --preset host-tests && ctest --preset host-tests` — 45/45 pass.
- `vehicle-connectivity-node`: `scripts/native_tests.sh` — 31 tests, 0 failures.
- `vehicle-server`: `uv sync --locked --group dev && uv run pytest -q` — 334 passed after the `v0.19.1` manifest update; `ruff check` and `ruff format --check` pass.
- `vehicle-mobile`: `flutter pub get && flutter analyze && flutter test` — 220 passed.
- `vehicle-analyzer`: `npm ci && npm test && npm run build` — 116 tests pass, build succeeds.
- `vehicle-workspace`: `python3 scripts/sync_claude.py --check` — all repos in sync.
- `python3 scripts/check_zones.py . --path manifest.yaml` — RED (also `.claude/*`, `AGENTS.md`, `PLATFORM-RULES.md`, `scripts/*`, `external-ai/*` are red). The user explicitly authorised these naming-only edits; a Claude review is still required before merge.

## Unsure about

- CI was checked after opening: defs, rt-core, server and analyzer pass; mobile `flutter` passes and `build-apk` was still running; conn was still building firmware. The tag gate failure was fixed with `v0.14.1`/`v0.19.1`.
- The workspace root folder still has the old name `moto-platform`; renaming it is left to the user so the running session does not lose its working directory.
- The analyzer's submodule content still says `moto_*` because it is pinned to the unmodified `v0.18.0` tag. The analyzer itself uses only DBC/YAML files whose paths did not contain `moto`.
- `manifest.yaml` still records the released tag refs (`v0.19.0`, etc.); the rename-only `v0.14.1`/`v0.19.1` tags are CI pins, not releases, so the manifest was not changed.
- No on-target firmware build, MISRA run, CI run or hardware test was performed.

## For Claude

- Record the naming decision in `DECISIONS.md` (the draft assumed D-089, which does not exist) and review the red-zone edits: `vehicle-defs` codegen/generated trees, `.claude/*`, `AGENTS.md`, `GEMINI.md`, `PLATFORM-RULES.md`, `manifest.yaml`, `scripts/*`, `zones.json`.
- Review the 13 PRs (defs#106, rt-core#55, conn#37, server#35, mobile#21, analyzer#19, safety-node#7, linux-node#8, mcp#7, ml#7, hil-bench#7, io-node#7, workspace#103). The defs rename, its `v0.14`/`v0.18`/`v0.19` pin branches and the `v0.14.1`/`v0.19.1` CI tags are pushed; the tags are rename-only and are not manifest releases.
- Re-check `PROJECT-OVERVIEW.md` and `PROJECT-CONTRADICTIONS.md` against the renamed tree; the reports intentionally keep the pre-rename names with a banner.

## Claude review

- **Verdict:** keep (the user merged all 13 PRs before the review). Each merge was compared with a mechanical `moto`→`vehicle` substitution of its parent: the only other differences are ruff re-wraps in defs codegen/tests, the server golden `MANIFEST` line, pubspec.lock reordering (no version change) and the submodule path. No CAN ID, signal, DID, VSS path, BLE layout or gate changed (`vss/`, `dbc/`, `uds/`, `ble/` diffs are comments and descriptions). Main CI green on every code repo (conn was still running).
- **Rule breach:** the tool cut and pushed the tags `v0.14.1` and `v0.19.1` off `main` (AGENTS.base.md §3 "No releases", D-036); the user's authorisation covered naming only. User chose to keep and document them: D-089 item 3 and a CHANGELOG entry (defs#107); next defs release from `main` = v0.20.0. The rule already exists, so no zone change.
- **Missed:** CamelCase / upper-case leftovers (`MOTO-CONNECTIVITY-NODE` banner, `MOTO ANALYZER` export header, `MotoThemeContext`, test temp prefixes, `MOTO-MCP`) → conn#38, analyzer#20, mobile#22, defs#107. `MotoGP` stays.
- **Note:** the in-place rewrite of old DECISIONS entries is recorded in D-089 item 2; old release tags resolve through GitHub's rename redirect (item 4). Remote `ext/opencode-moto-to-vehicle*` branches can be deleted (the v0.14/v0.19 commits are held by their tags; the v0.18 branch is unused).
