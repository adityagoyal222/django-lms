from django import forms

LANGUAGES_CHOICES = [
    ('python', 'Python'),
    ('java', 'Java'),
    ('c', 'C'),
    ('cpp', 'c++'),
    ('js', 'JavaScript(Node.js)'),
    ('php', 'PHP'),
    ('perl', 'Perl'),
    ('kotlin', 'Kotlin'),
    ('swift', 'Swift'),
    # Add more languages and labels as needed
]

class LanguageForm(forms.Form):
    language = forms.ChoiceField(
        choices=LANGUAGES_CHOICES,
        widget=forms.RadioSelect,
    )
