# Problems and contradictions — 2026-10-27

> Prepared and signed by **opencode / deepseek-v4.1-flash-free** (`AI-Agent: opencode/deepseek-v4.1-flash-free`) on 2026-10-27.
> Scope: every tracked text file in the 12 repos + workspace was scanned; binaries, `node_modules`, `.venv`, `.pio`, build outputs and `external/` submodules were excluded. Local checkouts were 0–3 commits behind `origin/main` when the scan started (C-02), so repo-state findings were re-checked against `origin/main` where the network allowed. Items marked **test-only** or **docs-only** are lower impact but still listed because the project's own rules treat them as invariants.
> Severity: **P0** safety/release integrity · **P1** wrong build/state/docs users rely on · **P2** stale or misleading docs · **P3** cosmetic. Owner: who can fix it under `external-ai/zones.json`.
>
> **Post-rename note (2026-10-28):** this report was written before the `moto` → `vehicle` rename. Repo and file paths below use the pre-rename spelling; the rename has since been executed on the `ext/opencode-moto-to-vehicle` branches. See `RENAME-PLAN.md` and `external-ai/log/2026-10-28-opencode-moto-to-vehicle.md`.

## A. Release and workspace state

| ID | Sev | Evidence | Finding |
|---|---|---|---|
| C-01 | ~~P0~~ false at origin (Claude 2026-10-28: remote `v0.16.0` = `9310893`; only a stale local tag) | `moto-vehicle-defs` tags `v0.15.0` and `v0.16.0` both resolve to `f7847a7`; `manifest.yaml:9` says `v0.16.0 = 9310893` | **The `v0.16.0` tag points at the `v0.15.0` commit.** A consumer that pins `v0.16.0` gets the older tree. `setup.sh:36` does not force-update existing tags, so a fresh setup can silently check out the wrong code. Owner: user + Claude (release). |
| C-02 | P1 | `git fetch` + `rev-list HEAD..origin/main`: defs 2 behind, rt-core 3, conn 2, analyzer 1; mobile fetch timed out | **Local workspace is not the state the docs describe.** Any session that trusts local files works on stale code. Pull all repos before the rename; re-run this report afterwards. |
| C-03 | P1 | `STATUS.md:21` says defs#105 merged and main is ahead only for server/rt-core; local defs HEAD is `8741baa` (PR #104), `origin/main` is `64b6b83` (PR #105) | True remotely, false locally. STATUS and the checkout disagree; D-088 and `docs/ideas/ride-summary-did-layout.md` exist only on `origin/main`. |
| C-04 | P2 | `ISSUES.md:85` says v0.19.0 is "tag pending the user"; tag exists at `4d96a33` | Issue table is stale; the gate was already released. |
| C-05 | P2 | `ISSUES.md:82` says v0.19.0 is untagged and server takes it "at its next bump"; server v0.6.0 already uses `moto_defs.platform.SIGNALS` | Same stale-issue class; E-20 (1) is done. |
| C-06 | P1 | `moto-server/src/moto_server/defs_pin.txt:1` = `v0.14.0`; submodule at `4d96a33` (v0.19.0); `tests/golden/MANIFEST.sha256:12` says v0.19.0 | The Docker fallback reports a defs version four releases old. A container without `.git` (`.dockerignore:1` excludes `.git`) will label sessions with the wrong defs version. |
| C-07 | ~~P2~~ fixed in server#38 (Claude 2026-10-30, opencode) | `moto-server/src/moto_server/api.py:63` FastAPI version `0.2.0`; `pyproject.toml:3` and `__init__.py:3` say `0.6.0` | Swagger/OpenAPI advertises the wrong server version. |
| C-08 | P3 | `STATUS.md:17` puts mobile v0.4.0 in the 2026-10-25 release batch; tag date is 2026-10-17 | Release chronology is wrong; harmless for builds. |
| C-09 | P2 | `moto-server/Dockerfile:10-13` installs git and relies on `git describe`; `.dockerignore:1` excludes `.git` | Defensive fallback exists (defs_pin), but the fallback is C-06; the two defects combine into wrong version reporting in containers. |

