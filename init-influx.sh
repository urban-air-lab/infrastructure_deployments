#!/bin/bash
set -e

influx bucket create -n ual-minute-calibration --org urban-air-lab --token s-0ZETVqp_AT_sWMnRwfSBaG9_vbUvicrWzJJSv_IsCeIg8OGuIQXoTNnbNdRNb_yVKm-PKmZtE246PrQ8e8Rw==
influx bucket create -n ual-minute-measurement --org urban-air-lab --token s-0ZETVqp_AT_sWMnRwfSBaG9_vbUvicrWzJJSv_IsCeIg8OGuIQXoTNnbNdRNb_yVKm-PKmZtE246PrQ8e8Rw==
influx bucket create -n lubw-hour --org urban-air-lab --token s-0ZETVqp_AT_sWMnRwfSBaG9_vbUvicrWzJJSv_IsCeIg8OGuIQXoTNnbNdRNb_yVKm-PKmZtE246PrQ8e8Rw==
influx bucket create -n lubw-minute --org urban-air-lab --token s-0ZETVqp_AT_sWMnRwfSBaG9_vbUvicrWzJJSv_IsCeIg8OGuIQXoTNnbNdRNb_yVKm-PKmZtE246PrQ8e8Rw==