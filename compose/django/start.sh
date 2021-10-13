#!/bin/bash


python /app/check_conn.py --service-name redis --port 6379  --ip redis
python /app/check_conn.py --service-name db --port 5432  --ip db
python /app/check_conn.py --service-name rabbit --port 5672  --ip rabbit

python /app/manage.py makemigrations
python /app/manage.py migrate --fake-initial
python /app/manage.py collectstatic --noinput
python /app/manage.py dockersuperuser
cd /app

daphne -b 0.0.0.0 -p 5000 project.asgi:application


