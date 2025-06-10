from machine import Pin, PWM
from time import sleep

from dcmotor import DCMotor

# Pins (Motor 1 , Motor 2, Enable)
base = [2, 3, 1]
shoulder = [7, 8, 9]
elbow = [11, 12, 10]
wrist = [13, 14, 15]
grip = [17, 18, 16]

# Choose the motor to test
motor_pins = base

frequency = 1000
speed = 10

motor = DCMotor(Pin(motor_pins[0], Pin.OUT), Pin(motor_pins[1], Pin.OUT), PWM(motor_pins[2], frequency))

print("Forward")
motor.forward(speed)
sleep(0.5)

print("Backward")
motor.backward(speed)
sleep(0.5)

print("Stop")
motor.stop()

