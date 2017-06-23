from celery import Celery

def make_celery(app):
    """
    This function creates a new Celery object, configures it with the broker from
    the application config, updates the rest of the Celery config from the Flask
    config and then creates a subclass of the task that wraps the task execution
    in an application context.
    """
    celery = Celery(app.import_name,
                    backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.confg)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery
