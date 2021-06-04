#!/bin/bash

python /app/manage.py collectstatic --noinput
python /app/manage.py dockersuperuser
cd /app

daphne -b 0.0.0.0 -p 5000 project.asgi:application
