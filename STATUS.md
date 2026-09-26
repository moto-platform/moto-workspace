# STATUS — session handoff

> Keep it short (≤60 lines). Updated by the `/handoff` skill. "Recent sessions" keeps at most 5 one-line entries; drop the oldest.

**Phase:** 1 — moto-vehicle-defs bootstrapped (untagged), other repos still README + CLAUDE.md only
**Last updated:** 2026-09-26

## Where we are

- All 11 repos + `moto-workspace` live in `github.com/moto-platform`, **private** (D-017). Architecture: `moto-vehicle-defs/docs/ARCHITECTURE.md`, `DECISIONS.md` (D-001..D-029, open Q-001..Q-016; Q-014/Q-015 have provisional answers in D-029).
- **moto-vehicle-defs** `main` (merged via [moto-vehicle-defs#2](https://github.com/moto-platform/moto-vehicle-defs/pull/2), **not tagged yet**): `uds/vehicle_cl250.yaml` (verified DIDs + evidence), `dbc/platform.dbc` (EkfLean 0x020, VehicleSpeed 0x021, EkfFrictionMass 0x022, heartbeats 0x081-0x085 — all E2E; VehicleEngine 0x110), `dbc/cl250.dbc` + `uds/dids.yaml` skeletons, `vss/overlay.vspec` (VSS 6.0 + first `Vehicle.Motorcycle.*` extensions, D-028), `limits/platform_limits.yaml` (provisional µ/mass/speed-age limits, D-029), `docs/legacy-telemetry-notes.md`, `docs/e2e-profile.md`.
- `tools/codegen` (uv): `gen/c/{rt_core,safety,io,conn,hil_sim}` (cantools + E2E + CL250 DID table with D-020 request/frame allow-list), `gen/python/moto_defs`, `gen/vss/vss_dbc.json`. `make check` = strict parse + checks + ruff + 157 pytest (C↔Python cross-checks, mutation-checked); `make drift`; GitHub Actions CI.
- safety-reviewer + architecture-guard ran on the defs bootstrap; findings applied (golden D-020 list, timeout inside E2E check, frame gate, response parser, stale_after_ms). D-029 limits reviewed too (bounded µ rule, no default lean, effective speed age).
- New Claude-proposal decisions awaiting user confirmation: D-024 (VSS 6.0 + vss-tools 6.0), D-025 (platform.dbc v0.1 set), D-026 (E2E details), D-027 (codegen targets + vehicle-bus guard).
- **Conflict:** the parallel session ("moto-connectivity-node ve moto-mobile", branch `claude/eager-edison-asifnn`) built its own defs bootstrap, [moto-vehicle-defs#1](https://github.com/moto-platform/moto-vehicle-defs/pull/1) (speed 0x030, no limits/decisions), and ported connectivity/mobile against it. The user chose #2 (merged); #1 must be closed without merging and the connectivity/mobile port rebased onto defs `main`.
- `HondaCl250_Telemetry` untouched (read-only reference, commit 16a4b26 cited as evidence).

## Next up (in order)

1. **User:** approve the `v0.1.0` tag of moto-vehicle-defs `main` → tag, update `manifest.yaml` ref (D-013); confirm D-024..D-027; close defs#1; tell the parallel session to rebase its port on defs `main`.
2. **Cloud session B: legacy port** (repos: moto-workspace, moto-vehicle-defs, moto-connectivity-node, moto-mobile, HondaCl250_Telemetry). `/repo-bootstrap moto-connectivity-node` per D-023 (PlatformIO arduino+espidf), submodule pinned to `v0.1.0`, replace hand-written DIDs with `gen/c/conn/` and gate every TX through `vehicle_cl250_frame_allowed()`; port the Flutter app into moto-mobile. Run `vss-schema-guardian` afterwards.
3. **moto-hil-bench host** skeleton (simulated CL250 UDS responder using `gen/python/moto_defs`) after deciding Q-009.
4. Later `/signal-change`: CoG height + cornering-warning output message, `Vehicle.Motorcycle.*` mappings once Q-016 is answered.

## Blockers / pending decisions

- Q-014/Q-015: provisional values in D-029; final values from the planned measurement device + server.
- Q-002 (safety-node on INVALID/lost rt-core data), more important with D-021.
- Q-016 remainder (heartbeat/VALID VSS paths), Q-001 remainder (passive CL250 broadcast?), Q-003, Q-006.
- License not decided (no LICENSE file anywhere).

## Recent sessions

- 2026-09-26 (cloud A, cont.): codegen refactor, defs#2 merged at user's request; D-028 Motorcycle VSS extensions, D-029 provisional limits + faster speed polling (safety-reviewed); found the duplicate defs bootstrap in the parallel session.
- 2026-09-25 (cloud A): moto-vehicle-defs bootstrap — CL250 YAML, platform.dbc, VSS overlay, codegen + CI, legacy notes; safety/architecture review applied; D-024..D-027, Q-014..Q-016. Branch `claude/jolly-euler-rdlvqr` in defs + workspace.
- 2026-09-25 (cont.): Legacy HondaCl250_Telemetry analysed, transferred (private, archived, tag legacy-final). Verified CL250 facts D-019; D-020..D-023 (allow-list, single tester, Flutter, hybrid port).
- 2026-09-25 (cont.): Org created, repos transferred and pushed, back to private, per-repo Claude asset sync added. Cloud credit = cloud sessions only.
- 2026-09-25: Reviewed all docs, resolved contradictions (D-008, D-009), wrote ARCHITECTURE + ADR log, built the Claude environment, translated the docs to English.
