from django.test import TestCase, Client
from django.urls import reverse

from .models import Quiz, Question, Choice
from .forms import QuestionForm
from django.contrib.auth import get_user_model
from .views import CreateQuestionView
from django.forms import modelformset_factory
ChoiceFormSet = modelformset_factory(Choice, fields=('text', 'is_correct'), extra=4, max_num=4)

User = get_user_model()
class CreateQuestionViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.quiz = Quiz.objects.create(quiz_title='Test Quiz')
        self.url = reverse('assignments:create_question', kwargs={'quiz_id': self.quiz.id})
        self.client.login(username='testuser', password='testpassword')

    def test_get_context_data(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['choice_formset'], ChoiceFormSet)
        self.assertEqual(response.context['quiz_id'], self.quiz.id)

    def test_form_valid(self):
        question_data = {
            'text': 'Test Question',
            'quiz': self.quiz.id,
        }
        response = self.client.post(self.url, question_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('courses:list'))
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(Choice.objects.count(), 0)

    def test_form_valid_with_choices(self):
        question_data = {
            'text': 'Test Question',
            'quiz': self.quiz.id,
        }
        choice_data = {
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-text': 'Choice 1',
            'form-1-text': 'Choice 2',
        }
        response = self.client.post(self.url, {**question_data, **choice_data})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('courses:list'))
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(Choice.objects.count(), 2)
        question = Question.objects.first()
        self.assertEqual(question.choices.count(), 2)

    def test_get_success_url(self):
        view = CreateQuestionView()
        view.kwargs = {'quiz_id': self.quiz.id}
        success_url = view.get_success_url()
        self.assertEqual(success_url, reverse('assignments:create_question', kwargs={'quiz_id': self.quiz.id}))