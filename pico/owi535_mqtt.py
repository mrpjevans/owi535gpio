from machine import Pin, PWM
from time import sleep
import network
import json

from umqtt_simple import MQTTClient
import owi535

import WIFI_CONFIG
import MQTT_CONFIG

# Take action when a payload is received
def mqtt_cb(topic, msg):
    global current, speed
    payload = json.loads(msg)
    print("Payload received: ", payload)
    owi535.all_stop()
    speed = 10 if'speed' not in payload else payload['speed']
    direction = False if payload['direction'] is 0 else True
    duration = 0 if 'duration' not in payload else payload['duration']
    owi535.move(payload['motor'], direction, speed, duration)

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
print('Wifi connected')

# Subscribe to MQTT broker
print("Subscribing to MQTT topic")
mqttClient = MQTTClient(MQTT_CONFIG.MQTT_CLIENT_ID, MQTT_CONFIG.MQTT_BROKER, keepalive=60)
mqttClient.set_callback(mqtt_cb)
mqttClient.connect()
mqttClient.subscribe(MQTT_CONFIG.MQTT_SUB_TOPIC)

led = Pin("LED", Pin.OUT)
led.on()

# Process MQTT messages
print("Waiting for MQTT messages")
try:
    while(True):
        mqttClient.wait_msg()
except KeyboardInterrupt:
    print('Keyboard Interrupt')
    owi535.all_stop()
    mqttClient.disconnect()
    wlan.disconnect()

