from django.db import models
from django.urls import reverse
from users.models import User

# Create your models here.
class Course(models.Model):
    course_name = models.CharField(max_length=200)
    course_description = models.TextField()
    teacher = models.ForeignKey(User, related_name="course", on_delete=models.CASCADE)
    students = models.ManyToManyField(User, through='Enrollment', related_name="student_course")

    def __str__(self):
        return self.course_name

    def get_absolute_url(self):
        return reverse('courses:detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['course_name']

class Chapter(models.Model):
    chapter_name = models.CharField(max_length=200)
    chapter_description = models.TextField()
    course = models.ForeignKey(Course, related_name="chapters", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.chapter_name
    class Meta:
        ordering = ['chapter_name']

class Lesson(models.Model):
    lesson_name = models.CharField(max_length=200)
    lesson_content = models.TextField(
        'Lesson Content',
        max_length=10000,
        help_text='Enter the course content in Markdown format.',
    )
    chapter = models.ForeignKey(Chapter, related_name="lessons", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.lesson_name
    class Meta:
        ordering = ['lesson_name']
        
class Enrollment(models.Model):
    course = models.ForeignKey(Course, related_name="enrollments",on_delete=models.CASCADE)
    student = models.ForeignKey(User, related_name="user_courses", on_delete=models.CASCADE)

    def __str__(self):
        self.student.username

    class Meta:
        unique_together = ('course', 'student')