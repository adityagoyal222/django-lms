from django.db import models
# from django.contrib import auth
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth import get_user_model
# from courses.models import Lesson
from django.utils.functional import lazy
# Create your models here.


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'Student'),
        (2, 'Teacher')
    )

    user_type = models.PositiveIntegerField(choices=USER_TYPE_CHOICES, default=1)
    # completed_lessons = models.ManyToManyField('courses.Lesson', through='CompletedLesson', related_name='completed_by', blank=True)
    completed_lessons = models.ManyToManyField('courses.CompletedLesson', related_name='completed_by', blank=True, null=True)


    def completed_quizzes(self, course=None):
        if course:
            return self.quiz.filter(quiz__course=course).count()
        return self.quizsubmission_set.all()
    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Profile(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    picture = models.ImageField(upload_to="profile_pictures", null=True, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
    