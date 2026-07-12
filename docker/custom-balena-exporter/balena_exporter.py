import asyncio
import logging
import os
from contextlib import asynccontextmanager
from pprint import pprint

import requests
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Response
from prometheus_client import CONTENT_TYPE_LATEST, CollectorRegistry, Gauge, generate_latest

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("balena_exporter")

BALENA_API_TOKEN = os.environ.get("BALENA_API_TOKEN", "")

registry = CollectorRegistry()
device_online = Gauge(
    "balena_device_online",
    "Online status of a Balena device (1 = online, 0 = offline)",
    ["device_name"],
    registry=registry,
)

def scrape_devices() -> None:
    """Query the Balena API and update the metrics for each device."""
    response = requests.get(
        "https://api.balena-cloud.com/v7/device?$select=device_name,is_online",
        #params={"$select": "device_name,is_online"},
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {BALENA_API_TOKEN}",
        },
        timeout=30,
    )
    print(response.content)
    response.raise_for_status()

    devices = response.json().get("d", [])
    for device in devices:
        device_online.labels(device_name=device["device_name"]).set(
            1 if device["is_online"] else 0
        )
    logger.info("Updated status for %d devices", len(devices))


async def scrape_loop() -> None:
    """Continuously refresh the device metrics on a fixed interval."""
    while True:
        try:
            await asyncio.to_thread(scrape_devices)
        except Exception:
            logger.exception("Failed to scrape Balena device status")
        await asyncio.sleep(60)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(scrape_loop())
    yield
    task.cancel()


app = FastAPI(lifespan=lifespan)

@app.get("/metrics")
def metrics() -> Response:
    return Response(generate_latest(registry), media_type=CONTENT_TYPE_LATEST)

@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {'status': 'healthy'}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
