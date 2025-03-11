import json
import asyncio
import sys
import tty
import termios
import paho.mqtt.client as mqtt
from paho.mqtt.client import MQTTv5

broker = "mqtt://192.168.1.10"
topic = "portable/owi535"
default_speed = 5

# Dictionary mapping keys to motor and direction values
key_map = {
    'q': ["wrist", 0],
    'w': ["wrist", 1],
    'a': ["elbow", 0],
    's': ["elbow", 1],
    'z': ["shoulder", 0],
    'x': ["shoulder", 1],
    'e': ["grip", 0],
    'r': ["grip", 1],
    'c': ["base", 0],
    'v': ["base", 1],
}

# Set up non-blocking keyboard input
def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

# Connect to MQTT broker
async def connect_mqtt():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=MQTTv5)
    
    # Extract hostname from broker URL
    hostname = broker.replace("mqtt://", "")
    
    # Connect to the broker
    await asyncio.to_thread(client.connect, hostname)
    return client

async def main():
    global default_speed
    
    # Connect to MQTT broker
    client = await connect_mqtt()
    
    print(f"Publishing to {topic} on {broker}")
    print("Ready")
    
    while True:
        key = get_key()
        
        # Exit on Ctrl+C
        if key == '\x03':
            break
            
        print(f"Pressed: '{key}'")
        
        payload = {
            "motor": "base",
            "speed": 0,
            "direction": 0,
            "duration": 0
        }
        
        if key == " ":
            payload["speed"] = 0
        elif key == "f" and default_speed < 10:
            default_speed += 1
            payload["speed"] = default_speed
        elif key == "d" and default_speed > 1:
            default_speed -= 1
            payload["speed"] = default_speed
        elif key in key_map:
            payload["motor"] = key_map[key][0]
            payload["direction"] = key_map[key][1]
            payload["speed"] = default_speed
        else:
            print("That doesn't do anything")
            continue
        
        string_payload = json.dumps(payload)
        print(f"Publishing: {string_payload}")
        
        # Publish message
        await asyncio.to_thread(client.publish, topic, string_payload)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(0)