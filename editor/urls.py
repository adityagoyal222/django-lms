from django.urls import re_path
from editor import views

app_name = "editor"

urlpatterns = [
    re_path(r'^ide/$', views.jdoodle_api_ide, name="ide"),
<<<<<<< HEAD
]
=======
]
>>>>>>> 1f11d46bf158a6134aaa2e8b777432759d714666
