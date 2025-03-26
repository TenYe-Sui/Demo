from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Book, BorrowRecord
from .serializers import BookSerializer, BorrowRecordSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.borrowrecord_set.exists():
            return Response(
                {"error": "不能销毁正在借阅的图书"}, status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class BorrowRecordViewSet(viewsets.ModelViewSet):
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer

    def create(self, request, *args, **kwargs):
        book_id = request.data.get("book")
        borrower = request.data.get("borrower")

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"error": "图书不存在"}, status=status.HTTP_404_NOT_FOUND)

        if not book.available:
            return Response(
                {"error": "图书不可借，可能已被借出或销毁"}, status=status.HTTP_400_BAD_REQUEST
            )

        # 更新图书状态为不可借
        book.available = False
        book.save()

        # 创建借阅记录
        borrow_record = BorrowRecord.objects.create(book=book, borrower=borrower,)

        # 序列化借阅记录并返回
        serializer = self.get_serializer(borrow_record)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except BorrowRecord.DoesNotExist:
            return Response({"error": "借阅记录不存在"}, status=status.HTTP_404_NOT_FOUND)

        if "return_date" in request.data:
            instance.return_date = request.data["return_date"]
            instance.book.available = True
            instance.book.save()
            instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
