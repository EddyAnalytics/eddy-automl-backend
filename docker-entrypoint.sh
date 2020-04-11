#!/bin/sh
set -e

until mysql --host=$DB_HOST --port=$DB_PORT --user=$DB_USER --password=$DB_PASS --execute="SHOW DATABASES;" $DB_NAME; do
  sleep 1
done

if [ "$1" = 'app' ]; then
    python3 manage.py migrate --no-input
    python3 manage.py collectstatic --no-input
    exec uwsgi --ini uwsgi.ini
fi

if [ "$1" = 'dev' ]; then
    python3 manage.py migrate --no-input
    python3 manage.py collectstatic --no-input
    exec uwsgi --ini uwsgi.dev.ini
fi

exec "$@"
