from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

# Create your views here.from rest_framework import viewsets, permissions
from .models import Feedback
from .serializers import FeedbackSerializer
from rest_framework import permissions


class FeedbackViewSet(ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Feedback.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
