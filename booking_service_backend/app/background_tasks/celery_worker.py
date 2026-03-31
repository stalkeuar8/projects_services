from celery import Celery

from app.settings.config import redis_settings

celery_app = Celery(
    "booking_service_bg_tasks", broker=redis_settings.REDIS_url, backend=redis_settings.REDIS_url, include=["app.background_tasks.tasks"]
)
