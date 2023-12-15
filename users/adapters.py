from allauth.account.adapter import DefaultAccountAdapter
from .forms import UserCreateForm

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_signup_form_class(self, request):
        return UserCreateForm