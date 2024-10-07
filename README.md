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
|EN1|16|
|IN1|20|
|IN2|21|
|Base|
|IN3|19|
|IN4|13|
|EN2|26|

|L298N 2|GPIO|
|-|-|
|Wrist|
|EN1|14|
|IN1|15|
|IN2|18|
|Elbow|
|IN3|3|
|IN4|4|
|EN2|2|

|L298N 3|GPIO|
|-|-|
|Grip|
|EN1|22|
|IN1|27|
|IN2|17|

Now connect each motor connector on the L298Ns to the relevant motos on the robot arm.

## Software

Activate the local environment

```
ca /path/to/repo
source ./bin/activate
```

Run `test.py`

```
python3 test.py
```

## Control

1-5: Select motor
A: Backward
D: Forward
F: Stop
W: Increase speed
S: Decrease speed

Exit: ctrl+c
