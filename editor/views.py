import json
import requests
from django.shortcuts import render
from .scripts import codex_api, jdoodle_api_call
from django.http import JsonResponse
from django.shortcuts import render

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
    input_code = ''  # Initialize input_code with a default value
    if request.method == "POST":
        input_code = request.POST.get('input', '')

    program = {
        "script": input_code,
        "language": "python3",
        "versionIndex": "4",
        "clientId": "337a83aa8cc0186032dc2189c403e950",
        "clientSecret": "a94de9c2bb09ce02dd34b688a22a635e5f2d07c942b757c8915e6287c0cc2240",
    }
    result = jdoodle_api_call(program)
    context = {
        'output': result
    }
    print(result)
    return render(request, 'editor/ide.html', context)
