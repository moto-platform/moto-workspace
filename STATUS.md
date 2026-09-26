# STATUS — session handoff

> Keep it short (≤60 lines). Updated by the `/handoff` skill. "Recent sessions" keeps at most 5 one-line entries; drop the oldest.

**Phase:** 1 — moto-vehicle-defs v0.1.0 released; legacy port realigned (connectivity-node PR open), mobile port merged
**Last updated:** 2026-09-26

## Where we are

- All 11 repos + `moto-workspace` in `github.com/moto-platform`, **private** (D-017). Decisions D-001..D-030 (D-024..D-027 user-confirmed; D-030 = Claude proposal), open Q-001..Q-016 (Q-014/Q-015 provisional via D-029).
- **moto-vehicle-defs `v0.1.0` = commit `acef075`** on `main` (CHANGELOG 0.1.0, `make check`/`make drift` clean, CI green). The annotated tag exists locally but the session's git proxy refused the tag push (HTTP 403) → **user must push/create tag `v0.1.0` on `acef075`**. `manifest.yaml` already pins `ref: v0.1.0`.
- Closed without merging: moto-vehicle-defs#1 and moto-workspace#1 (superseded by defs#2). Their `claude/eager-edison-asifnn` branches could not be deleted from the session (proxy 403) → **user deletes them**.
- **moto-connectivity-node [#1](https://github.com/moto-platform/moto-connectivity-node/pull/1)** (open, for user review/merge):
  - Realigned to defs v0.1.0: submodule relative URL @ `acef075`, only `gen/c/conn/` API (IDs, DIDs, formulas, poll/timeouts, `stale_after_ms`), responses via `vehicle_cl250_parse_response()`.
  - TX gate: request-ID check + `vehicle_cl250_frame_allowed()`. Poller off: `CONN_VEHICLE_TESTER=0` (no TWAI driver).
  - Latches off on a foreign tester or repeated bus-off; 0x78 cap. Native tests 35/35.
  - Reviews: vss-schema-guardian clean, architecture-guard ok, safety-reviewer no blocker (findings applied).
  - **CI red only because the `MOTO_DEFS_TOKEN` secret is empty in this repo** (org secret not granted / Free plan).
- **moto-mobile #1 merged** by the user (BLE schema v2). Follow-up [moto-mobile#2](https://github.com/moto-platform/moto-mobile/pull/2) (open): byte-identical schema drift test vs connectivity-node + optional `MOTO_CONN_READ_TOKEN` in CI; `flutter analyze` clean, 15/15 tests.
- `HondaCl250_Telemetry` untouched (tag `legacy-final`).

## Next up (in order)

1. **User:**
   - Push tag `v0.1.0` (defs, `acef075`).
   - Give `MOTO_DEFS_TOKEN` to moto-connectivity-node (or add a repo secret), re-run CI, then review/merge connectivity-node#1 and mobile#2.
   - Optionally add `MOTO_CONN_READ_TOKEN` to moto-mobile.
   - Delete the two superseded branches.
   - Confirm D-030.
2. **moto-hil-bench host** skeleton (simulated CL250 UDS responder using `gen/python/moto_defs`) — decide **Q-009** first; `/repo-bootstrap moto-hil-bench`.
3. connectivity-node follow-ups:
   - Rename the default env to `-vehicle-tester`.
   - Make the unverified 11-bit fallback opt-in.
   - Move `kMaxBusOffEvents` to defs (next defs MINOR).
   - Check GPIO4 recessive on the real board.
4. Later `/signal-change`: CoG height + cornering-warning output message, Q-016 remainder (heartbeat/VALID VSS paths).

## Blockers / pending decisions

- Q-009 (HIL realism level) blocks the hil-bench host.
- Q-014/Q-015: provisional values in D-029; final values from the planned measurement device + server.
- Q-002 (safety-node on INVALID/lost rt-core data), more important with D-021.
- Q-016 remainder, Q-001 remainder (passive CL250 broadcast?), Q-003, Q-006. License not decided.

## Recent sessions

- 2026-09-26 (cloud A, release): D-024..D-027 confirmed, defs v0.1.0 (`acef075`; tag push pending), manifest pinned, defs#1/workspace#1 closed, connectivity-node#1 realigned + safety-reviewed, mobile#2 drift test; D-030 proposed.
- 2026-09-26 (cloud A, cont.): codegen refactor, defs#2 merged; D-028 Motorcycle VSS extensions, D-029 provisional limits + faster speed polling; found the duplicate defs bootstrap.
- 2026-09-25 (cloud A): moto-vehicle-defs bootstrap — CL250 YAML, platform.dbc, VSS overlay, codegen + CI, legacy notes; D-024..D-027, Q-014..Q-016.
- 2026-09-25 (cont.): Legacy HondaCl250_Telemetry analysed, transferred (private, archived, tag legacy-final). Verified CL250 facts D-019; D-020..D-023.
- 2026-09-25 (cont.): Org created, repos transferred and pushed, back to private, per-repo Claude asset sync added.
