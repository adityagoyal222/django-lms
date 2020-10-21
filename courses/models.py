from django.db import models
from users.models import User

# Create your models here.
class Course(models.Model):
    course_name = models.CharField(max_length=200)
    course_description = models.TextField()
    teacher = models.ForeignKey(User, related_name="course", on_delete=models.SET_NULL)
    students = models.ManyToManyField(User, on_delete=models.SET_NULL)

    def __str__(self):
        return self.course_name

    class Meta:
        ordering = ['course_name']

class Enrollment(models.Model):
    course = models.ForeignKey(Course, related_name="enrollments",on_delete=models.SET_NULL)
    student = models.ForeignKey(User, related_name="user_courses", on_delete=models.SET_NULL)

    def __str__(self):
        self.student.username

    class Meta:
        unique_together = ('course', 'student')