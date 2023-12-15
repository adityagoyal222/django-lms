from django.urls import re_path,path
from django.contrib.auth import views as auth_views

from users import views

app_name = 'users'

urlpatterns = [
    # re_path(r'login/$', auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    # re_path(r'logout/$', auth_views.LogoutView.as_view(), name="logout"),
    # re_path(r'signup/$', views.SignUp.as_view(), name='signup'),
    path('signup/', views.CustomSignUpView.as_view(), name='signup'),
    re_path(r'contact/$', views.Contact, name='contact'),
]