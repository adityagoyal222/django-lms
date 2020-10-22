from django.conf.urls import url
from assignments import views

app_name = 'assignments'
urlpatterns = [
    url(r'^create/$', views.CreateAssignment.as_view(), name="create"),
    url(r'^detail/(?P<pk>[-\w]+)/$', views.AssignmentDetail.as_view(), name='detail'),
]
