from typing import Any, Dict
from django.shortcuts import render
import datetime
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.urls import reverse
from django.contrib import messages
from django.views import generic
from django.shortcuts import get_object_or_404
from users.models import User
from courses.models import Course, Enrollment, Lesson, Chapter
from assignments.models import Assignment
from resources.models import Resource
from .models import CompletedLesson
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction
from .models import Lesson

from .forms import CreateChapterForm, CreateLessonForm, UpdateChapterForm, UpdateLessonForm, UpdateCourseForm

# Create your views here.
class CreateCourse(LoginRequiredMixin, generic.CreateView):
    fields = ('course_name', 'course_description')
    model = Course

    def get(self, request,*args, **kwargs):
        self.object = None
        context_dict = self.get_context_data()
        context_dict.update(user_type=self.request.user.user_type)
        return self.render_to_response(context_dict)
    
    def form_valid(self, form):
        form.instance.teacher = self.request.user
        return super(CreateCourse, self).form_valid(form)
    
class CreateChapterView(LoginRequiredMixin, generic.CreateView):
    form_class = CreateChapterForm
    template_name = 'courses/create_chapter.html'
    success_url = '/all/'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    
    def form_valid(self, form):
        user_object = get_object_or_404(User, username=self.request.user.username)
        form.instance.teacher = user_object
        return super().form_valid(form)

class CreateLessonView(LoginRequiredMixin, generic.CreateView):
    form_class = CreateLessonForm
    template_name = 'courses/create_lesson.html'
    success_url = '/all/'
    
    def get_from_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    def form_valid(self, form):
        user_object = get_object_or_404(User, username=self.request.user.username)
        form.instance.teacher = user_object
        return super().form_valid(form)
    
class CourseDetail(generic.DetailView):
    model = Course
    
    def get_context_data(self,**kwargs):
        course = Course.objects.get(pk=self.kwargs['pk']) 
        
           # Get chapters related to the course
        chapters = Chapter.objects.filter(course=course)

        # chapters_with_lessons = {}
        
        # Create a dictionary to store chapters and their related lessons
        chapters_with_lessons = []
        
        for chapter in chapters:
            # Get lessons related to the chapter
            lessons = Lesson.objects.filter(chapter=chapter)
            chapters_with_lessons.append((chapter, lessons))
            
            
        assignments = Assignment.objects.filter(course=self.kwargs['pk'])
        resources = Resource.objects.filter(course=self.kwargs['pk'])


        # Get the total number of lessons for the course
        total_lessons = Lesson.objects.filter(chapter__course=course).count()
        print("Total Lessons:", total_lessons)
        
        # Get the total number of completed lessons for the user in that course
        if self.request.user.is_authenticated:
            completed_lessons = CompletedLesson.objects.filter(user=self.request.user, lesson__chapter__course=course).count()
            completion_percentage = round((completed_lessons / total_lessons) * 100)
            print("Completed Lessons:", completed_lessons)
            print("Completion Percentage:", completion_percentage)
        else:
            completed_lessons = 0
            
        
        context = super(CourseDetail, self).get_context_data(**kwargs)
        context['assignments'] = assignments
        context['resources'] = resources
        context['chapters_with_lessons'] = chapters_with_lessons 
        # return chapter name and lesson name
        context['total_lessons'] = total_lessons
        context['completed_lessons'] = completed_lessons
        context['course.pk'] = course
        context['completion_percentage'] = completion_percentage
        return context

class ListCourse(generic.ListView):
    model = Course

