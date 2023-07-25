# from django.conf.urls import url
from django.urls import re_path, include
from resources import views

app_name = "resources"

urlpatterns = [
    re_path(r'^create/$', views.CreateResource.as_view(), name="create"),
    re_path(r'^delete/(?P<pk>[-\w]+)/$', views.delete_view, name='delete')
]
