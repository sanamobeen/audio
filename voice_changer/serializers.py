from rest_framework import serializers
from .models import Audio


class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = ["id", "user", "audio_file", "effected_file", "uploaded_at"]
        read_only_fields = ["id", "user", "effected_file", "uploaded_at"]
