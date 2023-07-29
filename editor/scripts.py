import requests 
import json

codex_language_codes=['py','java','cpp','c','go','cs','js']
    
def codex_api(code, language, input=None):
    url = 'https://api.codex.jaagrav.in'
    data = {
        'code': (code),
        'language': (language),
        'input': (input), 
        }
   
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(url, headers=headers, data=data)
    return json.dumps(response.json())
