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

import requests
import json

def jdoodle_api_call(program):
    url = "https://api.jdoodle.com/v1/execute"
    payload = {
        "script": program["script"],
        "language": program["language"],
        "versionIndex": program["versionIndex"],
        "clientId": program["clientId"],
        "clientSecret": program["clientSecret"],
    }
    response = requests.post(url, json=payload)
    # Parse the JSON response
    json_response = response.json()
    # Extract the output
    output = json_response.get("output", "")
    return output

if __name__ == "__main__":
    program = {
        "script": "print('Hello World')",
        "language": "python3",
        "versionIndex": "4",
        "clientId": "337a83aa8cc0186032dc2189c403e950",
        "clientSecret": "a94de9c2bb09ce02dd34b688a22a635e5f2d07c942b757c8915e6287c0cc2240",
    }
    result = jdoodle_api_call(program)
    print("Output:", result)