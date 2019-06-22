from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from listen_connpass import ConnpassEvent
from bs4 import BeautifulSoup

# If modifying these scopes, delete the file token.pickle.
SCOPES = 'https://www.googleapis.com/auth/calendar'

def insert_event():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    events = ConnpassEvent(201906, ['東京', 'python'])
    event = events.get_connpass_events()
    # print('event:', event_formatter(event))
    event_body = event_formatter(event)
    event = service.events().insert(calendarId='primary', body=event_body).execute()
    # f'Event created:{(event.get('htmlLink')}'
    print(event)


def event_formatter(event):
    event_formatted = {
        'summary': event['title'],
        'location': event['address'],
        'description': format_html_to_text(event['description']),
        'start': {
            'dateTime': event['started_at'],
            'timeZone': 'Asia/Tokyo',
        },
        'end': {
            'dateTime': event['ended_at'],
            'timeZone': 'Asia/Tokyo',
        },
        'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=1'
        ],
        'attendees': [
            {'email': 'aku2kan@gmail.com'},
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
            {'method': 'email', 'minutes': 24 * 60},
            {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    return event_formatted


def format_html_to_text(html):
    soup_html = BeautifulSoup(html)
    for script in soup_html(["script", "style"]):
        script.extract()
    text = soup_html.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

if __name__ == '__main__':
    insert_event()
