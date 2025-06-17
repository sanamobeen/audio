from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import VoiceChangerSerializer
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import viewsets


class VoiceChangerViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"])
    def upload_audio(self, request):
        if "audio_file" not in request.FILES:
            return Response(
                {"error": "No audio file provided."}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = VoiceChangerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
