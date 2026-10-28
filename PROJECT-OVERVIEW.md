# Project overview — outside view (2026-10-27)

> Prepared and signed by **opencode / deepseek-v4.1-flash-free** (`AI-Agent: opencode/deepseek-v4.1-flash-free`) on 2026-10-27.
> Method: all tracked text files of the 12 repos plus the workspace were scanned (459 repo files + 31 workspace files mention `moto`), with targeted line-by-line reads of the load-bearing code and docs. Binaries, vendored dependencies (`node_modules`, `.venv`, `.pio`, `external/` submodules) and git history were excluded. Local clones were behind `origin/main` at review time (see `PROJECT-CONTRADICTIONS.md` C-02), so state claims were re-checked against `origin/main` where possible.
>
> **Post-rename note (2026-10-28):** this report was written before the `moto` → `vehicle` rename. Repo and file names below use the pre-rename spelling; the rename has since been executed on the `ext/opencode-moto-to-vehicle` branches. See `RENAME-PLAN.md` and `external-ai/log/2026-10-28-opencode-moto-to-vehicle.md`.

## 1. What this is

A **software-defined-vehicle (SDV) diagnostics, telemetry and ADAS platform for motorcycles**, built as a senior thesis around one real vehicle (Honda CL250) with the stated intent (D-078) to grow into a multi-vehicle product. Twelve public repos under the `vehicle-platform` GitHub org (renamed from `moto-platform`), MIT licensed, with an unusually strict written governance layer: architecture summary, 88 recorded decisions (D-xxx), 37 open questions (Q-xxx), edit zones for AI tools, safety review gates and pinned cross-repo versions.

This is not a demo: roughly half the repos contain working code with host tests and CI. The other half are documented skeletons.

## 2. Architecture in one page

- **Two CAN buses.** A read-only *vehicle bus* (CL250 OBD port, classic CAN 500 kbps, polled UDS `0x22`) with exactly one tester — `moto-rt-core` (currently `moto-connectivity-node` until the H755 exists) — and a separate *platform bus* for our own nodes.
- **One dual-core MCU for the vehicle side.** STM32H755: Cortex-M7 runs `moto-rt-core` (CAN gateway, UDS/ISO-TP, logging, EKF, derived signals, bootloader); Cortex-M4 runs the isolated safety partition `moto-safety-node` (cornering, blind spot, immobilizer, LEDs), linked only through an HSEM + E2E mailbox. The H755 board is not ordered yet.
- **Edge.** ESP32-S3 bike unit (`moto-connectivity-node`: temporary tester, BLE/Wi-Fi, later helmet unit with HUD/voice) and a Raspberry Pi 5 (`moto-linux-node`, `moto-mcp`) for Kuksa/VSS, CV, MCP and OTA.
- **Cloud/desktop.** `moto-server` (FastAPI, sessions, Parquet/MDF4, live stream), `moto-mobile` (Flutter companion), `moto-analyzer` (TypeScript/React CAN analyzer), `moto-hil-bench` (restbus HIL), `moto-ml` (offline training).
- **Single source of truth.** `moto-vehicle-defs` holds DBC, VSS overlay, UDS YAML, BLE schema and Python codegen; consumers pin it as a submodule to release tags.

## 3. Maturity matrix (from code, not from docs)

| Repo | State | Evidence |
|---|---|---|
| `moto-vehicle-defs` | **Real, mature** | DBC/VSS/UDS/BLE + Python codegen + generated C/Python/Dart, 153 tracked files, tagged v0.19.0 |
| `moto-rt-core` | **Real, host-tested** | 88 C + 53 header files, host Unity tests, EKF/ISO-TP/UDS/derived signals; target board path still scaffold |
| `moto-connectivity-node` | **Real, on-target tested** | 43 headers + 22 C++ sources for ESP32-S3, PlatformIO envs, native tests |
| `moto-server` | **Real** | 52 Python modules/tests, ingestion, reports, Parquet, live stream |
| `moto-mobile` | **Real** | 39 Dart files, BLE client, sessions, upload |
| `moto-analyzer` | **Real** | 45 TS + 17 TSX files, views, replay, SLCAN |
| `moto-safety-node` | **Docs only** | 11 markdown files; no `src/`, tests, CMake or submodule |
| `moto-linux-node`, `moto-mcp`, `moto-ml`, `moto-hil-bench` | **Docs only** | README/CLAUDE.md promise directories and submodules that do not exist |
| `moto-io-node` | **Retired** | D-072; docs only |
| `moto-apk`, `models/`, `RENAME-PLAN.md` | **Local, untracked** | APK builds (~215 MB), CAD/STL assets, rename draft |

