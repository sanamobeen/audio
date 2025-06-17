from rest_framework import serializers
from .models import VoiceChanger


class VoiceChangerSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoiceChanger
        fields = [
            "user",
            "original_audio",
            "effect_applied",
            "converted_audio",
            "uploaded_at",
            "converted_at",
        ]
        read_only_fields = [
            "user",
            "original_audio",
            "effect_applied",
            "converted_audio",
        ]
