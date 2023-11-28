from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from users import forms
from users.models import User, Profile
# from django.views.decorators.csrf import csrf_protect
# from .models import CompletedLesson
from django.http import JsonResponse
# from courses.models import Lesson

# Create your views here.
class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        profile_image = self.request.FILES.get('profile_image')
        print(profile_image)

        if profile_image:
            # Get or create the user's profile
            profile, created = Profile.objects.get_or_create(user=self.object)

            # Update the profile picture
            profile.picture = profile_image
            profile.save()

        return response

def Contact(request):
    return render(request, 'users/contact.html')


