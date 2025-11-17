import json
import os
import paho.mqtt.client as mqtt

# Defaults for quick testing in Wokwi
BROKER = os.getenv("MQTT_BROKER", "broker.hivemq.com")
PORT = int(os.getenv("MQTT_PORT", 1883))
TOPIC = os.getenv("MQTT_TOPIC", "phio/lights")

client = mqtt.Client()
client.connect(BROKER, PORT, 60)

def send_color_rgb(r: int, g: int, b: int):
    """Sends an RGB color JSON payload to the LED strip."""
    payload = json.dumps({"r": int(r), "g": int(g), "b": int(b)})
    client.publish(TOPIC, payload)
