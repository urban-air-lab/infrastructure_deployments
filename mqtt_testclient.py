import time
import json
import paho.mqtt.publish as publish
import random

BROKER = "localhost"
PORT = 1883
TOPIC = "sensors/ual1"


def get_sensor_data():
    return {
        "temperature": random.randint(15, 25),
        "humidity": random.randint(30, 60)
    }


def publish_sensor_data():
    data = get_sensor_data()
    payload = json.dumps(data)

    publish.single(
        topic=TOPIC,
        payload=payload,
        hostname=BROKER,
        port=PORT
    )

    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Published to {TOPIC}: {payload}")


if __name__ == "__main__":
    while True:
        publish_sensor_data()
        time.sleep(60)