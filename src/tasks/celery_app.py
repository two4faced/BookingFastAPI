from celery import Celery

from src.config import settings

celery_instance = Celery(
    'tasks',
    broker=settings.CACHE_URL,
    include=[
        'src.tasks.tasks'
    ]
)

celery_instance.conf.beat_schedule = {
    'send_email_beat_schedule': {
        'task': 'bookings_today_checkin',
        'schedule': 5
    }
}