from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core.files import File
from django.http import FileResponse
from googletrans import Translator
import asyncio
import edge_tts
import os

from .serializers import AudioSerializer, SelectLanguageSerializer
from .models import Audio


class TextToSpeechView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SelectLanguageSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        text = serializer.validated_data["text"]
        voice = "en-US-JennyNeural"  # Default voice
        file_name = f"tts_audio_{request.user.id}_{Audio.objects.count() + 1}.mp3"
        file_path = f"media/generated/{file_name}"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        try:
            # Run the async TTS task
            asyncio.run(self.generate_audio_with_edge_tts(text, voice, file_path))

            # Save to model
            audio = Audio(user=request.user, text=text, language="en")
            with open(file_path, "rb") as f:
                audio.audio_file.save(file_name, File(f), save=True)

            return Response({
                "message": "Audio generated successfully",
                "audio_url": request.build_absolute_uri(audio.audio_file.url),
            }, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

    async def generate_audio_with_edge_tts(self, text, voice, output_path):
        communicate = edge_tts.Communicate(text=text, voice=voice)
        await communicate.save(output_path)


class SelectLanguageOfAudio(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SelectLanguageSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        text = serializer.validated_data["text"]
        languages = serializer.validated_data["languages"]
        response_data = []

        translator = Translator()

        for lang in languages:
            try:
                translated = translator.translate(text, dest=lang).text

                voice_map = {
                    "en": "en-US-JennyNeural",
                    "fr": "fr-FR-DeniseNeural",
                    "ur": "ur-PK-AsadNeural",
                    "es": "es-ES-ElviraNeural",
                    "de": "de-DE-KatjaNeural",
                }

                voice = voice_map.get(lang)
                if not voice:
                    raise Exception(f"Voice for language '{lang}' is not configured.")

                filename = f"tts_{lang}_{request.user.id}_{Audio.objects.count() + 1}.mp3"
                filepath = os.path.join("media", "generated", filename)
                os.makedirs(os.path.dirname(filepath), exist_ok=True)

                asyncio.run(edge_tts.Communicate(text=translated, voice=voice).save(filepath))

                # Save in DB
                audio = Audio(user=request.user, text=text, language=lang)
                with open(filepath, "rb") as f:
                    audio.audio_file.save(filename, File(f), save=True)

                audio_url = request.build_absolute_uri(audio.audio_file.url)
                response_data.append({
                    "language": lang,
                    "translated_text": translated,
                    "audio_url": audio_url,
                })

            except Exception as e:
                response_data.append({"language": lang, "error": str(e)})

        return Response(response_data)


class ListOfAudios(APIView):
    def get(self, request):
        user = request.user
        audios = Audio.objects.filter(user=user).order_by("-uploaded_at")
        serializer = AudioSerializer(audios, many=True)
        return Response(serializer.data)
