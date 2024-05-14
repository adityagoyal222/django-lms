# from django.conf.urls import url
from django.urls import re_path, include, path
from resources import views

app_name = "resources"

urlpatterns = [
    re_path(r'^create/$', views.CreateResource.as_view(), name="create"),
    re_path(r'^delete/(?P<pk>[-\w]+)/$', views.delete_view, name='delete'),
    path('update_video_progress/', views.update_video_progress, name='update_video_progress'),
    path('video_lesson/', views.video_lesson_view, name='video_lesson'),
    # re_path(r'chatbot/', views.chatbot, name='chatbot')
]
