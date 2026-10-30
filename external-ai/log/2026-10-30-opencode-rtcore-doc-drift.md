---
date: 2026-10-30
tool: opencode/deepseek-v4.1-flash
topic: rtcore-doc-drift
repos: [vehicle-rt-core]
branches: [vehicle-rt-core:ext/opencode-rtcore-doc-drift]
prs: [vehicle-rt-core#57]
zone: yellow
review: done 2026-10-30 (clean; Claude removed the remaining pin literals incl. the red misra/README.md and derived README; rt-core#57)
---

# rt-core doc drift C-10 / C-11 / C-12

## Goal
Fix stale facts in rt-core docs (defs pin, golden-vector provenance, service/app layout,
comms signature) without touching red paths or any `.c`/`.h`.

## Changes
- `vehicle-rt-core/README.md`: the defs pin is no longer a literal (it points at the tag in
  `vehicle-workspace/manifest.yaml`); `com` is no longer listed as "not yet" (it exists:
  `src/services/com.c` / `src/services/com.h`).
- `vehicle-rt-core/tests/host/vectors/README.md`: the headers say the vectors were generated
  from **v0.19.0** (banner of every `derived_*.h`); the current pin is **v0.19.1**, a
  rename-only commit on top of v0.19.0 (D-089) with the same derived/DID tables. Text only,
  no vectors regenerated.
- `vehicle-rt-core/src/app/README.md`: `comms_pass` now shows the real parameter list and
  order from `src/app/comms.h` (`..., ekf, lean`).
- Left unchanged after reading `src/`: `src/services/README.md:19` (`signal pool, log` are
  still absent from `src/services/`; `com` already has its own done row) and
  `README.md:18` (`target task setup` is still empty; `src/app/` has only `comms` + `host/`
  and the app README's Target section still says so).

## Result
n/a (docs only)

## Checks
- `python3 scripts/check_zones.py vehicle-rt-core --base origin/main`: yellow
  (`README.md`, `src/app/README.md`, `tests/host/vectors/README.md`; all allowed).
  `misra/README.md` was checked separately and is red -> not touched.
- `git diff --stat`: only `*.md` (3 files: README.md, src/app/README.md,
  tests/host/vectors/README.md).
- `cmake --preset host-tests && cmake --build --preset host-tests && ctest --preset host-tests`:
  pass, 45/45 (verifies the v0.19.1 pin still matches the vectors' gen fingerprint; the
  build directory had to be recreated because it was configured from the old workspace path).

## Unsure about
- v0.19.1 vs v0.19.0: I read `git log v0.19.0..v0.19.1` in the submodule; it is one commit
  (`refactor(defs): rename moto identifiers to vehicle`) and its diff is rename-only, so the
  vector tables match. If the tag ever moves, the fingerprint test is the authority.
- The vectors README no longer states a minimum pin ("v0.14.0 or later"); the exact current
  pin plus the fingerprint explanation replace it.
- The host test run was not required by the task; I ran it to make sure the new README text
  about v0.19.1 is true (it passed). No build artifact is committed.

## For Claude
- `vehicle-rt-core/misra/README.md:15` is **red** (MISRA register), so not edited. It is
  stale: "That gate is not in a release yet; this repo pins defs v0.2.0, so the pinned copy
  predates it." The pinned copy is v0.19.1 and its `misra/` directory (README, suppressions,
  canary) is present. Wanted: drop the "not in a release yet / v0.2.0" sentence or replace
  it with the current pin, without claiming which release first carried the gate.
- `vehicle-rt-core/misra/README.md:8` ("dropped its two in rt-core v0.7.0") is historical,
  not a current-pin claim; left alone as instructed.
- `src/features/uds/README.md` and `src/features/cornering/README.md` are red and were
  not opened for this docs-only task; no request about them.

## Claude review
- Zones: three yellow, as logged. architecture-guard checked every claim (submodule = v0.19.1, all `derived_*.h` banners v0.19.0, `comms_pass(..., ekf, lean)` in `comms.h`, `services/com.c`): all correct.
- Claude's commits on `claude/rtcore-doc-drift` (the ext commit is kept): the vectors README states the requirement (same derived table) instead of a new "pins v0.19.1" literal that would drift at the next bump; README says the manifest records the known-good combination; *For Claude*: `misra/README.md` (red) no longer says the pinned defs is v0.2.0 and predates the gate; `src/features/derived/README.md` (yellow, listed in C-10 but missed) no longer says "banner v0.14.0, pinned v0.18.1". The heartbeat README's `defs v0.15.0` is historical and stays.
- Lesson for external tools: when a finding lists several files (C-10 named five), close or explicitly defer each one in the log.
- PR rt-core#57 (docs only). Closes C-10, C-11, C-12 on merge.
