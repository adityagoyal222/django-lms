from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from users import forms
# from django.views.decorators.csrf import csrf_protect
# from .models import CompletedLesson
from django.http import JsonResponse
# from courses.models import Lesson

# Create your views here.
class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/signup.html'


# @csrf_protect
# def complete_lesson(request):
#     if request.method == 'POST':
#         lesson_id = request.POST.get('lesson_id')
#         user = request.user
#         try:
#             lesson = Lesson.objects.get(pk=lesson_id)
#             CompletedLesson.objects.get_or_create(user=user, lesson=lesson)
#             return JsonResponse({'message': 'Lesson completed.'}, status=200)
#         except Lesson.DoesNotExist:
#             return JsonResponse({'message': 'Lesson not found.'}, status=404)
#     return JsonResponse({'message': 'Invalid request method.'}, status=400)