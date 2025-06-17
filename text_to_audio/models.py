from django.db import models
from django.conf import settings

class Audio(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    audio_file = models.FileField(upload_to='generated/') 
    uploaded_at = models.DateTimeField(auto_now_add=True)
    converted_text = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.title} by {self.user.email}"

