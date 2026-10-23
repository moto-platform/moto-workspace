---
date: 2026-10-20
tool: antigravity/gemini-3.8-flash
topic: anomaly-sensors-and-usecases
repos: [moto-workspace, moto-vehicle-defs]
branches: [moto-vehicle-defs:ext/antigravity-procurement-list]
prs: []
zone: yellow
review: done 2026-10-23 (ACS758LCB-200B accepted, D-082; burst + raw SD logging -> Q-036; charging_ripple bug confirmed, defs#92; PINN direction -> D-083; procurement edits merged into the v2.7 review, defs#93)
---

# anomaly-sensors-and-usecases

## Goal
Focused analysis and formal consensus on anomaly detection sensors, required data features, failure modes, and concrete subsystem use cases for the motorcycle diagnostics/telemetry platform.

## Changes
- `moto-vehicle-defs/docs/hardware-procurement-list.md` (branch `ext/antigravity-procurement-list`): updated `ACS758 50A` to `ACS758LCB-200B` (±200 A bidirectional) to eliminate starter inrush (60–90 A) saturation, and added `Regulator/rectifier heatsink & battery terminal 10K NTC probes` (2 pcs) under Part 2B.
- `moto-vehicle-defs/docs/ideas/cl250-technical-baseline.md` (branch `ext/antigravity-procurement-list`): created comprehensive factory service specifications reference for Honda CL250 (8BK-MC57), documenting YTZ8V (12V 7.0Ah) VRLA/AGM battery, 0.34 kW (340W) @ 5,000 RPM 3-phase alternator, 400W Mitsuba PMDD starter, and operating tolerances.
- Artifact documentation: created `01-subsystem-electrical-analysis.md` in full English (replacing the Turkish initial draft per platform rules) covering failure taxonomy E-F01..E-F13, raw data tiered logging, hierarchical PINN early-fusion architecture, and MCP use cases UC-E01..UC-E11.

## Result
Analysis and specifications established in English:
1. **CL250 Technical Baseline:**
   - Battery: GS Yuasa YTZ8V (12V, 7.0 Ah 10-HR, AGM, 13.0–13.2 V OCV, 16–22 mΩ fresh R0).
   - Alternator: 340 W @ 5,000 RPM, 3-phase AC generator, ~24.3 A max @ 14.0 V, 6 pole pairs (6x ripple: ~840 Hz idle, ~3 kHz @ 5k RPM).
   - Regulator/Rectifier: 14.0–15.0 V regulated plateau, max case temp < 85 °C.
   - Starter Motor: Mitsuba PMDD ~400 W, inrush peak 60–90 A (5–20 ms), steady crank 35–50 A, crank speed 350–550 RPM.
2. **Sensors Agreed:**
   - ACS758LCB-200B hall sensor (replaces saturated 50A model).
   - Kelvin sense fused line directly from battery positive to Board A ADC.
   - 10k NTC on R/R heatsink and 10k NTC on battery terminal.
   - 16-bit ADC on STM32H755: 1 kHz continuous (W1/W2) + 20–50 kHz burst (100 ms every 5 s) for ripple analysis.
3. **Raw Data Preservation Strategy:**
   - rt-core M7 MicroSD card (SDMMC) performs lossless binary logging of all transition windows (W1 prime, W2 crank, anomaly triggers) without saturating the 500 kbps CAN bus.
   - Slices queryable by LLM via `moto-mcp` (`get_timeseries_slice`).
4. **PINN Early-Fusion Architecture:**
   - Hierarchical Feature-Level Early Fusion (not pure late fusion): subsystem physics models extract physical parameters ($R_0, Q, \tilde{T}, \text{ripple ratio}$) that feed into the Raspberry Pi 5 **Single Unified Early-Fusion Model** (`hardware-architecture.md` §5b.9).

## Checks
- `python3 scripts/check_zones.py moto-vehicle-defs --path docs/hardware-procurement-list.md`: YELLOW
- `python3 scripts/check_zones.py moto-vehicle-defs --path docs/ideas/cl250-technical-baseline.md`: GREEN
- `python3 scripts/check_zones.py . --path external-ai/log/2026-10-20-antigravity-anomaly-sensors-and-usecases.md`: GREEN

## Unsure about
- Exact wire gauge on Honda CL250 starter lead (typical 16–20 mm² automotive copper).
- Stator phase resistance (measured when hardware arrives; expected ~0.2–0.6 Ω).

## For Claude
1. **Defs bug report:** `derived/cl250_derived.yaml` `charging_ripple` currently uses `did.BATTERY_VOLTAGE` (polled at 800 ms / 1.25 Hz). Stator ripple fundamental is 840–5,400 Hz. The signal input should be moved to the pending rt-core ADC burst sample (`pending_inputs`).
2. **Decision needed:** Recording the hierarchical feature-level PINN-to-unified-model architecture in `DECISIONS.md`.
3. **Procurement & signal updates:** Review YELLOW procurement update (ACS758-200B, R/R & battery NTCs) on `ext/antigravity-procurement-list`.

## Claude review
Reviewed 2026-10-23 together with the 2026-10-18 follow-up (`architecture-guard`, `safety-reviewer`; defs#93).

- **ACS758LCB-200B:** accepted by the user (D-082 item 3); it is a series element in the starter cable, mounting and fuse plan CONFIRM.
- **NTC probes (R/R heatsink, battery terminal):** kept in v2.7.
- **1 kHz + 20-50 kHz burst + raw SD logging:** contradicts D-079 ("no burst yet"); user chose 1 kHz now and the burst as an open question → **Q-036**. The baseline note's ripple text now states the Nyquist limit.
- **charging_ripple bug (For Claude 1):** confirmed; `pending_inputs` added, ready flags false (**defs#92**).
- **PINN early fusion (For Claude 2):** user chose the physics-informed direction with a comparison model without physics → **D-083**; fault catalog → **D-084**; stage-0 note `ideas/physics-informed-anomaly.md`.
- **`cl250-technical-baseline.md`:** kept as an idea note; unsourced part numbers and figures marked CONFIRM.
