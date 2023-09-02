from django.db import models
# from django.contrib import auth
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth import get_user_model
# from courses.models import Lesson

# Create your models here.
class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'Student'),
        (2, 'Teacher')
    )

    user_type = models.PositiveIntegerField(choices=USER_TYPE_CHOICES, default=1)
    # completed_lessons = models.ManyToManyField('courses.Lesson', through='CompletedLesson', related_name='completed_by', blank=True)
    completed_lessons = models.ManyToManyField('courses.CompletedLesson', related_name='completed_by', blank=True)


    def __str__(self):
        return self.first_name + ' ' + self.last_name
    