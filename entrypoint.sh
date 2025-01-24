#!/bin/sh

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser --username admin --email admin@gmail.com --user_type basic --password \!ADMIN00admin

exec "$@"