---
date: 2026-10-30
tool: opencode/deepseek-v4.1-flash-free
topic: analyzer-a8-worker
repos: [vehicle-analyzer]
branches: [vehicle-analyzer:ext/opencode-analyzer-a8-worker]
prs: [vehicle-analyzer#25, vehicle-analyzer#26]
zone: green
review: done 2026-10-29 (fix first: replay double-ingest + stale decode fixed in analyzer#26, which supersedes #25)
---

# analyzer-a8-worker

## Goal
Roadmap A8 part 2: parse and decode imported ASC/CSV logs in a module Web Worker,
apply worker results in batches through `CaptureStore.ingestBatch`, keep a synchronous
fallback, and show progress with cancellation in the Sync view.

## Changes
- `src/services/ingestProtocol.ts`: typed worker request/response contract and 2,000-frame
  batch size.
- `src/services/logIngest.ts`: shared parse/sort/decode pipeline used by both the worker and
  the fallback, with progress and batches; E2E and timing remain in `CaptureStore`.
- `src/services/ingest.worker.ts`: module worker entry point.
- `src/services/ingestClient.ts`: worker start/terminate/cancel plus synchronous fallback
  when `Worker` is unavailable or construction fails.
- `src/state/captureStore.ts`: `ingestBatch` shares the one-frame path and notifies once per
  batch; `ingest` keeps per-frame notifications.
- `src/services/pipeline.ts`: uses worker-decoded `decodedSignals` on import, so decoding is
  not repeated; the store still owns timing and E2E checks.
- `src/App.tsx` / `src/components/SyncPanel.tsx`: import start clears live state once,
  worker batches feed the store, the replay timeline is installed after completion, and the
  Sync view shows progress, frame counts, a cancel button, and cancellation/error status.
  Loading a DBC, resetting defs, changing the source, or leaving the view cancels a running
  import so a worker snapshot cannot mix with a newer catalog/source.
- `tests/ingest.test.ts`: batch equality for frames/history/E2E/UDS, one notification per
  batch, predecoded-frame path, and ASC/CSV fallback parity.
- `tests/perf.test.ts`: batch-ingest benchmark and shared simulated capture helper.
- `ui-tests/import.spec.ts`: builds a 200k-frame ASC from `platform.dbc`, imports it through
  the real worker, checks progress/final count/no foreign requests, and cancels a running
  import.

No `package.json`, lockfile, CI, dependency, vehicle-defs or red-zone files changed.

## Result
- Baseline (before changes), three runs of `tests/perf.test.ts`:
  - 119,800 frames in 0.42 s = 284,472 frames/s
  - 119,800 frames in 0.41 s = 294,590 frames/s
  - 119,800 frames in 0.40 s = 299,183 frames/s
  - Median: 294,590 frames/s (0.41 s).
- After changes, latest three runs:
  - per-frame ingest: 0.49 s / 246,418 fps, 0.41 s / 289,783 fps, 0.38 s / 311,642 fps;
    median 0.41 s, 289,783 fps (within run-to-run noise of the baseline).
  - batch ingest: 0.36 s / 335,680 fps, 0.35 s / 343,670 fps, 0.51 s / 234,480 fps;
    median 0.36 s, 335,680 fps.
  - Earlier repeated runs had one system-noise outlier (0.85 s batch); the stable range was
    0.32-0.37 s. No regression in the rounded ingest benchmark.
- The 200k ASC UI import completes in about 4.4 s in local Playwright, with progress shown.

## Checks
- `npm ci`: pass; no manifest/lock change (4 pre-existing audit advisories).
- `npm test`: 23 files, 140 tests passed.
- `npm run build`: pass; `dist/assets/ingest.worker-*.js` emitted (2.91 kB).
- `PLAYWRIGHT_CHROMIUM_EXECUTABLE="/Applications/Brave Browser.app/Contents/MacOS/Brave Browser" npm run test:ui`:
  12 tests passed, including the 200k import and cancel tests. Local Chromium was unavailable;
  Brave was used through the existing executable hook. CI uses its normal Chromium.
- `git diff --check`: pass.
- `python3 scripts/check_zones.py vehicle-analyzer --base origin/main`: all 11 changed paths
  GREEN.
- No non-localhost requests and no console errors in the UI tests.

## Unsure about
- The fallback runs synchronously, so a browser without module-worker support blocks the main
  thread for the import (same as the previous behaviour). It exists to keep correctness and
  parity, not as a performance path.
- `decodeLogFrames` takes a catalog snapshot at import start; the view now cancels an import
  before loading another DBC, but a future in-worker catalog hot reload would need a protocol
  change.

## For Claude
- No red-zone change requested. The 200k test fixture is generated from the pinned
  `platform.dbc` and synthetic zero payloads; it contains no real ride data.

## Claude review
Verdict: **fix first**. Zones all green; architecture-guard found no scope, dependency or defs-literal problem.

Findings (reproduced in a Vitest probe):
- The import streamed every frame into `CaptureStore` and then installed the replay timeline at index 0. Play fed the log a second time: duplicate frames, time running backwards and one `WRONG_SEQUENCE` per E2E message. The log's own tests compared batch with per-frame ingest, so they could not see it; the App wiring was the bug.
- `FramePipeline.process` reused worker-decoded `decodedSignals`, so replay ignored a DBC loaded after the import (the "catalog snapshot" in *Unsure about* was a real bug, not only a future concern).
- A cancelled import left a partial capture in the store.

Claude's fix (analyzer#26, on top of the ext commit, which is kept): the worker only parses and sorts; on completion the store gets the first frame as before. Decoding stays in `FramePipeline` with the active catalog; `CaptureStore.ingestBatch`, the catalog snapshot, the `decodedSignals` shortcut and cancel-on-DBC-load were removed (`pipeline.ts`, `captureStore.ts`, `perf.test.ts` equal main). The UI test now checks that only the first frame reaches the views. CI green. Merge #26, close #25.

Lesson for external tools: when moving work off the main thread, keep the state semantics of the old path (here: "load for replay" leaves the views at frame 0) and test the wiring, not only the moved function.
