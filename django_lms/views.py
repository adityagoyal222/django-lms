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
# from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from googleapiclient.errors import HttpError
from django.views.decorators.cache import cache_page


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
        # print(sender)


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
        # print(bot_reply)

        messages.append({"role": "system", "content": bot_reply})
         # Save the updated chat history back to the session
        # session["chat_history"] = messages
        # session.save()

        context = {
            'response': messages
        }

        return render(request, 'base.html', context)
    else:
        return render(request, 'base.html')
    

def get_calendar_events(request):
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

    def main():
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        dir_path = os.path.dirname(os.path.abspath(__file__))
        # Specify the paths to the credentials and token files
        credentials_path = os.path.join(dir_path, 'credentials.json')
        token_path = os.path.join(dir_path, 'token.json')
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_path, 'w') as token:
                token.write(creds.to_json())

        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=4, singleEvents=True,
                                          orderBy='startTime').execute()
        events = events_result.get('items', [])
        
        # Initialize an empty list to store the events
        event_list = []

        if not events:
            print('No upcoming events found.')
        else:
            # Prints the start and name of the next 10 events
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(start, event['summary'])
                event_list.append((start, event['summary']))
        # Return the event_list
        return event_list

    try:
        # Call the main function and get the events
        events = main()

        # Return the events as a JSON response
        return JsonResponse({'events': events})
    except Exception as e:
        # Log the exception for debugging purposes
        print(f"An error occurred: {e}")

        # Return an error message as a JSON response
        return JsonResponse({'error': 'An error occurred while fetching calendar events.'})

        

