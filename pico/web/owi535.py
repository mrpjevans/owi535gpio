from machine import Pin, PWM
from time import sleep

from dcmotor import DCMotor

base_pins = [4,3,2]
shoulder_pins = [15,18,14]
grip_pins = [27,22,17]
wrist_pins = [26,19,13]
elbow_pins = [16,20,21]

frequency = 1000
speed = 10

motors = {
    "base": DCMotor(Pin(base_pins[0], Pin.OUT), Pin(base_pins[1], Pin.OUT), PWM(base_pins[2], frequency)),
    "shoulder": DCMotor(Pin(shoulder_pins[0], Pin.OUT), Pin(shoulder_pins[1], Pin.OUT), PWM(shoulder_pins[2], frequency)),
    "grip": DCMotor(Pin(grip_pins[0], Pin.OUT), Pin(grip_pins[1], Pin.OUT), PWM(grip_pins[2], frequency)),
    "wrist": DCMotor(Pin(wrist_pins[0], Pin.OUT), Pin(wrist_pins[1], Pin.OUT), PWM(wrist_pins[2], frequency)),
    "elbow": DCMotor(Pin(elbow_pins[0], Pin.OUT), Pin(elbow_pins[1], Pin.OUT), PWM(elbow_pins[2], frequency))
}

def all_stop():
    motors["base"].stop()
    motors["shoulder"].stop()
    motors["grip"].stop()
    motors["wrist"].stop()
    motors["elbow"].stop()

def move(motor, forward=True, speed=10, duration=0):
    if forward:
        motors[motor].forward(speed)
    else:
        motors[motor].backward(speed)
    if duration > 0:
        sleep(duration)
        all_stop()


