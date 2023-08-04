from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from courses.models import Course
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import openai
from django.contrib.sessions.backends.db import SessionStore
from django.http import HttpResponseServerError
import os
from dotenv import load_dotenv

class UserProfile(LoginRequiredMixin, generic.ListView):
    model = Course
    template_name = 'user_profile.html'

def index(request):
    return render(request, 'index.html')



# @csrf_exempt 
def send_chatbot_response(request):
    # Load environment variables from .env file
    load_dotenv()
    openai.api_key = os.getenv('OPENAI_API_KEY')
    # openai.api_key = api_key

    if request.method == 'POST':
        sender = request.POST.get("chattext")
        print(sender)

        session_id = request.META.get('HTTP_X_SESSION_ID', None)

        if not session_id:
            # If the session ID is not provided, create a new session
            session = SessionStore()
            session.create()
            session_id = session.session_key

         # Get or create the session with the provided session ID
        session = SessionStore(session_key=session_id)

        
        # Retrieve the chat history from the session
        messages = session.get("chat_history", [])

        if not messages:
            messages.append({"role": "system", "content": "You are a knowledgeable blockchain assistant."})

        # Append the new user message to the chat history
        messages.append({"role": "user", "content": sender})

        response = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=messages)
        bot_reply = response['choices'][0]['message']['content']
        print(bot_reply)

        messages.append({"role": "system", "content": bot_reply})
         # Save the updated chat history back to the session
        session["chat_history"] = messages
        session.save()

        context = {
            'response': messages
        }

        return render(request, 'base.html', context)
    else:
        return render(request, 'base.html')
    