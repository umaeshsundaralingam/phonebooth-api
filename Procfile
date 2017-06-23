web: gunicorn --worker-class eventlet -w 1 pbapi:core.app
worker: celery worker -A pbapi.core.celery --concurrency=2 --pool=eventlet --loglevel=info
