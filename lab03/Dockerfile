
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV TZ=Europe/Chisinau

RUN apt-get update \
    && apt-get install -y --no-install-recommends cron tzdata \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir requests

COPY currency_exchange_rate.py /app/lab03/currency_exchange_rate.py
COPY cronjob.txt /etc/cron.d/exchange-rate
COPY entrypoint.sh /app/entrypoint.sh

RUN mkdir -p /app/data \
    && chmod 0644 /etc/cron.d/exchange-rate \
    && chmod +x /app/entrypoint.sh \
    && touch /var/log/cron.log \
    && chmod 666 /var/log/cron.log

ENTRYPOINT ["/bin/sh", "/app/entrypoint.sh"]