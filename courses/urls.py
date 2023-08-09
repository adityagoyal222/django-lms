# from django.conf.urls import url
from django.urls import re_path, path
from courses import views


app_name = "courses"

urlpatterns = [
    re_path(r'^new/$', views.CreateCourse.as_view(), name="create"),
    re_path(r'^detail/(?P<pk>[-\w]+)/$', views.CourseDetail.as_view(), name='detail'),
    re_path(r'^all/', views.ListCourse.as_view(), name="list"),
    re_path(r'^enroll/(?P<pk>[-\w]+)/$', views.EnrollCourse.as_view(), name='enroll'),
    re_path(r'^unenroll/(?P<pk>[-\w]+)/$', views.UnenrollCourse.as_view(), name='unenroll'),
    
]
