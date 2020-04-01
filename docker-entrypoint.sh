#!/bin/sh
set -e

if [ "$1" = 'app' ]; then
    python3 manage.py migrate --noinput
    exec uwsgi --ini uwsgi.ini
fi
if [ "$1" = 'dev' ]; then
    python3 manage.py migrate --noinput
    python3 manage.py runserver &
fi

exec "$@"
