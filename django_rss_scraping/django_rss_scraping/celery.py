from __future__ import absolute_import, unicode_literals
from celery import Celery

from celery.schedules import crontab # scheduler
import os

#default django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rss_scraping.settings')

app = Celery('django_rss_scraping')
app.conf.timezone = 'UTC'
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()



app.conf.beat_sheduler = {
	# executes every minute
	'scraping-task-ne-minute':{
	'task':'tasks.googlenews_rss',
	'shedule':crontab()
	}
}