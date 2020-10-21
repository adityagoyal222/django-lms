from django.conf.urls import url
from courses import views

app_name = "courses"

urlpatterns = [
    url(r'^new/$', views.CreateCourse.as_view(), name="create"),
]