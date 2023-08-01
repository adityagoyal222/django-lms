from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from courses.models import Course
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests

class UserProfile(LoginRequiredMixin, generic.ListView):
    model = Course
    template_name = 'user_profile.html'

def index(request):
    return render(request, 'index.html')



# @csrf_exempt 
def send_chatbot_response(request):
    if request.method == 'POST':
        # Get the input message from the POST request
        message = request.POST.get('chattext').value()
        print(message)
        # Send the input message to the ChatGPT API endpoint
        chatgpt_endpoint = 'https://api.openai.com/v1/engines/davinci-codex/completions'
        api_key = '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'  # Replace this with your actual API key from OpenAI
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
        }
        data = {
            'prompt': message,
            'max_tokens': 50,  # Adjust this as needed for the response length
        }

        try:
            response = requests.post(chatgpt_endpoint, headers=headers, json=data)
            response_data = response.json()
            chatbot_response = response_data['choices'][0]['text']
        except requests.exceptions.RequestException as e:
            # Handle the exception if the request to the API fails
            print(f"Error connecting to ChatGPT API: {e}")
            return JsonResponse({'error': 'Failed to connect to the ChatGPT API'})

        # Print the chatbot response (for debugging purposes)
        print(chatbot_response)
        context = {
            'chatbot_response': chatbot_response,
            'message': message,
        }
        # You can use the chatbot_response for further processing if needed
        # For example, you can save it to the database or perform other actions

        # Return a JSON response to the client (optional)
        return render(request, "base.html", context)
    else:
        return render (request, "base.html", context)


    #   openai.api_key = "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"
    # if request.method == "POST":
    #     # sender = request.POST.get("message-input")

    #     sender = "what is the fifa 23 in 5 words"
    #     messages = []
    #     messages.append({"role": "user", "content": sender})
    #     # sender = "Who is elon musk"
    #     while sender != "":
    #         user_msg = sender
    #         messages.append({"role": "user", "content": user_msg})
    #         completion  = openai.ChatCompletion.create(model='gpt-3.5-turbo',  messages=messages)
    #         print(completion.choices[0].message.content)
    #         messages.append({"role": "system", "content": completion.choices[0].message.content})
    #         sender = completion.choices[0].message.content