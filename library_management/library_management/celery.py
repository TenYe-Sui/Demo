# library_management/celery.py
from celery import Celery

app = Celery("library_management", broker="redis://localhost:6379/0")
app.conf.timezone = "Asia/Shanghai"

app.conf.beat_schedule = {
    "send-reminder-emails-every-day": {
        "task": "library.tasks.send_reminder_emails",
        "schedule": 86400.0,  # 每天执行一次
    },
}

app.conf.broker_connection_retry_on_startup = True
