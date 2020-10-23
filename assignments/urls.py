from django.conf.urls import url
from assignments import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'assignments'
urlpatterns = [
    url(r'^create/$', views.CreateAssignment.as_view(), name="create"),
    url(r'^detail/(?P<pk>[-\w]+)/$', views.AssignmentDetail.as_view(), name='detail'),
    url(r'^update/(?P<pk>[-\w]+)/$', views.UpdateAssignment.as_view(), name='update'),
    url(r'^delete/(?P<pk>[-\w]+)/$', views.DeleteAssignment.as_view(), name="delete"),
    url(r'^submit/$', views.SubmitAssignmentView.as_view(), name="submit"),
    url(r'^submission/detail/(?P<pk>[-\w]+)/$', views.SubmitAssignmentDetail.as_view(), name="submit_detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
