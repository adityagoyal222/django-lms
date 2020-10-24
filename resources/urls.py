from django.conf.urls import url
from resources import views

app_name = "resources"

urlpatterns = [
    url(r'^create/$', views.CreateResource.as_view(), name="create"),
    url(r'^delete/(?P<pk>[-\w]+)/$', views.delete_view, name='delete')
]
