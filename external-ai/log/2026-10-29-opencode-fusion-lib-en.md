---
date: 2026-10-29
tool: opencode/deepseek-v4.1-flash
topic: fusion-lib-en
repos: [vehicle-workspace]
branches: [vehicle-workspace:ext/opencode-fusion-lib-en]
prs: []
zone: green
review: done 2026-10-29 (faithful translation, accepted; docs stay untracked until git-lfs; log merged with the 2026-10-29 review PR)
---

# fusion-lib English translation

## Goal

Translate `models/fusion-lib/SCHEMATIC-README.md` (286 lines, v1.2) and `models/fusion-lib/README.md` (92 lines) into English in place, faithfully: no added, dropped, reordered or "improved" technical content. Every number, unit, pin name, part number, voltage, resistor value, table row, D-xxx/Q-xxx reference and CONFIRM/TBD/Proposal marker stays the same. `moto-platform` becomes `vehicle-platform` (D-089); `moto-*.lbr` file names and Fusion design names (`moto-bike-p0`, `moto-bike`, `moto-helmet`, `moto-hil`) stay as they are. `SCHEMATIC-README.md` version line becomes 1.3 with the note "1.2 → 1.3: English translation, no content change." The `*.lbr` files and `_generator/` were not touched.

## Changes

- `vehicle-workspace/models/fusion-lib/SCHEMATIC-README.md`: line-for-line English translation (still 286 lines). Version 1.2 — 2026-10-24 → 1.3 — 2026-10-29; the cross-check list and the "difference from 1.1" sentence are translated unchanged and the translation note is added. Markdown structure kept: same headings (§1–§9, S1–S5), same tables/columns, same three code blocks, same links.
- `vehicle-workspace/models/fusion-lib/README.md`: line-for-line English translation (still 92 lines). Library names `moto-*.lbr` kept; "Güven" column translated to "Confidence".
- Both files are **untracked** (`models/` still needs git-lfs before its first commit); nothing under `models/` was staged or committed.
- `vehicle-workspace/external-ai/log/2026-10-29-opencode-fusion-lib-en.md`: this log, the only committed file on the branch.

Project-name handling: the only `moto-platform` occurrences (both titles) are now `vehicle-platform`. `moto-vehicle-defs/docs/hardware-procurement-list.md` in README line 3 became `vehicle-defs/docs/hardware-procurement-list.md` because D-089 renamed the repo, not a file or design; see "Unsure about".

## Result

Both documents are fully English with the original structure and technical facts intact. `moto-*.lbr`, design names and the generator were not modified.

## Checks

- `grep -c '' models/fusion-lib/SCHEMATIC-README.md models/fusion-lib/README.md`:
  ```
  models/fusion-lib/SCHEMATIC-README.md:286
  models/fusion-lib/README.md:92
  ```
  (originals: 286 and 92 lines — exact match; `wc -l` gives the same 286/92/378 total)
- `grep -nE '[çğıöşüÇĞİÖŞÜ]' models/fusion-lib/*.md`: no output (exit 1, no Turkish characters left).
- `python3 scripts/check_zones.py . --path models/fusion-lib/SCHEMATIC-README.md models/fusion-lib/README.md external-ai/log/2026-10-29-opencode-fusion-lib-en.md`:
  ```
  YELLOW vehicle-workspace/models/fusion-lib/SCHEMATIC-README.md  (workspace files)
  YELLOW vehicle-workspace/models/fusion-lib/README.md  (workspace files)
  GREEN  vehicle-workspace/external-ai/log/2026-10-29-opencode-fusion-lib-en.md  (your session log)
  ```
  The branch commits only the log (green); the translated docs stay untracked, as requested, so the log's `zone` is green per the task.

## Unsure about

Translation choices (Turkish original → English choice):

