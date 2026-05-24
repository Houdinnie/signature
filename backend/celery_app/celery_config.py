from app.core.config import settings

broker_url = settings.REDIS_URL
result_backend = settings.REDIS_URL.replace("/0", "/1")

task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
timezone = "UTC"
enable_utc = True

worker_prefetch_multiplier = 1
task_acks_late = True
task_reject_on_worker_lost = True

task_routes = {
    "celery_app.tasks.daily_cycle.*": {"queue": "scheduler"},
    "celery_app.tasks.agent_tasks.*": {"queue": "agents"},
    "celery_app.tasks.maintenance.*": {"queue": "maintenance"},
}

result_expires = 86400
