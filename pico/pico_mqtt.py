from machine import Pin, PWM
from time import sleep
import network
import json

from umqtt_simple import MQTTClient
from dcmotor import DCMotor

import WIFI_CONFIG
import MQTT_CONFIG

motor_pins = [[2,3,1], [8,7,9], [11,12,10], [14,13,15], [17,18,16]]
frequency = 1000
current = 0
speed = 10

# Take action when a payload is received
def mqtt_cb(topic, msg):
    global current, speed
    payload = json.loads(msg)
    print("Payload received: ", payload)
    if "motor" in payload:
        if payload['motor'] is not current:
            motors[current].stop()
        current = payload['motor']
    if "speed" in payload:
        speed = payload['speed']
        if speed is 0:
            motors[current].stop()
    if "direction" in payload:
        if payload['direction'] is 0:
            motors[current].forward(speed)
        else:
            motors[current].backward(speed)

# Set up motor instances
motors = []
for motor_pin in motor_pins:
    motors.append(DCMotor(Pin(motor_pin[0], Pin.OUT), Pin(motor_pin[1], Pin.OUT), PWM(motor_pin[2], frequency)))

# Connect to wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_CONFIG.SSID, WIFI_CONFIG.PSK)
retry_count = 0
while wlan.isconnected() == False:
    print('Waiting for wifi connection...')
    retry_count += 1
    if retry_count > 10:
        print("Giving up")
        break
    sleep(1)

# Subscribe to MQTT broker
print("Subscribing to MQTT topic")
mqttClient = MQTTClient(MQTT_CONFIG.MQTT_CLIENT_ID, MQTT_CONFIG.MQTT_BROKER, keepalive=60)
mqttClient.set_callback(mqtt_cb)
mqttClient.connect()
mqttClient.subscribe(MQTT_CONFIG.MQTT_SUB_TOPIC)

# Process MQTT messages
print("Waiting for MQTT messages")
try:
    while(True):
        mqttClient.wait_msg()
except KeyboardInterrupt:
    print('Keyboard Interrupt')
    motors[current].stop()
