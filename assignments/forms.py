from django.forms import ModelForm
from assignments.models import SubmitAssignment

class GradeAssignmentForm(ModelForm):
    
    class Meta:
        model = SubmitAssignment
        fields = ['grade']