**The single biggest gap:** the safety partition — the part the invariants call the safety path — has no code yet. Cornering decisions currently exist only as rt-core's EKF output plus specs.

## 4. What looks strong

1. **Traceability.** Decisions, open questions, issue IDs, PR numbers and version pins are cross-referenced unusually well for a solo thesis project.
2. **Safety thinking is real.** Read-only tester policy, E2E profiles, fail-closed latch, fallback IMU, DTC freeze-frame rules, safety-reviewer gates.
3. **Generated signal layer.** No hand-written production CAN IDs found in the audited code; the defs pipeline and per-node gating are a genuine strength.
4. **AI governance.** Red/yellow/green zones, session logs and `AI-Agent:` trailers are ahead of most professional teams.
5. **Test culture** in rt-core/server/analyzer, including golden vectors and byte-exact frame tests.

## 5. What looks weak from outside

1. **Documentation drift is systemic.** Release pins, "not yet" tables, submodule claims and API versions lag behind the code in nearly every repo. A new contributor cannot trust the READMEs without diffing git.
2. **State is not reproducible from the workspace.** Local clones were 2–3 commits behind `origin/main`; STATUS.md and ISSUES.md describe a state the local tree does not contain. One release tag (`v0.16.0`) points at the wrong commit.
3. **Safety rules are documented better than enforced.** connectivity-node allocates `std::string` and parses with `sscanf` after init in a BLE write path; its CAN transmit can block 5 ms in the tester loop; the analyzer advertises "listen-only" but never verifies the adapter's `L` acknowledgement. These are exactly the kind of findings the zone/safety process should catch.
4. **Skeletons claim features.** HIL, linux-node, MCP and ML describe directories, submodules and build commands that do not exist. The same is true for safety-node's CLAUDE.md vs its README.
5. **The project is motorcycle-shaped at the identity level.** Org renamed, but repos, Python/Dart packages (`moto_defs`), C macros (`MOTO_*`/`VEHICLE_CL250_*`), VSS (`Vehicle.Motorcycle.*`), mobile label ("Honda CL250 Telemetry") and analyzer header are all motorcycle/CL250-specific. A repo rename alone is cosmetic; real generalization means a vehicle-class profile beside the CL250 profile (the plan keeps CL250 as a model profile, which is the right call).
6. **Bus factor 1 + no hardware.** The H755 board is not ordered, safety-node has no code, and the single tester still runs on the ESP32. The critical path is hardware, not more docs.

## 6. Rename status (as of this session)

- GitHub **org rename is already done**: `vehicle-platform` returns 200, `moto-platform` returns 404 via the API; `gh repo view vehicle-platform/moto-workspace` resolves. The org-root link in `README.md:3` is now a 404.
- **Repo names, packages, macros, paths and docs are unchanged** (`moto-*`, `moto_defs`, `MOTO_*`, `external/moto-vehicle-defs`).
- `RENAME-PLAN.md` is still accurate in intent but wrong in several numbers/prerequisites (see contradictions C-29..C-38). It also cannot be executed end-to-end by a non-Claude tool: the defs package/codegen, safety-node, io-node, `.claude/`, `AGENTS.md`, `PLATFORM-RULES.md`, `manifest.yaml`, `scripts/*` and every `gen/` tree are **red zones** (Claude only), and releases/pins are forbidden to external tools by D-036. A partial rename would break builds and CI rather than help.

## 7. Bottom line

The project is **more disciplined and more documented than its actual maturity**, with a strong data/defs core, credible rt-core/server/conn/mobile/analyzer code, and a safety story that is still mostly paper. The fastest quality win is not more documentation: it is syncing the workspace, fixing the release-tag/pin drift, and closing the safety-rule violations in connectivity-node and the analyzer. The rename is worth doing, but it must be a **phased, release-backed migration led by Claude**, not a bulk find-and-replace.
