# from django.conf.urls import url
from django.urls import re_path, path
from courses import views


app_name = "courses"

urlpatterns = [
    re_path(r'^new/$', views.CreateCourse.as_view(), name="create"),
    re_path(r'^detail/(?P<pk>[-\w]+)/$', views.CourseDetail.as_view(), name='detail'),
    path('all/', views.ListCourse.as_view(), name="list"),
    re_path(r'^enroll/(?P<pk>[-\w]+)/$', views.EnrollCourse.as_view(), name='enroll'),
    re_path(r'^unenroll/(?P<pk>[-\w]+)/$', views.UnenrollCourse.as_view(), name='unenroll'),
    path('create_chapter/', views.CreateChapterView.as_view(), name='create_chapter'),
    path('create_lesson/', views.CreateLessonView.as_view(), name='create_lesson'),
    path('update_chapter/<int:pk>/', views.UpdateChapterView.as_view(), name='update_chapter'),
    path('update_lesson/<int:pk>/', views.UpdateLessonView.as_view(), name='update_lesson'),
    path('update_course/<int:pk>/', views.UpdateCourseView.as_view(), name='update_course'),
    path('get_completed_lessons_count/<int:course_id>/', views.get_completed_lessons_count, name='completed_lesson_count'),
    path('mark_lesson_as_complete/', views.mark_lesson_as_complete, name='mark_lesson_as_complete'),
]
