from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.views.generic.edit import FormMixin
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import os
from django.conf import settings

# from django.contrib import messages
from django.views import generic
from django.shortcuts import get_object_or_404
from users.models import User
from assignments.models import Assignment, SubmitAssignment, Quiz, Question, Choice, QuizSubmission
from assignments.forms import GradeAssignmentForm, CreateAssignmentForm, SubmitAssignmentForm, QuizForm, QuestionForm, ChoiceForm, ChoiceFormSet, SubmitQuizForm
from courses.models import Course

# Create your views here.    
class CreateAssignment(LoginRequiredMixin, generic.CreateView):
    form_class = CreateAssignmentForm
    template_name = 'assignments/create_assignment_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
class CreateQuizView(LoginRequiredMixin, generic.CreateView):
    form_class = QuizForm
    template_name = 'assignments/create_quiz.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user']= self.request.user
        return kwargs
    
    def form_valid(self, form):
        user_object = get_object_or_404(User, username=self.request.user.username)
        form.instance.teacher = user_object
        return super().form_valid(form)
    
    
class CreateQuestionView(LoginRequiredMixin, generic.CreateView):
    model = Question
    template_name = 'assignments/create_question.html'
    form_class = QuestionForm
    
    def get_form_kwargs(self) :
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.quiz = Quiz.objects.get(id=self.kwargs['quiz_id'])
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('create_question', kwargs={'quiz_id': self.kwargs['quiz_id']})

    


# def create_question(request, quiz_id):
#     quiz = Quiz.objects.get(id=quiz_id)
#     if request.method == 'POST':
#         question_form = QuestionForm(request.POST)
#         choice_formset = ChoiceFormSet(request.POST)
#         if question_form.is_valid() and choice_formset.is_valid():
#             question = question_form.save(commit=False)
#             question.quiz = quiz
#             question.save()
#             choice_formset.instance = question
#             choice_formset.save()
#             return redirect('create_question', quiz_id=quiz_id)
#     else:
#         question_form = QuestionForm()
#         choice_formset = ChoiceFormSet()
#     return render(request, 'assignments/create_question.html', {'question_form': question_form, 'choice_formset': choice_formset})
    
    

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

class SubmitAssignmentView(LoginRequiredMixin, generic.CreateView):
    form_class = SubmitAssignmentForm
    template_name = 'assignments/submitassignment_form.html'
    select_related = ('author', 'assignment_ques')
    # success_url = reverse('assignments:submit_detail')

    def get_context_data(self, **kwargs):
        assignments = Assignment.objects.filter(pk=self.request.session.get('assignment'))
        assignment_object = get_object_or_404(assignments)
        context = super(SubmitAssignmentView, self).get_context_data(**kwargs)
        context['duedate'] = assignment_object.due_date
        context['time'] = timezone.now()
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['assignment_id'] = self.request.session.get('assignment')
        kwargs['user'] = self.request.user
        return kwargs
    
class SubmitQuizView(LoginRequiredMixin, generic.CreateView):
    form_class = SubmitQuizForm
    template_name = 'assignments/submitquiz_form.html'
    select_related = ('student', 'quiz')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['quiz'] = Quiz.objects.get(id=self.kwargs['quiz_id'])
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quiz'] = Quiz.objects.get(id=self.kwargs['quiz_id'])
        return context
    
    def form_valid(self, form):
        quiz = Quiz.objects.get(id=self.kwargs['quiz_id'])
        self.object = form.save(commit=False)
        self.object.quiz = quiz
        self.object.student = self.request.user
        
        score = 0
        for question in quiz.question_set.all():
            selected_choices = form.cleaned_data[f'question_{question.id}']
            correct_choices = question.choice_set.filter(is_correct=True)
            if set(selected_choices) == set(correct_choices):
                score += 1
        self.object.score = score
        self.object.save()
        
        return redirect('quiz_results', submission_id=self.object.id)
    
class QuizResultsView(LoginRequiredMixin, generic.TemplateView):
    model = QuizSubmission
    form_class = None  # i'm not using a form for this view
    template_name = 'assignments/quiz_results.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        submission_id = self.kwargs['submission_id']
        submission = get_object_or_404(QuizSubmission, id=submission_id)
        context['submission'] = submission
        return context

class SubmitAssignmentDetail(LoginRequiredMixin, generic.DetailView):
    model = SubmitAssignment
    template_name = 'assignments/submitassignment_detail.html'

    def get_context_data(self, **kwargs):
        submissions = SubmitAssignment.objects.filter(pk=self.kwargs['pk'])
        submissions_object = get_object_or_404(submissions)
        context = super(SubmitAssignmentDetail, self).get_context_data(**kwargs)
        context['submissions'] = submissions_object
        return context


class AssignmentDetail(LoginRequiredMixin, generic.DetailView):
    model = Assignment

    def get_context_data(self, **kwargs):
        course_obj = Course.objects.filter(students=self.request.user.id)
        context = super(AssignmentDetail, self).get_context_data(**kwargs)
        context['course'] = course_obj
        assignment = Assignment.objects.filter(pk=self.kwargs['pk'])
        assignment_object = get_object_or_404(assignment)
        context['duedate'] = assignment_object.due_date
        context['time'] = timezone.now()
        submitassignment = SubmitAssignment.objects.filter(assignment_ques=self.kwargs['pk'])
        context['submitted'] = submitassignment
        self.request.session['assignment'] = self.kwargs['pk']
        # print(self.request.session['assignment'])
        return context



@login_required
def delete_view(request, pk):
    obj = get_object_or_404(SubmitAssignment, pk=pk)
    context = {'submission': obj}
    if request.method == "POST":
        obj.delete()
        return HttpResponseRedirect(reverse("courses:list"))
    return render(request, "assignments/submission_confirm_delete.html", context)

@login_required
def grade_assignment(request, pk):
    submission = get_object_or_404(SubmitAssignment, pk=pk)
    if request.method=="POST":
        form=GradeAssignmentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data.get('grade')
            submission.grade_assignment(data)
            return redirect('assignments:submit_detail', pk=pk)
    else:
        form = GradeAssignmentForm()
    return render(request, 'assignments/grade_form.html', {'pk':pk, 'form':form, 'submissions':submission})