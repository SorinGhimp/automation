
#!/bin/sh
set -eu

touch /var/log/cron.log
chmod 666 /var/log/cron.log

echo "Starting cron service..."
cron
tail -f /var/log/cron.log
