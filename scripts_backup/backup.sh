SECONDS=0

echo "start backup influx data"
ssh root@91.99.65.22 \
  'docker run --rm \
    -v ual_infrastructure_deployments_influxdb-data:/data:ro \
    alpine \
    tar vczf - -C /data .' \
  > timeseries_volume.tar.gz
echo "finish backup Influx"

echo "start MLFlow - model data"
ssh root@91.99.65.22 \
  'docker run --rm \
    -v ual_infrastructure_deployments_minio_data:/data:ro \
    alpine \
    tar vczf - -C /data .' \
  > s3_volume.tar.gz
echo "finish MLFlow - model data"

echo "start MLFlow - meta data"
ssh root@91.99.65.22 \
  'docker run --rm \
    -v ual_infrastructure_deployments_dbdata:/data:ro \
    alpine \
    tar vczf - -C /data .' \
  > sql_volume.tar.gz
echo "finish MLFlow - meta data"

duration=$SECONDS
echo "$((duration / 60)) minutes and $((duration % 60)) seconds elapsed."


