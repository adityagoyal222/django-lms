from django.conf.urls import url
from assignments import views

app_name = 'assignments'
urlpatterns = [
    url(r'^create/$', views.CreateAssignment.as_view(), name="create"),
    url(r'^detail/(?P<pk>[-\w]+)/$', views.AssignmentDetail.as_view(), name='detail'),
    url(r'^update/(?P<pk>[-\w]+)/$', views.UpdateAssignment.as_view(), name='update'),
    url(r'^delete/(?P<pk>[-\w]+)/$', views.DeleteAssignment.as_view(), name="delete"),
]
