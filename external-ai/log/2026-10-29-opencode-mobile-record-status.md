---
date: 2026-10-29
tool: opencode/deepseek-v4.1-flash-free
topic: mobile-record-signal-status
repos: [vehicle-mobile]
branches: [vehicle-mobile:ext/opencode-mobile-record-status]
prs: [vehicle-mobile#24, vehicle-mobile#25]
zone: green
review: done 2026-10-30 (merge with one fix: skipped and never kept apart, mobile#25 supersedes #24)
---

# mobile-record-signal-status

## Goal
Complete `vehicle-mobile` E-18 item (3): show a compact vehicle-signal status line on the Record screen while recording, using the decoded vehicle-signal block, with fresh/stale/NRC/missing counts and widget coverage.

## Changes
- `vehicle-mobile/lib/ui/record_screen.dart`: refined the existing `VehicleSignalStatusLine` (merged earlier in #18) instead of adding a duplicate. It now takes the BLE link state and shows exactly `Vehicle signals: no data` with no link, no block, or no records. With data it reports `fresh` (`valid`), `stale`, `NRC` (`negativeResponse`) and `missing` (`skipped` + `neverReceived`) counts; unknown generated states remain visible as `unknown`, and `Lost blocks` is appended only when nonzero. All states still come from the generated `BleVehicleSignalState`; no BLE parsing was added.
- `vehicle-mobile/test/record_vsig_status_test.dart`: replaced the shallow tests with widget tests for no link, before the first block, fresh, stale, NRC, and missing (skipped/never) cases. The recording integration test now starts with a connected link and asserts the exact no-data and updated-count lines. Removed the synthetic `0xFFFF` DID from the test; DIDs still come from `vehicleSignalCatalog`.

## Result
The status line satisfies the requested no-data contract and four-category summary while reusing the recorder's existing per-DID state. No catalog facts, signal names, DIDs or millisecond limits were added to production code. Opened as PR vehicle-mobile#24.

## Checks
- `/Users/alihanesentas/development/flutter/bin/flutter test test/record_vsig_status_test.dart`: pass, 7 tests.
- `/Users/alihanesentas/development/flutter/bin/flutter analyze`: pass, no issues.
- `/Users/alihanesentas/development/flutter/bin/flutter test`: pass, 224 tests.
- `git diff --check`: pass.
- `python3 scripts/check_zones.py vehicle-mobile --base origin/main`: GREEN for both changed paths.
- GitHub Actions on PR #24: `flutter` pass (1m55s), `build-apk` pass (7m45s).
- `flutter` rewrote the local `pubspec.lock` while resolving deps; it was restored and is not committed.

## Unsure about
- E-18 item (3) was still listed open even though a status line had already merged in mobile#18. I treated the task as an exact-contract refinement (no-data text, four categories, link state) rather than a second line.
- `missing` counts both `skipped` and `neverReceived`; `NRC` counts every `negativeResponse`, not only NRC 0x31. If "unsupported" means only 0x31, the wording/count should be narrowed.
- The local Dart formatter is newer than the repository's formatting and rewrites the whole file. I kept the diff focused instead of committing unrelated formatting; CI runs only analyze/test.

## For Claude
No red-zone requests. Please confirm the `missing` mapping (skipped + neverReceived) and whether the `NRC` count should be restricted to 0x31. The existing #18 status line was refined, not duplicated.

## Claude review
Verdict: **merge with one fix** (mobile#25, contains #24's commit). Zones green, CI green on #24, `flutter analyze` / `flutter test` (224) pass on #25.

- The task prompt was Claude's mistake: the status line already existed since mobile#18. Refining it instead of adding a second line was the right call.
- Kept: `no data` without a link, before the first block or with no records (a lost link no longer shows a stale map as current); unknown states visible; `Lost blocks` only when nonzero; the `0xFFFF` literal DID removed from the test.
- Changed by Claude: `skipped` (the sender gave up after repeated timeouts, `did_skip_cooldown_ms`) and `neverReceived` (no answer since boot) were folded into one `missing` count. They mean different things (an ECU that stopped answering vs. one that never did), so they are counted apart again; zero counts are omitted (fresh always shown) so the line fits a phone.
- Answers to *For Claude*: `missing` mapping, no (see above). `NRC` stays every negative response, as the generated `negativeResponse` state defines; 0x31 only would hide other NRCs.
