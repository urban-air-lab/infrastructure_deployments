import os
import time
import random
from dotenv import load_dotenv
from ual.mqtt.mqtt_client import MQTTClient

load_dotenv()

def get_sensor_data() -> dict:
    return {
        "temperature": random.randint(15, 25),
        "humidity": random.randint(30, 60),
        "timestamp": time.time()
    }

if __name__ == "__main__":
    mqtt_client = MQTTClient(os.getenv("MQTT_SERVER"), int(os.getenv("MQTT_PORT")), os.getenv("MQTT_USERNAME"), os.getenv("MQTT_PASSWORD"))
    while True:
        data = get_sensor_data()
        mqtt_client.publish_data(data,"sensors/test-data/test" )
        time.sleep(60)
