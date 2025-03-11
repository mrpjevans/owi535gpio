# owi535gpio
Scripts for controlling a OWI-535 robot arm using Raspberry Pi's GPIO. This is a proof-of-concept
for GPIO-based control of a robot arm using H-bridges.

## You Will Need

- Raspberry Pi
- 3 x L298N H-Bridge boards
- OWI 535 Edge Robot Arm
- Jumper cables

## Wire-up

The L298N boards will need their own 12V power supply

Ensure there is a ground cable between the boards and the Raspberry Pi

For each board, wire up to the GPIO as follows:

|L298N 1|GPIO|
|-|-|
|Shoulder|
|EN1|14|
|IN1|15|
|IN2|18|
|Base|
|IN3|4|
|IN4|3|
|EN2|2|

|L298N 2|GPIO|
|-|-|
|Wrist|
|EN1|13|
|IN1|26|
|IN2|19|
|Elbow|
|IN3|16|
|IN4|20|
|EN2|21|

|L298N 3|GPIO|
|-|-|
|Grip|
|EN1|17|
|IN1|27|
|IN2|22|

Now connect each motor connector on the L298Ns to the relevant motors on the robot arm.

## Software

Upload the contents of `/pico` to your Raspberry Pi Pico W.

### Testing and Basic Commands

From a serial prompt:

```
import owi535
owi535.move("base", forward=True, duration=1, speed=10)
```

The base should rotate for one second.

Valid points of articulation are:

- base
- shoulder
- elbow
- wrist
- grip

Alter the values of Forward, Duration (seconds, float supported) and speed to change behaviour. If
duration is 0, the movement will not stop. If speed is 0, the motor will stop.

To stop everything:

```
owi535.all_stop()
```

You can use the `owi535` library to write scripts or interface however you want.

### MQTT Subscriber

You can control the OWI535 using MQTT messages.

- Edit `WIFI_CONFIG.example.py`

- Rename `WIFI_CONFIG.example.py` to `WIFI_CONFIG.py`

- Edit `MQTT_CONFIG.example.py`

- Rename `MQTT_CONFIG.example.py` to `MQTT_CONFIG.py`

- Restart the Pico

If all is well, the Pico will connect to you MQTT broker and start listening for instructions.

### MQTT Publisher

Included are two command line clients for sending commands to the robot arm over MQTT. Make sure their
connection details match the arm's.

These are provided for demonstration only.

#### Typescript

Installation:

```
cd ./mqtt_cli_typescript
npm install
```

Edit the MQTT details in the code (`/src/test.ts`) then rebuild:

```
npm build
```

To run:

```
cd dist
node test.js
```

#### Python

This application requires Python 3.7 or newer and uses asynchronous functionality. The required dependencies are listed in the requirements.txt file included below.

It's best practice to create a virtual environment for your Python projects:

```bash
cd mqtt_client_python
python -m venv venv
source venv/bin/activate
```

Install Dependencies

```bash
pip install -r requirements.txt
```
Open the Python script and modify the broker address if needed:

```python
broker = "mqtt://192.168.1.10"  # Change this to your MQTT broker address
topic = "portable/owi535"       # Change this if using a different topic
```

Running:

```bash
python robot_controller.py
```

## Usage Instructions

Once the application is running, you can control the robot arm using these keyboard commands:

- **Movement Controls:**
  - `q` / `w`: Wrist down / up
  - `a` / `s`: Elbow down / up
  - `z` / `x`: Shoulder down / up
  - `e` / `r`: Grip close / open
  - `c` / `v`: Base counterclockwise / clockwise
  - `Space`: Stop all movement

- **Speed Controls:**
  - `f`: Increase speed (maximum 10)
  - `d`: Decrease speed (minimum 1)

- **Exit:**
  - `Ctrl+C`: Exit the application

## Troubleshooting

1. **Connection Issues:**
   - Verify the MQTT broker address is correct
   - Ensure the broker is running and accessible
   - Check network connectivity

2. **Keyboard Input Not Working:**
   - Make sure the terminal window is in focus
   - Some terminals may require special configuration for raw input mode

3. **Dependencies:**
   - If you encounter module not found errors, verify all dependencies are installed correctly

#### Usage

For each version, start the script and then use these keys to control the arm.

- Q/W - Wrist
- A/S - Elbow
- Z/X - Shoulder
- E/R - Grip
- C/V - Base
- Space - All halt

Ctrl+C will exit
