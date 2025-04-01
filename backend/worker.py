from celery import Celery, Task
from flask import Flask

def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    # Initialize Celery with broker and backend
    celery_app = Celery(
        app.name,
        broker=app.config.get("CELERY_BROKER_URL", "redis://localhost:6379/0"),
        backend=app.config.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0"),
        task_cls=FlaskTask
    )

    # Load additional Celery settings if `celery_config.py` exists
    celery_app.config_from_object("celery_config", silent=True)

    # Store Celery instance in Flask app
    app.extensions["celery"] = celery_app
    return celery_app
