from django.db import models
from users.models import User
from courses.models import Course
from django.urls import reverse

# Create your models here.
class Assignment(models.Model):
    assignment_name = models.CharField(max_length=200)
    assignment_description = models.TextField()
    start_date = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField()
    course = models.ForeignKey(Course, on_delete=models.SET_NULL)

    def __str__(self):
        return self.assignment_name
    # def def get_absolute_url(self):
    #     return reverse('', kwargs={'pk': self.pk})

class SubmitAssignment(models.Model):
    author = models.ForeignKey(User, related_name='assignment', on_delete=models.SET_NULL)
    topic = models.CharField(max_length=200)
    description = models.TextField()
    assignment_file = models.FileField()
    submitted_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.topic