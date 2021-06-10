#!/bin/bash


python /app/check_conn.py --service-name redis --port 6379  --ip redis
python /app/check_conn.py --service-name db --port 5432  --ip db
python /app/check_conn.py --service-name rabbit --port 5672  --ip rabbit


celery -A project worker -l info
