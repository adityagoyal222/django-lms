from django.db import models
from users.models import User

from django.urls import reverse
from django.utils import timezone
import os
from django.conf import settings

# Create your models here.
class Resource(models.Model):
    resource_name = models.CharField(max_length=200, blank=False)
    resource_file = models.FileField(blank=False)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)

    def __str__(self):
        return self.resource_name

    def get_absolute_url(self):
        return reverse('courses:list')
    


class VideoLesson(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_lesson_id = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.title


class VideoProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_lesson = models.ForeignKey(VideoLesson, on_delete=models.CASCADE)
    progress = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.video_lesson.title}"