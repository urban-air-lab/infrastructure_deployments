#restore command for backup
VOLUME=scripts_backup_influxdb-data

docker volume create "$VOLUME"

docker run --rm \
  -v "$VOLUME":/data \
  -v "$(pwd)/influx_volume.tar.gz":/influx_volume.tar.gz:ro \
  alpine \
  tar -xzf /influx_volume.tar.gz -C /data

docker compose -f docker-compose-backup.yaml up -d influxdb
