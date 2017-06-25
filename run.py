from app import celery
from app import config
from app.factory import create_app
from app.utils.tasker import make_celery

app = create_app(config=config)
make_celery(app, celery)
