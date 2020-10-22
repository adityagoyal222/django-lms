from django.conf.urls import url
from courses import views

app_name = "courses"

urlpatterns = [
    url(r'^new/$', views.CreateCourse.as_view(), name="create"),
    url(r'^detail/(?P<pk>[-\w]+)/$', views.CourseDetail.as_view(), name='detail'),
    url(r'^all/', views.ListCourse.as_view(), name="list"),
    url(r'^enroll/(?P<pk>[-\w]+)/$', views.EnrollCourse.as_view(), name='enroll'),
    url(r'^unenroll/(?P<pk>[-\w]+)/$', views.UnenrollCourse.as_view(), name='unenroll'),
]
