#!/bin/sh
set -e

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
