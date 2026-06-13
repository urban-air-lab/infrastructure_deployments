import os
import time
import random

import pandas as pd
from dotenv import load_dotenv
from ual.mqtt.mqtt_client import MQTTClient

load_dotenv()

def get_sensor_data():
    return pd.DataFrame(data={
        "temperature": [random.randint(15, 25), random.randint(15, 25), random.randint(15, 25)],
        "humidity": [random.randint(30, 60), random.randint(30, 60), random.randint(30, 60)],
        "timestamp": [time.time(), time.time(), time.time()],
        "packet_count": 1
    }, index=[0, 1, 3])

if __name__ == "__main__":
    mqtt_client = MQTTClient(os.getenv("MQTT_SERVER"), int(os.getenv("MQTT_PORT")), os.getenv("MQTT_USERNAME"), os.getenv("MQTT_PASSWORD"))
    while True:
        data = get_sensor_data().to_dict(orient="records")
        for element in data:
            mqtt_client.publish_data(element,"sensors/test-data/test" )
        time.sleep(60)
