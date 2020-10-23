from django.contrib import admin
from assignments.models import Assignment, SubmitAssignment

# Register your models here.
admin.site.register(Assignment)
admin.site.register(SubmitAssignment)