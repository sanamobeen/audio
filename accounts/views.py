from django.shortcuts import render

# Create your views here.

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import SignUpSerializer, SignInSerializer, LogoutSerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


class SignUpView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializers = SignUpSerializer(data=request.data)
        if serializers.is_valid():
            user = serializers.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "User signed up successfully! ",
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class SignInView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SignInSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")

            user = authenticate(request, username=email, password=password)

            if user is not None:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                return JsonResponse(
                    {
                        "msg": "User signed in successfully!",
                        "tokens": {"refresh": str(refresh), "access": access_token},
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Invalid email or password!"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogOutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT
        )
