"""
Rotational Viscometer — Main Control & GUI Application
=======================================================
Author:      Rahul Kuravanparambil Rajan (Student ID: 12201084)
Institution: Deggendorf Institute of Technology
Supervisor:  Prof. Harald Zimmermann
Date:        April 2025

Description:
    Real-time rotational viscometer control system using Raspberry Pi 5.
    Controls a Phytron ZSH stepper motor via MCC-1-32-48-USB-H controller,
    reads torque from ZHKY2050 sensor via GPIO, computes viscosity using
    the infinite cup model, and displays results in a PyQt5 GUI.

Usage:
    python rotational_viscometer.py

Requirements:
    pip install PyQt5 matplotlib pandas gpiozero pyserial openpyxl numpy
"""

import json
import time
import gpiozero
import threading
import math
import pandas as pd
from datetime import datetime
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QTimer
import serial

time.sleep(10)

# ──────────────────────────────────────────────
# Serial Port Configuration for Motor Controller
# ──────────────────────────────────────────────
MCC_PORT = '/dev/ttyUSB0'
BAUD_RATE = 115200

# ──────────────────────────────────────────────
# Global Variables
# ──────────────────────────────────────────────
pulse_count = 0
speed_pulse_count = 0
time_data = []
torque_data = []
viscosity_data = []
sensor_rpm_data = []
temperature_data = []
direction_data = []
recording = False
motor_running = False
SAMPLE_TIME = 2.0        # seconds
user_rpm = 0
json_file_name = None
excel_file_name = None
immersion_depth = []     # metres
rod_radius = 0.012       # metres (default)
user_temperature = 25.0  # degrees Celsius

# ──────────────────────────────────────────────
# GPIO Configuration for Torque & Speed Signals
# ──────────────────────────────────────────────
PWM_GPIO = 27    # Torque signal pin
SPEED_GPIO = 22  # Speed signal pin

pwm_pin = gpiozero.Button(PWM_GPIO)
speed_pin = gpiozero.Button(SPEED_GPIO)


def pulse_callback():
    """Interrupt callback: counts torque pulses."""
    global pulse_count
    pulse_count += 1


def speed_pulse_callback():
    """Interrupt callback: counts speed pulses."""
    global speed_pulse_count
    speed_pulse_count += 1


pwm_pin.when_pressed = pulse_callback
speed_pin.when_pressed = speed_pulse_callback

# ──────────────────────────────────────────────
# Open Serial Port
# ──────────────────────────────────────────────
try:
    ser = serial.Serial(MCC_PORT, BAUD_RATE, timeout=2)
    print("Serial port opened successfully.")
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit(1)


# ──────────────────────────────────────────────
# Motor Control Functions
# ──────────────────────────────────────────────
def send_command(address, command):
    """Send a MINILOG ASCII command to the MCC motor controller."""
    try:
        full_command = f"\x02{address}{command}\x03"
        ser.write(full_command.encode())
        time.sleep(0.5)
    except Exception as e:
        print(f"Error sending command: {e}")


def control_motor(rpm, direction):
    """Start motor at given RPM and direction ('CW' or 'CCW')."""
    global motor_running
    motor_running = True
    send_command("0", "XP45S2")  # Half-step mode
    frequency = rpm_to_frequency(rpm)
    direction_command = "XL+" if direction == "CW" else "XL-"
    send_command("0", f"XP14S{frequency}")
    send_command("0", direction_command)


def stop_motor():
    """Stop the stepper motor."""
    global motor_running
    send_command("0", "XS")
    motor_running = False


def rpm_to_frequency(rpm, steps_per_revolution=400):
    """Convert RPM to step frequency for the motor controller."""
    return int((rpm / 60) * steps_per_revolution)


