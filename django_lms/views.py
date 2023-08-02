from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from courses.models import Course
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import openai

class UserProfile(LoginRequiredMixin, generic.ListView):
    model = Course
    template_name = 'user_profile.html'

def index(request):
    return render(request, 'index.html')



# @csrf_exempt 
def send_chatbot_response(request):
    api_key = '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'
    openai.api_key = api_key
    if request.method == 'POST':
        sender = request.POST.get("chattext")
        print(sender)
        # sender = "what is the fifa 23 in 5 words"
        messages = [{"role": "system", "content": "You are a knowledgable blockchain assistant."}]
        messages.append({"role": "user", "content": sender})
        # sender = "Who is elon musk"
        while sender != "":
            user_msg = sender
            messages.append({"role": "user", "content": user_msg})
            response  = openai.ChatCompletion.create(model='gpt-3.5-turbo',  messages=messages)
            bot_reply = response['choices'][0]['message']['content']
            print(bot_reply)
            messages.append({"role": "system", "content": bot_reply})
            sender = bot_reply

            context = {
                'response': messages
            }

        return render(request, 'base.html', context)
    else:
        return render(request, 'base.html')
    