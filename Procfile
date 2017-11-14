web: gunicorn --worker-class eventlet -w 1 run:app
worker: celery worker -E -A run.celery --concurrency=2 --pool=eventlet --loglevel=info --without-gossip --without-mingle --without-heartbeat

