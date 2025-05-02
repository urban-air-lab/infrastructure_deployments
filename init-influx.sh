#!/bin/bash
set -e

influx bucket create -n ual-minute-calibration --org urban-air-lab --token "$DOCKER_INFLUXDB_INIT_ADMIN_TOKEN"
influx bucket create -n ual-minute-measurement --org urban-air-lab --token "$DOCKER_INFLUXDB_INIT_ADMIN_TOKEN"
influx bucket create -n lubw-hour --org urban-air-lab --token "$DOCKER_INFLUXDB_INIT_ADMIN_TOKEN"
influx bucket create -n lubw-minute --org urban-air-lab --token "$DOCKER_INFLUXDB_INIT_ADMIN_TOKEN"