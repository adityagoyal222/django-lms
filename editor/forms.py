from django import forms

LANGUAGES_CHOICES = [
    ('python3', 'Python3'),
    ('java', 'Java'),
    ('c', 'C'),
    ('cpp14', 'c++'),
    ('nodejs', 'JavaScript(Node.js)'),
    ('php', 'PHP'),
    ('perl', 'Perl'),
    ('kotlin', 'Kotlin'),
    ('swift', 'Swift'),
    # Add more languages and labels as needed
]

class LanguageForm(forms.Form):
    language = forms.ChoiceField(
        choices=LANGUAGES_CHOICES
    )
