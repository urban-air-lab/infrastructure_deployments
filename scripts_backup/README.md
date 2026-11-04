# scripts_backup

Scripts to back up the Docker volumes of the production server and to check the backups locally.

## backup.sh – download the volumes

Connects to the server via SSH (`root@91.99.65.22`) and downloads the following Docker volumes as archives:

| Volume                                        | Archive                    | Content                  |
|-----------------------------------------------|----------------------------|--------------------------|
| `ual_infrastructure_deployments_influxdb-data` | `timeseries_volume.tar.gz` | InfluxDB time series     |
| `ual_infrastructure_deployments_minio_data`    | `s3_volume.tar.gz`         | MLflow models/artifacts  |
| `ual_infrastructure_deployments_dbdata`        | `sql_volume.tar.gz`        | MLflow metadata (MySQL)  |

The archives are written to the current directory, so run it from this directory:

```sh
cd scripts_backup
./backup.sh
```

## restore_backup.sh – check the backups

Restores the archives into local Docker volumes and starts containers from `docker-compose-backup.yaml`, so the backups can be checked:

- InfluxDB: http://localhost:8086
- MLflow: http://localhost:5000 (username = dummy, password = dummy12345678)

```sh
./restore_backup.sh
```

**The archives have to be in this directory.** If you want to check backups you downloaded again, put them here with the file names from the table above.

The credentials are read from the `.env` in the project root.

### Notes

- Volumes that already contain data are skipped. To check a newer backup, remove the old volume first, e.g.
  `docker volume rm scripts_backup_influxdb-data`.
- Users and passwords come from the backup, not from the compose file:
  - InfluxDB: login with the production user (`ual_influx`).
  - MySQL: the `MYSQL_*` values in `.env` have to match production.
  - MLflow: only the admin user from `configs/mlflow/credentials` exists, the MLflow user list is not part of the backup.
