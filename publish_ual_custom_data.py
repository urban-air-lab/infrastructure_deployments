import os
import sys
from os import listdir
import pandas as pd
import time
import logging
from dotenv import load_dotenv
from ual.mqtt.mqtt_client import MQTTClient

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

mqtt_client: MQTTClient = MQTTClient(os.getenv("MQTT_SERVER"), int(os.getenv("MQTT_PORT")), os.getenv("MQTT_USERNAME"), os.getenv("MQTT_PASSWORD"))

def publish_ual_custom_csv_data(file_path: str, topic: str) -> None:
    counter: int = 0
    if ".csv" not in file_path:
        logging.warning(f"file is not a .csv file: {file_path}")
    try:
        data: pd.DataFrame = pd.read_csv(f"./{file_path}", sep=';')
        data["Zeitstempel"] = pd.to_datetime(data["Zeitstempel"])
        data["unix_time"] = data["Zeitstempel"].astype('int64') // 10 ** 9
        data["Zeitstempel"] = data["Zeitstempel"].astype(str)

        data: list = data.to_dict(orient="records")
        for element in data[243324:]:
            mqtt_client.publish_data(element, topic)
            counter += 1
            if counter > 1000:
                time.sleep(30) # To not overfill message queue
                counter = 0
                logging.info(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Cool down for 15s")
        logging.info(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Published to {topic}")

    except Exception as e:
        logging.error(f"Could not publish data from file: {file_path}", e)


def publish_ual_custom_log_data(file_path: str, topic: str) -> None:
    counter: int = 0
    files = listdir(file_path)
    for file in files:
        if ".log" not in file:
            logging.warning(f"file is not a .log file: {file}")
            continue
        try:
            data = pd.read_csv(f"./{file_path}/{file}").to_dict(orient="records")
            for element in data[241909:]:
                mqtt_client.publish_data(element, topic)
                counter += 1
                if counter > 10000:
                    time.sleep(40)  # To not overfill message queue
                    counter = 0
                    logging.info(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Cool down for 15s")
            logging.info(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Published to {topic}: {file}")

        except Exception as e:
            logging.error(f"Could not publish data from file {file}", e)



publish_ual_custom_csv_data("./data/CSVExpMersy_klm2025-11-20_14-37.csv", topic="sensors/lubw-minute/DEBW015")