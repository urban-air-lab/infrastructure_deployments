import os
import time
import json
import paho.mqtt.publish as publish
import random
from dotenv import load_dotenv
import pandas as pd

load_dotenv()


def get_sensor_data():
    return pd.DataFrame(data={
        "temperature": [random.randint(15, 25), random.randint(15, 25), random.randint(15, 25)],
        "humidity": [random.randint(30, 60), random.randint(30, 60), random.randint(30, 60)],
        "timestamp": [time.time(), time.time(), time.time()]
    }, index=[0, 1, 3])


def publish_sensor_data(topic: str) -> None:
    data = get_sensor_data()
    payload = data.to_json()

    publish.single(
        topic=topic,
        payload=payload,
        hostname=os.getenv("MQTT_SERVER"),
        port=int(os.getenv("MQTT_PORT")),
        auth={'username': os.getenv("MQTT_USERNAME"), 'password': os.getenv("MQTT_PASSWORD")}
    )

    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Published to {topic}: {payload}")


if __name__ == "__main__":
    while True:
        publish_sensor_data("sensors/test-data/test")
        time.sleep(60)
