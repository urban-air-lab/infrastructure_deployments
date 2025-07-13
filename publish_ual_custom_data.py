import os
import sys
from os import listdir
import pandas as pd
import paho.mqtt.publish as publish
import json
import time
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)


def publish_sensor_data(data: pd.DataFrame, topic: str) -> None:
    # TODO: works, but needs refactoring :)
    json_str = data.to_json(orient='records')
    payload = json.loads(json_str)
    payload = json.dumps(payload)

    publish.single(
        topic=topic,
        payload=payload,
        hostname=os.getenv("MQTT_SERVER"),
        port=int(os.getenv("MQTT_PORT")),
        qos=1,
        auth= {'username': os.getenv("MQTT_USERNAME"), 'password': os.getenv("MQTT_PASSWORD")}
    )



def publish_ual_custom_data(file_path: str, topic: str):
    files = listdir(file_path)
    for file in files:
        if ".log" not in file:
            logging.warning(f"file is not a .log file: {file}")
            continue
        try:
            data = pd.read_csv(f"./{file_path}/{file}")
            publish_sensor_data(data, topic)
            logging.info(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Published to {topic}: {file}")
            time.sleep(1)
        except Exception as e:
            logging.error(f"Could not publish data from file {file}", e)



publish_ual_custom_data("./data/ual-1-calibration", topic="sensors/calibration/ual-1")
publish_ual_custom_data("./data/ual-1-measurement", topic="sensors/measurement/ual-1")
publish_ual_custom_data("./data/ual-3-calibration", topic="sensors/calibration/ual-3")
publish_ual_custom_data("./data/ual-3-measurement", topic="sensors/measurement/ual-3")