# ──────────────────────────────────────────────
# Viscosity Calculation (Two-Stage Calibration)
# ──────────────────────────────────────────────
def calculate_torque_and_viscosity(frequency_khz, rpm, h, r):
    """
    Calculate torque (Nm) and calibrated viscosity (Pa·s) from sensor frequency.

    Stage 1 — Infinite cup model:
        mu = T / (pi * d^2 * h * omega/2)

    Stage 1 Calibration:
        Calibrated_1 = mu * (0.1176 * T^-0.464)

    Stage 2 — Polynomial correction for immersion depth variation:
        f(T) = -150334*T^4 + 27627*T^3 - 1712.5*T^2 + 50.227*T + 0.4264
        Calibrated_2 = Calibrated_1 * f(T)
    """
    if frequency_khz > 20:
        return None, None  # Filter out out-of-range frequencies

    raw_torque_Nm = max(0.1 * frequency_khz - 1, 0)
    torque_Nm = raw_torque_Nm
    d = r * 2
    ang = (2 * math.pi * rpm) / 60
    viscosity_1 = torque_Nm / (math.pi * d**2 * h * max(ang / 2, 1e-6))

    if torque_Nm == 0:
        viscosity = 0.0
    else:
        viscosity_2 = viscosity_1 * (0.1176 * torque_Nm**-0.464)
        poly_correction = (
            -150334 * torque_Nm**4
            + 27627  * torque_Nm**3
            - 1712.5 * torque_Nm**2
            + 50.227 * torque_Nm
            + 0.4264
        )
        viscosity = viscosity_2 * poly_correction

    return torque_Nm, viscosity


# ──────────────────────────────────────────────
# Data Storage
# ──────────────────────────────────────────────
def save_sensor_data(data):
    """Append a data record to a timestamped JSON file."""
    global json_file_name
    if json_file_name is None:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        json_file_name = f"sensor_data_{timestamp}.json"
    try:
        with open(json_file_name, "r") as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        existing_data = []
    existing_data.append(data)
    with open(json_file_name, "w") as f:
        json.dump(existing_data, f, indent=4)


