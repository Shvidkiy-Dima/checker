#!/bin/bash

sleep 2

python /app/check_conn.py --service-name redis --port 6379  --ip redis
python /app/check_conn.py --service-name db --port 5432  --ip db
python /app/check_conn.py --service-name rabbit --port 5672  --ip rabbit
python /app/check_conn.py --service-name django --port 5000  --ip django

python /app/background_service/notifier/runner.py