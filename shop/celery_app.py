import os
import time

from celery import Celery
from django.conf import settings
from dotenv import load_dotenv

load_dotenv()

if os.environ.get('DEBUG') == 'True':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings.dev')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings.prod')

app = Celery('shop')
app.config_from_object('django.conf:settings')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()


@app.task()
def debug_task():
    time.sleep(20)
    print('Hello from debug task')
