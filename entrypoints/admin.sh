#!/usr/bin/env bash

set -e

if [[ -z "${DJANGO_PROD}" ]]
then
    /usr/local/bin/python manage.py makemigrations
else
    echo "in production env, there is no need to make migrations"
fi

/usr/local/bin/python manage.py migrate
exec /usr/local/bin/gunicorn -b 0.0.0.0:8001 --worker-class gthread --threads 200 tbk.wsgi
