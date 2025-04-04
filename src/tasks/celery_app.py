from celery import Celery
from celery.schedules import crontab

from src.config import settings

celery_instance = Celery(
    main="tasks",
    broker=settings.REDIS_URL,
    include=[
        "src.tasks.celery_tasks",
    ],
    result_backend=settings.REDIS_URL,
)

celery_instance.conf.beat_schedule = {
    "test": {
        "task": "booking_today_checkin",
        "schedule": crontab(minute=0, hour=1),
    }
}
