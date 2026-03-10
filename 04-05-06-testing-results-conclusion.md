# Chapter 4: Testing and Calibration

## 4.1 Experimental Setup

- Rotating rod: ø 0.024 m × 0.3 m length
- Torque sensor fixed to frame via aluminium plate
- Motor mounted in holder attached to same rigid frame
- Rod connected to sensor and motor via flexible shaft couplers

---

## 4.2 Trial Run Without Sample

First test validated motor control, electronic interfacing, and software. Initial full-step mode caused minor vibrations → resolved by switching to **half-step mode (microstepping)**.

---

## 4.3 Testing With a Sample

**Silicone oils used (from QUAX GmbH, Germany):**

| No. | Silicone Oil | Viscosity (Pa·s) |
|---|---|---|
| 1 | Silikonöl B 10,000 cSt | 9.65 |
| 2 | Silikonöl B 20,000 cSt | 19.3 |
| 3 | Silikonöl B 30,000 cSt | 29.1 |
| 4 | Silikonöl B 40,000 cSt | 38.8 |
| 5 | Silikonöl B 60,000 cSt | 58.2 |

Tests performed at **50–70 RPM** with immersion depth of **0.05 m**. Results showed RPM dependence → highlighted need for calibration.

---

## 4.4 Calibration

**Stage 1 — Initial Calibration:**

$$\text{Calibrated Viscosity}_1 = \mu \times (0.1176 \times T^{0.464})$$

**Stage 2 — Polynomial Correction (for immersion depth variation):**

$$f(x) = -150334 \cdot T^4 + 27627 \cdot T^3 - 1712.5 \cdot T^2 + 50.227 \cdot T + 0.4264$$

**Final Calibrated Viscosity:**

$$\text{Calibrated Viscosity}_2 = \text{Calibrated Viscosity}_1 \times f(T)$$

Calibration implemented in Python using `numpy.polyfit()` and `numpy.poly1d()`.

---

# Chapter 5: Results

## 5.1 Final Testing Results

Tests at 60, 70, and 80 RPM across immersion depths of 0.06–0.08 m:

| RPM | Depth (m) | Measured (Pa·s) | Required (Pa·s) |
|---|---|---|---|
| 70 | 0.06 | 10.75 | 9.65 |
| 70 | 0.07 | 19.49 | 19.3 |
| 70 | 0.06 | 29.74 | 29.1 |
| 70 | 0.08 | 38.53 | 38.2 |
| 70 | 0.06 | 57.55 | 58.2 |

## 5.2 Error Analysis

| Silicone Oil | Torque (Mean ± Std) | Viscosity (Mean ± Std) |
|---|---|---|
| 9.65 Pa·s | 0.00445 ± 0.00142 Nm | 9.92 ± 2.88 Pa·s |
| 19.3 Pa·s | 0.01396 ± 0.00117 Nm | 19.36 ± 1.35 Pa·s |
| 29.1 Pa·s | 0.02379 ± 0.00215 Nm | 29.11 ± 2.04 Pa·s |
| 38.8 Pa·s | 0.03192 ± 0.00209 Nm | 38.69 ± 1.85 Pa·s |
| 58.2 Pa·s | 0.03343 ± 0.00174 Nm | 57.79 ± 2.21 Pa·s |

Standard deviations were small relative to mean values, indicating **good measurement repeatability**.

System operates best at:
- Rotational speed: **55–85 RPM**
- Immersion depth: **0.05–0.09 m**

---

# Chapter 6: Conclusion and Future Scope

## 6.1 Findings

A functional laboratory prototype for real-time viscosity measurement was successfully developed. The system proved accuracy in viscosity measurement, automatic data collection, and analysis through a Raspberry Pi environment.

Key results:
- Mean measured viscosities matched reference values within acceptable variability
- The infinite cup model successfully eliminated container dimension dependency
- The two-stage polynomial calibration significantly improved reliability across varying immersion depths
- The system is **not suitable for direct molten glass measurement** in its current form (limited to ambient temperatures up to ~70°C)

## 6.2 Future Scope

1. **Improved mechanical alignment** — Precision couplings and enhanced mechanical stability to reduce vibration and misalignment effects
2. **Extended operational range** — Expand RPM range beyond 55–85 and immersion depth beyond 0.05–0.09 m
3. **High-temperature capability** — Replace rod and vessel with high-temperature-resistant materials; upgrade motor and sensor components beyond 70°C limit
4. **PCB integration** — Replace breadboard signal conditioning circuit with a proper PCB designed in Altium
5. **Wall effect modelling** — Compensate for vessel-wall hydrodynamic effects in finite industrial containers
6. **Wireless data logging** — Implement wireless communication for industrial automation compatibility
