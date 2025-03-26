from datetime import timedelta

from django.db import models
from django.utils import timezone


class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name="书名")
    author = models.CharField(max_length=255, verbose_name="作者")
    isbn = models.CharField(max_length=13, unique=True, verbose_name="ISBN")
    published_date = models.DateField(verbose_name="出版日期")
    available = models.BooleanField(default=True, verbose_name="是否可借")

    def __str__(self):
        return self.title


class BorrowRecord(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="图书")
    borrower = models.EmailField(verbose_name="借阅者邮箱")
    borrow_date = models.DateField(auto_now_add=True, verbose_name="借阅日期")
    return_date = models.DateField(null=True, blank=True, verbose_name="归还日期")
    due_date = models.DateField(null=True, blank=True, verbose_name="到期日期")
    has_been_reminded = models.BooleanField(default=False, verbose_name="是否已提醒")

    def save(self, *args, **kwargs):
        if not self.id:  # 默认30天
            self.due_date = timezone.now().date() + timedelta(days=30)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.book.title} - {self.borrower}"
