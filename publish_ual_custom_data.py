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
        port=int(os.getenv("MQTT_PORT"))
    )


attributes = ["CO",
              "NO",
              "NO2",
              "O3",
              "pm1",
              "pm25",
              "pm10",
              "RAW_ADC_CO_W",
              "RAW_ADC_CO_A",
              "RAW_ADC_NO_W",
              "RAW_ADC_NO_A",
              "RAW_ADC_NO2_W",
              "RAW_ADC_NO2_A",
              "RAW_ADC_O3_W",
              "RAW_ADC_O3_A",
              "sht_humid",
              "sht_temp",
              "timestamp"]

files = listdir("./data")

for file in files:
    if ".log" not in file:
        logging.warning(f"file is not a .log file: {file}")
        continue
    try:
        topic = "sensors/measurement/ual-1"
        data = pd.read_csv(f"./data/{file}")
        publish_sensor_data(data[attributes], topic)
        logging.info(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Published to {topic}: {file}")
    except Exception as e:
        logging.error(f"Could not publish data from file {file}", e)
