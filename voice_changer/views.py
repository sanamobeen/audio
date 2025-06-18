from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.viewsets import ViewSet
from .serializers import AudioSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
import os
import asyncio
import edge_tts
from .utils import apply_voice_effect
from django.http import FileResponse
from .models import Audio


# Create your views here.
class AudioUploadViewSet(ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["post"])
    def upload_audio(self, request):
        serializer = AudioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    def apply_effect(self, request):
        audio_file = request.FILES.get("audio_file")
        effect = request.data.get("effect")  # 'male', 'female', 'kids'

        if not audio_file:
            return Response({"error": "No audio file uploaded."}, status=400)

        if effect not in ["male", "female", "kids"]:
            return Response(
                {"error": "Invalid or missing effect (must be male, female, or kids)."},
                status=400,
            )

        try:
            file_name = f"uploaded_audio_{request.user.id}.mp3"
            file_path = os.path.join("media/generated", file_name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # ✅ Save the uploaded audio file to disk first
            with open(file_path, "wb") as f:
                for chunk in audio_file.chunks():
                    f.write(chunk)

            # ✅ Now pass the actual path string to the function
            effected_path = apply_voice_effect(file_path, effect)

            return FileResponse(
                open(effected_path, "rb"),
                as_attachment=True,
                filename="effected_audio.mp3",
            )

        except Exception as e:
            return Response({"error": str(e)}, status=500)

    @action(detail=True, methods=["delete"])
    def delete_audio(self, request, pk=None):
        try:
            audio = Audio.objects.get(id=pk, user=request.user)

            # Delete the audio file from disk
            if audio.audio_file and os.path.isfile(audio.audio_file.path):
                os.remove(audio.audio_file.path)

            # Delete the record from database
            audio.delete()

            return Response(
                {"message": "Audio deleted successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )

        except Audio.DoesNotExist:
            return Response(
                {"error": "Audio not found or unauthorized."},
                status=status.HTTP_404_NOT_FOUND,
            )
