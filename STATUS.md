# STATUS — session handoff

> Keep it short (≤60 lines). Updated by the `/handoff` skill. "Recent sessions" keeps at most 5 one-line entries; drop the oldest.

**Phase:** 1 — defs bootstrapped, legacy telemetry ported (PRs open, not merged)
**Last updated:** 2026-09-25

## Where we are

- Architecture and decisions: `moto-vehicle-defs/docs/ARCHITECTURE.md`, `DECISIONS.md` (D-001..D-023, Q-001..Q-013). Org `github.com/moto-platform`, all repos private (D-017).
- **moto-vehicle-defs** (PR moto-platform/moto-vehicle-defs#1, CI green): `uds/vehicle_cl250.yaml` (D-019/D-023 facts, D-020 allow-list), `dbc/platform.dbc` draft (LeanEstimate 0x020, CorneringParamEstimate 0x021, VehicleSpeed 0x030 E2E, heartbeats 0x081-0x085, VehiclePowertrain 0x110), `vss/overlay.vspec` (standard VSS v6.1 paths only), `tools/codegen` (`make gen/check/test/lint`), `gen/c/<node>/` incl. E2E lib + `vehicle_cl250_frame_allowed()` guard, `docs/legacy-telemetry-notes.md`. safety-reviewer ran; H1/H2/M1 fixed. **Not tagged** (v0.1.0 waits for the user).
- **moto-connectivity-node** (PR moto-platform/moto-connectivity-node#1): legacy firmware ported (verbatim import commit + adaptation commit), PlatformIO `arduino, espidf`, submodule pinned to defs commit `40cd2bb`, BLE schema v2, Wi-Fi JSON without `String`, `CONN_VEHICLE_TESTER=1`. Native tests 28/28 locally (`scripts/native_tests.sh`); **pio build never ran** (registry blocked here; CI blocked by missing secret).
- **moto-mobile** (PR moto-platform/moto-mobile#1): legacy Flutter app ported (verbatim + adaptation), decoder on BLE schema v2, tests check a copy of the schema. `flutter analyze`/`test` pass locally (Flutter 3.47.5).
- HondaCl250_Telemetry untouched (read-only).

## Next up (in order)

1. User: add repo secret `DEFS_READ_TOKEN` (contents:read on connectivity-node + vehicle-defs) to moto-connectivity-node, re-run CI, fix any ESP-IDF build errors (first real `pio run`).
2. Merge defs PR → user tags `v0.1.0` → re-pin connectivity-node submodule to the tag (merge commit SHA changes if squashed) → update `manifest.yaml`. Then merge conn + mobile PRs.
3. Decide Q-002 together with the numbers the safety review left open (mu/mass/CoG plausibility limits, max source age of republished VehicleSpeed); then generate a per-message RX wrapper (E2E + DLC + range) before safety-node consumes these messages (`/signal-change`).
4. **moto-hil-bench host** skeleton (simulated CL250 UDS responder, can use `gen/python/moto_defs`) after deciding Q-009 (`/repo-bootstrap`).

## Blockers / pending decisions

- CI secret for private submodules (every consumer repo will need it).
- Q-002 (safety-node on INVALID/lost rt-core data) + the value limits above.
- Q-001 remainder (passive broadcast on CL250 bus), Q-003 (F103 dual role), Q-006 (HARA/requirements location).
- Proposals awaiting the user: `Vehicle.Motorcycle.*` VSS paths for mu/mass/CoG (none added); Android applicationId + BLE name/UUID rename (legacy "Honda-CL250" kept).

## Recent sessions

- 2026-09-25 (cont.): Session A+B in one cloud session: defs bootstrap + codegen + CI, legacy port to connectivity-node (PlatformIO arduino+espidf) and moto-mobile (Flutter), BLE schema v2; 3 PRs open.
- 2026-09-25 (cont.): Legacy HondaCl250_Telemetry analysed, transferred (private, archived, tag legacy-final). Verified CL250 facts D-019; D-020..D-023 (allow-list, single tester, Flutter, hybrid port).
- 2026-09-25 (cont.): Org created, repos transferred and pushed, back to private, per-repo Claude asset sync added. Cloud credit = cloud sessions only.
- 2026-09-25: Reviewed all docs, resolved contradictions (D-008, D-009), wrote ARCHITECTURE + ADR log, built the Claude environment, translated the docs to English.
