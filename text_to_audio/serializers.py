from .models import Audio
from rest_framework import serializers
class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model= Audio
        fields = '__all__'
        Fields = ["title","uploaded_at","converted_at"]
        