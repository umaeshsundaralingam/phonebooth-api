from eve import Eve
from app import celery
from app.utils.auth import RolesAuth
from app.utils.tasker import init_celery
from app.utils.events import prepare_documents_for_import_callback
from app.views.tasks import task
from raven.contrib.flask import Sentry
from flask_cors import CORS


def create_app(config=None, environment=None):

    class BlinkerCompatibleEve(Eve):
        """
        Workaround for https://github.com/pyeve/eve/issues/1087
        """
        def __getattr__(self, name):
            if name in {"im_self", "im_func"}:
                raise AttributeError("type object '%s' has no attribute '%s'" %
                                     (self.__class__.__name__, name))
            return super(BlinkerCompatibleEve, self).__getattr__(name)

    app = BlinkerCompatibleEve(
        settings=config.settings,
        auth=RolesAuth
    )

    app.on_pre_POST += prepare_documents_for_import_callback
    app.config.update(config.extra_settings)
    init_celery(app, celery)
    app.register_blueprint(task, url_prefix='/tasks')

    CORS(app)
    
    sentry = Sentry()
    sentry.init_app(app)
    return app
