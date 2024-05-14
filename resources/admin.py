from django.contrib import admin
from resources.models import Resource, VideoLesson, VideoProgress
# Register your models here.
admin.site.register(Resource)
admin.site.register(VideoLesson)
admin.site.register(VideoProgress)