import json
import requests
from django.shortcuts import render
from .scripts import codex_api

def ide(request):
    output = codex_api('val = int(input("Enter your value: ")) + 5\nprint(val)', 'py', 5)
    print(output)
    return render(request, 'editor/ide.html')