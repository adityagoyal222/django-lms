from typing import Any, Dict
from django.shortcuts import render, redirect,HttpResponseRedirect
import datetime
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.urls import reverse
from django.contrib import messages
from django.views import generic
from django.shortcuts import get_object_or_404
from users.models import User
from courses.models import Course, Enrollment, Lesson, Chapter, CompletedCourse, Certificate
from assignments.models import Assignment, Quiz
from resources.models import Resource, VideoLesson, VideoProgress
from .models import CompletedLesson
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction
import datetime
import calendar
from .cert_request import send_certificate_request, verify_certificate
import json
from django.views import View
from django.http import JsonResponse
from .models import CompletedLesson, Course
from .forms import CreateChapterForm, CreateLessonForm, UpdateChapterForm, UpdateLessonForm, UpdateCourseForm
import mammoth
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
import io
from django.db import IntegrityError
from django.http import Http404
from assignments import models
from assignments.models import QuizSubmission, CompletedQuiz
from django.db.models import Count

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
    model = Chapter
    form_class = CreateChapterForm
    template_name = 'courses/create_chapter.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    
    def form_valid(self, form):
        user_object = get_object_or_404(User, username=self.request.user.username)
        form.instance.teacher = user_object
        return super().form_valid(form)
    def get_success_url(self):
        url = reverse('courses:list')
        return url

class CreateLessonView(LoginRequiredMixin, generic.CreateView):
    form_class = CreateLessonForm
    template_name = 'courses/create_lesson.html'
  
    
    def get_from_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    def form_valid(self, form):
        user_object = get_object_or_404(User, username=self.request.user.username)
        form.instance.teacher = user_object
        word_file = form.cleaned_data['word_file']

        if word_file:
            if hasattr(word_file, 'read'):
                # File is in memory, read its content
                content = word_file.read()
                # Perform the Word to Markdown conversion
                result = mammoth.convert_to_markdown(io.BytesIO(content))
                form.instance.lesson_content = result.value
            else:
                # File is on disk, perform conversion as before
                with open(word_file.path, 'rb') as docx_file:
                    result = mammoth.convert_to_markdown(docx_file)
                    form.instance.lesson_content = result.value

        return super().form_valid(form)
    def get_success_url(self) -> str:
        return reverse('courses:list')
    
