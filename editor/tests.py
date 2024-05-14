from django.test import TestCase
from django.urls import reverse, reverse_lazy
from .forms import LanguageForm

class JDoodleApiIdeViewTest(TestCase):

    def test_jdoodle_api_ide_view(self):
        # Create a test request with POST data
        data = {
            'input': 'print("Hello, World!")',
            'language': 'python3',
        }
        response = self.client.post(reverse_lazy('editor:jdoodle_api_ide'), data)

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the 'output' key is present in the response context
        self.assertIn('output', response.context)

        # Check if the rendered template is correct
        self.assertTemplateUsed(response, 'editor/ide.html')

        # You may add more specific checks based on your view's behavior and expected output
        # For example, you can check if the rendered HTML contains a specific output

    def test_jdoodle_api_ide_view_get(self):
        # Create a test request without POST data (GET request)
        response = self.client.get(reverse_lazy('editor:jdoodle_api_ide'))

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the 'form' key is present in the response context
        self.assertIn('form', response.context)

        # Check if the rendered template is correct
        self.assertTemplateUsed(response, 'editor/ide.html')