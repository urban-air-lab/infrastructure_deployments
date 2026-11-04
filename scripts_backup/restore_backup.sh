#restore command for backup
set -e
cd "$(dirname "$0")"

# credentials from the project root .env
ENV_FILE=../.env
if [ ! -f "$ENV_FILE" ]; then
  echo "missing $ENV_FILE"
  exit 1
fi
COMPOSE="docker compose --env-file $ENV_FILE -f docker-compose-backup.yaml"

# restore_volume <volume> <archive>
restore_volume() {
  if [ ! -f "$2" ]; then
    echo "missing $2"
    exit 1
  fi

  docker volume create "$1"

  if [ -n "$(docker run --rm -v "$1":/data alpine ls -A /data)" ]; then
    echo "volume $1 is not empty, skip restore (to restore again: docker volume rm $1)"
    return
  fi

  echo "restore $2 into $1"
  docker run --rm \
    -v "$1":/data \
    -v "$(pwd)/$2":/"$2":ro \
    alpine \
    tar -xzf /"$2" -C /data
}

# influx
restore_volume scripts_backup_influxdb-data timeseries_volume.tar.gz
$COMPOSE up -d influxdb

# mlflow - the MYSQL_* credentials in .env must match production, they are stored in the restored database
restore_volume scripts_backup_dbdata sql_volume.tar.gz
restore_volume scripts_backup_minio_data s3_volume.tar.gz
$COMPOSE up -d --build db rustfs web
