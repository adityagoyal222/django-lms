from django.db import models
from users.models import User
from courses.models import Course, Chapter
from django.urls import reverse
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
import os
from django.conf import settings
from django.contrib.auth.models import User
from django.conf import settings


# Create your models here.
class Assignment(models.Model):
    assignment_name = models.CharField(max_length=200, blank=False)
    assignment_description = models.TextField(blank=False)
    start_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.assignment_name

    def get_absolute_url(self):
        return reverse('assignments:detail', kwargs={'pk': self.pk})

class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, related_name="chapter_quizzes", on_delete=models.CASCADE)
    quiz_title = models.CharField(max_length=200, unique=True)
    quiz_description = models.TextField()

    def __str__(self):
        return self.quiz_title
    
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    completed_quizzes = models.ManyToManyField(Quiz, related_name='completed_by_users', blank=True)

class Question(models.Model):
    quiz_title = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.TextField()

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name="choice",on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class QuizSubmission(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='quiz', on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    submitted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.quiz.quiz_title} - Score: {self.score}"
    class Meta:
        unique_together = ('student', 'quiz')
    
class SubmitAssignment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='assignment', on_delete=models.CASCADE)
    topic = models.CharField(max_length=200, blank=False)
    description = models.TextField(blank=False)
    assignment_file = models.FileField(blank=False, upload_to='assignments')
    submitted_date = models.DateTimeField(default=timezone.now)
    assignment_ques = models.ForeignKey(Assignment, related_name="question", on_delete=models.CASCADE, null=True)
    graded = models.BooleanField(default=False)
    grade = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ]
    )

    def __str__(self):
        return self.topic

    def grade_assignment(self, grade):
        self.grade = grade
        self.graded = True
        self.save()

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.assignment_file.name))
        super().delete(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('assignments:submit_detail', kwargs={'pk': self.pk})
