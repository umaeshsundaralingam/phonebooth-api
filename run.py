from app import celery
from app import config
from app.factory import create_app
from app.utils.tasker import init_celery

app = create_app(config=config)
init_celery(app, celery)
