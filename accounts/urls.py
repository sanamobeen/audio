from django.shortcuts import render
from django.urls import path
from accounts import views
from .views import SignUpView
from .views import SignInView
from .views import LogOutView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("SignUp/", SignUpView.as_view(), name="SignUp"),
    path("SignIn/", SignInView.as_view(), name="SignIn"),
    path("LogOut/", LogOutView.as_view(), name="LogOut"),
]
