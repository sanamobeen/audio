from .models import Audio
from rest_framework import serializers


class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = ["user", "text", "audio_file", "uploaded_at", "converted_text"]
        read_only_fields = ["user", "audio_file", "uploaded_at", "converted_text"]
