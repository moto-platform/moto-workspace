# Rename plan: moto-* → vehicle-* (draft)

Draft (Claude, 2026-10-27), **executed by opencode on 2026-10-28** on local `ext/opencode-moto-to-vehicle` branches (not pushed). User choices: GitHub org `vehicle-platform`; mobile `applicationId` unchanged; new prefix `vehicle-*`; scope = everything including the GitHub org and repos; the CL250 files stay the CL250 model profile (layer 3 of `moto-vehicle-defs/docs/ideas/vehicle-agnostic-anomaly-reasoning.md`) and a vehicle-class template is added beside them instead.

Execution deviations from this draft:

- No decision D-089 was recorded and no release tag or version bump was made (red zone; left for Claude/user).
- Consumers keep their pinned defs content: the defs rename is repeated on the `v0.14.0`, `v0.18.0` and `v0.19.0` bases. Mobile pins the renamed `v0.14.0` (`325898a`), rt-core/conn/server pin the renamed `v0.19.0` (`16b8648`), and the analyzer keeps the original `v0.18.0` tag because it reads only untagged source files.
- `moto-io-node` was renamed to `vehicle-io-node`, not archived.
- Local repo folders were renamed, but the workspace root folder (`~/Desktop/moto-platform`) was left for the user; remotes were pointed at `vehicle-platform/vehicle-*`.
- No `moto_defs` shim and no old env-var transition were added; all identifiers were replaced in place.
- Nothing was pushed, merged, tagged or released.

Scale measured on 2026-10-27: about 680 files mention "moto"; `moto_defs` is used 235 times; `MOTO_*` identifiers about 400 times; every consumer has the `external/moto-vehicle-defs` submodule (relative URL `../moto-vehicle-defs.git`).

## 1. Name map

| Today | New | Note |
|---|---|---|
| GitHub org `moto-platform` | `vehicle-platform` | Confirmed by the user (2026-10-27); check availability on GitHub before step 0 |
| Workspace folder / repo `moto-workspace` | `vehicle-workspace` | Local folder `~/Desktop/moto-platform` → `~/Desktop/vehicle-platform` |
| `moto-vehicle-defs` | `vehicle-defs` | Not `vehicle-vehicle-defs` |
| `moto-rt-core` | `vehicle-rt-core` | |
| `moto-safety-node` | `vehicle-safety-node` | |
| `moto-connectivity-node` | `vehicle-connectivity-node` | |
| `moto-linux-node` | `vehicle-linux-node` | |
| `moto-mcp` | `vehicle-mcp` | |
| `moto-hil-bench` | `vehicle-hil-bench` | |
| `moto-server` | `vehicle-server` | |
| `moto-ml` | `vehicle-ml` | |
| `moto-mobile` | `vehicle-mobile` | |
| `moto-analyzer` | `vehicle-analyzer` | |
| `moto-io-node` | archived, not renamed | Retired by D-072, holds no code |
| Python package `moto_defs` | `vehicle_defs` | One release keeps a `moto_defs` shim that re-exports and warns |
| C macros / env vars `MOTO_*` | **open: `VP_*` proposed** | `VEHICLE_*` is already taken by per-vehicle and signal macros (`VEHICLE_CL250_*` about 18 000 uses, `VEHICLE_SIGNAL_*`, `VEHICLE_SPEED_*`); reusing it would mix platform names with vehicle facts |
| CL250 files (`cl250_constants.yaml`, `vehicle_cl250.yaml`, `cl250_derived.yaml`, `VEHICLE_CL250_*`) | unchanged | Model profile (D-078) |

Not renamed: recorded decision text D-001..D-088 (history keeps the names of its time; the new decision carries the map), `docs/archive/`, git history, release tags.

## 2. Order (one PR per step, CI green before the next)

0. **User, GitHub:** check that `vehicle-platform` is free; rename the org, then each repo (Settings → Rename). GitHub redirects the old URLs, so clones, submodules and CI keep working during the migration. Archive `moto-io-node`.
1. **Workspace:** record the decision (next free D-number after D-089) with this map; update `manifest.yaml` URLs, `scripts/sync_claude.py` repo list, `PLATFORM-RULES.md`, `CLAUDE.md`, `external-ai/` base and zones, `setup.sh`, `STATUS.md`; run the sync. Rename the local folders and `git remote set-url` in each clone.
2. **vehicle-defs:** package `vehicle_defs` + `moto_defs` shim; codegen output names; the platform macro prefix; docs and README; release as a MINOR (0.x) with a CHANGELOG migration section.
3. **Consumers, each its own PR + release:** move the submodule to `external/vehicle-defs` (URL `../vehicle-defs.git`), bump to the new defs tag, update imports, macros, CMake/PlatformIO/pyproject/pubspec names, CI paths. Order: server → rt-core → connectivity-node → analyzer → mobile → empty repos (README/rules only).
4. **Runtime names with a transition:** env vars accept the old `MOTO_*` name for one release with a warning (server `MOTO_LIVE_SOURCE`, `MOTO_CORS_ORIGINS`, `MOTO_DATA*`, `MOTO_API*`); BLE device name and the ESP32 project name change together with a mobile release that accepts both.
5. **Last:** drop the `moto_defs` shim and the old env names in the next defs/server release; pin everything in the manifest; `/handoff`.

## 3. Risks to check

- Mobile `applicationId`: **kept unchanged** (user, 2026-10-27); only the display name and the repo/package names change, so installed apps update in place and keep their local data.
- The 12 repos are public: old links in READMEs and papers keep working only through GitHub's redirect, which breaks if someone later creates a repo with an old name.
- Open worktrees and branches: run `scripts/worktrees.py --prune` before step 1.
- Local git needs delete permission in the connected folder (lock files) for Claude to run the steps from a linked session; otherwise run them in a local Claude Code session at the workspace root.
