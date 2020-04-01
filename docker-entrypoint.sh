#!/bin/sh
set -e

if [ "$1" = 'app' ]; then
    python3 manage.py migrate --noinput
    exec uwsgi --ini uwsgi.ini
fi

exec "$@"
