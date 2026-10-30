---
date: 2026-10-30
tool: opencode/deepseek-v4.1-flash
topic: analyzer-dtc-export
repos: [vehicle-analyzer]
branches: [vehicle-analyzer:ext/opencode-analyzer-dtc-export]
prs: [vehicle-analyzer#30]
zone: green
review: done 2026-10-30 (clean; Claude added the code column, ext-data CSV row and a shared didHex; analyzer#30)
---

# analyzer A5.1 DTC report export + composer default DID from defs

## Goal
Export the observed DTCs (with the A5-decoded freeze frames) as JSON and CSV from the
DTCs tab, and remove the hand-written `0xF40C` default DID from the UDS composer.

## Changes
- `vehicle-analyzer/src/services/dtcReport.ts` (new): pure `dtcReportToJson` /
  `dtcReportToCsv` builders; names, units and DIDs come from `defs.catalogByDid`, the
  record framing from `defs.iso.dtcRecordReports`.
- `vehicle-analyzer/src/components/UdsPanel.tsx`: two export buttons (JSON, CSV) on the
  DTCs tab through `downloadFile()`; composer default DID now the first
  `defs.vehicle.dids` entry instead of the literal `'0xF40C'`.
- `vehicle-analyzer/tests/dtcReport.test.ts` (new): builds entries from the pinned defs
  vectors (`dtc_records.yaml`) and checks both outputs, multi-value DID and stopped walk.
- `vehicle-analyzer/tests/components/UdsPanel.test.tsx`: export buttons on the DTCs tab;
  composer default DID test.
- `vehicle-analyzer/docs/ROADMAP.md`: A5.1 row in the Built table.

## Result
n/a (code change)

## Checks
- `npm test`: pass (26 files, 159 tests)
- `npm run build`: pass (tsc -b + vite build; only the pre-existing >500 kB chunk warning)
- `npm run test:ui`: pass (12 Playwright tests)
- `python3 scripts/check_zones.py vehicle-analyzer --base origin/main`: green (5 files, all green)

## Unsure about
- "raw bytes as hex strings" in the JSON: `snapshot`/`extData` stay exactly the
  `decodeDtc*Records()` result (byte arrays), and the raw record payloads are added as
  `snapshotRaw` / `extDataRaw` hex strings next to them. If the intent was to hex-encode
  the `data`/`rest` arrays inside the decoded result too, that is a one-line change.
- CSV `status` is written as hex (`0x08`) like `dtc`/`did`; JSON `status` stays numeric.
- The composer fallback is an empty DID string if `defs.vehicle.dids` is empty (it is not
  today); the option list still comes from defs.
- The two export buttons show only while the DTCs tab is active and at least one DTC exists.

## For Claude
- None. Venturing no guess about A5.1 wording in `docs/ROADMAP.md`; adjust freely.

## Claude review
- Zones: all green; `udsComposer*` (red) untouched, the default-DID change is UI state only. architecture-guard and vss-schema-guardian: no blocker, no hand-written DID/SID/unit in `src/`.
- Claude's commits on `claude/a51-dtc-export` (the ext commit is kept): `didHex` moved to `services/format` and used for the composer options too (the options were unpadded, the new default padded, so a DID below 0x1000 would have had no matching option); the SAE `code` the DTCs tab shows is in both reports; the CSV writes an `ext:<kind>` row (first record number, raw bytes) instead of a bare row when only extended data exists; ROADMAP row updated.
- *Unsure about* answers: keeping `snapshot` / `extData` as the decoder result plus `snapshotRaw` / `extDataRaw` hex is right (no change); hex status in CSV, numeric in JSON is fine; the empty fallback DID is fine.
- Accepted: the tests repeat values from the defs vectors (`0x123456`, `VEHICLE_SPEED`, `km/h`); a defs change fails them loudly. Noted for later: the composer's `0x22` / `0x03` SID/sub defaults are older literals (could default to the first `composerServices(defs)` entry).
- Checks: `npm test` 159/159, `npm run build`, `npm run test:ui` 12/12. PR analyzer#30.
