# Chapter 3: Methodology

## 3.1 Design and Development

The rotational viscometer works according to the load generated on the rotating rod in the viscous fluid. The torque generated on the rod is then used to find the viscosity of the glass fluid.

### 3.1.1 Working Principle

A rotating rod is immersed in the sample fluid and rotated at a controlled speed. The torque required to maintain this rotation is directly proportional to the viscosity of the fluid.

**Core Viscosity Equation (Infinite Cup Model):**

$$\mu = \frac{T}{\pi \cdot d^2 \cdot h \cdot \frac{\omega}{2}}$$

**Angular Velocity:**

$$\omega = \frac{2 \cdot \pi \cdot RPM}{60}$$

**Torque from Sensor Frequency:**

$$T = 0.1 \cdot f - 1$$

The infinite cup assumption ensures that variations in container dimensions do not influence viscosity measurements.

---

## 3.2 Schematic Diagram

The system integrates the following components:

1. Stepper Motor
2. Stepper Motor Controller MCC-1-32-48-USB-H
3. Dynamic Torque Sensor (ZHKY2050)
4. Switching Mode Power Supply (Manson HCS-3302)
5. Raspberry Pi 5
6. Signal Conditioning Circuit
7. Graphical User Interface (GUI)

---

## 3.3 Components and Devices

### 3.3.1 Mechanical Parts

- **Motor Bracket:** STEPPERONLINE NEMA 23 bracket for precise shaft alignment
- **Shaft Coupler 1:** 6.35 mm → 8 mm (motor to sensor), aluminum + polyurethane, flexible
- **Shaft Coupler 2:** 8 mm → 22 mm (sensor to rod), absorbs shock and alignment errors
- **Cylindrical Rod:** Ceramic, ø 0.024 m × 0.3 m length, smooth surface for laminar flow

### 3.3.2 Stepper Motor

- **Model:** Phytron ZSH 57/2.200.2,8
- Step angle: **1.8°** (200 steps/rev)
- Holding torque: **1.25 Nm**
- Protection: IP54 (optional IP68)
- Operating temperature: up to +100°C

### 3.3.3 Stepper Motor Controller

- **Model:** Phytron MCC-1-32-48-USB-H
- Current: up to 3.5 A peak
- Step resolution: up to 1/1024 microstepping
- Interface: USB → Raspberry Pi via `/dev/ttyUSB0`

### 3.3.4 Dynamic Rotary Torque Sensor

- **Model:** ZHKY2050
- Range: 0–0.5 Nm
- Accuracy: ±0.1% F.S.
- Output: Push-pull frequency signal, 10 ± 5 kHz at zero torque
- Supply: 24V DC

### 3.3.5 Raspberry Pi 5

Central control unit running **Raspberry Pi OS (64-bit)**. Accessed via:
- Direct (HDMI + keyboard/mouse)
- SSH: `ssh pi@<Raspberry_Pi_IP>`
- Remote GUI via Raspberry Pi Connect

---

## 3.4 Motor Integration

Motor controlled via MINILOG ASCII commands over serial:

| Command | Description |
|---|---|
| `XL+` | Clockwise rotation |
| `XL-` | Counter-clockwise rotation |
| `XS` | Stop movement |
| `XMA` | Enable motor |
| `XMD` | Disable motor |
| `XP45S1` | Full step mode |
| `XP45S2` | Half step mode |
| `XP14S<freq>` | Set frequency (RPM) |

---

## 3.5 Torque Sensor Integration

**Frequency to Torque conversion:**

$$T(Nm) = 0.1 \times f_{khz} - 1$$

**RPM from speed signal:**

$$RPM = \frac{f_{speed}}{60} \times 1000$$

**Signal Conditioning Circuit:**
- Voltage divider reduces 5V → 3.3V for Raspberry Pi GPIO compatibility
- RC band-pass filter removes noise

| Signal | GPIO Pin | Frequency Range | Filter Components |
|---|---|---|---|
| Torque | GPIO 17 | 4–16 kHz | 5nF, 5kΩ, 8kΩ, 2nF |
| Speed | GPIO 21 | 2–32 kHz | 10nF, 1kΩ, 8kΩ, 5nF |

---

## 3.6 Graphical User Interface (GUI)

Built with **PyQt5**. Features:
- Motor direction (CW/CCW), RPM, sample time, immersion depth, rod radius, temperature inputs
- Start/Stop motor and recording buttons
- Live text data display (time, torque, viscosity)
- Real-time **Viscosity vs. Time** plot (updated every second via `QTimer`)
- Export to Excel (`.xlsx`) with auto-generated plots

---

## 3.7 Data Acquisition

Data is sampled every **2 seconds** (default). Each record stores:
- Time (s), Torque (Nm), Viscosity (Pa·s), User RPM, Temperature (°C), Direction, Immersion Depth, Vessel Diameter

Data is auto-saved to timestamped `.xlsx` files. Plots are generated with `matplotlib` and saved as `.png`.
