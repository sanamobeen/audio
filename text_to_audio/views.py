from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import AudioSerializer,SelectLanguageSerializer
from rest_framework.response import Response
from rest_framework import status
from gtts import gTTS
from django.core.files import File
from .models import Audio
import os
from django.http import FileResponse, Http404
from rest_framework.decorators import api_view
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
# Create your views here.
class TextToSpeechView(APIView):
    def post(self, request):
        serializer = AudioSerializer(data=request.data)
        if serializer.is_valid():
            text = serializer.validated_data["text"]

            file_name = f"tts_audio_{request.user.id}_{Audio.objects.count() + 1}.mp3"
            file_path = f"media/generated/{file_name}"

            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            tts = gTTS(text)
            tts.save(file_path)

            audio = Audio(user=request.user, text=text)
            with open(file_path, "rb") as f:
                audio.audio_file.save(file_name, File(f), save=True)

            return Response(AudioSerializer(audio).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SelectLanguageOfAudio(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SelectLanguageSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        text = serializer.validated_data['text']
        languages = serializer.validated_data['languages']
        response_data = []

        for lang in languages:
            try:
                # Generate audio
                tts = gTTS(text=text, lang=lang)
                filename = f"tts_{lang}_{request.user.id}_{Audio.objects.count()+1}.mp3"
                filepath = f"media/generated/{filename}"
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                tts.save(filepath)

                # Save to Audio model
                audio = Audio(user=request.user, text=text, language=lang)
                with open(filepath, 'rb') as f:
                    audio.audio_file.save(filename, File(f), save=True)

                audio_url = request.build_absolute_uri(audio.audio_file.url)
                response_data.append({
                    'language': lang,
                    'audio_url': audio_url
                })

            except Exception as e:
                response_data.append({
                    'language': lang,
                    'error': str(e)
                })

        return Response(response_data)
class ListOfAudios(APIView):
    def get(self,request):
        user = request.user
        audios = Audio.objects.filter(user=user).order_by('-uploaded_at')
        serializer = AudioSerializer(audios, many=True)
        return Response(serializer.data)
    

