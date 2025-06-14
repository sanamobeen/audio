from django.shortcuts import render
from django.urls import path
from accounts import views
from .views import UploadAudioView



urlpatterns = [

    path("Upload_Audio/", UploadAudioView.as_view(), name="Upload_Audio"),
  

]