## B. Documentation vs code

| ID | Sev | Evidence | Finding |
|---|---|---|---|
| C-10 | ~~P1~~ fixed in rt-core#57 (Claude 2026-10-30, opencode) | `moto-rt-core/README.md:5` says defs pinned to `v0.8.0`; actual submodule `4d96a33` = v0.19.0. Other stale pins: `misra/README.md:15` (v0.2.0), `tests/host/vectors/README.md:19` (v0.14.0), `src/features/derived/README.md:51` (v0.18.1), `src/features/heartbeat/README.md:11` (v0.15.0) | Five different "pinned defs" values in one repo. Readers cannot tell which is authoritative. |
| C-11 | ~~P2~~ fixed in rt-core#57 (Claude 2026-10-30, opencode) | `moto-rt-core/README.md:14,18` and `src/services/README.md:10,12,18` mark signal pool/com/target setup "not yet"; `src/services/README.md` later marks them implemented | Self-contradicting status table. |
| C-12 | ~~P2~~ fixed in rt-core#57 (Claude 2026-10-30, opencode) | `src/app/README.md:5` documents `comms_pass(client, server, republisher, heartbeat, ekf)`; `src/app/comms.h:112-113` has a sixth `lean_tx_t*` argument; `comms.c:94-113` calls lean step and health | Doc is one refactor behind the code. |
| C-13 | P3 | `src/features/derived/README.md:56` says 547 speed samples in the 60 s window; `:60` says 548 | Off-by-one in prose. |
| C-14 | P2 | `src/features/uds/README.md:233` says client is 1328 B; `:328` says 1608 B; `src/hal/README.md:55` says RX FIFO holds 9 CFs, `src/features/uds/README.md:324` says 36 | Two sizes for the same object; the transport assumptions differ by 4x. |
| C-15 | P1 | `moto-safety-node/CLAUDE.md:7,37` describes `src/features/` modules and `tests/host/`; the repo has 11 markdown files, no `src/`, no tests, no CMake | The safety repo documents code that does not exist. README.md:7 correctly says "skeleton". |
| C-16 | P1 | `moto-connectivity-node/README.md:33` says the RX queue is 32 in other builds; `src/hal/CanRxQueue.h:20` defines 64 unconditionally; `CLAUDE.md:53` says 64 | Memory/throughput claim is wrong for the tester builds. |
| C-17 | P2 | `platformio.ini:95` says segmented reception is probe-only; `src/HondaCANModule.h:11` includes `IsoTpReceiver.h` unconditionally and `HondaCANModule.cpp:817+` uses it for DTCs; `CLAUDE.md:53` documents this | Build documentation contradicts the compiled feature. |
| C-18 | P1 | `moto-connectivity-node/CLAUDE.md:11` says "UDS/ISO-TP/bootloader does NOT live here"; `README.md:5`, `CLAUDE.md:45` and `src/HondaCANModule.cpp` implement the temporary tester | The scope statement would reject the code the repo actually ships. |
| C-19 | P2 | `CLAUDE.md:22` says the repo builds two ESP32-S3 images, then in the same paragraph says the helmet env does not exist; `platformio.ini` has no helmet env | Self-contradiction; the second half is the truth today. |
| C-20 | P2 | `src/main.cpp:90`, `platformio.ini:72` say IMU I2C pins 1/2; `src/ImuModule.cpp:9-13` uses GPIO7/6; `README.md:7` agrees with the code | Wrong pinout in comments/config. |
| C-21 | P2 | `README.md:17` says the worst-case step is not counted at runtime; `src/TesterStatsTracker.h:21-31` records `stepGapMaxMs`; `HondaCANModule.cpp:341` feeds it | Doc denies a metric the code publishes. |
| C-22 | P2 | `README.md:5-9,34` documents no DTC output; `CLAUDE.md:53` documents D-080; `src/DtcSnapshot.h:100+` emits `[DTC]` lines in every tester build | README is incomplete for the current feature set. |
| C-23 | P2 | `test/test_embedded/test_main.cpp:41` uses `BLETelemetryPacketV3`, removed from `src/BLETelemetryPacket.h:69,100` (only V2/V4 remain) | Embedded test does not compile. It is hidden because `platformio.ini:34` filters `test_embedded` while CI runs only `pio test -e native` (`ci.yml:103`). |
| C-24 | P1 | `moto-server/README.md:205-207` says a `vehicle_signal_block_version` mismatch is a `warn`; `report.py:615-622` fails; `tests/test_vsig_consistency.py:164-174` expects `fail`. `gps_block_version` also fails and README does not say so | Operators get the wrong severity contract. |
| C-25 | P1 | `moto-server/CLAUDE.md:34` says location history is "stored encrypted at the disk/DB level"; `README.md:162-164` says "No position, ever"; no encryption code/config exists in the repo | One of the two privacy statements is false. Given D-076 (position may be stored on the user's own server), this needs a precise, testable statement. |
| C-26 | P2 | `src/moto_server/ingest.py:8-9` shows `derived.parquet`/`derived_summary.parquet` at the session root; actual path is `parquet/` (`derived/__init__.py:32-33`, `README.md:81-82`) | Storage layout doc is wrong. |
| C-27 | P2 | `moto-server/src/moto_server/mdf4.py:8,23-24` has `TODO(phase0 WP-2)` + `NotImplementedError`; README/CLAUDE correctly call it skeleton | Not a contradiction, but the feature is advertised in the architecture flow (ARCHITECTURE §7 "MDF4/Parquet") without a "not implemented" note there. |
| C-28 | P1 | `moto-hil-bench/README.md:6-9,11` and `CLAUDE.md:8-11,31-32` list `simulator/`, `host/`, `scenarios/`, `vehicles/cl250/`, build commands and a defs submodule; none exists (README:11 also says "skeleton, no code yet") | The skeleton promises a full tree. |
| C-29 | P1 | `moto-linux-node/README.md:13`, `moto-mcp/README.md:10`, `moto-ml/README.md:10` claim a pinned `moto-vehicle-defs` submodule; no `.gitmodules`/`external/` in any of them. `moto-mcp` is code-less; `moto-ml` is code-less | Dependency claim is false. |
| C-30 | P2 | `moto-analyzer/README.md:19,54` says adapters open listen-only; `src/services/webSerialCan.ts:42-45` sends `L` but never parses/validates the reply | See C-35 (safety). |
| C-31 | P2 | `moto-analyzer/src/components/Header.tsx:53,197`, `OscilloscopePanel.tsx:311`, `mathChannels.ts:195` hard-code "Honda CL250" | Branding/vehicle identity is hard-coded, not defs-driven — directly relevant to the vehicle-generic goal. |
| C-32 | P2 | `moto-mobile/lib/services/session_store.dart:104-108` share list = meta/telemetry/events/summary/imu/gps; `test/session_upload_test.dart:70-75` and upload manifest include `signals.csv` | Manual export omits the vehicle-signal data the upload includes. |
| C-33 | P2 | `moto-mobile/android/app/src/main/AndroidManifest.xml:24` label "Honda CL250 Telemetry"; `android/app/build.gradle.kts:9,24` applicationId `com.honda.telemetry.cl250`; `test/widget_test.dart:10` asserts the label | Product is branded as one Honda model. `applicationId` is intentionally kept (rename plan), but the label/test should change. |
| C-34 | P3 | `moto-server/CLAUDE.md:16` says the golden writer needs "v0.14.0+"; `defs_pin` and actual pin are newer | Low-risk stale floor. |

## C. Safety and invariant violations

| ID | Sev | Evidence | Finding |
|---|---|---|---|
| C-35 | **P0** | `moto-analyzer/src/services/webSerialCan.ts:42-45` sends `L` and proceeds without checking the adapter's acknowledgement; UI says "opened listen-only" (`Header.tsx:53,197`) | **The listen-only invariant is not enforced.** A failed `L` would leave the adapter in normal mode while the UI claims passive observation. Needs a reply check + refusal test (D-081 item 2). |
| C-36 | **P0** | `moto-connectivity-node/src/BLEServerModule.cpp:219-252` copies BLE write values into `std::string` and parses with `sscanf` after init; `src/main.cpp:460` admits BLE notifications allocate | Violates "no heap after init / no string parsing on MCUs" (AGENTS.md hard rules, PLATFORM-RULES invariant 5). The tester BLE path is safety-adjacent. |
| C-37 | P1 | `moto-connectivity-node/src/hal/TwaiCanBus.cpp:57` calls `twai_transmit(..., pdMS_TO_TICKS(5))` | Up to 5 ms blocking in the tester loop against a 10 ms step budget; violates "no blocking calls in the tester loop" (AGENTS.md:41). |
| C-38 | P2 (test-only) | `moto-connectivity-node/test/test_discovery_probe/test_main.cpp:165,239,1044` hard-code `{0x22,0xF4,0x00}` / `{0x22,0xF4,0xE0}` instead of generated scan entries | Hand-written DID literals in tests; invariant 2 says signal facts come from defs. Tests should use the generated table. |
| C-39 | P3 (docs-only) | `moto-hil-bench/CLAUDE.md:19,23` hard-code `0x18DA10F1`, `0x18DAF110`, `0x22`, `0x020/0x022/0x081` | Docs-only; still models the wrong habit for a repo that must load definitions at runtime. |
| C-40 | P3 (test-only) | `moto-server/src/moto_server/mock_stream.py:115,129` and several tests repeat CAN IDs/DIDs/scales | Production code reads defs; tests duplicate facts by design. Acceptable, but a single `tests/fixtures` source would reduce drift. |
| Clean | — | Audited code | No second tester, no UDS write/clear/reset/unlock service, and no hard-written production signal IDs were found in rt-core/conn/server/analyzer. |

## D. Naming and the rename plan

| ID | Sev | Evidence | Finding |
|---|---|---|---|
| C-41 | P1 | `README.md:3` links `https://github.com/moto-platform` (API 404); `gh repo view vehicle-platform/moto-workspace` works; `RENAME-PLAN.md:3` says "not applied" | **The org rename is already applied**; every doc and manifest still names the old org. The plan's step 0 is half done. |
| C-42 | P2 | `manifest.yaml:4` comment and all 12 URLs use `moto-platform`; `PLATFORM-RULES.md:5`; `AGENTS.md:80`/`GEMINI.md:80` (generated); `moto-linux-node/README.md:3`, `moto-io-node/README.md:3` | Old-org references rely on GitHub redirects for repos, but org-root links are already 404. |
| C-43 | P2 | `RENAME-PLAN.md:5` says "about 680 files mention moto"; measured: 459 tracked repo files + 31 workspace files = **490** | Count is inflated by ~39%; scope/effort estimate is wrong. |
| C-44 | P2 | `RENAME-PLAN.md:5` says "every consumer has the `external/moto-vehicle-defs` submodule"; only rt-core, conn, server, mobile, analyzer have it (5/12) | The migration order assumes submodules that do not exist; safety-node/linux/mcp/hil/ml/io-node need the first-time add, not a rename. |
| C-45 | P2 | `RENAME-PLAN.md:29` says decisions end at D-088 (true on origin); `:34` says "next free D-number after D-089", but D-089 does not exist | Decision numbering is wrong; the new decision is D-089 (or later if the user records another one first). |
| C-46 | P1 | `RENAME-PLAN.md:34` step 1 update list omits `.gitignore:2` (`/moto-*/`), `scripts/worktrees.py:49,71` (`ROOT.glob("moto-*")`, `moto-platform/<slug>`), `scripts/sync_claude.py:42` (repo map), `external-ai/zones.json` (repo keys + `external/moto-vehicle-defs` glob), `external-ai/README.md:26` | A repo/folder rename without these breaks the zone checker, sync, worktree report and PR tooling. All are red zones except the docs. |
| C-47 | P2 | `RENAME-PLAN.md:27,34` name `cl250_constants.yaml`, `vehicle_cl250.yaml`, `cl250_derived.yaml` without directories; actual paths are `vehicle/`, `uds/`, `derived/` | The "do not rename" list is ambiguous for anyone executing it. |
| C-48 | P1 | `RENAME-PLAN.md` steps 1–3 touch `moto-vehicle-defs` codegen/package, `safety-node`, `io-node`, `gen/`, `.claude/`, `AGENTS.md`, `PLATFORM-RULES.md`, `manifest.yaml`, `scripts/*` | **All red zones for non-Claude tools** (`external-ai/zones.json`). D-036 also forbids external tools from tags, version bumps, pin changes and manifest edits. The plan is not executable by opencode end-to-end. |
| C-49 | P2 | `RENAME-PLAN.md:43` says GitHub redirects keep old links working; `README.md:3` org-root link is already 404 | Repo URL redirects work; org-root links do not. |
| C-50 | P3 | "11 platform repos" in `.claude/agents/architecture-guard.md:8`, `external-ai/README.md:26`, `external-ai/log/2026-10-18-gemini-contributor-task-plan.md:30`; "12" in `PLATFORM-RULES.md:7`, `.gitignore:1` | Repo count is inconsistent after D-081 added analyzer. |
| C-51 | P3 | `moto-safety-node/.claude/agents/safety-reviewer.md:3,18` and `feature-module/SKILL.md:3` still name retired `moto-io-node`; `scripts/sync_claude.py:42` keeps syncing it | Stale agent triggers keep pointing at a retired repo. |
| C-52 | P3 | `PLATFORM-RULES.md:30`, `repo-bootstrap/SKILL.md:64` list `HondaCl250_Telemetry` as the legacy reference; it is private/archived, absent locally and absent from `manifest.yaml`/`setup.sh` | Referenced repo is not available to the workspace; new contributors cannot follow the instruction. |
| C-53 | P3 | `AGENTS.md:22` lists `docs/*` before `docs/ideas/*`; `AGENTS.md:35` says the more specific glob is listed first in `zones.json`; `external-ai/zones.json` does list `docs/ideas/*` first | Rendered rule text is ordered misleadingly. The checker is correct; humans reading only AGENTS.md may apply the wrong zone. |
| C-54 | P2 | `moto-apk/` (4 APKs, ~215 MB) and `models/` are untracked local directories; `.gitignore:2` ignores `/moto-*/` so `moto-apk` is hidden, `models/` is not; `RENAME-PLAN.md` untracked | Rename/setup tooling does not know these; a careless `git add` could commit 215 MB of APKs or CAD assets. |
| C-55 | P2 | `moto-mobile/lib/services/session_store.dart:104-108` (C-32) and `Header.tsx` (C-31) keep the CL250 identity after a rename | A repo rename does not make the product vehicle-generic; display strings, VSS `Vehicle.Motorcycle.*` (`vss/overlay.vspec:47`), packages and macros must change too. |

## E. Not verified / limits of this review

- Hardware behaviour, on-target timing, CI-only checks and the H755 port were not run.
- `moto-mobile` and part of `moto-analyzer` origin state could not be fetched (SSL timeout); those places were checked at the local HEAD and flagged where the local tree is known to be behind.
- The defs codegen drift check (`make check`) was not executed; generated `gen/` trees were compared structurally, not rebuilt.
- No security audit of dependencies or secrets was performed beyond a scan for obvious committed keys/positions (none found).