- `Öneri` → **Proposal** (as required; all 5 occurrences).
- `moto-vehicle-defs/docs/...` → `vehicle-defs/docs/...`: repo renamed by D-089; it is not an `.lbr` file or Fusion design name.
- `Öncelik sırası` → "Priority order"; `Sürüm` → "Version"; `farkı` → "Difference"; `çapraz kontrol` → "cross-check".
- `md.` (madde, in D-072 md. 4a etc.) → "item" (reference itself unchanged).
- `Ölü-adam` → "Dead-man"; `Kıvılcım klipsi` → "Spark clip".
- `usta-mekanik sensorleri` → "master mechanic sensors" (README Part 2 heading).
- `Burgulu çift` → "Twisted pair"; `düğüm` → "node"; `kelepçe` → "clamp"; `kırpar` → "clamps".
- `rakor` → "cable gland"; `klemens` → "terminal"; `distans` → "standoff"; `Sönümlü tabla` → "damped plate".
- `tezgah` → "bench"; `şasi` → "chassis"; `gövde` → "body"/"housing" depending on context (relay/terminal vs. JST housing).
- `Bozuk çerçeve enjeksiyonu` → "Malformed frame injection"; `arıza/besleme düğümü` → "fault/supply node".
- `açık kollektör` → "open collector"; `boştayken (yüksüz)` → "unloaded (no target)"; `Kart üstü` → "on-board".
- `takılı giriş` (IND_L/R failure list) → "stuck input" (could also read "plugged-in input"; "stuck" fits the failure-mode list).
- `kayıt` (S2 page plan) → "logging"; `park modu` → "park mode"; `halka` → "ring"; `sinyal lambası` → "turn signal".
- `Güven` → "Confidence" (README table column); `Bilinen açıklar` → "Known gaps"; `kenar birimi` → "edge unit".
- `baskı` → "silkscreen"; `kumpas` → "calipers"; `damar` (cable) → "core"; `blendaj` → "shield".
- `yer tut` → "use as a placeholder"; `krimp aleti` → "crimp tool"; `spiral` → "spiral wrap"; `kalem` (BOM) → "item".
- `iletim` → "conducting"; `kopar` → "drops out"; `bozulur` → "damages"; `yedek` → "spare".
- `yıldız bağlantı` → "star connection"; `havada` → "floating"; `net-tie` kept.
- `sızdırmazlık` → "sealing"; `müdahale` → "intervention"; `takılmadan önce` → "before fitting".
- `Kask` → "helmet"; `ses birimi` → "audio unit"; `sürücü transistör` → "driver transistor"; `bölücü direnç` → "divider resistor".
- `kendi lisansında kontrol et` → "check under your own licence"; `önceki sürümün BOM eksikleri` → "the previous version's BOM gaps".
- "M12x60 govde" (already ASCII Turkish) → "M12x60 body"; "Ana kontrolcu, guc zinciri" → "Main controller, power chain"; "Guvenlik" → "Safety"; "tezgahi" → "bench".

## For Claude

- Nothing red-zone was touched. The two translated docs are untracked under `models/`; they need git-lfs and the user's first commit, not this branch.
- If `moto-vehicle-defs` should stay verbatim in README line 3 instead of the post-D-089 `vehicle-defs`, revert that one token; everything else is a pure translation.
- No content was reordered. Please spot-check the version line (1.3) and a few table rows against the Turkish originals before the user's commit.

## Claude review

- Verdict: accepted, no fix. Zone green (only this log is committed; `models/` stays untracked by design).
- Spot check: the SCHEMATIC-README header (version line, priority order, libraries, the CONFIRM/TBD/Proposal rule, the §1 sheet table) matches the Turkish original read earlier the same day line by line; the power-chain values (SMBJ30CA 33.3-36.8 V / 48.4 V, electrolytic ≥ 50 V, 1N5822 note, L1 TBD) and every CONFIRM/TBD marker are intact; no Turkish characters left; line counts 286/92 unchanged.
- Limitation: the originals were overwritten in place and were never tracked, so a full diff against them is not possible; the user keeps the only copy check (Turkish originals in `docs/archive/` are not read by Claude, D-038).
- `moto-vehicle-defs` → `vehicle-defs` in README line 3 is correct (D-089 renamed the repo). The `moto-*.lbr` and design names stay until the library rename is decided with the git-lfs commit (STATUS S-track).
- `takılı giriş` → "stuck input" fits the failure-mode list.
