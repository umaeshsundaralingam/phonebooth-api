web: gunicorn --worker-class eventlet -w 1 run:app
worker: celery worker -A run.celery --concurrency=2 --pool=eventlet --loglevel=info
