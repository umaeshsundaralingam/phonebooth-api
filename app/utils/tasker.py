def init_celery(app, celery):
    """
    This function creates a new Celery object, configures it with the broker from
    the application config, updates the rest of the Celery config from the Flask
    config and then creates a subclass of the task that wraps the task execution
    in an application context.
    """
    client = Client(app.config['SENTRY_DSN'])
    register_logger_signal(client)
    register_signal(client)

    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask

