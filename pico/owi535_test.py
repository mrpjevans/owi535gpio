from machine import Pin, PWM
from time import sleep

from dcmotor import DCMotor

#
# Uncomment the motor_pins for the motor you want to test
#

# Base
motor_pins = [4,3,2]

# Shoulder
#motor_pins = [15,18,14]

# Grip
#motor_pins = [27,22,17]

# Wrist
#motor_pins = [26,19,13]

# Elbow
#motor_pins = [16,20,21]

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

