from django.forms import ModelForm
from courses.models import Course, Lesson, Chapter
from users.models import User
from django.shortcuts import get_object_or_404


class CreateChapterForm(ModelForm):
    class Meta:
        model = Chapter
        fields = ('chapter_name', 'chapter_description', 'course')
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        user_object = User.objects.filter(username = user.username)
        new_user_object = get_object_or_404(user_object)
        self.fields['course'].queryset = self.fields['course'].queryset.filter(teacher = new_user_object.id)

class CreateLessonForm(ModelForm):
    class Meta:
        model = Lesson
        fields = ('lesson_name', 'lesson_content', 'chapter')
        
        def __init__(self, *args, **kwargs):
            user = kwargs.pop('user')
            super().__init__(*args, **kwargs)
            user_object = User.objects.filter(username = user.username)
            new_user_object = get_object_or_404(user_object)
            self.fields['chapter'].queryset = self.fields['chapter'].queryset.filter(course__teacher = new_user_object.id)

class UpdateCourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ('course_name', 'course_description')
    
                
class UpdateChapterForm(ModelForm):
    class Meta:
        model = Chapter
        fields = ('chapter_name', 'chapter_description', 'course')
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        user_object = User.objects.filter(username = user.username)
        new_user_object = get_object_or_404(user_object)
        self.fields['course'].queryset = self.fields['course'].queryset.filter(teacher = new_user_object.id)


class UpdateLessonForm(ModelForm):
    class Meta:
        model = Lesson
        fields = ('lesson_name', 'lesson_content', 'chapter')
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        user_object = User.objects.filter(username = user.username)
        new_user_object = get_object_or_404(user_object)
        self.fields['chapter'].queryset = self.fields['chapter'].queryset.filter(course__teacher = new_user_object.id)