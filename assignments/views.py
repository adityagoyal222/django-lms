from typing import Any, Dict
from django.forms.models import BaseModelForm
from typing import Any, Dict
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
from django.forms import modelformset_factory

# from django.contrib import messages
from django.views import generic
from django.shortcuts import get_object_or_404
from users.models import User
from assignments.models import Assignment, SubmitAssignment, Quiz, Question, Choice, QuizSubmission
from assignments.forms import GradeAssignmentForm, CreateAssignmentForm, SubmitAssignmentForm, QuizForm, QuizAnswerForm, QuestionForm, ChoiceForm, SubmitQuizForm
from courses.models import Course

# Create your views here.    
class CreateAssignment(LoginRequiredMixin, generic.CreateView):
    form_class = CreateAssignmentForm
    template_name = 'assignments/create_assignment_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

# class CreateQuizView(LoginRequiredMixin, generic.CreateView):
#     model = Quiz
#     form_class = QuizForm
#     template_name = 'assignments/create_quiz.html'

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['user']= self.request.user
#         return kwargs

#     def form_valid(self, form):
#         user_object = get_object_or_404(User, username=self.request.user.username)
#         form.instance.teacher = user_object
#         return super().form_valid(form)

ChoiceFormSet = modelformset_factory(Choice, fields=('text', 'is_correct'), extra=4, max_num=4)

class CreateQuestionView(LoginRequiredMixin, generic.CreateView):
    template_name = 'assignments/create_question.html'
    form_class = QuestionForm
    model = Question
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['choice_formset'] = ChoiceFormSet(queryset=Choice.objects.none())
        context['quiz_id'] = self.kwargs['quiz_id']
        return context
    
    def form_valid(self, form):
        quiz_id = self.kwargs['quiz_id']
        question = form.save(commit=False)
        question.quiz = Quiz.objects.get(id=quiz_id)
        question.save()
        
        choice_formset = ChoiceFormSet(self.request.POST, queryset=Choice.objects.none())
        if choice_formset.is_valid():
            for form in choice_formset.forms:
                choice = form.save(commit=False)
                choice.question = question
                choice.save()
                
        # Check if the "Finish Creating" button was clicked
        if 'finish' in self.request.POST:
            # Redirect to a different view
            return redirect('courses:list')

        return super().form_valid(form)
    def get_success_url(self):
        return reverse('assignments:create_question', kwargs={'quiz_id': self.kwargs['quiz_id']})


class CreateQuestionViewWithoutId(LoginRequiredMixin, generic.CreateView):
    template_name = 'assignments/create_question.html'
    form_class = QuestionForm
    model = Question
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['choice_formset'] = ChoiceFormSet(queryset=Choice.objects.none())
        return context
    
    def form_valid(self, form):
        question = form.save(commit=False)
        question.quiz = Quiz.objects.get(quiz_title=question.quiz_title)
        question.save()
        
        choice_formset = ChoiceFormSet(self.request.POST, queryset=Choice.objects.none())
        if choice_formset.is_valid():
            for form in choice_formset.forms:
                choice = form.save(commit=False)
                choice.question = question
                choice.save()
                
        # Check if the "Finish Creating" button was clicked
        if 'finish' in self.request.POST:
            # Redirect to a different view
            return redirect('courses:list')

        return super().form_valid(form)
    def get_success_url(self):
        return reverse('assignments:create_question_without_id')
    
def create_quiz(request):
    if request.method == 'POST':
        quiz_form = QuizForm(request.POST, user=request.user)
        if quiz_form.is_valid():
            quiz = quiz_form.save(commit = False)
            quiz.teacher = request.user
            #get quiz_id value from form
            quiz_id = quiz_form.cleaned_data.get('id')
            quiz.save()
            if quiz_id:
                quiz = Quiz.objects.get(id=quiz_id)
                print(quiz)
            else:
                print("no quiz")
            return redirect(reverse('assignments:create_question', kwargs={'quiz_id': quiz.id}))
    else:
        quiz_form = QuizForm(user=request.user)
    return render(request, 'assignments/create_quiz.html', {'quiz_form': quiz_form})

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
    
# class SubmitQuizView(LoginRequiredMixin, generic.CreateView):
#     form_class = SubmitQuizForm
#     template_name = 'assignments/submitquiz_form.html'
#     select_related = ('student', 'quiz')
    
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['user'] = self.request.user
#         kwargs['quiz'] = Quiz.objects.get(id=self.kwargs['quiz_id'])
#         return kwargs
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['quiz'] = Quiz.objects.get(id=self.kwargs['quiz_id'])
#         return context
    
#     def form_valid(self, form):
#         quiz = Quiz.objects.get(id=self.kwargs['quiz_id'])
#         self.object = form.save(commit=False)
#         self.object.quiz = quiz
#         self.object.student = self.request.user
        
#         score = 0
#         for question in quiz.question_set.all():
#             selected_choices = form.cleaned_data[f'question_{question.id}']
#             correct_choices = question.choice_set.filter(is_correct=True)
#             if set(selected_choices) == set(correct_choices):
#                 score += 1
#         self.object.score = score
#         self.object.save()
        
#         return redirect('quiz_results', submission_id=self.object.id)
    
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
class QuizAnswerView(LoginRequiredMixin,generic.FormView):
    template_name = 'assignments/quiz_answer.html'
    form_class = QuizAnswerForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['quiz_id'] = self.kwargs['quiz_id']
        return kwargs

    def get_quiz(self):
        return get_object_or_404(Quiz, pk=self.kwargs['quiz_id'])

    def calculate_score(self, form):
        score = 0
        for name, value in form.cleaned_data.items():
            if name.startswith('question_') and value is not None:
                question_id = int(name.split('_')[1])
                question = Question.objects.get(pk=question_id)
                correct_choices = question.choice.filter(is_correct=True).values_list('id', flat=True)
                print(f"Question ID: {question_id}, Selected Choice: {value}, Correct Choices: {list(correct_choices)}")
                if str(value) in map(str, correct_choices):
                    score += 1
                print(f"Current Score: {score}")
        return score    
    
    def form_valid(self, form):
        quiz = self.get_quiz()
        score = self.calculate_score(form)
        submission = quiz.quizsubmission_set.create(
            student=self.request.user,
            score=score
        )
        self.kwargs['submission_id'] = submission.id
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('assignments:quiz_results', args=[self.kwargs['submission_id']])





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