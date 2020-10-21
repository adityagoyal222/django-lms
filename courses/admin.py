from django.contrib import admin
from courses import models
# Register your models here.


class GroupMemberInline(admin.TabularInline):
    model = models.Enrollment

admin.site.register(models.Course)
