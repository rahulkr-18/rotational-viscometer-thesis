# Development of a Laboratory Prototype of a Rotational Viscometer

**Entwicklung eines Laborprototypen eines Rotationsviskometers**

---

<p align="center">
  <img src="https://img.shields.io/badge/Degree-M.Sc.%20Electrical%20Engineering%20%26%20IT-blue" />
  <img src="https://img.shields.io/badge/Institution-Deggendorf%20Institute%20of%20Technology-green" />
  <img src="https://img.shields.io/badge/Year-2025-orange" />
  <img src="https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey" />
</p>

---

## 📄 Abstract

This project developed a laboratory rotational viscometer prototype for determining the viscosity of liquids with relevance to industrial glass applications. The device follows a foundational model toward creating future implementations of real-time in-line viscosity monitors for glass manufacturing.

The system uses a **torque measurement method** through a stepper motor-driven ceramic rod spinning inside test fluids, using dynamic rotary torque sensors. A **Raspberry Pi 5** system enables motor control, data logging, and real-time interface monitoring through a specialised graphical user interface (GUI).

The prototype was validated with silicone oils of viscosities ranging from **5,000 to 60,000 cSt** under different RPM levels and immersion depths. An **infinite cup geometry assumption** ensures measurement consistency independent of the radial distance between the rotating rod and container wall — offering advantages over standard coaxial cylinder technologies.

Experimental results confirmed that the system reliably measures viscosity across a range of silicone oil samples, with the following final accuracy:

| Silicone Oil | Mean Measured (Pa·s) | Reference (Pa·s) | Std Dev |
|---|---|---|---|
| 9.65 Pa·s | 9.92 | 9.65 | ±2.88 |
| 19.3 Pa·s | 19.36 | 19.3 | ±1.35 |
| 29.1 Pa·s | 29.11 | 29.1 | ±2.04 |
| 38.8 Pa·s | 38.69 | 38.8 | ±1.85 |
| 58.2 Pa·s | 57.79 | 58.2 | ±2.21 |

**Keywords:** Viscosity determination · Glass-forming melts · Torque measurement · Stepper motor · Raspberry Pi · Graphical interface monitoring · Infinite cup model · Polynomial calibration

---

## 🧑‍💻 Author

**Rahul Kuravanparambil Rajan**  
Student ID: 12201084  
M.Sc. Electrical Engineering and Information Technology  
[Deggendorf Institute of Technology (DIT)](https://www.th-deg.de), Bavaria, Germany  
Submitted: April 20, 2025

**Supervisor:** Prof. Harald Zimmermann  
**Technical Supervisors:** Roland Stange, Florian Reischl  
**Laboratory:** Technologie Anwender Zentrum (TAZ) Spiegelau

---

## 📁 Repository Structure

```
├── README.md                        # This file
├── LICENSE                          # Creative Commons BY 4.0
├── CITATION.cff                     # Citation metadata
├── thesis.pdf                       # Full thesis (PDF)
├── chapters/
│   ├── 01-introduction.md           # Chapter 1: Introduction
│   ├── 02-literature-background.md  # Chapter 2: Literature Background
│   ├── 03-methodology.md            # Chapter 3: Methodology
│   ├── 04-testing-calibration.md    # Chapter 4: Testing & Calibration
│   ├── 05-results.md                # Chapter 5: Results
│   └── 06-conclusion.md             # Chapter 6: Conclusion & Future Scope
└── code/
    └── rotational_viscometer.py     # Main Python source code (GUI + control)
```

---

## ⚙️ System Overview

### Hardware Components
- **Phytron ZSH 57/2.200.2,8** — 2-phase hybrid stepper motor (1.8° step angle, 1.25 Nm holding torque)
- **Phytron MCC-1-32-48-USB-H** — Programmable stepper motor controller (USB interface)
- **ZHKY2050 Dynamic Rotary Torque Sensor** — 0–0.5 Nm range, ±0.1% F.S. accuracy
- **Raspberry Pi 5** — Central control unit running Raspberry Pi OS (64-bit)
- **Manson HCS-3302 SMPS** — Adjustable DC power supply (1–32V, 15A)
- **Ceramic cylindrical rod** — ø 0.024 m × 0.3 m, thermally resistant

### Software Stack
- **Python 3** with `PyQt5`, `matplotlib`, `pandas`, `gpiozero`, `pyserial`, `openpyxl`
- **Thonny IDE** — For on-device development
- **PyCharm** — For calibration and advanced debugging

### Viscosity Calculation

The core viscosity measurement equation (infinite cup model):

$$\mu = \frac{T}{\pi \cdot d^2 \cdot h \cdot \frac{\omega}{2}}$$

Where:
- `T` = measured torque (Nm)
- `d` = rod diameter (m)
- `h` = immersion depth (m)
- `ω` = angular velocity (rad/s)

A two-stage polynomial calibration corrects for hydrodynamic and geometric variations.

---

## 🚀 How to Run

### Requirements
```bash
pip install PyQt5 matplotlib pandas gpiozero pyserial openpyxl numpy
```

### Launch
```bash
python code/rotational_viscometer.py
```

The GUI will launch and allow you to:
1. Set motor direction (CW/CCW), RPM, sample time, immersion depth, and rod radius
2. Start/stop the motor and recording
3. View real-time viscosity plots
4. Export data to Excel (`.xlsx`) automatically

---

## 📚 Citation

If you use this work in your research, please cite:

```bibtex
@mastersthesis{RajanRahul2025,
  author    = {Rahul Kuravanparambil Rajan},
  title     = {Development of a Laboratory Prototype of a Rotational Viscometer},
  school    = {Deggendorf Institute of Technology},
  year      = {2025},
  address   = {Deggendorf, Bavaria, Germany},
  month     = {April},
  type      = {Master's Thesis},
  note      = {Faculty of Electrical Engineering and Media Technology}
}
```

---

## 📜 License

This work is licensed under a [Creative Commons Attribution 4.0 International License (CC BY 4.0)](LICENSE).

You are free to share and adapt this work for any purpose, provided appropriate credit is given.

---

## 🙏 Acknowledgements

Sincere thanks to **Prof. Harald Zimmermann** for supervision and guidance, **Roland Stange** and **Florian Reischl** for technical support, and all TAZ Spiegelau staff, family, friends, and the academic community at DIT for their continued support.
