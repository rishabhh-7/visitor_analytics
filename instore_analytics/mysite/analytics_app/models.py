from django.db import models
from django.contrib.auth.models import User

class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.FileField(upload_to='videos/')
    title = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class ProcessedData(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    people_count = models.JSONField()


# Create your models here.
