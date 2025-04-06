import paho.mqtt.publish as publish
import json

data = {
    "temperature": 23.5,
    "humidity": 50
}

publish.single(
    topic="sensors/ual1",
    payload=json.dumps(data),
    hostname="localhost",
    port=1883
)