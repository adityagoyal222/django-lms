from django.db import models
# from django.contrib import auth
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth import get_user_model

# Create your models here.
class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'Student'),
        (2, 'Teacher')
    )

    user_type = models.PositiveIntegerField(choices=USER_TYPE_CHOICES, default=1)
    completed_lessons = models.ManyToManyField('courses.Lesson', through='CompletedLesson', related_name='completed_by', blank=True)


    def __str__(self):
        return self.first_name + ' ' + self.last_name
    

class CompletedLesson(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    lesson = models.ForeignKey('courses.Lesson', on_delete=models.CASCADE)
    completed_date = models.DateTimeField(auto_now_add=True)