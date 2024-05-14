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
from django.db import transaction, IntegrityError

# from django.contrib import messages
from django.views import generic
from django.shortcuts import get_object_or_404
from users.models import User
from assignments.models import Assignment, SubmitAssignment, Quiz, Question, Choice, QuizSubmission
from assignments.forms import GradeAssignmentForm, CreateAssignmentForm, SubmitAssignmentForm, QuizForm, QuizAnswerForm, QuestionForm, ChoiceForm, SubmitQuizForm
from courses.models import Course
from django.contrib import messages
from django.views.generic.edit import FormView
from django.urls import resolve
from .models import QuizSubmission, CompletedQuiz
from django.urls import reverse
from django.contrib.sessions.models import Session
import requests
from datetime import datetime, timedelta
from django.contrib.sessions.models import Session
from django.utils import timezone

# Create your views here.    
class CreateAssignment(LoginRequiredMixin, generic.CreateView):
    form_class = CreateAssignmentForm
    template_name = 'assignments/create_assignment_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

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

class QuizAnswerView(LoginRequiredMixin, FormView):
    template_name = 'assignments/quiz_answer.html'
    form_class = QuizAnswerForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['quiz_id'] = self.kwargs['quiz_id']
        return kwargs
    
    def get_quiz(self):
        return get_object_or_404(Quiz, pk=self.kwargs['quiz_id'])
    
    def get_course_id(self):
        quiz = self.get_quiz()
        chapter = quiz.chapter  
        course = chapter.course  
        return course.pk

    def calculate_score(self, form):
        score = 0
        for name, value in form.cleaned_data.items():
            if name.startswith('question_') and value is not None:
                question_id = int(name.split('_')[1])
                question = Question.objects.get(pk=question_id)
                correct_choices = question.choice.filter(is_correct=True).values_list('id', flat=True)
                if str(value) in map(str, correct_choices):
                    score += 1
        return score

    def form_valid(self, form):
        quiz = self.get_quiz()
        session_key = self.request.session.session_key
        quiz_session_key = f"quiz_attempts_{self.request.user.id}_{quiz.id}"
        if not session_key:
            self.request.session.save()
            session_key = self.request.session.session_key


        if quiz_session_key not in self.request.session:
            self.request.session[quiz_session_key] = 3  # Initialize attempts for the quiz


        # Check if the user has a quiz attempt session variable
        if 'quiz_attempts' not in self.request.session:
            self.request.session['quiz_attempts'] = 3
            self.request.session['quiz_last_attempt'] = int(timezone.now().timestamp())
            print("Stored last attempt time:", self.request.session['quiz_last_attempt'])



        if 'quiz_attempts' not in self.request.session or 'quiz_last_attempt' not in self.request.session:
            # Handle session expiration or start a new session
            messages.warning(self.request, "Your session has expired. Please log in again.")
            return super().form_invalid(form)
        else:
            last_attempt_time = timezone.datetime.fromtimestamp(self.request.session['quiz_last_attempt'])
            remaining_time_seconds = max(0, (last_attempt_time.astimezone(timezone.get_current_timezone()) + timedelta(hours=24) - timezone.now()).total_seconds())
        # context["remaining_time_seconds"] = remaining_time_seconds


        # Check if the user has attempts remaining
        remaining_attempts = self.request.session.get(quiz_session_key, 0)
        # When retrieving the last_attempt_time
        last_attempt_time = timezone.datetime.fromtimestamp(self.request.session['quiz_last_attempt'])
        print("Retrieved last attempt time:", last_attempt_time)

        cooldown_time = last_attempt_time + timedelta(hours=24)

        if remaining_attempts <= 0 and timezone.now() < cooldown_time.replace(tzinfo=timezone.get_current_timezone()):
            messages.warning(self.request, "You have used all your attempts for this quiz. Please try again after 24 hours.")
            return super().form_invalid(form)

        # Process the quiz submission
        score = self.calculate_score(form)


        
        try:
            # Try to create a new QuizSubmission instance
            with transaction.atomic():
                submission = quiz.quizsubmission_set.create(
                    student=self.request.user,
                    score=score
                )
        except IntegrityError:
            # If IntegrityError occurs, it means the combination (user, quiz) already exists
            # Retrieve the existing instance and update the score
            submission = QuizSubmission.objects.get(student=self.request.user, quiz=quiz)
            submission.score = score
            submission.save()

         # Update the user's quiz attempts in the session
        self.request.session[quiz_session_key] -= 1
        self.request.session['quiz_last_attempt'] = timezone.now().timestamp()


        quiz_id = self.kwargs.get('quiz_id')

        # Get the completed quiz for the current user and quiz, if it exists
        completed_quiz_instance = CompletedQuiz.objects.filter(user=self.request.user, quiz_id=quiz_id).first()




        # Calculate the percentage score
        total_questions = quiz.question_set.count()
        percentage_score = round((score / total_questions) * 100)

        # Check if the score is >= 75%
        total_questions = quiz.question_set.count()
        if percentage_score >= 75:
            # If score is >= 75%, add the quiz ID to completed quizzes
            # If the user has not completed this quiz, add it to completed quizzes
            if completed_quiz_instance is None:
                CompletedQuiz.objects.create(user=self.request.user, quiz_id=quiz_id)
                messages.success(self.request, f"Your score is {percentage_score}%. You have passed this quiz.")
                print("Completed Quizzes:", CompletedQuiz.objects.filter(user=self.request.user).values_list('quiz_id', flat=True))
            else:
                messages.warning(self.request, "You have already completed this quiz.")
        else:
            messages.warning(self.request, f"Your score is {percentage_score}%. You have failed this quiz.")

        
        # Check if user has attempts remaining
        remaining_attempts = self.request.session.get(quiz_session_key, 0)

        if remaining_attempts <= 0 and timezone.now() < cooldown_time.replace(tzinfo=timezone.get_current_timezone()):
            messages.warning(self.request, "You have used all your attempts for this quiz. Please try again after 24 hours.")
        else:
            messages.info(self.request, f"You have {remaining_attempts} attempt(s) remaining for this quiz.")

        
        self.kwargs['submission_id'] = submission.id
        # remaining attempts context
        print("Remaining attempts1:", remaining_attempts)
        # Include quiz_id in the context when calling get_context_data
        # return super().form_valid(form, quiz_id=self.kwargs['quiz_id'])
        quiz_id = self.kwargs.get('quiz_id')
        print("Percentage score:", percentage_score)
        percentage_score = round((score / total_questions) * 100)
        print("Percentage score:", percentage_score)
        print("Quiz ID:", quiz_id)
        print("course ID:", self.get_course_id())
        return super().form_valid(form)

    def get_success_url(self):
        # Access submission_id and quiz_id from self.kwargs
        submission_id = self.kwargs.get('submission_id')
        quiz_id = self.kwargs.get('quiz_id')

        # Use reverse to generate the URL
        return reverse('assignments:quiz_results', args=[submission_id, quiz_id])

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Access quiz_id directly from self.kwargs
        quiz_id = self.kwargs.get('quiz_id')
        context["quiz_id"] = quiz_id
        quiz = self.get_quiz()
        context["quiz_title"] = quiz.quiz_title
        # print("Quiz object:", quiz.__dict__)
        context["course_id"] = self.get_course_id()
        # Check if 'quiz_last_attempt' is present in the session
        if 'quiz_last_attempt' in self.request.session:
            last_attempt_time = timezone.datetime.fromtimestamp(self.request.session['quiz_last_attempt'])
            remaining_time_seconds = max(0, (last_attempt_time.astimezone(timezone.get_current_timezone()) + timedelta(hours=24) - timezone.now()).total_seconds())
            context["remaining_time_seconds"] = remaining_time_seconds
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