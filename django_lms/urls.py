"""django_lms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from assignments import views
from django_lms import views as project_views
from graphene_django.views import GraphQLView
from graphene_file_upload.django import FileUploadGraphQLView

urlpatterns = [
    url(r'^$', project_views.index, name="home"),
    path('admin/', admin.site.urls),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^courses/', include('courses.urls', namespace="courses")),
    url(r'^assignments/', include('assignments.urls', namespace='assignments')),
    url(r'^resources/', include('resources.urls', namespace="resources")),
    url(r'^user_profile/(?P<pk>[-\w]+)/$',
        project_views.UserProfile.as_view(), name="profile"),
    url('graphql/', FileUploadGraphQLView.as_view(graphiql=True))
]
