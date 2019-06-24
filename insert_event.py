from __future__ import print_function
import pickle
import csv
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from listen_connpass import ConnpassEvent
from bs4 import BeautifulSoup

SCOPES = 'https://www.googleapis.com/auth/calendar'


def insert_event():
    creds = check_google_token()
    service = build('calendar', 'v3', credentials=creds)

    events_10 = ConnpassEvent(201907, ['東京', 'python'])
    events = events_10.get_connpass_events()
    for event in events:
        print(event['event_id'])
        if duplicate_event(event['event_id']):
            print('duplicate data found in', event['event_id'])
            continue
        print('inset event data', event['title'])
        event_body = event_formatter(event)
        event = service.events().insert(calendarId='primary',
                                        body=event_body).execute()


def check_google_token():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


def duplicate_event(event_id) -> bool:
    with open('test.csv', 'r') as f:
        reader = csv.reader(f)
        for t in reader:
            if str(event_id) in t:
                return True
    with open('test.csv', 'a') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow([event_id])
    return None


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
