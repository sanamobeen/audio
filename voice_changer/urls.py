from django.shortcuts import render
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from voice_changer import views
from .views import VoiceChangerViewSet

router = DefaultRouter()
router.register(r"voice", VoiceChangerViewSet, basename="voice")
urlpatterns = [
    path("", include(router.urls)),
]
