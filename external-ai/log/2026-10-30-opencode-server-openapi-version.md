---
date: 2026-10-30
tool: opencode/deepseek-v4.1-flash
topic: server-openapi-version
repos: [vehicle-server]
branches: [vehicle-server:ext/opencode-server-openapi-version]
prs: [vehicle-server#38]
zone: green
review: done 2026-10-30 (clean, no Claude change; server#38)
---

# server OpenAPI version from the package version (C-07)

## Goal
Stop the OpenAPI document from advertising a stale version: use
`vehicle_server.__version__` instead of the `"0.2.0"` literal, and pin that it matches
`pyproject.toml`.

## Changes
- `vehicle-server/src/vehicle_server/api.py`: `FastAPI(..., version=__version__)`.
- `vehicle-server/tests/test_api.py`: `GET /openapi.json` -> `info.version` equals
  `vehicle_server.__version__` and the `[project].version` read with `tomllib`.

## Result
n/a (code change)

## Checks
- `uv sync && uv run pytest`: pass (345 passed, 1 pre-existing Starlette deprecation warning)
- `uv run ruff check .`: pass (all checks passed)
- `uv run ruff format --check .`: pass (64 files already formatted)
- `python3 scripts/check_zones.py vehicle-server --base origin/main`: green (2 files)

## Unsure about
- Nothing guessed: the test checks all three values (OpenAPI, `__version__`,
  `[project].version`). If the two version sources ever diverge, the test fails even though
  the OpenAPI value follows `__version__`.

## For Claude
- None.

## Claude review
- Zones green; architecture-guard: no finding. The chained assertion catches a missed bump in either `__init__.py` or `pyproject.toml`. A single version source (`importlib.metadata`) is possible later, not needed.
- PR server#38 opened from the ext branch as is. Closes C-07 (`PROJECT-CONTRADICTIONS.md`) on merge.
