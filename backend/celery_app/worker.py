from celery import Celery

app = Celery("signature")
app.config_from_object("celery_app.celery_config")
app.autodiscover_tasks(["celery_app.tasks"])
