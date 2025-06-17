from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import AudioSerializer
from rest_framework.response import Response
from rest_framework import status
from gtts import gTTS
from django.core.files import File
from .models import Audio
# Create your views here.
class UploadAudioView(APIView):
    def post(self,request):
        serializer = AudioSerializer(data=request.data)
        if serializer.is_valid():
            text = serializer.validated_data['text']
            
            tts = gTTS(text)
            file_name = f"audio_{request.user.id}.mp3"
            file_path = f"media/generated/{file_name}"
            tts.save(file_path)
            
            audio = Audio(user=request.user, text=text)
            with open(file_path, 'rb') as f:
                audio.audio_file.save(file_name, File(f), save=True)

            return Response(AudioSerializer(audio).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)