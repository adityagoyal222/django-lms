from django.forms import ModelForm, DateInput, TimeInput, Form, DateTimeInput
from django import forms
from django.shortcuts import get_object_or_404
from assignments.models import SubmitAssignment, Assignment, Quiz, Question, Choice, QuizSubmission
from django.utils import timezone
from courses.models import Course
from users.models import User

class GradeAssignmentForm(ModelForm):
    
    class Meta:
        model = SubmitAssignment
        fields = ['grade']

class CreateAssignmentForm(ModelForm):
    class Meta:
        model = Assignment
        fields = ('assignment_name', 'assignment_description',
                  'due_date', 'course')
        labels = {
            'due_date': 'Due Date (yyyy-mm-dd HH:MM)'
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        user_object = User.objects.filter(username=user.username)
        new_user_object = get_object_or_404(user_object)
        self.fields['course'].queryset = self.fields['course'].queryset.filter(teacher=new_user_object.id)

class SubmitAssignmentForm(ModelForm):
    class Meta:
        model = SubmitAssignment
        fields = ('topic', 'description', 'assignment_file', 'assignment_ques', 'author')
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        assignment = kwargs.pop('assignment_id')
        super().__init__(*args, **kwargs)
        self.fields['assignment_ques'].queryset = self.fields['assignment_ques'].queryset.filter(pk=assignment)
        self.fields['author'].queryset = self.fields['author'].queryset.filter(username=user.username)

class SubmitQuizForm(ModelForm):
    class Meta:
        model = QuizSubmission
        fields = ('quiz', 'student', 'score')
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        quiz = kwargs.pop('quiz_id')
        super().__init__(*args, **kwargs)
        self.fields['quiz'].queryset = self.fields['quiz'].queryset.filter(pk=quiz)
        self.fields['student'].queryset = self.fields['student'].queryset.filter(username=user.username)

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['course','quiz_title', 'quiz_description']
        labels = {
            'course': 'Course Name',
            'quiz_title': 'Quiz Title',
            'quiz_description': 'Quiz Description'
        }
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        user_object = User.objects.filter(username=user.username)
        new_user_object = get_object_or_404(user_object)
        self.fields['course'].queryset = self.fields['course'].queryset.filter(teacher=new_user_object.id)

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['quiz_title', 'question_text']

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['question', 'text', 'is_correct']

ChoiceFormSet = forms.inlineformset_factory(Question, Choice, form=ChoiceForm, extra=4)
