# Discovery Scan & Adaptive Polling Strategy: Full Parameter Mapping vs. Runtime Budgeting

## 1. Executive Summary & Problem Statement

To detect complex mechanical, electrical, and thermal anomalies (e.g., clutch slippage, knock, lean-angle-dependent fueling starvation, or charging circuit degradation), machine learning models ideally require access to the richest possible sensor telemetry pool. Modern vehicle ECUs (such as the Honda CL250 Keihin/Denso unit) contain between 50 and 100+ internal Diagnostic Identifiers (DIDs) and standard PIDs.

However, the physical nature of UDS (ISO 14229) over classical CAN is strictly **request-response (half-duplex polling)**. Each query incurs a physical round-trip time ($t_{RT} \approx 20\text{ ms}$). Blindly querying 50 parameters sequentially reduces the sampling rate to $\le 1\text{ Hz}$, which completely misses transient dynamic anomalies (such as wheel slip or lean instability occurring within $30\text{--}50\text{ ms}$).

This document establishes the official engineering roadmap to:
1. Map 100% of the ECU's internal telemetry space offline via automated discovery.
2. Restrict continuous runtime polling to an optimized, high-frequency core budget ($\le 0.8$).
3. Transition auxiliary parameters into an **event-triggered / adaptive polling** scheme.

---

## 2. Roadmap to Full Parameter Discovery (Phase 0 -> Phase 1)

Extracting the complete internal parameter map without manufacturer documentation follows three systematic stages:

```
+-------------------------------------------------------------------------------+
| STAGE 1: AUTOMATED BITMAP SCANNING (D-059 Discovery Mode)                     |
| Execution: One-shot scan during bench bootup (`esp32-s3-devkitc-1-probe`).    |
| Mechanism: Query standard support bitmaps (OBD Mode 0x01 PID 0x00, 0x20...)   |
|            and UDS Service 0x22 ranges (0xF400, 0xF420, 0xF440, 0xF460...).   |
| Outcome: Binary map of which of the 255 standard PIDs are physically wired.  |
+-------------------------------------------------------------------------------+
                                      │
                                      ▼
+-------------------------------------------------------------------------------+
| STAGE 2: PHYSICAL STIMULUS & CORRELATION MAPPING (Bench Testing)             |
| Execution: Interactive harness capture on static motorcycle.                  |
| Mechanism: Read candidate proprietary DID ranges (0x1000..0x2FFF) while       |
|            toggling mechanical states (clutch lever, side stand, gear shift,   |
|            front/rear brake switches, kill switch).                           |
| Outcome: De-anonymize proprietary DIDs by identifying bit flips matching      |
|          physical actions (e.g., bit 2 of DID 0x1005 transitions on clutch).  |
+-------------------------------------------------------------------------------+
                                      │
                                      ▼
+-------------------------------------------------------------------------------+
| STAGE 3: VEHICLE SNOOPING / DIAGNOSTIC REPLAY (Honda HDS Sniffing)            |
| Execution: Pass-through tap on OEM diagnostic tool communication.             |
| Mechanism: Sniff request-response pairs when factory service tool queries     |
|            sensor screens. Extract exact DID offsets, scaling, and units.     |
+-------------------------------------------------------------------------------+
```

---

## 3. The Runtime Invariant: Why All Parameters Must NOT Be Continuously Polled

Continuous runtime polling is constrained by strict automotive real-time invariants:

### 3.1 Mathematical Polling Budget Invariant (`D-029`)
The ECU compute budget must never be saturated by diagnostic requests. The normalized polling utilization $U_{poll}$ is bounded by:

$$U_{poll} = \sum_{i=1}^{N} \frac{t_{round\_trip}}{T_{poll, i}} \le 0.8$$

Where:
- $t_{round\_trip} = 20\text{ ms}$ (assumed safe average request-response latency).
- $T_{poll, i}$ is the polling period of parameter $i$.
- Currently, the 5 active DIDs (`ENGINE_SPEED`, `VEHICLE_SPEED`, `THROTTLE_POS`, `COOLANT_TEMP`, `BATTERY_VOLTAGE`) consume $U_{poll} = 0.514$.
- Polling 50 parameters at high frequency would result in $U_{poll} > 2.5$, causing ECU request dropped frames, timing jitter, and safety lockouts.

