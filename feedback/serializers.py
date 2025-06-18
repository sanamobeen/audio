from rest_framework import serializers
from .models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ["id", "user", "message", "created_at"]
        read_only_fields = ["id", "user", "created_at"]
