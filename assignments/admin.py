from django.contrib import admin
from assignments.models import Assignment, SubmitAssignment, Quiz, Question, Choice, QuizSubmission

# Register your models here.
admin.site.register(Assignment)
admin.site.register(SubmitAssignment)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(QuizSubmission)
