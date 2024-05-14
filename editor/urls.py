from django.urls import re_path
from editor import views

app_name = "editor"

urlpatterns = [
    re_path(r'^ide/$', views.jdoodle_api_ide, name="jdoodle_api_ide"),
]