class CourseDetail(generic.DetailView):
    model = Course
    
    
    def get_context_data(self, **kwargs):
         # Initialize user_profile
        user_profile = None
        try:
            user_id = self.request.user.id
            # Attempt to get user_profile
            # user_profile = UserProfile.objects.get(user=self.request.user)
            course = get_object_or_404(Course, pk=self.kwargs['pk'])
        except Http404:
            # Handle the case where UserProfile does not exist
            pass
            # Handle the case where the course does not exist
            messages.error(self.request, 'Course not found.')
            return HttpResponseRedirect(reverse('courses:list')) 
        
        completed_lesson_ids = []
        
        # Get chapters related to the course
        chapters = Chapter.objects.filter(course=course)

        # chapters_with_lessons = {}
        
        # Create a dictionary to store chapters and their related lessons
        chapters_with_lessons = []
        chapters_with_lessons_and_quizzes = {}

        # Initialize chapters_with_completion as an empty list
        chapters_with_completion = []

        # Initialize completed_chapter_ids as an empty list
        completed_chapter_ids = []

        
        for chapter in chapters:
            # Get lessons related to the chapter
            lessons = Lesson.objects.filter(chapter=chapter)
            # get the count of lessons that exist in each chapter
            lesson_count = lessons.count()
            chapters_with_lessons.append((chapter, lessons))
            
            quizzes = Quiz.objects.filter(chapter=chapter)
            chapters_with_lessons_and_quizzes[chapter] = {
                'lessons': lessons,
                'quizzes': quizzes,
                'lesson_count': lesson_count,
            }

            print("Lesson Count: ", lesson_count)
            

            
        assignments = Assignment.objects.filter(course=self.kwargs['pk'])
        resources = Resource.objects.filter(course=self.kwargs['pk'])

        # Get the total number of lessons for the course
        total_lessons = Lesson.objects.filter(chapter__course=course).count()
        total_quizzes = course.total_quizzes()
        completed_quizzes_count = 0
        lesson_count = 0
        completion_status = False
        completed_courses = 0
        # Handle the case where total_lessons is zero
        if total_lessons > 0:
            # Get the total number of completed lessons for the user in that course
            if self.request.user.is_authenticated:
                user_id = self.request.user.id
                completed_lessons = CompletedLesson.objects.filter(user=user_id, lesson__chapter__course=course).count()

                completed_lessons = CompletedLesson.objects.filter(user=user_id, lesson__chapter__course=course).aggregate(count=Count('id'))['count']



                completion_percentage = round((completed_lessons / total_lessons) * 100)
                print("Completed Lessons:", completed_lessons)

                # Access and print the lesson IDs directly
                completed_lessons1 = CompletedLesson.objects.filter(user=user_id, lesson__chapter__course=course)
                completed_lesson_ids = [completed_lesson.lesson.id for completed_lesson in completed_lessons1]
                print("Lesson IDs completed:", completed_lesson_ids)

                # can i get the chapter ids
                completed_chapter_ids = [completed_lesson.lesson.chapter.id for completed_lesson in completed_lessons1]
                print("Chapter IDs completed:", completed_chapter_ids)

                # Create a list to store chapter information including completion status
                chapters_with_completion = []

            # create a list of completed courses
            completed_courses = []

            completed_quizzes = []
            

            # Check if the chapter ID occurs in completed chapter IDs and the count matches the lesson count
            for chapter in chapters:
                lessons = Lesson.objects.filter(chapter=chapter)
                # Get quizzes related to the chapter
                quizzes = Quiz.objects.filter(chapter=chapter)
                # get the count of lessons and quizzes that exist in each chapter
                lesson_count = lessons.count()
                quiz_count = quizzes.count()
                # Get the completed quiz IDs from the completedquiz model
                completed_quizzes = CompletedQuiz.objects.filter(user=user_id, quiz__chapter__course=course).values_list('quiz_id', flat=True)
                
                completed_quizzes_ids = set(completed_quizzes)

                # Check if all lessons and quizzes in the chapter are completed
                is_completed = all(
                    ((chapter.id in completed_chapter_ids and completed_chapter_ids.count(chapter.id) == lesson_count) and
                    (quiz.id in completed_quizzes_ids and len(completed_quizzes_ids.intersection([quiz.id])) == 1))
                    for quiz in quizzes
                )





                chapter_info = {
                    'chapter_id': chapter.id,
                    'lessons': lessons,
                    'quizzes': quizzes,
                    'is_completed': is_completed,
                }

                if is_completed:
                    chapters_with_completion.append(chapter_info)

            # Check if the total number of chapters equals the number of completed chapters for each course
            total_chapters = Chapter.objects.filter(course=course).count()

            completed_chapters_count = sum(1 for chapter_info in chapters_with_completion if chapter_info['is_completed'])
            print(f"Course: {course}, Total Chapters: {total_chapters}, Completed Chapters: {completed_chapters_count}")

            if total_chapters == completed_chapters_count:
                completed_courses.append(course)

            print("Completed Courses:", completed_courses)
                   

            print("Chapters with completion:", chapters_with_completion)
                
            
 
            # get the total number of quizzes for the course
            total_quizzes = course.total_quizzes()
            print("Total Quizzes:", total_quizzes)

            # get the completed quizzes
            completed_quizzes = CompletedQuiz.objects.filter(user=user_id, quiz__chapter__course=course)

            # Get the completed quiz IDs from the UserProfile
            # completed_quizzes = user_profile.completed_quizzes.values_list('id', flat=True)
            # completed_quizzes_ids = list(completed_quizzes)
            # print("Completed Quizzeddds:", completed_quizzes_ids)

            completed_quizzes_count = len(completed_quizzes) if completed_quizzes else 0
            completed_lessons = CompletedLesson.objects.filter(user=user_id, lesson__chapter__course=course).count()

            # calculate if a course is complete or not if the total_lessons + total_quizes == the sum of completed lessons + completed quizes          
            if total_lessons + total_quizzes == completed_lessons + completed_quizzes_count:
                completion_status = True
            else:
                completion_status = False
            print("Completion Status:", completion_status)
             
            completion_percentage = round(((completed_lessons + completed_quizzes_count) / (total_lessons + total_quizzes)) * 100)
            print("Completed Quizees Count:", completed_quizzes_count)
            print("Completion Percentage:", completion_percentage)
        else:
            completed_lessons = 0
            completed_quizzes = 0
            completion_percentage = 0
        
        if completion_percentage >= 100:
            #this is how i choose to update to the db that a user has completed a course
            # popup a congratulations window with instructions to generate/get your certificate
            # Check if the user has already completed the course
            print(user_id, course)
            if not CompletedCourse.objects.filter(user_id=user_id, course=course).exists():
                # Create a new CompletedCourse instance only if it doesn't exist
                try:
                    completedcourse = CompletedCourse(user_id, course=course)
                    completedcourse.save()
                except IntegrityError:
                    # Handle the case where the user has already completed the course
                    messages.warning(self.request, 'You have already completed this course.')
            

        context = super(CourseDetail, self).get_context_data(**kwargs)
        context['assignments'] = assignments
        context['resources'] = resources
        context['chapters_with_lessons'] = chapters_with_lessons 
        # return chapter name and lesson name
        context['chapters_with_lessons_and_quizzes'] = chapters_with_lessons_and_quizzes
        context['total_lessons'] = total_lessons
        context['completed_lessons'] = completed_lessons
        context['course.pk'] = course
        context['course_id'] = course.pk
        # context['course_id'] = course.pk
        context['completed_lesson_ids'] = completed_lesson_ids
        # context['completed_lesson_ids_json'] = json.dumps(completed_lesson_ids)
        context['completed_quizzes'] = completed_quizzes
        context['completed_quizzes_count'] = completed_quizzes_count
        context['completion_percentage'] = completion_percentage
        context['completed_chapter_ids'] = completed_chapter_ids
            # lesson_count
        context['lesson_count'] = lesson_count
        context['chapters_with_completion'] = chapters_with_completion
        context['completion_status'] = completion_status
        context['completed_courses'] = completed_courses
        context['user_profile'] = user_profile
        return context


