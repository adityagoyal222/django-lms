from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from users import forms

# Create your views here.
class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/signup.html'