# CLAUDE.md — moto-platform (workspace root)

SDV-architecture diagnostics / telemetry / ADAS platform for motorcycles (first vehicle: Honda CL250). Senior thesis (Manisa Celal Bayar Univ., Computer Engineering) → GitHub org `moto-platform`.
This folder is the `moto-workspace` repo (manifest, setup, shared `.claude/`). It ignores the 11 independent platform repos cloned inside it (D-015). **Always start Claude from this root**, because the platform agents and skills live in `.claude/`.
The user writes in Turkish. Reply in Turkish, but write every project artifact in English (D-011).

## Session protocol (token budget is limited, so follow it)

1. At session start read `STATUS.md` (short). Do NOT read the large docs.
2. Architecture questions: first `moto-vehicle-defs/docs/ARCHITECTURE.md` and `DECISIONS.md`. For details, use the section index in `docs/README.md` and read **only the relevant range** (`Read` offset/limit), or ask the `docs-researcher` agent. Never read a whole raw doc (~230 KB total).
3. Broad code search → `Explore` agent. Single file/symbol → Grep/Read directly.
4. One session = one task. When done, run `/handoff` to update `STATUS.md` and suggest `/clear`.
5. Do not re-litigate decisions recorded in `DECISIONS.md`. If a new decision is needed, ask the user, then record it there.
6. Delegate bulk mechanical work (translation, boilerplate, wide scans) to subagents with `model: sonnet`/`haiku`. Keep Opus for architecture and safety judgment.

## Repo map (dependencies are one-way: everyone → moto-vehicle-defs)

| Repo | Runtime | Language/tooling | Role |
|---|---|---|---|
| `moto-vehicle-defs` | — (definitions) | DBC, VSS, UDS YAML, Python codegen | Single source of truth for signals + all platform docs |
| `moto-rt-core` | STM32H7 | C, CMake+CubeMX, FreeRTOS | Domain controller: CAN gateway, logging, fusion, UDS/ISO-TP, bootloader, XCP, EKF, context, dyno, anomaly safety net |
| `moto-safety-node` | STM32G4 | C, CMake+CubeMX, bare-metal | ONLY the cornering safety decision (closed form), isolated |
| `moto-io-node` | STM32G0 (proto: F103) | C, CMake+CubeMX, bare-metal | Blind spot + immobilizer + power management |
| `moto-connectivity-node` | ESP32-S3 | C, ESP-IDF | Wi-Fi/BLE + voice commands (ESP-SR); telemetry here is TEMPORARY |
| `moto-linux-node` | Raspberry Pi 5 | Python/C++ | Kuksa Databroker, CAN→VSS, lane keeping (classic CV), anomaly model, HMI, OTA |
| `moto-mcp` | Raspberry Pi 5 | Python | Standalone open-source MCP server (read-only tools) |
| `moto-hil-bench` | STM32F4 + i7 host | C + Python | Restbus HIL bench, scenario engine, CI runner |
| `moto-server` | Server | Python (FastAPI) | Ingestion, time-series storage, MDF4/Parquet conversion, OTA packages |
| `moto-ml` | Offline | Python | Training only (inference lives in node `features/`) |
| `moto-mobile` | Phone | Flutter (open, Q-007) | Loosely coupled companion |

Each repo's `CLAUDE.md` defines its scope boundary. Read it before working in that repo.

## Platform invariants (non-negotiable; if one must be broken, STOP and ask)

1. **Never write to the ECU.** No repo writes to the engine ECU, flashes it, or changes maps. On the vehicle bus the only transmissions allowed are rt-core's OBD/UDS *read* requests. All other nodes stay listen-only on that bus (D-009).
2. **Never invent signals.** CAN IDs, signal names, scales, VSS paths and DIDs come only from `moto-vehicle-defs` (generated `gen/` code or DBC/VSS). Hand-written literals → `vss-schema-guardian`.
3. **The safety path is isolated.** The cornering decision (safety-node) and the blind-spot decision (io-node) work without the Raspi, the phone, Wi-Fi, VSS or ML. ML may only tighten thresholds, never loosen the safety ceiling.
4. **Critical work never depends on a slow channel.** µs-critical → MCU + CAN. ms → Raspi. Latency-tolerant → phone/server.
5. **No dynamic memory on MCUs** (strictly none on safety paths, avoided everywhere else). No string/DBC/VSS parsing on MCUs.
6. **The immobilizer acts on the starter-relay coil circuit only.** Default state unlocked, hidden bypass, 10 s timeout to unlock.
7. **The LLM never does its own math, and raw GPS never goes to the cloud.**
8. After any change to a safety-critical module (cornering/, safety-node, immobilizer, blind spot, watchdog/heartbeat, anomaly-safety-net, E2E, bootloader), run `safety-reviewer` before committing.

## Conventions

- English for docs, code, comments, commits and READMEs. Turkish originals are archived in `moto-vehicle-defs/docs/tr/` (not maintained); the advisor-facing university docs there stay Turkish.
- Conventional Commits (`feat(uds): ...`). Commit or push only when the user asks.
- `moto-vehicle-defs` uses semver. Consumers pin the `external/moto-vehicle-defs` submodule (relative URL) to a **tag**. The known-good combination is recorded in the root `manifest.yaml`.
- New repo skeleton → `/repo-bootstrap`. Signal add/change → `/signal-change`. New firmware feature → `/feature-module`. End of session → `/handoff`.

## Agents (`.claude/agents/`)

| Agent | Model | Use |
|---|---|---|
| `docs-researcher` | haiku | Answers questions from the docs without loading them into the main context |
| `vss-schema-guardian` | haiku | Detects hardcoded CAN IDs/signals/VSS paths and checks the defs submodule pin |
| `architecture-guard` | sonnet | Checks repo scope, layering, dependency direction, bus rules and decisions |
| `safety-reviewer` | opus | ISO 26262/MISRA-aware review of safety-critical changes |
| `hil-scenario-validator` | (repo-level, moto-hil-bench) | Validates HIL scenario YAML |