class ListCourse(generic.ListView):
    model = Course
    template_name = 'courses/course_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_list = Course.objects.all()

        if not course_list:
            messages.info(self.request, 'No courses available at the moment.')

        return context


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
        
def certificate_view(request, course_id):
    user = request.user
    course = get_object_or_404(Course, pk=course_id)

    try:
        existing_certificate = Certificate.objects.get(user=user, course=course)
        name = existing_certificate.name
        issuer_date = existing_certificate.issued_at
        issuer = existing_certificate.issuer
        certificate_id = existing_certificate.certificate_id
        context = {
            "name": name,
            "issuer_date": issuer_date,
            "course": course,
            "issuer": issuer,
            "certificate_id": certificate_id
        }
        return render(request, 'courses/certificate.html', {'context': context})
    except ObjectDoesNotExist:
        first_name = user.first_name
        last_name = user.last_name
        full_name = first_name + ' ' + last_name
        course_name = course.course_name
        issuer = "ABYA Africa"
        now = datetime.datetime.now()
        unixtime = calendar.timegm(now.utctimetuple())
        certificate_response = {
            "name": full_name,
            "course": course_name,
            "issuer": issuer,
            "issuer_date": unixtime
        }

        if all(value is not None for value in certificate_response.values()):
            certificate_data = send_certificate_request(certificate_response["name"], certificate_response["issuer"], certificate_response["issuer_date"])

            # Store the certificate in the database
            new_certificate = Certificate(user=user, course=course, name=certificate_data['name'], issuer=certificate_data["issuer"], issued_at=certificate_data["issue_date"], certificate_id=certificate_data["certificate_id"])
            new_certificate.save()
            
            return render(request, 'courses/certificate.html', {'context': certificate_data})
        else:
            return render(request, 'courses/certificate.html')

