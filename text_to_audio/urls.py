from django.shortcuts import render
from django.urls import path
from accounts import views
from .views import TextToSpeechView


urlpatterns = [
    path("text_to_speech/", TextToSpeechView.as_view(), name="Text_To_Speech"),
]
