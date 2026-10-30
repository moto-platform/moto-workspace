---
date: 2026-10-30
tool: opencode/deepseek-v4.1-flash
topic: analyzer-a5-freeze-frames
repos: [vehicle-analyzer]
branches: [ext/opencode-analyzer-a5-freeze-frames]
prs: [vehicle-analyzer#29]
zone: yellow
review: done 2026-10-30 (clean, merged as analyzer#29 with Claude's style/int32 fix commit)
---

# analyzer-a5-freeze-frames

## Goal
Implement vehicle-analyzer ROADMAP A5 (decoded DTC freeze frames, D-090/D-080 item 5): decode 0x19 0x04 / 0x06 with the defs framing and DID catalog, pass every defs vector, show cards in UdsPanel, and move A5 to Built.

## Changes
- `src/defs/model.ts`: load `dtc_record_reports` into `iso.dtcRecordReports`; build a merged catalog of polled vehicle DIDs and OBD candidates, including multi-value `fields`; expose `catalogByDid`.
- `src/services/dtcRecords.ts` (new): pure snapshot/extended-data decoders using the YAML header, record-header and identifier lengths. Unknown DIDs stop with `unknown_did`, identification DIDs with `variable_length`, short records with `truncated`; the remainder stays raw.
- `tests/dtcRecords.test.ts` (new): reads `tools/codegen/tests/vectors/dtc_records.yaml` from the pinned submodule and runs every snapshot, extended-data and invalid vector, plus a count guard.
- `src/components/UdsPanel.tsx`: freeze-frame cards with DID names, values and units; extended-data record kind; stop reason and raw remainder; raw bytes remain visible.
- `src/services/udsMonitor.ts`: comment updated; it still stores the record bytes raw for the UI decoder.
- `tests/components/UdsPanel.test.tsx` (new): feeds ISO-TP responses and checks a decoded snapshot, extended-data kind and a stopped walk.
- `docs/ROADMAP.md`: UDS observer line updated, A5 row moved to Built.

## Result
A5 implemented on `ext/opencode-analyzer-a5-freeze-frames`. No vehicle bus traffic is added; decoding is host-only and listen-only behavior is unchanged.

## Checks
- `npm test`: PASS, 25 files / 155 tests.
- `npm run build`: PASS (tsc + vite; existing >500 kB chunk warning only).
- `npm run test:ui`: PASS, 12 Chromium tests. The first run failed because the Playwright browser was not installed; `npx playwright install chromium` fixed it, no repo files changed.
- `python3 scripts/check_zones.py vehicle-analyzer --base origin/main`: `src/defs/model.ts` YELLOW (defs loader), all other changed paths GREEN. No red path touched.
- `git -C external/vehicle-defs describe --tags`: `v0.20.0`.

## Unsure about
- `src/defs/model.ts` is yellow in `zones.json`, although the task described the source tree as green; the change is the defs loader required to read the new YAML block, not a signal fact or hard-coded value.
- The UI keeps the full raw bytes under every card, so a decoded card is additive rather than replacing the evidence.

## For Claude
- Review `src/defs/model.ts` (yellow) and mark the PR `needs-claude-review`.
- Check that exposing the OBD candidate catalog in `Defs` is the intended shape for future host-side decoders; it is read-only and derives every value from defs.

## Claude review
- Zones: one yellow path (`src/defs/model.ts`), no red. architecture-guard and vss-schema-guardian: no blocker, no new hand-written DID/SID/scale in `src/`; the decoder mirrors the generated Python reference in defs v0.20.0 line by line.
- The tool left its work uncommitted; Claude committed it as is with the `AI-Agent:` trailer (commit 1) and added commit 2 on `claude/a5-freeze-frames`: camelCase result fields (the vector test maps the snake_case keys), multi-value fields decoded with arithmetic instead of `&` (int32 cut a 4-byte field), a scalar OBD candidate must carry its formula (only a multi-value entry gets the codegen's neutral raw view, which the defaults matched), no try/catch around decoders that never throw, unique React keys, a vector guard without a hard-coded count, a comment on why identification DIDs stay out of `catalog`.
- *For Claude* answers: the yellow `model.ts` change is the intended shape (loader only, every value from defs); exposing `catalog` / `catalogByDid` with the `polled | candidate` status is fine for future host decoders.
- Checks: `npm test` 155/155, build, `test:ui` 12/12, CI green. analyzer#29 merged on the user's request. Process note: commit your work before ending a session (AGENTS.md: branch + commits + log).
