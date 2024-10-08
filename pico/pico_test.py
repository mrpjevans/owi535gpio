from dcmotor import DCMotor
from machine import Pin, PWM
from time import sleep

frequency = 1000

pin1 = Pin(17, Pin.OUT)
pin2 = Pin(18, Pin.OUT)
enable = PWM(Pin(16), frequency)

dc_motor = DCMotor(pin1, pin2, enable)

# Set min duty cycle (15000) and max duty cycle (65535) 
#dc_motor = DCMotor(pin1, pin2, enable, 15000, 65535)

try:
    print('Backwards with speed: 10%')
    dc_motor.backwards(10)
    sleep(3)
    print('Forward with speed: 10%')
    dc_motor.forward(10)
    sleep(3)
    dc_motor.stop()
    
except KeyboardInterrupt:
    print('Keyboard Interrupt')
    dc_motor.stop()
