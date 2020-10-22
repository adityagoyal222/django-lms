from django.shortcuts import render
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
# from django.contrib import messages
from django.views import generic
# from django.shortcuts import get_object_or_404
from users.models import User
from assignments.models import Assignment, SubmitAssignment
from assignments.forms import GradeAssignmentForm, CreateAssignmentForm
from courses.models import Course

# Create your views here.    
class CreateAssignment(LoginRequiredMixin, generic.CreateView):
    form_class = CreateAssignmentForm
    template_name = 'assignments/create_assignment_form.html'
    # success_url = reverse('assignments/list/')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class AssignmentDetail(generic.DetailView):
    model = Assignment

class UpdateAssignment(LoginRequiredMixin, generic.UpdateView):
    model = Assignment
    form_class = CreateAssignmentForm
    template_name = 'assignments/create_assignment_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class DeleteAssignment(LoginRequiredMixin, generic.DeleteView):
    model = Assignment
    success_url = reverse_lazy('courses:list')
