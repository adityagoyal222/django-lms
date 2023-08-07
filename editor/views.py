import json
import requests
from django.shortcuts import render
from .scripts import codex_api, jdoodle_api_call
from django.http import JsonResponse
from django.shortcuts import render
from . forms import LanguageForm

# def ide(request):
    
#     inputr = int(input("Enter your value: "))
#     output = codex_api('val = ' + str(inputr) + ' + 5\nprint(val)', 'py', 5)
#     # output = codex_api('val = int(input("Enter your value: ")) + 5\nprint(val)', 'py', 5)
#     print(output)
#     output_obj = json.loads(output)
#     # print(output_obj["output"])
#     context = {
#         'output': output_obj["output"]
#     }
#     return render(request, 'editor/ide.html', context)



def jdoodle_api_ide(request):
    input_code = ''
    language = 'python3'  # Default language if the form is not submitted
    if request.method == "POST":
        form = LanguageForm(request.POST)
        if form.is_valid():
            input_code = request.POST.get('input', '')
            language = form.cleaned_data['language']

        input_code = request.POST.get('input', '')
    program = {
        "script": input_code,
        "language": language,  # Use the selected language or default
        "versionIndex": "4",
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
