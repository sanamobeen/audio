from django.db import models
from django.conf import settings


class Audio(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="voice_changed_files",
    )
    audio_file = models.FileField(upload_to="audios/originals/")
    effected_file = models.FileField(
        upload_to="audios/effected/", null=True, blank=True
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.audio_file.name}"
