from django.db import models
from users.models import User
from courses.models import Course
from django.urls import reverse
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Assignment(models.Model):
    assignment_name = models.CharField(max_length=200, blank=False)
    assignment_description = models.TextField(blank=False)
    start_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateField(blank=True)
    due_time = models.TimeField(default="00:00")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.assignment_name

    def get_absolute_url(self):
        return reverse('assignments:detail', kwargs={'pk': self.pk})

class SubmitAssignment(models.Model):
    author = models.ForeignKey(User, related_name='assignment', on_delete=models.CASCADE)
    topic = models.CharField(max_length=200, blank=False)
    description = models.TextField(blank=False)
    assignment_file = models.FileField(blank=False)
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

    def upload(self):
        self.submitted_date = timezone.now()
        self.save()

    def grade_assignment(self, grade):
        self.grade = grade
        self.graded = True
        self.save()
    
    # def get_absolute_url(self):
    #     return reverse('', kwargs={'pk': self.pk})
