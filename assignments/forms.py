from django.forms import ModelForm, DateInput, TimeInput
from django.shortcuts import get_object_or_404
from assignments.models import SubmitAssignment, Assignment
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
                  'due_date', 'due_time', 'course')
        widgets = {
            'due_date': DateInput(format=('%d/%m/%Y'), attrs={'class': 'form-control', 'placeholder': 'Select a date', 'type': 'date'}),
            'due_time': TimeInput(format=('%H:%M'),),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        user_object = User.objects.filter(username=user.username)
        new_user_object = get_object_or_404(user_object)
        self.fields['course'].queryset = self.fields['course'].queryset.filter(teacher=new_user_object.id)

# class SubmitAssignmentForm(ModelForm):
#     class Meta:
#         model = SubmitAssignment
#         fields = ('topic', 'description', 'assignment_file')
        
#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user')
#         super().__init__(*args, **kwargs)
#         user_object = User.objects.filter(username=user.username)
#         new_user_object = get_object_or_404(user_object)
#         self.fields['course'].queryset = self.fields['course'].queryset.filter(teacher=new_user_object.id)
