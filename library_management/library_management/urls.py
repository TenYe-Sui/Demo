from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from library.views import BookViewSet, BorrowRecordViewSet

router = DefaultRouter()
router.register(r"books", BookViewSet)
router.register(r"borrow-records", BorrowRecordViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]
