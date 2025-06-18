from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AudioUploadViewSet

router = DefaultRouter()
router.register(r"audios", AudioUploadViewSet, basename="audio")

urlpatterns = [
    path("", include(router.urls)),
]
