---
date: 2026-10-30
tool: opencode/deepseek-v4.1-flash
topic: mcp-v0.1
repos: [vehicle-mcp]
branches: [vehicle-mcp:ext/opencode-mcp-v0.1]
prs: [vehicle-mcp#9]
zone: yellow
review: pending
---

# vehicle-mcp v0.1: read-only MCP server over the vehicle-server HTTP API

## Goal
A stdio MCP server exposing the vehicle-server read API as read-only tools: sessions,
reports, series, slices, computed statistics and session comparison. Environment-only
config, bearer token never exposed, no position tool (D-076 item 3 not implemented).

## Changes
- `vehicle-mcp/pyproject.toml`: uv_build package, Python >=3.11, runtime deps `mcp` and
  `httpx` only, dev deps `pytest` and `ruff`, console script `vehicle-mcp`, ruff/pytest
  config matching the repo family.
- `vehicle-mcp/src/vehicle_mcp/config.py`: `VEHICLE_SERVER_URL` (default
  `http://127.0.0.1:8000`) and required `VEHICLE_API_TOKEN` from the environment; URL
  validation; `Settings.__repr__` hides the token.
- `vehicle-mcp/src/vehicle_mcp/client.py`: synchronous httpx client with bearer header and
  10 s timeout; GET only; 401/403/404/422/503 and connection/timeout errors become
  explanatory `VehicleServerError` messages (no stack trace, no token, detail truncated).
- `vehicle-mcp/src/vehicle_mcp/stats.py`: `count`, exact `min`/`max`, population `std`,
  linearly interpolated p05/p50/p95, `duration_ms`, `unit`; when the server reports
  `downsampled`, mean/std/percentiles are `None` with `approximate_reason` and the exact
  extremes are kept.
- `vehicle-mcp/src/vehicle_mcp/tools.py`: the six tools, series-name validation against
  the server's own list, 2000-point slice cap (default 500), stats request at
  `max_points=20000`, `b - a` deltas for non-null fields, unit-mismatch rejection, and a
  token-based position filter that drops/rejects lat/lon/lng/latitude/longitude/height/alt/
  altitude names (D-076 item 3).
- `vehicle-mcp/src/vehicle_mcp/server.py`: `MCPServer` registration, stdio-only `main()`,
  startup failure without the token (exit 2, message on stderr).
- `vehicle-mcp/tests/`: 60 pytest tests over `httpx.MockTransport` with synthetic sessions;
  covers auth header, missing-token startup, every tool happy path, 2000 cap, downsampled
  stats, hand-computed stats, compare deltas, 401/403/404/422/503 mapping, position
  filtering, unknown names, and the no-non-GET/no-token-in-result guarantees.
- `vehicle-mcp/README.md`: v0.1 status, install, environment variables, stdio client
  example, tool table, read-only/no-math/no-position/token guarantees, development checks.
- `vehicle-mcp/.gitignore`: Python virtualenv, bytecode, pytest/ruff caches and build output.
- `vehicle-mcp/uv.lock`: generated lock (41 packages).

Dependencies (direct, licences checked from installed metadata):
- `mcp` 2.3.0 — MIT
- `httpx` 0.28.1 — BSD-3-Clause
- `pytest` 9.2.0 (dev) — MIT
- `ruff` 0.17.3 (dev) — MIT

## Result
n/a (code change)

## Checks
- `uv run pytest -q`: pass (60 passed)
- `uv run ruff check .`: pass
- `uv run ruff format --check .`: pass
- `uv build`: pass (wheel and sdist)
- `env -u VEHICLE_API_TOKEN uv run vehicle-mcp`: exits 2 with
  `VEHICLE_API_TOKEN is required` (manual startup check)
- `python3 scripts/check_zones.py vehicle-mcp --base origin/main`: yellow (all 16 changed
  files; vehicle-mcp is yellow as a repo; no red paths)

## Unsure about
- The installed MCP SDK is 2.3.0, where `FastMCP` was renamed to `MCPServer`
  (`mcp.server.mcpserver`). The code targets that API and pins `mcp>=2.3,<3`; if the project
  ever wants mcp 1.x, the import/tool registration changes.
- `MCPServer.call_tool()` raises `ToolError` directly in the SDK; the protocol layer turns it
  into an `is_error` result. Tests assert the explanatory message, not the wire rendering.
- Percentiles use linear interpolation and `std` is the population standard deviation; both
  are documented in the README, but they are choices, not dictated by the server.
- `duration_ms` is the span of the returned samples, not the requested window; for a
  downsampled window it is approximate even though `min`/`max` stay exact.
- The position filter is token-based; a legitimate signal whose name contains `height`,
  `alt`, `lat`, etc. would be hidden. No such series is known today, and D-076 item 3 is
  not implemented on the server.
- Tests use only synthetic `httpx.MockTransport` data (privacy); there is no live
  vehicle-server integration test in this change.
- `httpx` logs each request at INFO on stderr; it contains no token, but it may be noisy for
  an MCP host.
- Only the four direct dependencies were licence-checked; `uv.lock` also contains their
  transitive dependencies.

## For Claude
- CI workflow (`.github/` is red); v0.1 has no CI yet.
- Streamable HTTP transport (open D-077 item); v0.1 is stdio only.
- Defs submodule decision: v0.1 has none; series names/kinds/units come from the server
  responses, and the code hard-codes no signal facts.
- A release tag for v0.1.0 (no tags/version bumps by this tool, D-036).
- `CLAUDE.md` still lists the old fixed tool set (`get_live_snapshot`, ...) and says "No raw
  GPS returned". This task's user-approved list replaces it in the README; `CLAUDE.md` is
  red, so it was not edited. Please sync it.
- Consider whether `list_sessions` should return the raw list or the chosen
  `{"sessions": [...]}` wrapper; the wrapper gives one MCP text block instead of one block
  per session.
- `README.md` now says v0.1.0; this is not a release, just the package version.

## Claude review
(Filled by Claude's /external-review: findings, fixes, PRs.)
