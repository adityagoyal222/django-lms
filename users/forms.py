from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.conf import settings
from .models import Profile

class UserCreateForm(UserCreationForm):
    profile_image = forms.ImageField(required=False, label='Profile Image')

    class Meta:
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'user_type', 'profile_image')
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].label = 'Last Name'
        self.fields['email'].label = "Email Address"
        self.fields['user_type'].label = "Register as:"
        self.fields['profile_image'].label = 'Profile Image'
    def try_save(self, request,commit=True):
        user = super().save(commit=False)
        user.save()
        profile_image = self.cleaned_data.get('profile_image')
        if profile_image:
            profile, created = Profile.objects.get_or_create(user=user)
            profile.picture = profile_image
            profile.save()
        return user