import json
import requests
from django.shortcuts import render
from .scripts import codex_api
from django.http import JsonResponse
from django.shortcuts import render

def ide(request):
    
    inputr = int(input("Enter your value: "))
    output = codex_api('val = ' + str(inputr) + ' + 5\nprint(val)', 'py', 5)
    # output = codex_api('val = int(input("Enter your value: ")) + 5\nprint(val)', 'py', 5)
    print(output)
    output_obj = json.loads(output)
    # print(output_obj["output"])
    context = {
        'output': output_obj["output"]
    }
    return render(request, 'editor/ide.html', context)