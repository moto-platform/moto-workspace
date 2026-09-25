# STATUS — session handoff

> Keep it short (≤60 lines). Updated by the `/handoff` skill. "Recent sessions" keeps at most 5 one-line entries; drop the oldest.

**Phase:** 1 — moto-vehicle-defs bootstrapped (untagged), other repos still README + CLAUDE.md only
**Last updated:** 2026-09-25

## Where we are

- All 11 repos + `moto-workspace` live in `github.com/moto-platform`, **private** (D-017). Architecture: `moto-vehicle-defs/docs/ARCHITECTURE.md`, `DECISIONS.md` (D-001..D-027, open Q-001..Q-016).
- **moto-vehicle-defs** on branch `claude/jolly-euler-rdlvqr` (pushed, no PR yet, **not tagged**): `uds/vehicle_cl250.yaml` (verified DIDs + evidence), `dbc/platform.dbc` (EkfLean 0x020, VehicleSpeed 0x021, EkfFrictionMass 0x022, heartbeats 0x081-0x085 — all E2E; VehicleEngine 0x110), `dbc/cl250.dbc` + `uds/dids.yaml` skeletons, `vss/overlay.vspec` (VSS 6.0, standard paths only), `docs/legacy-telemetry-notes.md`, `docs/e2e-profile.md`.
- `tools/codegen` (uv): `gen/c/{rt_core,safety,io,conn,hil_sim}` (cantools + E2E + CL250 DID table with D-020 request/frame allow-list), `gen/python/moto_defs`, `gen/vss/vss_dbc.json`. `make check` = strict parse + checks + ruff + 103 pytest (C↔Python cross-checks, mutation-checked); `make drift`; GitHub Actions CI.
- safety-reviewer + architecture-guard ran on the defs bootstrap; findings applied (golden D-020 list, timeout inside E2E check, frame gate, response parser, stale_after_ms). Remaining items are Q-014/Q-015.
- New Claude-proposal decisions awaiting user confirmation: D-024 (VSS 6.0 + vss-tools 6.0), D-025 (platform.dbc v0.1 set), D-026 (E2E details), D-027 (codegen targets + vehicle-bus guard).
- `HondaCl250_Telemetry` untouched (read-only reference, commit 16a4b26 cited as evidence).

## Next up (in order)

1. **User:** review/merge the moto-vehicle-defs branch, answer Q-016 (Vehicle.Motorcycle.* paths, TPS mapping), approve D-024..D-027, then approve the `v0.1.0` tag → tag, update `manifest.yaml` ref (D-013).
2. **Cloud session B: legacy port** (repos: moto-workspace, moto-vehicle-defs, moto-connectivity-node, moto-mobile, HondaCl250_Telemetry). `/repo-bootstrap moto-connectivity-node` per D-023 (PlatformIO arduino+espidf), submodule pinned to `v0.1.0`, replace hand-written DIDs with `gen/c/conn/` and gate every TX through `vehicle_cl250_frame_allowed()`; port the Flutter app into moto-mobile. Run `vss-schema-guardian` afterwards.
3. **moto-hil-bench host** skeleton (simulated CL250 UDS responder using `gen/python/moto_defs`) after deciding Q-009.
4. Later `/signal-change`: CoG height + cornering-warning output message, `Vehicle.Motorcycle.*` mappings once Q-016 is answered.

## Blockers / pending decisions

- Q-014 (how conservative DEFAULT µ/mass/lean must be) and Q-015 (max VEHICLE_SPEED_AGE; poll 0xF40D faster than 800 ms?) — both before safety-node code.
- Q-002 (safety-node on INVALID/lost rt-core data), more important with D-021.
- Q-016 (motorcycle VSS extensions), Q-001 remainder (passive CL250 broadcast?), Q-003, Q-006.
- License not decided (no LICENSE file anywhere).

## Recent sessions

- 2026-09-25 (cloud A): moto-vehicle-defs bootstrap — CL250 YAML, platform.dbc, VSS overlay, codegen + CI, legacy notes; safety/architecture review applied; D-024..D-027, Q-014..Q-016. Branch `claude/jolly-euler-rdlvqr` in defs + workspace.
- 2026-09-25 (cont.): Legacy HondaCl250_Telemetry analysed, transferred (private, archived, tag legacy-final). Verified CL250 facts D-019; D-020..D-023 (allow-list, single tester, Flutter, hybrid port).
- 2026-09-25 (cont.): Org created, repos transferred and pushed, back to private, per-repo Claude asset sync added. Cloud credit = cloud sessions only.
- 2026-09-25: Reviewed all docs, resolved contradictions (D-008, D-009), wrote ARCHITECTURE + ADR log, built the Claude environment, translated the docs to English.
