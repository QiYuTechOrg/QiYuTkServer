#!/usr/bin/env bash

# 开发环境的 运行脚本

set -e

export DJANGO_DEV=1

if [[ -z "${DJANGO_PROD}" ]]
then
    /usr/local/bin/python manage.py makemigrations
else
    echo "in production env, there is no need to make migrations"
fi

/usr/local/bin/python manage.py migrate
exec /usr/local/bin/python manage.py runserver 0.0.0.0:8001