def export_to_excel():
    """Export all recorded data to a timestamped Excel file with plots."""
    global excel_file_name
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    excel_file_name = f"sensor_data_{timestamp}.xlsx"
    data = {
        "Time_s": time_data,
        "Torque_Nm": torque_data,
        "Viscosity_Pa_s": viscosity_data,
        "User_RPM": [user_rpm] * len(time_data),
        "Temperature_C": temperature_data,
        "Direction": direction_data,
        "Immersion_depth": immersion_depth,
    }
    df = pd.DataFrame(data)
    with pd.ExcelWriter(excel_file_name, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Sensor Data")
    save_plots(df)


def save_plots(df):
    """Save viscosity vs. time and viscosity vs. torque plots as PNG files."""
    # Viscosity vs. Time
    fig1 = Figure(figsize=(8, 6))
    ax1 = fig1.add_subplot(111)
    ax1.plot(df["Time_s"], df["Viscosity_Pa_s"], label="Viscosity (Pa.s)", marker="o", linestyle="-")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Viscosity (Pa.s)")
    ax1.set_title("Viscosity vs. Time (Detailed)")
    ax1.legend()
    ax1.grid(True)
    fig1.savefig("viscosity_vs_time_detailed.png")

    # Viscosity vs. Torque
    fig2 = Figure(figsize=(8, 6))
    ax2 = fig2.add_subplot(111)
    ax2.plot(df["Torque_Nm"], df["Viscosity_Pa_s"], label="Viscosity (Pa.s)", marker="o", linestyle="-")
    ax2.set_xlabel("Torque (Nm)")
    ax2.set_ylabel("Viscosity (Pa.s)")
    ax2.set_title("Viscosity vs. Torque (Detailed)")
    ax2.legend()
    ax2.grid(True)
    fig2.savefig("viscosity_vs_torque_detailed.png")


# ──────────────────────────────────────────────
# Sensor Data Collection Thread
# ──────────────────────────────────────────────
def collect_sensor_data():
    """
    Background thread: reads GPIO pulse counts every SAMPLE_TIME seconds,
    computes torque and viscosity, and appends to global data lists.
    """
    global pulse_count, speed_pulse_count, time_data, torque_data
    global viscosity_data, sensor_rpm_data, temperature_data, direction_data
    global recording, user_rpm, immersion_depth, rod_radius, user_temperature

    start_time = time.time()
    previous_time = start_time

    while recording:
        current_time = time.time()
        elapsed_time = current_time - previous_time

        if elapsed_time < SAMPLE_TIME:
            continue

        sensor_rpm = speed_pulse_count / elapsed_time
        frequency_khz = (pulse_count / elapsed_time) / 1000.0
        torque, viscosity = calculate_torque_and_viscosity(
            frequency_khz, user_rpm, immersion_depth, rod_radius
        )

        if torque is None or viscosity is None:
            pulse_count = 0
            speed_pulse_count = 0
            previous_time = current_time
            continue

        time_data.append(current_time - start_time)
        torque_data.append(torque)
        viscosity_data.append(viscosity)
        sensor_rpm_data.append(sensor_rpm)
        temperature_data.append(user_temperature)
        direction = "Clockwise" if window.direction.currentText() == "CW" else "Counterclockwise"
        direction_data.append(direction)

        print(
            f"Time: {current_time - start_time:.2f}s | "
            f"Freq: {round(frequency_khz, 3)} kHz | "
            f"Torque: {torque:.3f} Nm | "
            f"Viscosity: {viscosity:.3f} Pa.s"
        )

        pulse_count = 0
        speed_pulse_count = 0
        previous_time = current_time
        time.sleep(SAMPLE_TIME)


# ──────────────────────────────────────────────
# PyQt5 GUI Application
# ──────────────────────────────────────────────
class MotorSensorApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.figure = Figure(figsize=(6, 5))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Rotational Viscometer")
        self.setGeometry(100, 100, 1200, 600)

        main_layout = QtWidgets.QVBoxLayout()

        # Header
        header = QtWidgets.QLabel("ROTATIONAL VISCOMETER")
        header.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Bold))
        header.setAlignment(QtCore.Qt.AlignCenter)
        sub_header = QtWidgets.QLabel("Technologie Anwender Zentrum")
        sub_header.setFont(QtGui.QFont("Arial", 10))
        sub_header.setAlignment(QtCore.Qt.AlignRight)

        # Controls Panel
        controls_layout = QtWidgets.QGridLayout()
        self.direction = QtWidgets.QComboBox()
        self.direction.addItems(["CW", "CCW"])
        self.rpm_input = QtWidgets.QLineEdit()
        self.rpm_input.setPlaceholderText("Enter Motor RPM")
        self.sample_time_input = QtWidgets.QLineEdit()
        self.sample_time_input.setPlaceholderText(f"Sample Time (s) [Default: {SAMPLE_TIME}]")
        self.depth_input = QtWidgets.QLineEdit()
        self.depth_input.setPlaceholderText(f"Immersion Depth (m) [Default: {immersion_depth}]")
        self.radius_input = QtWidgets.QLineEdit()
        self.radius_input.setPlaceholderText(f"Rod Radius (m) [Default: {rod_radius}]")
        self.temperature_input = QtWidgets.QLineEdit()
        self.temperature_input.setPlaceholderText("Enter Temperature (C)")

        self.start_motor_btn = QtWidgets.QPushButton("Start Motor")
        self.stop_motor_btn = QtWidgets.QPushButton("Stop Motor")
        self.start_recording_btn = QtWidgets.QPushButton("Start Recording")
        self.stop_recording_btn = QtWidgets.QPushButton("Stop Recording")
        self.export_btn = QtWidgets.QPushButton("Export Data")
        self.reset_btn = QtWidgets.QPushButton("Reset GUI")
        self.motor_status = QtWidgets.QLabel()
        self.motor_status.setAlignment(QtCore.Qt.AlignCenter)
        self.motor_status.setFont(QtGui.QFont("Arial", 12))
        self.update_motor_status(False)

        rows = [
            ("Direction:", self.direction),
            ("RPM:", self.rpm_input),
            ("Sample Time:", self.sample_time_input),
            ("Immersion Depth:", self.depth_input),
            ("Rod Radius:", self.radius_input),
            ("Temperature (C):", self.temperature_input),
        ]
        for i, (label, widget) in enumerate(rows):
            controls_layout.addWidget(QtWidgets.QLabel(label), i, 0)
            controls_layout.addWidget(widget, i, 1)

        controls_layout.addWidget(self.start_motor_btn, 6, 0)
        controls_layout.addWidget(self.stop_motor_btn, 6, 1)
        controls_layout.addWidget(self.start_recording_btn, 7, 0)
        controls_layout.addWidget(self.stop_recording_btn, 7, 1)
        controls_layout.addWidget(self.export_btn, 8, 0, 1, 2)
        controls_layout.addWidget(self.reset_btn, 9, 0, 1, 2)
        controls_layout.addWidget(QtWidgets.QLabel("Motor Status:"), 10, 0)
        controls_layout.addWidget(self.motor_status, 10, 1)

        data_layout = QtWidgets.QVBoxLayout()
        self.result_display = QtWidgets.QTextEdit()
        self.result_display.setReadOnly(True)
        data_layout.addWidget(self.result_display)

        plot_layout = QtWidgets.QVBoxLayout()
        plot_layout.addWidget(self.canvas)

        top_layout = QtWidgets.QVBoxLayout()
        top_layout.addWidget(header)
        top_layout.addWidget(sub_header)
        bottom_layout = QtWidgets.QHBoxLayout()
        bottom_layout.addLayout(controls_layout)
        bottom_layout.addLayout(data_layout)
        bottom_layout.addLayout(plot_layout)
        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)

        # Connect buttons
        self.start_motor_btn.clicked.connect(self.start_motor)
        self.stop_motor_btn.clicked.connect(self.stop_motor)
        self.start_recording_btn.clicked.connect(self.start_recording)
        self.stop_recording_btn.clicked.connect(self.stop_recording)
        self.export_btn.clicked.connect(export_to_excel)
        self.reset_btn.clicked.connect(self.reset_gui)
        self.setLayout(main_layout)

    def start_motor(self):
        global user_rpm, motor_running
        user_rpm = int(self.rpm_input.text())
        direction = self.direction.currentText()
        threading.Thread(target=control_motor, args=(user_rpm, direction), daemon=True).start()
        motor_running = True
        self.update_motor_status(True)

    def stop_motor(self):
        stop_motor()
        self.update_motor_status(False)

    def start_recording(self):
        global recording, SAMPLE_TIME, immersion_depth, rod_radius, user_temperature
        try:
            if self.sample_time_input.text():
                SAMPLE_TIME = float(self.sample_time_input.text())
            if self.depth_input.text():
                immersion_depth = float(self.depth_input.text())
            if self.radius_input.text():
                rod_radius = float(self.radius_input.text())
            if self.temperature_input.text():
                user_temperature = float(self.temperature_input.text())
        except ValueError:
            print("Invalid input. Using default values.")
        recording = True
        threading.Thread(target=collect_sensor_data, daemon=True).start()
        self.timer.start(1000)

    def stop_recording(self):
        global recording
        recording = False
        self.timer.stop()

    def reset_gui(self):
        global time_data, torque_data, viscosity_data, sensor_rpm_data, temperature_data, direction_data
        for lst in [time_data, torque_data, viscosity_data, sensor_rpm_data, temperature_data, direction_data]:
            lst.clear()
        self.result_display.clear()
        self.ax.clear()
        self.canvas.draw()
        self.update_motor_status(False)
        print("GUI Reset Complete.")

    def update_motor_status(self, running):
        if running:
            self.motor_status.setText("Running")
            self.motor_status.setStyleSheet("color: green;")
        else:
            self.motor_status.setText("Stopped")
            self.motor_status.setStyleSheet("color: red;")

    def update_plot(self):
        """Refresh the real-time Viscosity vs. Time plot."""
        self.ax.clear()
        self.ax.plot(time_data, viscosity_data, label="Viscosity (Pa.s)", marker="o", linestyle="-")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Viscosity (Pa.s)")
        self.ax.set_title("Viscosity vs. Time (Detailed)")
        self.ax.legend()
        self.ax.grid(True)
        self.canvas.draw()
        if torque_data and viscosity_data:
            self.result_display.append(
                f"Time: {time_data[-1]:.2f}s, "
                f"Torque: {torque_data[-1]:.3f} Nm, "
                f"Viscosity: {viscosity_data[-1]:.3f} Pa.s"
            )


# ──────────────────────────────────────────────
# Entry Point
# ──────────────────────────────────────────────
window = None

app = QtWidgets.QApplication([])
window = MotorSensorApp()
window.show()
app.exec_()

ser.close()
