import asyncio
from datetime import datetime, timezone

from celery.schedules import crontab

from app.background_tasks.background_processes import BackgroundProcesses
from app.background_tasks.celery_worker import celery_app


@celery_app.task(name="delete_pending_bookings")
def delete_pending_bookings():
    asyncio.run(BackgroundProcesses.background_bookings_cleaner())

    return f"Pending bookings cleaned. Time: {datetime.now(tz=timezone.utc)}"


@celery_app.task(name="repair_bookings_status")
def repair_bookings_status():
    asyncio.run(BackgroundProcesses.background_status_checker())
    return f"Completed and Checked In bookings statuses changed. Time: {datetime.now(tz=timezone.utc)}"


celery_app.conf.beat_schedule = {
    "check_delete_pending_bookings_15min": {"task": "delete_pending_bookings", "schedule": crontab(minute="*/15")},
    "change_completed_and_checkedin_bookings_status": {"task": "repair_bookings_status", "schedule": crontab(minute=0, hour=4)},
}
