from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from .models import BorrowRecord


@shared_task
def send_reminder_emails():
    today = timezone.now().date()
    due_date_start = today
    due_date_end = today + timedelta(days=7)

    records = BorrowRecord.objects.filter(
        due_date__range=(due_date_start, due_date_end),
        return_date__isnull=True,
        has_been_reminded=False,
    )
    print(f"Records found: {records}")

    for record in records:
        send_mail(
            "图书借阅提醒",
            f"您借阅的《{record.book.title}》将在7天内到期，请尽快归还。",
            "library@example.com",
            [record.borrower],
            fail_silently=False,
        )
        # 更新 has_been_reminded 字段为 True
        record.has_been_reminded = True
        record.save()
