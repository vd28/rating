#!/bin/sh

while ! nc -z "$DB_HOST" "$DB_PORT"; do sleep 1; done;

python manage.py migrate --no-input
python manage.py collectstatic --no-input --clear
python manage.py compress

exec "$@"
