#!/bin/bash
set -e

sleep 5

influx bucket create -n UALMinuteCalibrationBucket --org some_org --token s-0ZETVqp_AT_sWMnRwfSBaG9_vbUvicrWzJJSv_IsCeIg8OGuIQXoTNnbNdRNb_yVKm-PKmZtE246PrQ8e8Rw==
influx bucket create -n UALMinuteMeasurmentBucket --org some_org --token s-0ZETVqp_AT_sWMnRwfSBaG9_vbUvicrWzJJSv_IsCeIg8OGuIQXoTNnbNdRNb_yVKm-PKmZtE246PrQ8e8Rw==
influx bucket create -n LUBWHourBucket --org some_org --token s-0ZETVqp_AT_sWMnRwfSBaG9_vbUvicrWzJJSv_IsCeIg8OGuIQXoTNnbNdRNb_yVKm-PKmZtE246PrQ8e8Rw==
influx bucket create -n LUBWMinuteBucket --org some_org --token s-0ZETVqp_AT_sWMnRwfSBaG9_vbUvicrWzJJSv_IsCeIg8OGuIQXoTNnbNdRNb_yVKm-PKmZtE246PrQ8e8Rw==