### 3.2 Nyquist-Shannon Sampling vs. Anomaly Transients
Mechanical and vehicle-dynamic anomalies possess distinct characteristic frequencies:

| Anomaly Class | Characteristic Duration | Required Sampling Rate | Polling Feasibility |
|---|:---:|:---:|---|
| **Cornering Loss of Traction** | $30\text{--}50\text{ ms}$ | $\ge 20\text{ Hz}$ ($50\text{ ms}$) | High (Core 5-11 signals only) |
| **Engine Knock / Rapid Misfire** | $10\text{--}20\text{ ms}$ | $50\text{--}100\text{ Hz}$ | IMU / Crank pickup (Not possible via UDS) |
| **Coolant Overheat / Head Gasket** | $5\text{--}30\text{ s}$ | $0.2\text{--}1\text{ Hz}$ | Low priority polling |
| **Charging / Rectifier Breakdown** | $500\text{--}2000\text{ ms}$ | $1\text{ Hz}$ | Low priority polling |

Polling low-priority parameters (e.g., ambient temperature or fuel level) at 10 Hz steals bandwidth from traction-critical signals (`VEHICLE_SPEED` and `ENGINE_SPEED`).

### 3.3 The Hardware Bottleneck Invariant (Amdahl's Law on Vehicle Bus)
A critical systems engineering reality governs the vehicle bus interface:
- **The Physical Bottleneck**: The OEM engine ECU runs on a fixed **500 kbps** classical CAN clock with an internal round-trip processing constraint of **15--20 ms**. Upgrading the tester MCU (e.g., from an entry-level MCU to a 480 MHz STM32H7) does **NOT** decrease this response latency by even one microsecond. The throughput ceiling on the `VEHICLE CAN` bus is physically dictated by the OEM ECU silicon.
- **The Dual-CAN Architecture Solution**:
  1. **`VEHICLE CAN` (OEM Bus - 500 kbps)**: Dedicated strictly to the single-tester UDS polling link with the factory ECU. Operating in strict adherence to the conservative polling budget ($U_{poll} \le 0.8$).
  2. **`PLATFORM CAN` (Internal Bus - 500 kbps / CAN-FD)**: An independent, unconstrained physical network connecting our STM32H7, STM32G4, Raspberry Pi 5, and auxiliary sensors. Because the factory ECU is not on this bus, it operates at **up to 1000 Hz** without budget constraints.
- **Role of the STM32H7**: The high compute capacity of the Cortex-M7 is leveraged not for accelerating vehicle bus polling, but for running complex Extended Kalman Filter (EKF) matrix algebra at 100+ Hz, managing high-throughput `PLATFORM CAN` sensor ingestion, and executing local predictive anomaly models.

---

## 4. Architectural Solution: Tiered & Triggered Adaptive Polling

Rather than static uniform polling, the platform employs a three-tier execution model:

```
[TIER 1: CORE REAL-TIME POOL (Always Active, 110-200 ms)]
  • Engine Speed (0xF40C), Vehicle Speed (0xF40D), Throttle Pos (0xF411)
  • Gear Position, Calculated Engine Load
  • Budget Allocation: ~0.50

[TIER 2: THERMAL & HEALTH POOL (Slow Background, 800-2000 ms)]
  • Coolant Temp (0xF405), Battery Voltage (0xF442), Intake Air Temp (0xF40F)
  • DTC Active Count (UDS 0x19 0x01)
  • Budget Allocation: ~0.20

[TIER 3: EVENT-TRIGGERED DIAGNOSTIC BURST (Conditional)]
  • Trigger: Coolant > 105°C, or Battery < 11.8V, or Misfire detected in Tier 1.
  • Action: Dynamically suspend Tier 2; inject single-shot diagnostic requests
    for O2 Sensor Voltage, Short/Long-Term Fuel Trims, and Full DTC Freeze Frames.
  • Upon resolution: Return to default Tier 1 + Tier 2 schedule.
```

---

## 5. Verification Checklist for Full Discovery Integration
1. [ ] Complete `discovery_scan` on CL250 hardware using `esp32-s3-devkitc-1-probe` env.
2. [ ] Dump resulting supported PID/DID bitmaps over serial logging.
3. [ ] Calculate incremental budget impact before moving any discovered signal into `uds/vehicle_cl250.yaml`.
4. [ ] Ensure all static configuration DIDs (e.g., VIN, CalID) are queried strictly once per ignition cycle and cached in non-volatile memory.
