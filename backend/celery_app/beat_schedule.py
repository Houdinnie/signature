from celery.schedules import crontab
from app.core.config import settings

beat_schedule = {
    "morning-cycle": {
        "task": "celery_app.tasks.daily_cycle.run_morning_cycle",
        "schedule": crontab(hour=6, minute=0),
        "options": {"queue": "scheduler"},
    },
    "evening-cycle": {
        "task": "celery_app.tasks.daily_cycle.run_evening_cycle",
        "schedule": crontab(hour=20, minute=0),
        "options": {"queue": "scheduler"},
    },
    "social-sweep": {
        "task": "celery_app.tasks.agent_tasks.run_social_sweep",
        "schedule": crontab(minute=0, hour="*/2"),
        "options": {"queue": "agents"},
    },
    "email-sweep": {
        "task": "celery_app.tasks.agent_tasks.run_email_sweep",
        "schedule": crontab(minute=30, hour="*/3"),
        "options": {"queue": "agents"},
    },
    "finance-sync": {
        "task": "celery_app.tasks.agent_tasks.run_finance_sync",
        "schedule": crontab(minute=0, hour="*/6"),
        "options": {"queue": "agents"},
    },
}
