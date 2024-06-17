#!/bin/bash

redis-server &
celery -A make_celery worker --concurrency=4 --loglevel INFO &
python3 ./cleanup_jobs.py &
gunicorn --worker-class gevent --workers 1 "fermo_gui:create_app()" --bind "0.0.0.0:8001"
