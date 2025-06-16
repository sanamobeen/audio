from django.shortcuts import render
from django.urls import path
from accounts import views
from .views import TextToSpeechView,ListOfAudios,SelectLanguageOfAudio


urlpatterns = [
    path("text_to_speech/", TextToSpeechView.as_view(), name="Text_To_Speech"),
    path("select_language_of_audio/", SelectLanguageOfAudio.as_view(), name="select_language_of_audio"),
    path("list_of_audios/", ListOfAudios.as_view(), name="List_Of_Audios"),

]
