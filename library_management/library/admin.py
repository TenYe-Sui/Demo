from django.contrib import admin
from django.utils import timezone

from .models import Book, BorrowRecord


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "isbn", "published_date", "available")


@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = (
        "book",
        "borrower",
        "borrow_date",
        "return_date",
        "due_date",
        "has_been_reminded",
    )

    def save_model(self, request, obj, form, change):
        # 自定义保存逻辑
        # 书籍不能借出不执行
        if not obj.pk and not obj.book.available:
            self.message_user(request, "该书已借出", level="error")
            return
        if not obj.pk:  # 如果是新建对象
            obj.borrow_date = timezone.now()  # 自动设置借阅日期为当前时间
            obj.book.available = False  # 更新书籍状态为不可借
            obj.book.save()
        if obj.return_date:  # 如果设置了还书日期
            obj.book.available = True  # 更新书籍状态为可借
            obj.book.save()
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        # 自定义删除逻辑
        # 更新书籍状态为可借
        obj.book.available = True
        obj.book.save()
        # 调用父类的 delete_model 方法以删除 BorrowRecord 对象
        super().delete_model(request, obj)
