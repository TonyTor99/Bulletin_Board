import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BulletinBoard.settings')

app = Celery('BulletinBoard')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.beat_schedule = {
    'clear_board_every_minute': {
        'task': 'board.tasks.weekly_send',
        'schedule': crontab(hour='12', minute='0', day_of_week='monday'),
    },
}

app.autodiscover_tasks()

