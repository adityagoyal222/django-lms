from django.contrib import admin
from courses import models
# Register your models here.


class GroupMemberInline(admin.TabularInline):
    model = models.Enrollment

admin.site.register(models.Course)
admin.site.register(models.Chapter)
admin.site.register(models.Lesson)
admin.site.register(models.CompletedLesson)
admin.site.register(models.CompletedCourse)
