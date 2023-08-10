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
# languages along with their version index
languages={
    'python3': 4,
    'java': 3,
    'cpp17': 1,
    'kotlin':3,
    'php':4,
    'nodejs':4
}

class LanguageForm(forms.Form):
    language = forms.ChoiceField(
        choices=LANGUAGES_CHOICES
    )
