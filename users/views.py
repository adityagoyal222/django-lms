from django.shortcuts import render, redirect

from django.urls import reverse_lazy
from django.views.generic import CreateView
from users import forms
from users.models import User, Profile
# from django.views.decorators.csrf import csrf_protect
# from .models import CompletedLesson
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
# from courses.models import Lesson
from allauth.account.views import LoginView, SignupView
from .adapters import CustomAccountAdapter

# Create your views here.
# class SignUp(CreateView):
#     form_class = forms.UserCreateForm
#     success_url = reverse_lazy('users:login')
#     template_name = 'users/signup.html'

#     def form_valid(self, form):
#         response = super().form_valid(form)
#         profile_image = self.request.FILES.get('profile_image')
#         print(profile_image)

#         if profile_image:
#             # Get or create the user's profile
#             profile, created = Profile.objects.get_or_create(user=self.object)

#             # Update the profile picture
#             profile.picture = profile_image
#             profile.save()

#         return response

class CustomSignUpView(SignupView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('users:login')
    template_name = 'account/signup.html'
    account_adapter = CustomAccountAdapter
    def form_valid(self, form):
        self.user = form.try_save(self.request)
        return redirect(self.get_success_url())
class CustomLoginView(LoginView):
    template_name = 'users/login.html'

def Contact(request):
    return render(request, 'users/contact.html')


