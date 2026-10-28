---
date: 2026-10-29
tool: opencode/deepseek-v4.1-flash
topic: ble-onwrite-parse
repos: [vehicle-connectivity-node, vehicle-workspace]
branches: [vehicle-connectivity-node:ext/opencode-ble-onwrite-parse, vehicle-workspace:ext/opencode-ble-onwrite-parse]
prs: [vehicle-connectivity-node#39]
zone: yellow
review: pending
---

# BLE telematics write parser without heap or sscanf (E-25 3)

## Goal

Fix ISSUES E-25 item (3): `BLEServerModule::onWrite` copied the BLE write into a `std::string` and parsed it with `strstr` + `sscanf` on the BLE stack task (PLATFORM-RULES 5: no dynamic memory / string parsing on MCUs). Replace it with a fixed-size copy from `getData()`/`getLength()` and a small hand-written parser with no heap and no `sscanf`, keeping the wire format and semantics. E-25 item (4) (the 5 ms TWAI wait) was explicitly out of scope.

## Changes

- `vehicle-connectivity-node/src/TelematicsParser.h` (new): `kTelematicsMaxWrite = 160`, `TelematicsEventType` and `TelematicsEvent` moved here from `BLEServerModule.h`, and the pure declaration `bool parseTelematicsWrite(const uint8_t* data, size_t len, TelematicsEvent& out)`. No Arduino/BLE includes, so it compiles on the host.
- `vehicle-connectivity-node/src/TelematicsParser.cpp` (new): bounded key search (no `strstr` on an unterminated buffer), 31-character NUL-terminated text copy, hand-written decimal parser (no `sscanf`), range checks for DIST/ICON, whole-write rejection above `kTelematicsMaxWrite`. No `new`, no `malloc`, no STL string.
- `vehicle-connectivity-node/src/BLEServerModule.h`: includes `TelematicsParser.h`; the enum/struct moved out; the G1.2 queue comment stays.
- `vehicle-connectivity-node/src/BLEServerModule.cpp`: `onWrite` now calls `parseTelematicsWrite(pCharacteristic->getData(), pCharacteristic->getLength(), evt)` and enqueues with `xQueueSend(..., 0)` as before. The empty write / no queue case still returns without enqueueing.
- `vehicle-connectivity-node/test/test_native/test_main.cpp`: includes `../../src/TelematicsParser.h` and `../../src/TelematicsParser.cpp`, plus 10 new tests and their `RUN_TEST` lines.

Wire format and semantics kept: fields `SONG:`, `ARTIST:`, `DIST:`, `ICON:` in any order separated by `|`; SONG/ARTIST stop at the next `|` or the end, max 31 characters, always NUL-terminated; DIST/ICON are decimal integers; each field sets its `has*` flag only when present and valid; a write with no valid field returns false and enqueues nothing; a partial write never clears the other fields (the parser leaves their `has*` flags clear). As with the old `sscanf("%d")`, trailing text after the digits is ignored (`DIST:12km` parses as 12) and an empty `SONG:` still clears the title.

Two deliberate tightenings (as requested):

1. DIST outside 0..65535 and ICON outside 0..255 are rejected instead of silently wrapping through the old `(uint16_t)`/`(uint8_t)` casts.
2. A write longer than `kTelematicsMaxWrite` (160 bytes) is dropped entirely. Every read is bounded by `len`; the ATT value is not NUL-terminated (an embedded NUL ends the scanned range, matching the old `c_str()` behaviour).

## Result

`onWrite` no longer allocates or parses strings with libc on the BLE stack task. The parser is host-testable and has no BLE dependency. No red-zone file was touched; `platformio.ini` is unchanged.

PR: vehicle-connectivity-node#39 (branch `ext/opencode-ble-onwrite-parse`, marked `needs-claude-review`).

## Checks

- `pio test -e native`: PASSED — 279 test cases, 279 succeeded (all six native suites; 10 new telematics parser tests).
- `pio run -e esp32-s3-devkitc-1`: SUCCESS — RAM 18.4% (60220 / 327680 B), Flash 42.5% (1336913 / 3145728 B).
- `cppcheck --std=c++11 --enable=warning,performance,portability --error-exitcode=1 --inline-suppr --suppress=missingIncludeSystem -I src -I external/vehicle-defs/gen/c/conn src`: exit 0, no findings (CI's blocking invocation).
- `python3 scripts/check_zones.py vehicle-connectivity-node`:
  ```
  YELLOW vehicle-connectivity-node/src/BLEServerModule.cpp  (MCU firmware: no heap after init, loop step bound (D-053))
  YELLOW vehicle-connectivity-node/src/BLEServerModule.h  (MCU firmware: no heap after init, loop step bound (D-053))
  YELLOW vehicle-connectivity-node/src/TelematicsParser.cpp  (MCU firmware: no heap after init, loop step bound (D-053))
  YELLOW vehicle-connectivity-node/src/TelematicsParser.h  (MCU firmware: no heap after init, loop step bound (D-053))
  YELLOW vehicle-connectivity-node/test/test_native/test_main.cpp  (MCU firmware: no heap after init, loop step bound (D-053))
  ```
  No red paths.

## Unsure about

- `DIST:12km` is accepted as 12 because the old `sscanf("%d")` stopped at the first non-digit. I kept that and added a test; if the reviewer prefers strict end-of-field validation, that is a one-line change.
- An empty `SONG:`/`ARTIST:` (key with no text) still sets its `has` flag and clears the field, because the old code set the flag on the key alone even when `sscanf` matched nothing. This is tested.
- An embedded NUL ends the scanned range (keys after it are not found), matching the old `std::string::c_str()` + `strstr` behaviour; the new parser still never reads past `len`.
- `kTelematicsMaxWrite` is 160 as specified; a write exactly 160 bytes long is still parsed, 161 is dropped (tested).
- No device was available; the firmware check is a build only. The native tests cover the parser, not the BLE stack callback itself.

## For Claude

- Please review the two tightenings and the `DIST:12km` / empty-`SONG:` semantics above; both are intentional to match the old wire behaviour.
- E-25 (3) can be closed after review (ISSUES.md was not edited, as instructed). E-25 (4) (TWAI 5 ms wait) is untouched.
- The new parser file is yellow (MCU firmware), not red; no red-zone request.

## Claude review

(Filled by Claude's /external-review: findings, fixes, PRs.)
