# Chapter 1: Introduction

## 1.1 Overview

All primary stages of glass production depend on the fundamental material parameter known as viscosity, which guides glass melting along with refining and mould formation, and annealing steps. The flow behaviour of molten glass emerges from viscosity, which affects product quality control and creates system stability requirements as well as operational energy expenditure.

Industrial operators currently measure viscosity by tracking temperature changes using the Vogel-Fulcher-Tammann (VFT) model. However, this approach ignores multiple interacting elements including mixture composition, recycled components, and batch variations.

Research has proven that silicate and non-silicate melts show non-linear viscosity behaviours that depend on composition, while temperature alone fails to predict these effects. The practice of managing glass quality through temperature controls alone creates potential risks regarding product standards.

The **Technologie Anwender Zentrum (TAZ) Spiegelau** within Technische Hochschule Deggendorf recognised the industry requirement for strong viscosity measurement solutions that could operate in-line. This research investigates design principles and methods that will aid future commercial implementations.

---

## 1.2 Problem Statement

The existing industrial viscosity monitoring system faces issues because it uses temperature as a substitute for direct viscosity measurement. Glass composition, impurities, recycled content, and volatile species cause significant viscosity variations at equivalent temperatures — factors this approach ignores.

The main difficulty exists in obtaining a durable in-line viscometer that functions properly in typical glass manufacturing furnace environments. Commercial viscometers developed for benchtop or MEMS-scale purposes cannot survive in the continuous, high-temperature, corrosive environments of industrial glass plants.

The present work presents a rotational viscometer prototype for laboratory testing with future industrial scalability as its main objective.

---

## 1.3 Objectives

- **Prototype Development:** Develop a laboratory viscometer prototype for accurate measurement of dynamic viscosity of molten glass-like fluids.
- **Method Validation:** Validate torque-based viscosity measurements with silicone oils operated at controlled RPM and depths at ambient temperatures.
- **Data Acquisition System:** Develop a Raspberry Pi system functioning as a data acquisition interface for monitoring process parameters in real-time and permanent data storage.
- **Industrial Relevance:** Use the model as a base to build an advanced viscometer system that can withstand glass furnace environmental conditions.
- **Quality Improvement:** Replace temperature-based quality assessment methods with direct viscosity measurement.

---

## 1.4 Glass Viscosity

Glass-forming liquids need viscosity modelling to gain full comprehension of their behavioural characteristics throughout different temperature ranges.

### 1.4.1 Vogel-Fulcher-Tammann (VFT) Equation

$$\log_{10}\eta(T, x) = \log_{10}\eta_\infty(x) + \frac{A(x)}{T - T_o(x)}$$

First developed by Gordon S. Fulcher in 1925, this model efficiently predicts viscosity across more than ten orders of magnitude through three adjustable parameters: A, B, and T₀.

### 1.4.2 Avramov-Milchev (AM) Model

$$\log\eta(T) = \log\eta_\infty + \frac{\beta}{T^\alpha}$$

Unlike VFT, this model does not create an artificial singularity at T₀ and uses atomic-scale mechanics to describe viscous flow physically.

---

## 1.5 Basic Equations of Viscosity

Viscosity is the resistance of a fluid to a change in shape or movement of neighbouring portions relative to one another.

**Maxwell's Kinetic Theory:**

$$\eta = \frac{f/A}{v/H}$$

Where `f` is the applied force, `A` is the surface area, `v` is velocity, and `H` is the separation height.

**Newton's Law of Viscosity:**

$$\tau = \mu \frac{\partial u}{\partial y}$$

This shows that a higher viscosity or greater surface area increases the force required to maintain the fluid's motion.
