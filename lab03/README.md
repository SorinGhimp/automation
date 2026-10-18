# Laboratory Work No. 3 — Cron and Docker

## Objective

Automate the execution of the currency exchange rate Python script using cron in a Docker container.

## Project structure

- `currency_exchange_rate.py` — retrieves exchange-rate data.
- `cronjob` — defines daily and weekly scheduled tasks.
- `entrypoint.sh` — prepares the log file and starts cron.
- `Dockerfile` — installs dependencies and builds the container image.
- `docker-compose.yml` — builds and starts the container.
- `README.md` — project documentation.

## Scheduled tasks

- Every day at 06:00: retrieve the MDL to EUR rate for the previous day.
- Every Friday at 17:00: retrieve the MDL to USD rate for the previous week.

The timezone is set to `Europe/Chisinau`.

## Build and run

Run the following command from this directory:

```bash
docker compose up --build -d
```

Check the container:

```bash
docker compose ps
```

## Check logs

Display the cron output:

```bash
docker compose exec currency-cron cat /var/log/cron.log
```

Follow the log in real time:

```bash
docker compose exec currency-cron tail -f /var/log/cron.log
```

View container logs:

```bash
docker compose logs -f
```

## Stop the container

```bash
docker compose down
```

## Notes

The API service must be available at the configured API URL. The Python script must accept the currency codes and date arguments supplied by cron. Verify that the API supports the requested historical dates.

## Conclusion

This laboratory demonstrates scheduled Python execution using cron and containerization with Docker.
