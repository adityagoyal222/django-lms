from django.urls import re_path, path
from assignments import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'assignments'
urlpatterns = [
    re_path(r'^create/$', views.CreateAssignment.as_view(), name="create"),
    re_path(r'^detail/(?P<pk>[-\w]+)/$', views.AssignmentDetail.as_view(), name='detail'),
    re_path(r'^update/(?P<pk>[-\w]+)/$', views.UpdateAssignment.as_view(), name='update'),
    re_path(r'^delete/(?P<pk>[-\w]+)/$', views.DeleteAssignment.as_view(), name="delete"),
    re_path(r'^submit/$', views.SubmitAssignmentView.as_view(), name="submit"),
    re_path(r'^submission/detail/(?P<pk>[-\w]+)/$', views.SubmitAssignmentDetail.as_view(), name="submit_detail"),
    re_path(r'^submission/delete/(?P<pk>[-\w]+)/$', views.delete_view, name="submit_delete"),
    re_path(r'^grade/(?P<pk>[-\w]+)/$', views.grade_assignment, name='grade'),
    path('create_quiz/', views.create_quiz, name='create_quiz'),
    path('create_question/<int:quiz_id>/', views.CreateQuestionView.as_view(), name='create_question'),
    path('create_question/', views.CreateQuestionViewWithoutId.as_view(), name='create_question_without_id'),
    # path('submit_quiz/<int:quiz_id>', views.QuizAnswerView.as_view(), name='submit_quiz'),
    re_path(r'^submit_quiz/(?P<quiz_id>\d+)/$', views.QuizAnswerView.as_view(), name='submit_quiz'),
    path('quiz/results/<int:submission_id>/<int:quiz_id>/', views.QuizResultsView.as_view(), name='quiz_results'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
