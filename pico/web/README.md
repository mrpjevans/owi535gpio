# OWI-535 Robot Arm Web Controller (Pico)

This directory contains code to control the OWI-535 robot arm using a Raspberry Pi Pico via a web interface.

## Features

- Simple web UI for controlling the robot arm's base, shoulder, elbow, wrist, and grip motors.
- STOP button for emergency stop.
- MicroPython backend to drive the motors via GPIO.

## Files

- `index.html`: Web interface for robot control.
- `owi535_web.py`: MicroPython web server for the Pico.
- `owi535.py`: Motor control logic.
- `dcmotor.py`: DC motor driver class.
- `WIFI_CONFIG.py`: WiFi credentials (not included, see below).

## Setup Instructions

### 1. Install MicroPython on the Pico

- Download the latest MicroPython UF2 file for the Raspberry Pi Pico from [micropython.org](https://micropython.org/download/rp2-pico/).
- Hold the BOOTSEL button on the Pico and connect it to your computer via USB.
- Drag and drop the UF2 file onto the Pico's USB drive.

### 2. Install Thonny

- Download and install [Thonny](https://thonny.org/) (available for Windows, macOS, and Linux).

### 3. Connect to the Pico in Thonny

- Open Thonny.
- Go to **Tools > Options > Interpreter**.
- Select **MicroPython (Raspberry Pi Pico)** and choose the correct port.

### 4. Upload the Code

- Copy the following files to the Pico using Thonny's file browser:
  - `index.html`
  - `owi535_web.py`
  - `owi535.py`
  - `dcmotor.py`
- Also copy `WIFI_CONFIG.py` (create from `WIFI_CONFIG.example.py` and fill in your WiFi SSID and password).

### 5. Run the Web Server

- In Thonny, open `owi535_web.py` and click **Run**.
- The Pico will connect to WiFi and print its IP address in the Thonny shell.
- Open a web browser and go to `http://<PICO_IP_ADDRESS>/` to access the robot arm controls.

## Notes

- Ensure your robot arm is wired correctly to the Pico's GPIO pins as specified in `owi535.py`.
- The web UI is designed for local network use only.
- For troubleshooting, check the Thonny shell for error messages.
