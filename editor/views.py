from django.shortcuts import render
from .scripts import  jdoodle_api_call

from django.shortcuts import render
from . forms import LanguageForm, languages



def jdoodle_api_ide(request):
    input_code = ''
    language = 'python3'  # Default language if the form is not submitted
    version_index = 4  # Default version index if the form is not submitted
    if request.method == "POST":
        form = LanguageForm(request.POST)
        if form.is_valid():
            input_code = request.POST.get('input', '')
            language = form.cleaned_data['language']

        input_code = request.POST.get('input', '')
        version_index = languages[language]
    program = {
        "script": input_code,
        "language": language,  # Use the selected language or default
        "versionIndex": version_index,
        "clientId": "337a83aa8cc0186032dc2189c403e950",
        "clientSecret": "a94de9c2bb09ce02dd34b688a22a635e5f2d07c942b757c8915e6287c0cc2240",
    }
    
    result = jdoodle_api_call(program)
    
    context = {
        'output': result,
        'form': LanguageForm(initial={'language': language}),
        'script': input_code
    }
    
    return render(request, 'editor/ide.html', context)

