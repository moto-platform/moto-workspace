---
date: 2026-10-29
tool: opencode/deepseek-v4.1-flash-free
topic: analyzer-a8-tests
repos: [vehicle-analyzer]
branches: [vehicle-analyzer:ext/opencode-analyzer-a8-tests]
prs: [vehicle-analyzer#24]
zone: yellow
review: done 2026-10-29 (merge: clean work; Claude added the single tab list and the CI UI step; analyzer#24)
---

# analyzer-a8-tests

## Goal
Roadmap A8 part 1: component tests for the six panels that render without hardware,
Playwright smoke coverage of every view, persistence of the active view and HUD layout,
and the approved test tooling (`test:ui`, Playwright, Testing Library, jsdom).

## Changes
- `chore(analyzer): add approved UI test tooling` (`a5c8770`): added the exact approved
  dev dependencies `@playwright/test@1.64.1`, `@testing-library/react@16.3.3` and
  `jsdom@29.0.0`; added the `test:ui` script and allowed `tests/**/*.test.tsx` in Vitest.
  jsdom 30.1.3 requires a newer Node than the local Node 25.2.1, so 29.0.0 is the latest
  compatible release.
- `feat(analyzer): persist the active view and HUD layout` (`a5fc508`): new
  `src/ui/layout.ts` stores `{ view, hud }` under `vehicle-analyzer.layout`; reads/writes
  are guarded so empty, invalid or blocked storage falls back to the original `trace` +
  HUD-visible startup state. `App.tsx` initialises from it and writes on change. Added six
  unit tests for defaults, invalid JSON, unknown values, blocked reads/writes and round-trip.
- `fix(analyzer): free the E shortcut for recorded sessions` (`42ec497`): the Trace and
  Oscilloscope export shortcuts used `E`, which `GLOBAL_KEYS` reserves for recorded
  sessions; Trace therefore swallowed `E` before App saw it. Both exports now use `V`
  (matching Compare's export key) and their hints were updated.
- `test(analyzer): cover panels and views without hardware` (`0e15154`): component tests
  for Cluster, Health, Trace, Session, Compare and ReplayScrubber using defs-driven frames
  and mocked read-only HTTP; Playwright config plus ten smoke tests covering all nine views,
  the virtual-only source, console errors, non-localhost requests and layout persistence
  across a reload. Playwright report/test-result folders are ignored.

## Result
- Component/unit suite: 22 files, 134 tests passed (12 new tests).
- Production build passes (`tsc -b && vite build`); only the existing >500 kB chunk warning.
- Playwright: 10/10 passed against the built preview.
- Branch was pushed as `ext/opencode-analyzer-a8-tests`; the work log stays uncommitted.

## Checks
- `npm test` - PASS (134/134).
- `npm run build` - PASS.
- `npm run test:ui` - PASS (10/10) with the local Chromium substitute noted below.
- `git diff --check` - clean.
- `python3 scripts/check_zones.py vehicle-analyzer --base origin/main` - one YELLOW
  (`package.json`, approved dependency manifest) and all other paths GREEN; no RED.
- Licence check: Playwright Apache-2.0, Testing Library MIT, jsdom MIT; added transitive
  licences are Apache-2.0/BSD/BlueOak/CC0/ISC/MIT/MIT-0. `npm audit` still reports the
  pre-existing vitest/tinypool/yaml advisories (2 moderate, 2 critical); no unrelated
  dependency upgrade was made.

## Unsure about
- `npx playwright install chromium` was attempted twice but the CDN delivered at roughly
  6-80 kB/s; the second attempt reached 50% after 20 minutes and was stopped. Local browser
  tests therefore ran through the system Brave binary using the
  `PLAYWRIGHT_CHROMIUM_EXECUTABLE` hook in `playwright.config.ts`. CI should install the
  normal Playwright Chromium and needs no environment variable.
- `@testing-library/react` renders without `@testing-library/jest-dom`; assertions use the
  built-in Vitest/Playwright matchers.
- Node 25 exposes a stub `localStorage` without `clear/getItem/setItem`; the layout test
  injects an in-memory `Storage` instead of relying on the environment.

## For Claude
- CI wiring of `npm run test:ui` and `npx playwright install chromium` (`.github/*` is red).
- Review the YELLOW `package.json` dependency change.
- Confirm the Trace/Oscilloscope export shortcut move from `E` to `V`; the README only
  documents `E` for recorded sessions, so no README change was made.