def verify_certificate(request):
    certificate_id = request.POST.get('certificate_id')

    if certificate_id:
        certificate_response = verify_certificate(certificate_id)
        return certificate_response
    else:
        return JsonResponse({"error": "Invalid request. Certificate ID is missing."}, status=400)
    
def get_completed_lessons_count(request, course_id):
    if request.user.is_authenticated:
        course = get_object_or_404(Course, pk=course_id)
        completed_lessons_count = request.user.completed_lessons.filter(
            lesson__chapter__course=course
        ).count()
        # Access and print the lesson IDs directly
        completed_lessons1 = CompletedLesson.objects.filter(user=request.user, lesson__chapter__course=course)
        completed_lesson_ids = [completed_lesson.lesson.id for completed_lesson in completed_lessons1]
        print("Lesson IDss completed:", completed_lesson_ids)
        for i in completed_lesson_ids:
            # count
            print("Lesson: ", i)
        print(completed_lessons1.count())
        completed_lesson_count = completed_lessons1.count()
        context = {
            'completed_lessons_count': completed_lesson_count,
            'completed_lesson_ids': completed_lesson_ids,
        }
        print("completed_lessons_count:", completed_lesson_count)
        return JsonResponse(context)
    else:
        return JsonResponse({'message': 'Invalid request method.'}, status=400)
# class CompletedLessonCountView(View):
#     def get(self, request, *args, **kwargs):
#         course_pk = self.kwargs['pk']  # Access the 'pk' parameter from the URL
#         # Your logic to calculate completed lesson count
#         course = get_object_or_404(Course, pk=course_pk)
#         completed_lessons_count = request.user.completed_lessons.filter(
#             lesson__chapter__course=course
#         ).count()
#         data = {'completed_lessons_count': completed_lessons_count}
#         return JsonResponse(data)
        

def mark_lesson_as_complete(request):
    if request.method != 'POST':
        return JsonResponse({'message': 'Invalid request method.'}, status=400)

    try:
        data = json.loads(request.body.decode('utf-8'))
        lesson_id = data.get('lesson_id')
    except json.JSONDecodeError:
        return JsonResponse({'message': 'Invalid JSON data.'}, status=400)

    if not lesson_id:
        return JsonResponse({'message': 'Missing lesson ID.'}, status=400)

    try:
        lesson = Lesson.objects.get(pk=lesson_id)
    except Lesson.DoesNotExist:
        return JsonResponse({'message': 'Lesson not found.'}, status=404)

    user = request.user

    # Check if the lesson is already marked as complete for the user
    if CompletedLesson.objects.filter(user=user, lesson=lesson).exists():
        return JsonResponse({'message': 'Lesson is already marked as complete.'}, status=200)

    # Mark the lesson as complete for the user
    completed_lesson = CompletedLesson(user=user, lesson=lesson)
    completed_lesson.save()

    # Calculate the completion percentage for the course
    course = lesson.chapter.course
    total_lessons = Lesson.objects.filter(chapter__course=course).count()
    total_quizzes = course.total_quizzes()
    completed_lessons = user.completed_lessons.filter(lesson__chapter__course=course).count()
    completed_quizzes = user.completed_quizzes(course)
    completion_percentage = round(((completed_lessons + completed_quizzes) / (total_lessons + total_quizzes)) * 100)
    print("completed quizes: ", completed_quizzes)

    # Update the progress bar or any other elements as needed

    return JsonResponse({'message': 'Lesson marked as complete successfully.', 'completed_lessons_count': completed_lessons, 'completion_percentage': completion_percentage}, status=200)


@csrf_protect
def update_video_progress(request):
    if request.method == 'POST':
        video_id = request.POST.get('video_id')
        progress = request.POST.get('progress')
        video_lesson = VideoLesson.objects.get(video_lesson_id=video_id)    
        # Find the VideoProgress object for the specified video_id and update the progress
        video_progress, created = VideoProgress.objects.get_or_create(video_lesson=video_lesson, user=request.user)
        video_progress.progress = progress
        if float(progress) == 75:
            video_progress.status = True
        video_progress.save()
        
        return JsonResponse({'message': 'Video progress updated successfully.'})

    return JsonResponse({'message': 'Invalid request method.'}, status=400)
