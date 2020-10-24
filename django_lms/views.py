from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from courses.models import Course
from django.shortcuts import render

class UserProfile(LoginRequiredMixin, generic.ListView):
    model = Course
    template_name = 'user_profile.html'

def index(request):
    return render(request, 'index.html')