class EnrollCourse(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('courses:detail', kwargs={'pk':self.kwargs.get('pk')})
    
    def get(self, *args, **kwargs):
        course = get_object_or_404(Course, pk=self.kwargs.get('pk'))

        try:
            Enrollment.objects.create(student=self.request.user, course=course)
        except:
            messages.warning(self.request, 'You are already enrolled in the course.')
        else:
            messages.success(self.request, 'You are now enrolled in the course.')
        return super().get(self.request, *args, **kwargs)

class UnenrollCourse(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('courses:detail', kwargs={'pk':self.kwargs.get('pk')})

    def get(self, *args, **kwargs):

        try:
            enrollment = Enrollment.objects.filter(
                student=self.request.user,
                course__pk=self.kwargs.get('pk')
            ).get()
        except Enrollment.DoesNotExist:
            messages.warning(self.request, 'You are not enrolled in this course.')
        else:
            enrollment.delete()
            messages.success(self.request, 'You have unenrolled from the course.')
        return super().get(self.request, *args, **kwargs)

class UpdateCourseView(LoginRequiredMixin, generic.UpdateView):
    model = Course
    form_class = UpdateCourseForm
    template_name = 'courses/update_course.html'
    success_url = '/all/'  

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')  # Get the value of the 'pk' parameter from kwargs
        return get_object_or_404(Course, pk=pk)  # Retrieve the lesson object using the 'pk'




    
class UpdateChapterView(LoginRequiredMixin, generic.UpdateView):
    model = Chapter
    form = UpdateChapterForm
    template_name = 'courses/update_chapter.html'
    success_url = '/all/'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')  # Get the value of the 'pk' parameter from kwargs
        return get_object_or_404(Chapter, pk=pk)  # Retrieve the lesson object using the 'pk'
    
    def form_valid(self, form):
        if form.instance.course.teacher == self.request.user:
            return super().form_valid(form)
        else:
            form.add_error(None, "You don't have permission to edit this chapter.")
            return self.form_invalid(form)
        
class UpdateLessonView(LoginRequiredMixin, generic.UpdateView):
    model = Lesson
    form = UpdateLessonForm
    template_name = "courses/update_lesson.html"
    success_url = '/all/'
    
    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')  # Get the value of the 'pk' parameter from kwargs
        return get_object_or_404(Lesson, pk=pk)  # Retrieve the lesson object using the 'pk'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        if form.instance.chapter.course.teacher == self.request.user:
            return super().form_valid(form)
        else:
            form.add_error(None, "You don't have permission to edit this lesson.")
            return self.form_invalid(form)


def get_completed_lessons_count(request, course_id):
    if request.user.is_authenticated:
        course = get_object_or_404(Course, pk=course_id)
        print("Course:", course)
        print("Course ID:", course_id)
        completed_lessons_count = request.user.completed_lessons.filter(lesson__chapter__course_id=course_id).count()
        context = {
            'completed_lessons_count': completed_lessons_count,
            'course': course,
        }
        return render(request, 'courses/course_detail.html', context)
    else:
        return JsonResponse({'message': 'Invalid request method.'}, status=400)
    

@require_POST
def mark_lesson_as_read(request, lesson_id):
    try:
        if request.user.is_authenticated and request.method == "POST":
            lesson = get_object_or_404(Lesson, pk=lesson_id)
            
            with transaction.atomic():
                # Check if the lesson is already marked as completed for the user
                completed_lesson, created = CompletedLesson.objects.get_or_create(
                    user=request.user, lesson=lesson
                )

                if created:
                    # A new CompletedLesson instance was created, increment the count
                    request.user.completed_lessons.add(completed_lesson)
                    request.user.save()

                completed_lessons_count = request.user.completed_lessons.count()
                total_lessons = Lesson.objects.count()
                completion_percentage = (completed_lessons_count / total_lessons) * 100
                context = {
                    'completed_lessons_count': completed_lessons_count,
                    'lesson': lesson,
                    'completion_percentage': completion_percentage,
                }
                print("Completed Lesson Count:", completed_lessons_count)
                print("Lesson:", lesson)
                print("Completion Percentage:", completion_percentage)
                return JsonResponse({"message": "Lesson marked as read successfully."})
                # return JsonResponse({"completed_lessons_count": completed_lessons_count})

        else:
            return JsonResponse({"message": "Invalid request method."}, status=400)

    except Exception as e:
        # Log the exception for debugging purposes
        print("Exception:", str(e))
        return JsonResponse({"error": "An error occurred."}, status=500)


# get chapters and lesson titles and render them 
@require_POST
def get_chapter_lesson(request, course_id):
    if request.user.is_authenticated:
        course = get_object_or_404(Course, pk=course_id)
        print("Course:", course)
        print("Course ID:", course_id)
        chapters = Chapter.objects.filter(course=course)
        print("Chapters:", chapters)
        lessons = Lesson.objects.filter(chapter__course=course)
        print("Lessons:", lessons)
        context = {
            'chapters': chapters,
            'lessons': lessons,
            'course': course,
        }
        return render(request, 'courses/course_detail.html', context)
    else:
        return JsonResponse({'message': 'Invalid request method.'}, status=400)