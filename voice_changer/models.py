from django.db import models

from django.conf import settings


# User = User()


class VoiceChanger(models.Model):
    VOICE_EFFECT_CHOICES = [
        ("robot", "Robot"),
        ("chipmunk", "Chipmunk"),
        ("echo", "Echo"),
        ("deep", "Deep Voice"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    original_audio = models.FileField(upload_to="original_voices/")
    effect_applied = models.CharField(
        max_length=20, choices=VOICE_EFFECT_CHOICES, default="none"
    )
    converted_audio = models.FileField(
        upload_to="voice_changer/converted/", null=True, blank=True
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    converted_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.effect_applied}"


# Create your models here.
